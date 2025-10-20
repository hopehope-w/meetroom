#!/bin/bash

# 会议室预约系统启动脚本
# 使用方法：在Git Bash中运行 ./start_system.sh

echo "=========================================="
echo "211会议室预约系统启动脚本"
echo "=========================================="

# 获取本机IP地址
echo "正在获取本机IP地址..."
IP=$(ipconfig | grep "IPv4" | head -1 | awk '{print $NF}' | tr -d '\r')
if [ -z "$IP" ]; then
    IP="192.168.1.100"
    echo "无法自动获取IP，使用默认IP: $IP"
else
    echo "检测到本机IP: $IP"
fi

echo ""
echo "系统访问地址："
echo "前端: http://$IP:8080"
echo "后端: http://$IP:5000"
echo ""

# 检查Python是否安装
if ! command -v python &> /dev/null; then
    echo "错误: 未找到Python，请先安装Python"
    exit 1
fi

# 检查依赖是否安装
echo "检查后端依赖..."
cd backend
if [ ! -f "requirements.txt" ]; then
    echo "错误: 未找到requirements.txt文件"
    exit 1
fi

# 安装依赖（如果需要）
echo "安装/更新依赖..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "启动说明："
echo "1. 后端将在端口5000启动"
echo "2. 前端将在端口8080启动"
echo "3. 管理员账号: zy / admin123"
echo "4. 局域网用户可通过以下地址访问:"
echo "   http://$IP:8080"
echo "=========================================="
echo ""

read -p "按回车键开始启动系统..."

echo "正在启动后端服务..."
python main.py &
BACKEND_PID=$!

echo "等待后端启动..."
sleep 3

echo "正在启动前端服务..."
cd ../frontend
python -m http.server 8080 --bind 0.0.0.0 &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo "系统启动完成！"
echo "=========================================="
echo "前端访问地址: http://$IP:8080"
echo "后端API地址: http://$IP:5000"
echo ""
echo "请确保防火墙允许端口5000和8080的访问"
echo ""
echo "按Ctrl+C停止系统"
echo "=========================================="

# 等待用户中断
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
