#!/usr/bin/env python3
"""
生成静态网页脚本
将论文数据生成为 HTML 页面
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTMLGenerator:
    """HTML 生成器"""
    
    def __init__(self, data_path: str = "data/papers.json", 
                 output_dir: str = "docs"):
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.papers = []
        self.papers_by_month = {}  # 按月份分组的论文
        
    def load_papers(self):
        """加载论文数据"""
        if not self.data_path.exists():
            logger.warning(f"数据文件不存在: {self.data_path}")
            return
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.papers = json.load(f)
        
        logger.info(f"加载了 {len(self.papers)} 篇论文")
        
        # 按月份分组
        for paper in self.papers:
            # 从 published 字段提取年月 (格式: 2025-10-31)
            published = paper.get('published', '')
            if published:
                year_month = published[:7]  # 提取 "2025-10"
                if year_month not in self.papers_by_month:
                    self.papers_by_month[year_month] = []
                self.papers_by_month[year_month].append(paper)
        
        logger.info(f"论文分布: {', '.join([f'{k}: {len(v)}篇' for k, v in sorted(self.papers_by_month.items(), reverse=True)])}")
    
    def generate_monthly_data_files(self):
        """生成按月份分离的数据文件"""
        data_dir = self.output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # 为每个月份生成独立的 JSON 文件
        for year_month, papers in self.papers_by_month.items():
            file_path = data_dir / f"{year_month}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(papers, f, ensure_ascii=False, indent=2)
            logger.info(f"生成月度数据文件: {file_path} ({len(papers)} 篇)")
        
        # 生成索引文件，包含所有月份的元数据
        months_index = []
        for year_month in sorted(self.papers_by_month.keys(), reverse=True):
            papers = self.papers_by_month[year_month]
            months_index.append({
                'month': year_month,
                'count': len(papers),
                'published_count': sum(1 for p in papers if p.get('conference')),
                'preprint_count': sum(1 for p in papers if not p.get('conference'))
            })
        
        with open(data_dir / "index.json", 'w', encoding='utf-8') as f:
            json.dump(months_index, f, ensure_ascii=False, indent=2)
        
        logger.info(f"生成月份索引文件: {data_dir / 'index.json'}")
    
    def generate_month_buttons(self):
        """生成月份筛选按钮"""
        buttons = []
        for year_month in sorted(self.papers_by_month.keys(), reverse=True):
            count = len(self.papers_by_month[year_month])
            buttons.append(f'<button class="filter-btn month-btn" data-month="{year_month}">{year_month} ({count})</button>')
        return '\n                    '.join(buttons)
    
    def generate_index_html(self):
        """生成主页 HTML"""
        # 计算各分类数量
        published_count = sum(1 for p in self.papers if p.get('conference'))
        preprint_count = sum(1 for p in self.papers if not p.get('conference'))
        cv_count = sum(1 for p in self.papers if 'Computer Vision' in p.get('tags', []))
        nlp_count = sum(1 for p in self.papers if 'Natural Language Processing' in p.get('tags', []))
        ml_count = sum(1 for p in self.papers if 'Machine Learning' in p.get('tags', []))
        robotics_count = sum(1 for p in self.papers if 'Robotics' in p.get('tags', []))
        multimodal_count = sum(1 for p in self.papers if 'Multimodal' in p.get('tags', []))
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DailyPaper - AI/ML/CV/NLP 最新论文</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>📚 DailyPaper</h1>
            <p class="subtitle">每日自动更新 AI/ML/CV/NLP 领域最新论文</p>
            <p class="update-time">最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
        </div>
    </header>
    
    <nav class="container">
        <div class="filter-section">
            <div class="filter-group">
                <label class="filter-label">📅 月份：</label>
                <div class="filters month-filters">
                    <button class="filter-btn month-btn active" data-month="all">全部 ({len(self.papers)})</button>
                    {self.generate_month_buttons()}
                </div>
            </div>
            <div class="filter-group">
                <label class="filter-label">📌 发表状态：</label>
                <div class="filters status-filters">
                    <button class="filter-btn status-btn active" data-status="all">全部 ({len(self.papers)})</button>
                    <button class="filter-btn status-btn" data-status="published">已发表 ({published_count})</button>
                    <button class="filter-btn status-btn" data-status="preprint">预印本 ({preprint_count})</button>
                </div>
            </div>
            <div class="filter-group">
                <label class="filter-label">🏷️ 研究领域：</label>
                <div class="filters category-filters">
                    <button class="filter-btn category-btn active" data-category="all">全部 ({len(self.papers)})</button>
                    <button class="filter-btn category-btn" data-category="Computer Vision">Computer Vision ({cv_count})</button>
                    <button class="filter-btn category-btn" data-category="Natural Language Processing">NLP ({nlp_count})</button>
                    <button class="filter-btn category-btn" data-category="Machine Learning">Machine Learning ({ml_count})</button>
                    <button class="filter-btn category-btn" data-category="Robotics">Robotics ({robotics_count})</button>
                    <button class="filter-btn category-btn" data-category="Multimodal">Multimodal ({multimodal_count})</button>
                </div>
            </div>
            <div class="filter-group">
                <label class="filter-label">🔄 排序方式：</label>
                <div class="filters sort-filters">
                    <button class="filter-btn sort-btn active" data-sort="date-desc">最新优先</button>
                    <button class="filter-btn sort-btn" data-sort="date-asc">最早优先</button>
                </div>
            </div>
        </div>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 搜索论文标题、作者、摘要...">
        </div>
        <div class="results-info">
            <span id="resultsCount">加载中...</span>
            <div class="export-controls">
                <button class="select-btn" id="selectAllBtn">✓ 全选</button>
                <button class="select-btn" id="clearAllBtn">✗ 清空</button>
                <button class="export-btn" id="exportBtn">📥 导出选中 (<span id="selectedCount">0</span>)</button>
            </div>
        </div>
    </nav>
    
    <main class="container">
        <div id="papers-container">
            <!-- Papers will be loaded by JavaScript -->
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>© 2025 DailyPaper | 数据来源: ArXiv | <a href="https://github.com/yourusername/DailyPaper" target="_blank">GitHub</a></p>
        </div>
    </footer>
    
    <script src="js/main.js"></script>
</body>
</html>
"""
        
        output_file = self.output_dir / "index.html"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"生成主页: {output_file}")
    
    def get_category_name(self, category: str) -> str:
        """将 ArXiv 类别代码转换为友好的名称"""
        category_map = {
            'cs.AI': 'Artificial Intelligence',
            'cs.CV': 'Computer Vision',
            'cs.CL': 'Computational Linguistics (NLP)',
            'cs.LG': 'Machine Learning',
            'cs.IR': 'Information Retrieval',
            'cs.RO': 'Robotics',
            'cs.NE': 'Neural and Evolutionary Computing',
            'cs.CR': 'Cryptography and Security',
            'cs.HC': 'Human-Computer Interaction',
            'cs.MM': 'Multimedia',
            'stat.ML': 'Machine Learning (Statistics)',
        }
        return category_map.get(category, category)
    
    def extract_code_links(self, abstract: str) -> Dict[str, str]:
        """从摘要中提取代码和项目链接"""
        import re
        links = {}
        
        # 提取 Code: 链接
        code_pattern = r'[Cc]ode[:\s]+(?:available at\s+)?(\S+)'
        code_match = re.search(code_pattern, abstract)
        if code_match:
            links['code'] = code_match.group(1).rstrip('.,;')
        
        # 提取 Project: 链接
        project_pattern = r'[Pp]roject[:\s]+(?:page\s+)?(\S+)'
        project_match = re.search(project_pattern, abstract)
        if project_match:
            links['project'] = project_match.group(1).rstrip('.,;')
        
        # 提取 GitHub 链接
        github_pattern = r'(https?://(?:www\.)?github\.com/[\w\-]+/[\w\-]+)'
        github_match = re.search(github_pattern, abstract)
        if github_match and 'code' not in links:
            links['code'] = github_match.group(1)
        
        return links
    
    def get_venue_badge(self, conference: str) -> tuple:
        """获取会议徽章的样式类和显示文本"""
        if not conference:
            return ('preprint', 'Preprint')
        
        # 顶级会议配色
        venue_styles = {
            'NeurIPS': ('venue-neurips', 'NeurIPS'),
            'CVPR': ('venue-cvpr', 'CVPR'),
            'ICCV': ('venue-iccv', 'ICCV'),
            'ECCV': ('venue-eccv', 'ECCV'),
            'ICML': ('venue-icml', 'ICML'),
            'ICLR': ('venue-iclr', 'ICLR'),
            'ACL': ('venue-acl', 'ACL'),
            'EMNLP': ('venue-emnlp', 'EMNLP'),
            'AAAI': ('venue-aaai', 'AAAI'),
            'IJCAI': ('venue-ijcai', 'IJCAI'),
        }
        
        # 检查会议名称
        for venue_name, (style, display) in venue_styles.items():
            if venue_name in conference:
                return (style, conference)
        
        return ('venue-other', conference)
    
    def generate_papers_html(self) -> str:
        """生成论文列表 HTML"""
        if not self.papers:
            return '<p class="no-results">暂无论文数据</p>'
        
        html_parts = []
        for paper in self.papers:
            tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in paper.get('tags', [])])
            authors_html = ', '.join(paper['authors'][:5])
            if len(paper['authors']) > 5:
                authors_html += ' et al.'
            
            # 获取友好的类别名称
            primary_category = paper.get('primary_category', paper['venue'])
            category_name = self.get_category_name(primary_category)
            
            # 获取会议信息和徽章样式
            conference = paper.get('conference')
            venue_class, venue_display = self.get_venue_badge(conference)
            
            # 确定发表状态
            is_published = 'published' if conference else 'preprint'
            
            # 提取代码链接
            code_links = self.extract_code_links(paper['abstract'])
            code_links_html = ''
            if code_links.get('code'):
                code_links_html += f'<a href="{code_links["code"]}" target="_blank" class="btn-link btn-code">💻 Code</a>'
            if code_links.get('project'):
                code_links_html += f'<a href="{code_links["project"]}" target="_blank" class="btn-link btn-project">🌐 Project</a>'
            
            paper_html = f"""
            <article class="paper-card" data-tags="{','.join(paper.get('tags', []))}" data-status="{is_published}" data-date="{paper['published']}">
                <div class="venue-badge {venue_class}">{venue_display}</div>
                <h2 class="paper-title">
                    <a href="{paper['arxiv_url']}" target="_blank">{paper['title']}</a>
                </h2>
                <div class="paper-meta">
                    <span class="meta-item">📅 {paper['published']}</span>
                    <span class="meta-item">📖 ArXiv {category_name}</span>
                </div>
                <div class="paper-authors">
                    👥 {authors_html}
                </div>
                <div class="paper-tags">
                    {tags_html}
                </div>
                <div class="paper-abstract">
                    <details>
                        <summary>查看摘要</summary>
                        <p>{paper['abstract']}</p>
                    </details>
                </div>
                <div class="paper-links">
                    <a href="{paper['pdf_url']}" target="_blank" class="btn-link">📄 PDF</a>
                    <a href="{paper['arxiv_url']}" target="_blank" class="btn-link">🔗 ArXiv</a>
                    {code_links_html}
                </div>
            </article>
            """
            html_parts.append(paper_html)
        
        return '\n'.join(html_parts)
    
    def generate_css(self):
        """生成 CSS 样式"""
        css = """/* 全局样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* 头部样式 */
header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem 0;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
}

.update-time {
    font-size: 0.9rem;
    opacity: 0.8;
    margin-top: 0.5rem;
}

/* 导航和筛选 */
nav {
    background: white;
    padding: 1.5rem 20px;
    margin: 2rem auto;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.filter-section {
    margin-bottom: 1rem;
}

.filter-group {
    margin-bottom: 1rem;
}

.filter-label {
    display: inline-block;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}

.filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.filter-btn {
    padding: 0.5rem 1rem;
    border: 2px solid #667eea;
    background: white;
    color: #667eea;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 0.9rem;
}

.filter-btn:hover {
    background: #f0f0f0;
}

.filter-btn.active {
    background: #667eea;
    color: white;
}

.search-box {
    margin-top: 1.5rem;
}

.search-box input {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.search-box input:focus {
    outline: none;
    border-color: #667eea;
}

/* 主内容区域 */
main {
    margin-top: 0;
}

#papers-container {
    margin-top: 1rem;
}

/* 结果信息栏 */
.results-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding: 0.8rem;
    background: #f8f9fa;
    border-radius: 8px;
}

#resultsCount {
    font-size: 0.9rem;
    color: #666;
    font-weight: 500;
}

.export-btn {
    padding: 0.5rem 1rem;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background 0.3s;
}

.export-btn:hover {
    background: #5568d3;
}

/* 论文卡片 */
.paper-card {
    position: relative;
    background: white;
    padding: 1.5rem;
    padding-top: 2.5rem;
    padding-left: 4rem;
    margin-bottom: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: transform 0.3s, box-shadow 0.3s;
    display: flex;
    align-items: flex-start;
}

.paper-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

/* 复选框样式 */
.paper-select {
    position: absolute;
    left: 1.2rem;
    top: 1.5rem;
}

.paper-checkbox {
    width: 20px;
    height: 20px;
    cursor: pointer;
    accent-color: #667eea;
}

.paper-content {
    flex: 1;
}

/* 导出控制按钮 */
.export-controls {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

.select-btn {
    padding: 0.5rem 1rem;
    background: white;
    border: 2px solid #667eea;
    color: #667eea;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.3s;
}

.select-btn:hover {
    background: #667eea;
    color: white;
}

/* Venue 徽章 - 增强对比度和可见性 */
.venue-badge {
    display: inline-block;
    padding: 0.4rem 0.9rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: none;
    letter-spacing: 0.3px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    margin-left: 0.5rem;
    max-width: 600px;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.4;
}

.badge-neurips {
    background: #6B46C1;
    color: white;
}

.badge-cvpr, .badge-iccv, .badge-eccv {
    background: #E53E3E;
    color: white;
}

.badge-icml, .badge-iclr {
    background: #3182CE;
    color: white;
}

.badge-acl, .badge-emnlp, .badge-naacl {
    background: #38A169;
    color: white;
}

.badge-aaai, .badge-ijcai {
    background: #D69E2E;
    color: white;
}

.badge-published {
    background: #4A5568;
    color: white;
}

.preprint {
    background: #f5f5f5;
    color: #757575;
}

.paper-title {
    font-size: 1.3rem;
    margin-bottom: 0.8rem;
}

.paper-title a {
    color: #333;
    text-decoration: none;
    transition: color 0.3s;
}

.paper-title a:hover {
    color: #667eea;
}

.paper-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 0.8rem;
    font-size: 0.9rem;
    color: #666;
}

.meta-item.venue-conference {
    color: #2e7d32;
    font-weight: 600;
    background: #e8f5e9;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
}

.meta-item.venue-preprint {
    color: #666;
}

.paper-authors {
    margin-bottom: 0.8rem;
    color: #555;
    font-size: 0.95rem;
}

.paper-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.tag {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    background: #e3f2fd;
    color: #1976d2;
    border-radius: 15px;
    font-size: 0.85rem;
}

.paper-abstract {
    margin-bottom: 1rem;
}

.paper-abstract details summary {
    cursor: pointer;
    color: #667eea;
    font-weight: 500;
    user-select: none;
}

.paper-abstract details[open] summary {
    margin-bottom: 0.5rem;
}

.paper-abstract p {
    color: #555;
    line-height: 1.8;
    text-align: justify;
}

.paper-links {
    display: flex;
    gap: 1rem;
}

.btn-link {
    padding: 0.5rem 1rem;
    background: #667eea;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    font-size: 0.9rem;
    transition: background 0.3s;
    display: inline-block;
}

.btn-link:hover {
    background: #5568d3;
}

.btn-code {
    background: #28a745;
}

.btn-code:hover {
    background: #218838;
}

.btn-project {
    background: #17a2b8;
}

.btn-project:hover {
    background: #138496;
}

/* 底部 */
footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
}

footer a {
    color: #667eea;
    text-decoration: none;
}

/* 无结果提示 */
.no-results {
    text-align: center;
    padding: 3rem;
    color: #999;
    font-size: 1.1rem;
}

/* 加载指示器 */
.loading-indicator {
    text-align: center;
    padding: 2rem;
    color: #667eea;
    font-size: 1rem;
    font-weight: 500;
}

.loading-indicator::after {
    content: '';
    display: inline-block;
    width: 20px;
    height: 20px;
    margin-left: 10px;
    border: 3px solid #667eea;
    border-radius: 50%;
    border-top-color: transparent;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
    header h1 {
        font-size: 2rem;
    }
    
    .filters {
        justify-content: center;
    }
    
    .paper-meta {
        flex-direction: column;
        gap: 0.3rem;
    }
}
"""
        
        css_dir = self.output_dir / "css"
        css_dir.mkdir(parents=True, exist_ok=True)
        
        with open(css_dir / "style.css", 'w', encoding='utf-8') as f:
            f.write(css)
        
        logger.info("生成 CSS 样式文件")
    
    def generate_js(self):
        """生成 JavaScript 文件"""
        js = """// 筛选、搜索、排序和懒加载功能
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded');
    
    // 获取DOM元素
    const monthBtns = document.querySelectorAll('.month-btn');
    const statusBtns = document.querySelectorAll('.status-btn');
    const categoryBtns = document.querySelectorAll('.category-btn');
    const sortBtns = document.querySelectorAll('.sort-btn');
    const searchInput = document.getElementById('searchInput');
    const exportBtn = document.getElementById('exportBtn');
    const selectAllBtn = document.getElementById('selectAllBtn');
    const clearAllBtn = document.getElementById('clearAllBtn');
    const selectedCount = document.getElementById('selectedCount');
    const resultsCount = document.getElementById('resultsCount');
    const papersContainer = document.getElementById('papers-container');
    
    console.log('DOM elements:', {
        monthBtns: monthBtns.length,
        statusBtns: statusBtns.length,
        categoryBtns: categoryBtns.length,
        sortBtns: sortBtns.length,
        searchInput: !!searchInput,
        exportBtn: !!exportBtn,
        selectAllBtn: !!selectAllBtn,
        clearAllBtn: !!clearAllBtn,
        resultsCount: !!resultsCount,
        papersContainer: !!papersContainer
    });
    
    // 状态变量
    let allPapersData = [];  // 所有论文数据
    let currentMonth = 'all';  // 当前选中的月份
    let currentStatus = 'all';
    let currentCategory = 'all';
    let currentSort = 'date-desc';
    let searchTerm = '';
    let filteredPapers = [];
    let loadedCount = 0;
    const initialBatchSize = 20;  // 第一次加载20个
    const subsequentBatchSize = 10;  // 后续每次加载10个
    let isLoading = false;
    let observer = null;
    let monthsCache = {};  // 缓存已加载的月份数据
    
    // 加载月份索引
    async function loadMonthsIndex() {
        try {
            const response = await fetch('data/index.json');
            const monthsIndex = await response.json();
            console.log('Months index loaded:', monthsIndex);
            
            // 默认加载最新月份的数据
            if (monthsIndex.length > 0) {
                await loadMonthData('all');
            }
        } catch (e) {
            console.error('Failed to load months index:', e);
        }
    }
    
    // 加载指定月份的数据
    async function loadMonthData(month) {
        if (month === 'all') {
            // 加载所有月份
            try {
                const response = await fetch('data/index.json');
                const monthsIndex = await response.json();
                
                // 加载所有月份数据
                allPapersData = [];
                for (const monthInfo of monthsIndex) {
                    if (!monthsCache[monthInfo.month]) {
                        const monthResponse = await fetch(`data/${monthInfo.month}.json`);
                        monthsCache[monthInfo.month] = await monthResponse.json();
                    }
                    allPapersData.push(...monthsCache[monthInfo.month]);
                }
                console.log(`Loaded all months, total ${allPapersData.length} papers`);
            } catch (e) {
                console.error('Failed to load all months data:', e);
            }
        } else {
            // 加载单个月份
            if (!monthsCache[month]) {
                try {
                    const response = await fetch(`data/${month}.json`);
                    monthsCache[month] = await response.json();
                    console.log(`Loaded month ${month}, ${monthsCache[month].length} papers`);
                } catch (e) {
                    console.error(`Failed to load month ${month}:`, e);
                    return;
                }
            }
            allPapersData = monthsCache[month];
            console.log(`Using cached data for ${month}, ${allPapersData.length} papers`);
        }
        
        // 数据加载完成后，触发筛选
        filterAndSortPapers();
    }
    
    // 生成论文HTML
    function createPaperHTML(paper) {
        const tags = paper.tags ? paper.tags.map(tag => `<span class="tag">${tag}</span>`).join('') : '';
        
        // 提取代码链接
        let codeLink = '';
        if (paper.code_link) {
            codeLink = `<a href="${paper.code_link}" target="_blank" class="code-link">📄 Code/Project</a>`;
        }
        
        // 获取会议徽章
        let venueBadge = '';
        if (paper.conference) {
            const badgeInfo = getVenueBadge(paper.conference);
            if (badgeInfo) {
                venueBadge = `<span class="venue-badge ${badgeInfo.class}">${badgeInfo.text}</span>`;
            }
        }
        
        const status = paper.conference ? 'published' : 'preprint';
        const firstCategory = paper.categories && paper.categories.length > 0 ? paper.categories[0] : '';
        
        return `
            <article class="paper-card" data-date="${paper.published}" data-status="${status}" data-tags="${paper.tags ? paper.tags.join(',') : ''}" data-paper-id="${paper.id}">
                <div class="paper-select">
                    <input type="checkbox" class="paper-checkbox" id="check-${paper.id}" data-paper-id="${paper.id}">
                    <label for="check-${paper.id}"></label>
                </div>
                <div class="paper-content">
                    <h2 class="paper-title">
                        <a href="https://arxiv.org/abs/${paper.id}" target="_blank">${paper.title}</a>
                    </h2>
                    <div class="paper-meta">
                        <span class="meta-item">📅 ${paper.published}</span>
                        ${venueBadge}
                        ${codeLink}
                    </div>
                    <div class="paper-authors">
                        👥 ${paper.authors}
                    </div>
                    <div class="paper-tags">
                        ${tags}
                    </div>
                    <div class="paper-abstract">
                        <details>
                            <summary>查看摘要</summary>
                            <p>${paper.abstract}</p>
                        </details>
                    </div>
                </div>
            </article>
        `;
    }
    
    // 获取会议徽章信息
    function getVenueBadge(conference) {
        if (!conference) return null;
        
        // 根据会议名称中包含的关键词决定徽章样式
        const conferenceUpper = conference.toUpperCase();
        let badgeClass = 'badge-published';  // 默认样式
        
        // 顶级会议匹配
        if (conferenceUpper.includes('NEURIPS')) {
            badgeClass = 'badge-neurips';
        } else if (conferenceUpper.includes('ICLR')) {
            badgeClass = 'badge-iclr';
        } else if (conferenceUpper.includes('ICML')) {
            badgeClass = 'badge-icml';
        } else if (conferenceUpper.includes('CVPR')) {
            badgeClass = 'badge-cvpr';
        } else if (conferenceUpper.includes('ICCV')) {
            badgeClass = 'badge-iccv';
        } else if (conferenceUpper.includes('ECCV')) {
            badgeClass = 'badge-eccv';
        } else if (conferenceUpper.includes('ACL')) {
            badgeClass = 'badge-acl';
        } else if (conferenceUpper.includes('EMNLP')) {
            badgeClass = 'badge-emnlp';
        } else if (conferenceUpper.includes('NAACL')) {
            badgeClass = 'badge-naacl';
        } else if (conferenceUpper.includes('AAAI')) {
            badgeClass = 'badge-aaai';
        } else if (conferenceUpper.includes('IJCAI')) {
            badgeClass = 'badge-ijcai';
        }
        
        // 直接使用从 ArXiv comments 提取的完整会议名称
        return { class: badgeClass, text: conference };
    }
    
    // 更新研究领域按钮的数量
    function updateCategoryButtonCounts() {
        // 先筛选出符合当前状态的论文
        const statusFilteredPapers = allPapersData.filter(paper => {
            const status = paper.conference ? 'published' : 'preprint';
            return currentStatus === 'all' || status === currentStatus;
        });
        
        // 计算各个领域的数量
        const categoryCounts = {
            'all': statusFilteredPapers.length,
            'Computer Vision': 0,
            'Natural Language Processing': 0,
            'Machine Learning': 0,
            'Robotics': 0,
            'Multimodal': 0
        };
        
        statusFilteredPapers.forEach(paper => {
            const tags = paper.tags || [];
            tags.forEach(tag => {
                if (categoryCounts.hasOwnProperty(tag)) {
                    categoryCounts[tag]++;
                }
            });
        });
        
        // 更新按钮文本
        categoryBtns.forEach(btn => {
            const category = btn.dataset.category;
            const displayName = category === 'all' ? '全部' : 
                               category === 'Natural Language Processing' ? 'NLP' : category;
            const count = categoryCounts[category] || 0;
            btn.textContent = `${displayName} (${count})`;
        });
    }
    
    // 筛选和排序论文
    function filterAndSortPapers() {
        console.log('Filtering papers:', { currentStatus, currentCategory, searchTerm, currentSort });
        
        // 筛选
        filteredPapers = allPapersData.filter(paper => {
            const status = paper.conference ? 'published' : 'preprint';
            const tags = paper.tags || [];
            const text = `${paper.title} ${paper.authors} ${paper.abstract}`.toLowerCase();
            
            const matchStatus = currentStatus === 'all' || status === currentStatus;
            const matchCategory = currentCategory === 'all' || tags.includes(currentCategory);
            const matchSearch = searchTerm === '' || text.includes(searchTerm);
            
            return matchStatus && matchCategory && matchSearch;
        });
        
        console.log(`Filtered to ${filteredPapers.length} papers`);
        
        // 排序
        filteredPapers.sort((a, b) => {
            const dateA = new Date(a.published);
            const dateB = new Date(b.published);
            
            if (currentSort === 'date-desc') {
                return dateB - dateA;
            } else {
                return dateA - dateB;
            }
        });
        
        // 更新研究领域按钮的数量
        updateCategoryButtonCounts();
        
        // 更新显示
        if (resultsCount) {
            resultsCount.textContent = `显示 ${filteredPapers.length} 篇论文`;
        }
        
        // 重置懒加载
        loadedCount = 0;
        if (papersContainer) {
            papersContainer.innerHTML = '';
        }
        
        // 移除旧的 observer
        if (observer) {
            observer.disconnect();
        }
        
        // 加载第一批
        loadMorePapers();
    }
    
    // 加载更多论文
    function loadMorePapers() {
        if (isLoading || loadedCount >= filteredPapers.length) {
            console.log('Skip loading:', { isLoading, loadedCount, total: filteredPapers.length });
            return;
        }
        
        isLoading = true;
        
        // 第一次加载50个，后续每次10个
        const batchSize = loadedCount === 0 ? initialBatchSize : subsequentBatchSize;
        console.log(`Loading papers ${loadedCount} to ${loadedCount + batchSize} (batch size: ${batchSize})`);
        
        const endIndex = Math.min(loadedCount + batchSize, filteredPapers.length);
        const fragment = document.createDocumentFragment();
        
        for (let i = loadedCount; i < endIndex; i++) {
            const paperHTML = createPaperHTML(filteredPapers[i]);
            const temp = document.createElement('div');
            temp.innerHTML = paperHTML;
            fragment.appendChild(temp.firstElementChild);
        }
        
        // 移除旧的加载指示器
        const oldIndicator = document.getElementById('loading-indicator');
        if (oldIndicator) {
            oldIndicator.remove();
        }
        
        papersContainer.appendChild(fragment);
        loadedCount = endIndex;
        isLoading = false;
        
        console.log(`Loaded ${endIndex} papers total`);
        
        // 如果还有更多，设置加载触发器
        if (loadedCount < filteredPapers.length) {
            setupLoadTrigger();
        }
    }
    
    // 设置加载触发器
    function setupLoadTrigger() {
        let indicator = document.getElementById('loading-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'loading-indicator';
            indicator.className = 'loading-indicator';
            indicator.style.height = '100px';
            indicator.style.margin = '20px 0';
            indicator.style.textAlign = 'center';
            indicator.style.color = '#666';
            indicator.textContent = '加载更多...';
            papersContainer.appendChild(indicator);
        }
        
        // 创建新的 observer
        if (observer) {
            observer.disconnect();
        }
        
        observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    console.log('Loading more papers (intersection detected)');
                    loadMorePapers();
                }
            });
        }, {
            rootMargin: '200px'
        });
        
        observer.observe(indicator);
    }
    
    // 月份筛选
    monthBtns.forEach(btn => {
        btn.addEventListener('click', async function() {
            console.log('Month button clicked:', this.dataset.month);
            monthBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentMonth = this.dataset.month;
            
            // 显示加载提示
            if (resultsCount) {
                resultsCount.textContent = '加载中...';
            }
            if (papersContainer) {
                papersContainer.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;">加载中...</div>';
            }
            
            // 加载月份数据
            await loadMonthData(currentMonth);
        });
    });
    
    // 发表状态筛选
    statusBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('Status button clicked:', this.dataset.status);
            statusBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentStatus = this.dataset.status;
            filterAndSortPapers();
        });
    });
    
    // 研究领域筛选
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('Category button clicked:', this.dataset.category);
            categoryBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentCategory = this.dataset.category;
            filterAndSortPapers();
        });
    });
    
    // 排序按钮
    sortBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            console.log('Sort button clicked:', this.dataset.sort);
            e.preventDefault();
            sortBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentSort = this.dataset.sort;
            filterAndSortPapers();
        });
    });
    
    // 搜索输入
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            searchTerm = this.value.toLowerCase();
            console.log('Search term:', searchTerm);
            filterAndSortPapers();
        });
    }
    
    // 更新选中数量
    function updateSelectedCount() {
        const count = document.querySelectorAll('.paper-checkbox:checked').length;
        if (selectedCount) {
            selectedCount.textContent = count;
        }
    }
    
    // 监听复选框变化（使用事件委托）
    if (papersContainer) {
        papersContainer.addEventListener('change', function(e) {
            if (e.target.classList.contains('paper-checkbox')) {
                updateSelectedCount();
            }
        });
    }
    
    // 全选功能
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('.paper-checkbox');
            checkboxes.forEach(cb => cb.checked = true);
            updateSelectedCount();
            console.log('All papers selected');
        });
    }
    
    // 清空选择
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('.paper-checkbox');
            checkboxes.forEach(cb => cb.checked = false);
            updateSelectedCount();
            console.log('All selections cleared');
        });
    }
    
    // 导出功能
    if (exportBtn) {
        exportBtn.addEventListener('click', function(e) {
            console.log('Export button clicked');
            e.preventDefault();
            exportToBibTeX();
        });
    }
    
    // 导出为 BibTeX
    function exportToBibTeX() {
        // 获取所有选中的复选框
        const checkboxes = document.querySelectorAll('.paper-checkbox:checked');
        
        if (checkboxes.length === 0) {
            alert('请至少选择一篇论文导出！');
            return;
        }
        
        // 获取选中的论文ID
        const selectedIds = Array.from(checkboxes).map(cb => cb.dataset.paperId);
        
        // 从所有论文数据中找到对应的论文
        const selectedPapers = allPapersData.filter(paper => selectedIds.includes(paper.id));
        
        let bibtex = '';
        selectedPapers.forEach((paper, index) => {
            const arxivId = paper.id;
            const year = paper.published.split('-')[0];
            
            bibtex += `@article{${arxivId.replace('.', '_')},\\n`;
            bibtex += `  title={${paper.title}},\\n`;
            bibtex += `  author={${paper.authors}},\\n`;
            bibtex += `  year={${year}},\\n`;
            bibtex += `  journal={arXiv preprint arXiv:${arxivId}}`;
            if (paper.conference) {
                bibtex += `,\\n  note={${paper.conference}}`;
            }
            bibtex += `\\n}\\n\\n`;
        });
        
        console.log(`Exporting ${selectedPapers.length} selected papers`);
        downloadFile(bibtex, 'papers.bib', 'text/plain');
    }
    
    // 下载文件
    function downloadFile(content, filename, contentType) {
        const blob = new Blob([content], { type: contentType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        console.log('File download triggered:', filename);
    }
    
    // 初始化 - 加载数据
    console.log('Initializing...');
    loadMonthsIndex();
});
"""
        
        js_dir = self.output_dir / "js"
        js_dir.mkdir(parents=True, exist_ok=True)
        
        with open(js_dir / "main.js", 'w', encoding='utf-8') as f:
            f.write(js)
        
        logger.info("生成 JavaScript 文件")
    
    def run(self):
        """运行生成流程"""
        logger.info("开始生成静态网页...")
        
        self.load_papers()
        self.generate_monthly_data_files()  # 生成月度数据文件
        self.generate_css()
        self.generate_js()
        self.generate_index_html()
        
        logger.info(f"网页生成完成! 输出目录: {self.output_dir}")


def main():
    generator = HTMLGenerator()
    generator.run()


if __name__ == "__main__":
    main()
