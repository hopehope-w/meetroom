@echo off
chcp 65001 >nul
title 211会议室预约系统

echo ==========================================
echo 211会议室预约系统启动脚本
echo ==========================================
echo.

echo 正在获取本机IP地址...
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr "IPv4"') do (
    set IP=%%i
    goto :found
)
:found
set IP=%IP: =%
if "%IP%"=="" set IP=192.168.1.100

echo 检测到本机IP: %IP%
echo.
echo 系统访问地址：
echo 前端: http://%IP%:8080
echo 后端: http://%IP%:5000
echo.

echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo 安装后端依赖...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 启动说明：
echo 1. 后端将在端口5000启动
echo 2. 前端将在端口8080启动  
echo 3. 管理员账号: zy / admin123
echo 4. 局域网用户可通过以下地址访问:
echo    http://%IP%:8080
echo ==========================================
echo.

pause

echo 正在启动后端服务（绑定到所有网络接口）...
start "后端服务" python main.py

echo 等待后端启动...
timeout /t 5 /nobreak >nul

echo 正在启动前端服务（绑定到所有网络接口）...
cd ..\frontend
start "前端服务" python -m http.server 8080 --bind 0.0.0.0

echo 等待前端启动...
timeout /t 3 /nobreak >nul

echo.
echo ==========================================
echo 系统启动完成！
echo ==========================================
echo 前端访问地址: http://%IP%:8080
echo 后端API地址: http://%IP%:5000
echo.
echo 请确保防火墙允许端口5000和8080的访问
echo.
echo 关闭此窗口将停止系统
echo ==========================================

pause
