#!/usr/bin/env python3
"""
论文抓取脚本
从 ArXiv 等数据源抓取最新论文
"""

import arxiv
import json
import yaml
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PaperFetcher:
    """论文抓取器"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """初始化"""
        self.config = self.load_config(config_path)
        self.papers = []
        
    def load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def fetch_arxiv_papers(self) -> List[Dict]:
        """从 ArXiv 抓取论文"""
        logger.info("开始从 ArXiv 抓取论文...")
        
        arxiv_config = self.config['sources']['arxiv']
        if not arxiv_config['enabled']:
            logger.info("ArXiv 数据源未启用")
            return []
        
        papers = []
        categories = arxiv_config['categories']
        max_results = arxiv_config['max_results']
        days_back = arxiv_config.get('days_back', 1)
        
        # 计算时间范围（使用 UTC 时区）
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days_back)
        
        for category in categories:
            logger.info(f"抓取类别: {category}")
            
            try:
                # 构建查询
                search = arxiv.Search(
                    query=f"cat:{category}",
                    max_results=max_results,
                    sort_by=arxiv.SortCriterion.SubmittedDate,
                    sort_order=arxiv.SortOrder.Descending
                )
                
                # 获取结果
                count = 0
                for result in search.results():
                    # 检查发布时间（使用更新时间或发布时间）
                    paper_date = result.updated if result.updated else result.published
                    
                    # 只获取时间范围内的论文
                    if paper_date < start_date:
                        continue
                    
                    paper = {
                        'id': result.entry_id.split('/')[-1],
                        'title': result.title,
                        'authors': [author.name for author in result.authors],
                        'abstract': result.summary,
                        'published': result.published.strftime('%Y-%m-%d'),
                        'updated': result.updated.strftime('%Y-%m-%d'),
                        'categories': result.categories,
                        'primary_category': result.primary_category,
                        'pdf_url': result.pdf_url,
                        'arxiv_url': result.entry_id,
                        'source': 'ArXiv',
                        'venue': category
                    }
                    
                    # 分类论文
                    paper['tags'] = self.classify_paper(paper)
                    
                    papers.append(paper)
                    count += 1
                
                logger.info(f"从 {category} 抓取了 {count} 篇论文（时间范围：{start_date.strftime('%Y-%m-%d')} 至今）")
                
            except Exception as e:
                logger.error(f"抓取 {category} 时出错: {e}")
                continue
        
        logger.info(f"ArXiv 总共抓取了 {len(papers)} 篇论文")
        return papers
    
    def classify_paper(self, paper: Dict) -> List[str]:
        """根据关键词分类论文"""
        tags = set()
        text = (paper['title'] + ' ' + paper['abstract']).lower()
        
        categories = self.config.get('categories', {})
        for category_name, category_info in categories.items():
            keywords = category_info.get('keywords', [])
            for keyword in keywords:
                if keyword.lower() in text:
                    tags.add(category_name)
                    break
        
        return list(tags)
    
    def save_papers(self, papers: List[Dict], output_path: str = "data/papers.json"):
        """保存论文数据"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 加载已有数据
        existing_papers = []
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_papers = json.load(f)
        
        # 去重（根据论文ID）
        existing_ids = {p['id'] for p in existing_papers}
        new_papers = [p for p in papers if p['id'] not in existing_ids]
        
        # 合并数据
        all_papers = new_papers + existing_papers
        
        # 按日期排序
        all_papers.sort(key=lambda x: x['published'], reverse=True)
        
        # 保存
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_papers, f, ensure_ascii=False, indent=2)
        
        logger.info(f"保存了 {len(new_papers)} 篇新论文，总共 {len(all_papers)} 篇")
        
        # 同时保存今日论文
        today = datetime.now().strftime('%Y-%m-%d')
        today_papers = [p for p in papers if p['published'] == today]
        if today_papers:
            today_file = output_file.parent / f"papers_{today}.json"
            with open(today_file, 'w', encoding='utf-8') as f:
                json.dump(today_papers, f, ensure_ascii=False, indent=2)
            logger.info(f"今日论文保存到: {today_file}")
    
    def run(self):
        """运行抓取流程"""
        logger.info("=" * 60)
        logger.info("开始抓取论文")
        logger.info("=" * 60)
        
        # 从各个数据源抓取
        arxiv_papers = self.fetch_arxiv_papers()
        
        # 合并所有论文
        all_papers = arxiv_papers
        
        # 保存数据
        if all_papers:
            self.save_papers(all_papers)
            logger.info(f"抓取完成！共获取 {len(all_papers)} 篇论文")
        else:
            logger.warning("未抓取到任何论文")
        
        logger.info("=" * 60)


def main():
    """主函数"""
    fetcher = PaperFetcher()
    fetcher.run()


if __name__ == "__main__":
    main()
