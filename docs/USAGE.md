# DailyPaper 使用指南

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/DailyPaper.git
cd DailyPaper
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 本地测试

```bash
# 抓取论文
python scripts/fetch_papers.py

# 生成网页
python scripts/generate_html.py

# 查看生成的网页
# 在浏览器中打开 docs/index.html
```

## 部署到 GitHub Pages

### 方法一：使用 GitHub Actions（推荐）

1. **Fork 本项目到你的 GitHub 账户**

2. **启用 GitHub Actions**
   - 进入 Settings > Actions > General
   - 确保 "Allow all actions and reusable workflows" 已勾选

3. **配置 GitHub Pages**
   - 进入 Settings > Pages
   - Source 选择 "Deploy from a branch"
   - Branch 选择 `gh-pages` 和 `/ (root)`
   - 点击 Save

4. **手动触发首次运行**（可选）
   - 进入 Actions 标签
   - 选择 "Update Papers Daily" workflow
   - 点击 "Run workflow"

5. **等待部署完成**
   - Actions 运行完成后，访问 `https://yourusername.github.io/DailyPaper/`

### 方法二：手动部署

```bash
# 运行脚本
python scripts/fetch_papers.py
python scripts/generate_html.py

# 提交更改
git add .
git commit -m "Update papers"
git push

# 部署到 gh-pages 分支
git subtree push --prefix docs origin gh-pages
```

## 配置说明

### 编辑 config.yaml

```yaml
# 修改 ArXiv 类别
sources:
  arxiv:
    categories:
      - cs.AI    # 添加或删除你关注的类别
      - cs.CV
      - cs.CL

# 修改抓取数量
sources:
  arxiv:
    max_results: 50  # 每个类别抓取的最大论文数

# 修改更新频率
schedule:
  cron: "0 0 * * *"  # 每天 UTC 0:00
```

### 自定义分类关键词

在 `config.yaml` 中修改 `categories` 部分来自定义论文分类：

```yaml
categories:
  Your Custom Category:
    keywords:
      - keyword1
      - keyword2
      - keyword3
```

## 高级功能

### 添加新的数据源

在 `scripts/fetch_papers.py` 中添加新的抓取方法：

```python
def fetch_custom_source(self) -> List[Dict]:
    """从自定义数据源抓取论文"""
    papers = []
    # 你的抓取逻辑
    return papers
```

然后在 `run()` 方法中调用：

```python
def run(self):
    arxiv_papers = self.fetch_arxiv_papers()
    custom_papers = self.fetch_custom_source()  # 添加这行
    all_papers = arxiv_papers + custom_papers   # 修改这行
```

### 自定义网页样式

编辑 `docs/css/style.css` 来修改网页外观。

### 添加更多筛选选项

在 `scripts/generate_html.py` 的 `generate_index_html()` 方法中添加更多筛选按钮。

## 故障排除

### 问题：GitHub Actions 运行失败

**解决方案**：
- 检查 Actions 日志查看具体错误
- 确保 requirements.txt 中的依赖正确
- 检查网络问题（可能是 ArXiv API 访问限制）

### 问题：网页没有更新

**解决方案**：
- 检查 GitHub Pages 设置是否正确
- 清除浏览器缓存
- 等待几分钟（GitHub Pages 部署需要时间）

### 问题：抓取不到论文

**解决方案**：
- 检查 config.yaml 中的类别是否正确
- 检查 ArXiv API 是否正常（访问 https://arxiv.org）
- 增加 `days_back` 参数来抓取更长时间范围的论文

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
