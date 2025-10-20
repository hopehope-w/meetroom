@echo off
chcp 65001 >nul
title 会议室预约系统 - 局域网配置

echo ==========================================
echo 会议室预约系统 - 局域网访问配置
echo ==========================================
echo.

echo 正在检查管理员权限...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ 已获得管理员权限
) else (
    echo ✗ 需要管理员权限来配置防火墙
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo.
echo 正在获取本机IP地址...
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr "IPv4"') do (
    set IP=%%i
    goto :found
)
:found
set IP=%IP: =%
if "%IP%"=="" (
    echo ✗ 无法获取IP地址，请手动检查网络连接
    pause
    exit /b 1
)

echo ✓ 检测到本机IP: %IP%
echo.

echo 正在配置Windows防火墙...
echo.

echo 1. 配置端口5000（后端API服务）...
netsh advfirewall firewall delete rule name="会议室预约系统-后端" >nul 2>&1
netsh advfirewall firewall add rule name="会议室预约系统-后端" dir=in action=allow protocol=TCP localport=5000
if %errorLevel% == 0 (
    echo ✓ 端口5000配置成功
) else (
    echo ✗ 端口5000配置失败
)

echo.
echo 2. 配置端口8080（前端Web服务）...
netsh advfirewall firewall delete rule name="会议室预约系统-前端" >nul 2>&1
netsh advfirewall firewall add rule name="会议室预约系统-前端" dir=in action=allow protocol=TCP localport=8080
if %errorLevel% == 0 (
    echo ✓ 端口8080配置成功
) else (
    echo ✗ 端口8080配置失败
)

echo.
echo 3. 检查Python HTTP服务器防火墙规则...
netsh advfirewall firewall delete rule name="Python HTTP Server" >nul 2>&1
netsh advfirewall firewall add rule name="Python HTTP Server" dir=in action=allow program="python.exe"
if %errorLevel% == 0 (
    echo ✓ Python HTTP服务器规则配置成功
) else (
    echo ✗ Python HTTP服务器规则配置失败
)

echo.
echo ==========================================
echo 配置完成！
echo ==========================================
echo.
echo 系统访问信息：
echo 本机IP地址: %IP%
echo 前端访问地址: http://%IP%:8080
echo 后端API地址: http://%IP%:5000
echo.
echo 局域网访问说明：
echo 1. 确保所有设备连接到同一WiFi网络
echo 2. 其他设备可通过以下地址访问系统：
echo    http://%IP%:8080
echo 3. 如果仍无法访问，请检查：
echo    - 网络连接是否正常
echo    - 路由器是否启用了设备隔离
echo    - 杀毒软件是否阻止了连接
echo.
echo 测试连接：
echo 可以在其他设备的浏览器中输入以下地址测试：
echo http://%IP%:8080
echo.

pause

echo.
echo 是否现在启动系统？(Y/N)
set /p choice=请选择: 
if /i "%choice%"=="Y" (
    echo.
    echo 正在启动系统...
    start "启动系统" "%~dp0start_system.bat"
) else (
    echo.
    echo 配置完成，您可以稍后手动启动系统
)

echo.
echo 配置完成！按任意键退出...
pause >nul
