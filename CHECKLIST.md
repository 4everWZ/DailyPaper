# ✅ 部署检查清单

在部署到 GitHub 之前，请确认：

## 📋 部署前检查

- [ ] Python 依赖已安装 (`pip install -r requirements.txt`)
- [ ] 本地测试成功 (`python quick_test.py` 或 `python simple_test.py`)
- [ ] 已生成网页文件 (`docs/index.html` 存在)
- [ ] Git 已安装 (`git --version`)
- [ ] 已有 GitHub 账号

## 🚀 部署步骤

### 方式 1：使用一键部署脚本（推荐）

```powershell
.\deploy.ps1
```

按照提示操作即可！

### 方式 2：手动部署

#### 步骤 1：初始化 Git
```powershell
git init
git add .
git commit -m "Initial commit: DailyPaper"
```

#### 步骤 2：在 GitHub 创建仓库
- [ ] 访问 https://github.com/new
- [ ] 仓库名：`DailyPaper`
- [ ] 类型：`Public`
- [ ] 不勾选 "Add a README file"
- [ ] 点击 "Create repository"

#### 步骤 3：推送代码
```powershell
git remote add origin https://github.com/4everWZ/DailyPaper.git
git branch -M main
git push -u origin main
```

#### 步骤 4：配置 GitHub Pages
- [ ] 进入 Settings > Pages
- [ ] Source: `Deploy from a branch`
- [ ] Branch: `gh-pages` / `(root)`
- [ ] 点击 Save

#### 步骤 5：配置 Actions 权限
- [ ] 进入 Settings > Actions > General
- [ ] Workflow permissions: `Read and write permissions`
- [ ] 勾选 "Allow GitHub Actions to create and approve pull requests"
- [ ] 点击 Save

#### 步骤 6：触发首次运行
- [ ] 进入 Actions 标签
- [ ] 选择 "Update Papers Daily"
- [ ] 点击 "Run workflow"
- [ ] 等待运行完成（绿色 ✓）

#### 步骤 7：访问网站
- [ ] 等待 2-3 分钟
- [ ] 访问 `https://4everWZ.github.io/DailyPaper/`

## 🎉 部署成功标志

- ✅ GitHub Actions 显示绿色 ✓
- ✅ 创建了 `gh-pages` 分支
- ✅ 网站可以正常访问
- ✅ 显示了论文列表

## ⚠️ 常见问题

### Actions 失败？
- 检查 Settings > Actions 权限设置
- 查看 Actions 日志获取详细错误

### 网站 404？
- 确认 Pages 配置使用 `gh-pages` 分支
- 等待 3-5 分钟让部署完成
- 检查 Actions 是否成功

### 论文没有更新？
- 手动触发 Actions: Actions > Run workflow
- 检查 `config.yaml` 中的配置
- 查看 Actions 运行日志

## 📝 后续操作

### 每日自动更新
✅ 已配置！每天 UTC 0:00 自动运行

### 手动触发更新
Actions > Update Papers Daily > Run workflow

### 修改配置
编辑 `config.yaml` 然后：
```powershell
git add config.yaml
git commit -m "Update config"
git push
```

## 📚 相关文档

- 详细部署指南：[DEPLOYMENT.md](DEPLOYMENT.md)
- 使用说明：[docs/USAGE.md](docs/USAGE.md)
- 项目介绍：[README.md](README.md)

---

🎯 **目标**：让你的论文汇总工具在 5 分钟内上线！
