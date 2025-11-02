# 🚀 一键部署脚本
# 运行此脚本快速初始化 Git 并准备推送到 GitHub

Write-Host "🚀 DailyPaper GitHub 部署准备" -ForegroundColor Green
Write-Host "=" * 60
Write-Host ""

# 检查 Git
try {
    $gitVersion = git --version
    Write-Host "✅ Git 已安装: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到 Git，请先安装 Git" -ForegroundColor Red
    Write-Host "下载地址: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# 检查是否已经是 Git 仓库
if (Test-Path ".git") {
    Write-Host "⚠️  已经是 Git 仓库" -ForegroundColor Yellow
    $continue = Read-Host "是否继续？这将添加并提交所有更改 (y/n)"
    if ($continue -ne "y") {
        Write-Host "取消操作" -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "📦 初始化 Git 仓库..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git 仓库初始化完成" -ForegroundColor Green
}

Write-Host ""

# 添加所有文件
Write-Host "📝 添加文件到 Git..." -ForegroundColor Yellow
git add .

Write-Host ""

# 提交
Write-Host "💾 提交更改..." -ForegroundColor Yellow
git commit -m "Initial commit: DailyPaper - 自动文献汇总工具"

Write-Host ""
Write-Host "=" * 60
Write-Host "✅ 本地 Git 准备完成！" -ForegroundColor Green
Write-Host ""

# 提示下一步
Write-Host "📋 下一步操作：" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  在 GitHub 上创建新仓库" -ForegroundColor Yellow
Write-Host "   访问: https://github.com/new" -ForegroundColor White
Write-Host "   - 仓库名: DailyPaper" -ForegroundColor White
Write-Host "   - 类型: Public" -ForegroundColor White
Write-Host "   - 不要勾选 'Add a README file'" -ForegroundColor White
Write-Host ""

Write-Host "2️⃣  获取你的 GitHub 用户名" -ForegroundColor Yellow
$username = Read-Host "   请输入你的 GitHub 用户名"

if ($username) {
    Write-Host ""
    Write-Host "3️⃣  执行以下命令连接到 GitHub：" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "git remote add origin https://github.com/$username/DailyPaper.git" -ForegroundColor White
    Write-Host "git branch -M main" -ForegroundColor White
    Write-Host "git push -u origin main" -ForegroundColor White
    Write-Host ""
    
    $autoPush = Read-Host "是否现在就执行这些命令？(y/n)"
    
    if ($autoPush -eq "y") {
        Write-Host ""
        Write-Host "🚀 正在推送到 GitHub..." -ForegroundColor Yellow
        
        try {
            git remote add origin "https://github.com/$username/DailyPaper.git" 2>$null
            git branch -M main
            git push -u origin main
            
            Write-Host ""
            Write-Host "✅ 成功推送到 GitHub！" -ForegroundColor Green
            Write-Host ""
            Write-Host "🎯 最后一步：配置 GitHub Pages" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "1. 访问: https://github.com/$username/DailyPaper/settings/pages" -ForegroundColor White
            Write-Host "2. Source 选择: Deploy from a branch" -ForegroundColor White
            Write-Host "3. Branch 选择: gh-pages 和 / (root)" -ForegroundColor White
            Write-Host "4. 点击 Save" -ForegroundColor White
            Write-Host ""
            Write-Host "5. 访问: https://github.com/$username/DailyPaper/settings/actions" -ForegroundColor White
            Write-Host "6. Workflow permissions 选择: Read and write permissions" -ForegroundColor White
            Write-Host "7. 勾选: Allow GitHub Actions to create and approve pull requests" -ForegroundColor White
            Write-Host "8. 点击 Save" -ForegroundColor White
            Write-Host ""
            Write-Host "9. 访问: https://github.com/$username/DailyPaper/actions" -ForegroundColor White
            Write-Host "10. 点击 'Update Papers Daily' > 'Run workflow'" -ForegroundColor White
            Write-Host ""
            Write-Host "⏰ 等待 2-3 分钟后，访问你的网站：" -ForegroundColor Cyan
            Write-Host "   https://$username.github.io/DailyPaper/" -ForegroundColor Green -BackgroundColor Black
            Write-Host ""
            
        } catch {
            Write-Host ""
            Write-Host "⚠️  推送失败，可能的原因：" -ForegroundColor Yellow
            Write-Host "   - 远程仓库已存在" -ForegroundColor White
            Write-Host "   - 用户名错误" -ForegroundColor White
            Write-Host "   - 需要先在 GitHub 上创建仓库" -ForegroundColor White
            Write-Host ""
            Write-Host "请手动执行上面显示的命令" -ForegroundColor White
        }
    }
}

Write-Host ""
Write-Host "📖 详细部署说明请查看: DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host ""
