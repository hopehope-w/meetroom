# 会议室预约系统 - 局域网访问配置指南

## 🚀 快速配置（推荐）

### 一键配置局域网访问：
1. **右键点击** `setup_lan_access.bat`
2. **选择** "以管理员身份运行"
3. **按提示操作** 完成防火墙配置
4. **运行** `start_system.bat` 启动系统

## 📋 详细配置步骤

### 1. 查看本机IP地址

#### 方法一：命令行查看
```bash
# 在CMD中执行
ipconfig | findstr "IPv4"
```

#### 方法二：网络设置查看
1. 右键点击网络图标
2. 选择"打开网络和Internet设置"
3. 点击"属性"查看IPv4地址

#### 方法三：使用配置脚本
运行 `setup_lan_access.bat` 会自动显示IP地址

### 2. 配置Windows防火墙

#### 自动配置（推荐）：
运行 `setup_lan_access.bat`（需要管理员权限）

#### 手动配置：
1. 打开"Windows Defender 防火墙"
2. 点击"高级设置"
3. 选择"入站规则" → "新建规则"
4. 选择"端口" → "TCP" → 输入"5000,8080"
5. 选择"允许连接"
6. 应用到所有配置文件
7. 命名规则（如：会议室预约系统）

### 3. 启动系统服务

#### 确保服务绑定到所有网络接口：
- 后端：Flask app.run(host='0.0.0.0', port=5000)
- 前端：python -m http.server 8080 --bind 0.0.0.0

### 4. 测试局域网访问

### 在其他设备上测试：
1. 确保设备连接到同一WiFi网络
2. 打开浏览器访问：`http://你的IP:8080`
3. 如果无法访问，检查防火墙设置

### 常见问题：
- **无法访问**：检查防火墙和IP地址
- **页面空白**：检查后端服务是否正常启动
- **功能异常**：检查后端API地址配置

## 5. 二维码更新

修改IP后，需要重新生成二维码：
```bash
cd meeting_booking
python simple_qr.py
```

新的二维码文件：`meeting_room_qr.png`

## 6. 启动系统

### Git Bash启动：
```bash
cd meeting_booking
./start_system.sh
```

### Windows启动：
双击 `start_system.bat` 文件

### 手动启动：
```bash
# 后端
cd meeting_booking/backend
python main.py

# 前端（新开终端）
cd meeting_booking/frontend  
python -m http.server 8080 --bind 0.0.0.0
```

## 7. 访问地址

- **员工访问**：`http://你的IP:8080`
- **管理员登录**：账号 `zy`，密码 `admin123`
- **API接口**：`http://你的IP:5000/api/`

## 8. 注意事项

1. **IP地址变化**：如果电脑重启后IP变化，需要重新配置
2. **网络环境**：确保所有用户连接到同一局域网
3. **服务时间**：系统设计为工作时间使用（8:00-17:00）
4. **数据备份**：定期备份 `backend/database.db` 文件
