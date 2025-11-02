# PowerShell 快速启动脚本（Windows）

Write-Host "🚀 DailyPaper 快速启动" -ForegroundColor Green
Write-Host ""

# 检查 Python
try {
    $pythonVersion = python --version
    Write-Host "✅ Python 已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到 Python，请先安装" -ForegroundColor Red
    exit 1
}

# 创建虚拟环境（可选）
if (-not (Test-Path "venv")) {
    Write-Host "📦 创建虚拟环境..." -ForegroundColor Yellow
    python -m venv venv
}

# 激活虚拟环境
Write-Host "🔧 激活虚拟环境..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# 安装依赖
Write-Host "📥 安装依赖..." -ForegroundColor Yellow
pip install -r requirements.txt

# 运行测试
Write-Host ""
Write-Host "🧪 运行测试..." -ForegroundColor Yellow
python test.py

Write-Host ""
Write-Host "✅ 完成！" -ForegroundColor Green
Write-Host "💡 在浏览器中打开 docs\index.html 查看效果" -ForegroundColor Cyan
