# DailyPaper - 自动文献汇总工具

![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

每天自动汇总 AI/ML/CV/NLP 领域的最新论文，节省你的检索时间！

## 🎯 功能特点

- ✨ **自动更新**：每天自动抓取最新论文
- 📚 **多源聚合**：支持 ArXiv、顶级会议、期刊等多个数据源
- 🔍 **智能分类**：按领域自动分类（CV、NLP、ML 等）
- 🎨 **美观展示**：响应式网页设计，支持搜索和筛选
- 🔗 **快速访问**：论文原文直接链接

## 📖 支持的数据源

- **ArXiv**：cs.AI, cs.CV, cs.CL, cs.LG 等分类
- **会议**：NeurIPS, ICML, CVPR, ICCV, ECCV, ACL, EMNLP 等
- **期刊**：Nature, Science, PAMI, JMLR 等

## 🚀 快速开始

### 本地运行

```bash
# 克隆项目
git clone https://github.com/4everWZ/DailyPaper.git
cd DailyPaper

# 安装依赖
pip install -r requirements.txt

# 运行爬虫
python scripts/fetch_papers.py

# 生成网页
python scripts/generate_html.py
```

### 部署到 GitHub Pages

**快速部署（推荐）：**
```powershell
# 运行一键部署脚本
.\deploy.ps1
```

**手动部署：**
1. 在 GitHub 创建新仓库（名为 `DailyPaper`，Public）
2. 将代码推送到 GitHub
3. 在 Settings > Pages 中配置：Source = `gh-pages` 分支
4. 在 Settings > Actions > General 中配置权限：Read and write
5. 在 Actions 中手动运行 "Update Papers Daily"
6. 访问 `https://4everWZ.github.io/DailyPaper/`

**详细步骤请查看：[DEPLOYMENT.md](DEPLOYMENT.md)**

## 📁 项目结构

```
DailyPaper/
├── .github/
│   └── workflows/
│       └── update-papers.yml    # GitHub Actions 自动化脚本
├── scripts/
│   ├── fetch_papers.py          # 论文抓取脚本
│   ├── generate_html.py         # 生成静态页面
│   └── utils.py                 # 工具函数
├── data/
│   └── papers.json              # 论文数据存储
├── docs/                        # GitHub Pages 源文件
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── requirements.txt
└── README.md
```

## ⚙️ 配置

编辑 `config.yaml` 文件来自定义：

```yaml
# 抓取配置
sources:
  arxiv:
    enabled: true
    categories: ['cs.AI', 'cs.CV', 'cs.CL', 'cs.LG']
    max_results: 50
  
# 更新频率
schedule: "0 0 * * *"  # 每天 UTC 0:00

# 领域关键词
keywords:
  CV: ['computer vision', 'image', 'video', 'detection', 'segmentation']
  NLP: ['natural language', 'language model', 'transformer', 'nlp']
  ML: ['machine learning', 'deep learning', 'neural network']
```

## 📊 数据来源

- [ArXiv](https://arxiv.org/) - 开放获取的预印本论文库

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

感谢所有开源数据源提供者和贡献者！

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star ⭐️
