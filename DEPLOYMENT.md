# 🚀 部署到 GitHub Pages 指南

## 步骤 1：初始化 Git 仓库（本地）

在项目目录下运行：

```powershell
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: DailyPaper project"
```

## 步骤 2：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `DailyPaper` (或其他你喜欢的名字)
   - **Description**: `📚 每日自动更新 AI/ML/CV/NLP 领域最新论文`
   - **Public** (必须是 Public 才能使用免费的 GitHub Pages)
   - **不要** 勾选 "Add a README file"（我们已经有了）
3. 点击 **Create repository**

## 步骤 3：连接到 GitHub 并推送

复制 GitHub 上显示的命令，类似这样（替换成你的用户名）：

```powershell
# 添加远程仓库
git remote add origin https://github.com/4everWZ/DailyPaper.git

# 重命名分支为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

## 步骤 4：配置 GitHub Pages

1. 进入你的 GitHub 仓库页面
2. 点击 **Settings** (设置)
3. 在左侧菜单找到 **Pages**
4. 在 "Build and deployment" 下：
   - **Source**: 选择 `Deploy from a branch`
   - **Branch**: 选择 `gh-pages` 和 `/ (root)`
   - 点击 **Save**

## 步骤 5：配置 GitHub Actions 权限

1. 在 Settings 中，点击左侧的 **Actions** > **General**
2. 滚动到 **Workflow permissions**
3. 选择 **Read and write permissions**
4. 勾选 **Allow GitHub Actions to create and approve pull requests**
5. 点击 **Save**

## 步骤 6：触发首次自动更新

方法 1：手动触发
1. 在 GitHub 仓库页面，点击 **Actions** 标签
2. 在左侧选择 **Update Papers Daily** workflow
3. 点击右侧的 **Run workflow** 按钮
4. 点击绿色的 **Run workflow** 确认

方法 2：修改文件触发
```powershell
# 随便修改一个文件，比如 README.md，然后提交
git add .
git commit -m "Trigger GitHub Actions"
git push
```

## 步骤 7：等待部署完成

1. 在 **Actions** 标签中查看运行状态
2. 等待绿色的 ✓ 出现（通常需要 1-3 分钟）
3. 访问你的网站：`https://4everWZ.github.io/DailyPaper/`

## 🎉 完成！

现在你的论文汇总工具将：
- ✅ 每天 UTC 0:00 自动运行
- ✅ 自动抓取最新论文
- ✅ 自动更新网站

## 📝 后续维护

### 修改配置
编辑 `config.yaml` 后提交推送：
```powershell
git add config.yaml
git commit -m "Update config"
git push
```

### 手动触发更新
在 GitHub Actions 页面点击 "Run workflow"

### 查看网站
访问：`https://4everWZ.github.io/DailyPaper/`

## ⚠️ 常见问题

### 问题 1：Actions 运行失败
- 检查 Settings > Actions > General 中的权限设置
- 查看 Actions 日志了解具体错误

### 问题 2：网站显示 404
- 确保已在 Settings > Pages 中配置了 `gh-pages` 分支
- 等待 3-5 分钟让 GitHub Pages 完成部署
- 检查 Actions 是否成功创建了 `gh-pages` 分支

### 问题 3：网站没有更新
- 检查 Actions 运行日志
- 清除浏览器缓存
- 等待几分钟（GitHub Pages 有缓存延迟）

## 🎯 自定义域名（可选）

如果你有自己的域名：
1. 在 Settings > Pages > Custom domain 中输入域名
2. 在你的域名提供商处添加 CNAME 记录指向 `你的用户名.github.io`
