#!/usr/bin/env python3
"""
测试脚本 - 快速测试项目是否正常工作
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scripts.fetch_papers import PaperFetcher
from scripts.generate_html import HTMLGenerator


def test_fetch():
    """测试论文抓取"""
    print("=" * 60)
    print("测试论文抓取功能")
    print("=" * 60)
    
    fetcher = PaperFetcher()
    papers = fetcher.fetch_arxiv_papers()
    
    if papers:
        print(f"✅ 成功抓取 {len(papers)} 篇论文")
        print(f"\n第一篇论文示例：")
        print(f"标题: {papers[0]['title']}")
        print(f"作者: {', '.join(papers[0]['authors'][:3])}")
        print(f"日期: {papers[0]['published']}")
        return True
    else:
        print("❌ 未能抓取到论文")
        return False


def test_generate():
    """测试网页生成"""
    print("\n" + "=" * 60)
    print("测试网页生成功能")
    print("=" * 60)
    
    generator = HTMLGenerator()
    generator.load_papers()
    
    if generator.papers:
        print(f"✅ 加载了 {len(generator.papers)} 篇论文")
        generator.generate_css()
        generator.generate_js()
        generator.generate_index_html()
        print(f"✅ 网页生成成功")
        print(f"📁 输出目录: {generator.output_dir}")
        return True
    else:
        print("❌ 没有论文数据")
        return False


def main():
    """主测试流程"""
    print("\n🚀 开始测试 DailyPaper 项目\n")
    
    # 测试抓取
    fetch_success = test_fetch()
    
    # 测试生成
    generate_success = test_generate()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    if fetch_success and generate_success:
        print("✅ 所有测试通过！")
        print("\n下一步：")
        print("1. 在浏览器中打开 docs/index.html 查看效果")
        print("2. 修改 config.yaml 自定义配置")
        print("3. 提交到 GitHub 并配置 GitHub Pages")
        return 0
    else:
        print("❌ 部分测试失败")
        print("\n请检查：")
        print("1. 是否已安装所有依赖: pip install -r requirements.txt")
        print("2. 网络连接是否正常")
        print("3. config.yaml 配置是否正确")
        return 1


if __name__ == "__main__":
    sys.exit(main())
