#!/usr/bin/env python3
"""
工具函数模块
"""

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime


def load_json(file_path: str) -> List[Dict]:
    """加载 JSON 文件"""
    path = Path(file_path)
    if not path.exists():
        return []
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: List[Dict], file_path: str):
    """保存为 JSON 文件"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def deduplicate_papers(papers: List[Dict], key: str = 'id') -> List[Dict]:
    """去除重复论文"""
    seen = set()
    unique_papers = []
    
    for paper in papers:
        paper_id = paper.get(key)
        if paper_id and paper_id not in seen:
            seen.add(paper_id)
            unique_papers.append(paper)
    
    return unique_papers


def format_authors(authors: List[str], max_authors: int = 5) -> str:
    """格式化作者列表"""
    if len(authors) <= max_authors:
        return ', '.join(authors)
    else:
        return ', '.join(authors[:max_authors]) + ' et al.'


def truncate_text(text: str, max_length: int = 200) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'


def parse_date(date_str: str) -> datetime:
    """解析日期字符串"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except:
        return datetime.now()


def get_papers_by_date(papers: List[Dict], date: str) -> List[Dict]:
    """获取指定日期的论文"""
    return [p for p in papers if p.get('published') == date]


def get_papers_by_category(papers: List[Dict], category: str) -> List[Dict]:
    """获取指定类别的论文"""
    return [p for p in papers if category in p.get('tags', [])]


def count_papers_by_category(papers: List[Dict]) -> Dict[str, int]:
    """统计各类别论文数量"""
    counts = {}
    for paper in papers:
        for tag in paper.get('tags', []):
            counts[tag] = counts.get(tag, 0) + 1
    return counts
