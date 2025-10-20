@echo off
chcp 65001 >nul
title 网络连接测试

echo ==========================================
echo 会议室预约系统 - 网络连接测试
echo ==========================================
echo.

echo 1. 获取本机网络信息...
echo.
ipconfig | findstr /C:"IPv4" /C:"子网掩码" /C:"默认网关"
echo.

echo 2. 检查端口占用情况...
echo.
echo 检查端口5000:
netstat -an | findstr ":5000"
if %errorLevel% == 0 (
    echo ✓ 端口5000正在使用中
) else (
    echo ✗ 端口5000未被占用
)

echo.
echo 检查端口8080:
netstat -an | findstr ":8080"
if %errorLevel% == 0 (
    echo ✓ 端口8080正在使用中
) else (
    echo ✗ 端口8080未被占用
)

echo.
echo 3. 检查防火墙规则...
echo.
netsh advfirewall firewall show rule name="会议室预约系统-后端" >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ 后端防火墙规则已配置
) else (
    echo ✗ 后端防火墙规则未配置
)

netsh advfirewall firewall show rule name="会议室预约系统-前端" >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ 前端防火墙规则已配置
) else (
    echo ✗ 前端防火墙规则未配置
)

echo.
echo 4. 测试本地连接...
echo.
echo 测试后端连接:
curl -s http://localhost:5000/api/health >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ 后端服务正常
) else (
    echo ✗ 后端服务无响应
)

echo.
echo 测试前端连接:
curl -s http://localhost:8080 >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ 前端服务正常
) else (
    echo ✗ 前端服务无响应
)

echo.
echo ==========================================
echo 测试完成
echo ==========================================
echo.
echo 如果发现问题，请检查：
echo 1. 系统是否已启动（运行 start_system.bat）
echo 2. 防火墙是否已配置（运行 setup_lan_access.bat）
echo 3. 网络连接是否正常
echo.

pause
