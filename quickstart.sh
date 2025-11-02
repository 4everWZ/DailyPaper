#!/bin/bash
# 快速启动脚本（Linux/Mac）

echo "🚀 DailyPaper 快速启动"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装"
    exit 1
fi

# 创建虚拟环境（可选）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt

# 运行测试
echo ""
echo "🧪 运行测试..."
python test.py

echo ""
echo "✅ 完成！"
echo "💡 在浏览器中打开 docs/index.html 查看效果"
