项目概述
开发一个轻量级会议预约系统，包含前后端功能，支持100人以下团队使用，运行在局域网环境中。

技术栈要求
后端：Python (Flask框架)

前端：Vue.js (v2或v3)

数据库：SQLite (避免MySQL/PostgreSQL连接问题)

通信：RESTful API

系统架构
text
/项目根目录
  /backend
    main.py              # 主入口文件
    config.py            # 配置文件
    models.py            # 数据模型定义
    routes.py            # API路由
    auth.py              # 认证模块
    scheduler.py         # 定时任务模块
    database.db          # SQLite数据库
    requirements.txt     # Python依赖
    
  /frontend
    index.html           # 主页面
    /src
      main.js            # Vue入口文件
      App.vue            # 根组件
      /components
        BookingForm.vue  # 预约表单组件
        AdminPanel.vue   # 管理员面板
        CalendarView.vue # 日历视图组件
      /router            # 路由配置
      /store             # 状态管理
      /assets            # 静态资源
    package.json         # 前端依赖
后端功能需求
1. 数据模型 (models.py)
用户模型：id, 用户名, 密码(哈希), 角色(管理员/普通用户)

会议室模型：id, 房间号, 容量, 设备信息

预约模型：id, 预约人, 会议室ID, 开始时间, 结束时间, 状态(待审批/已批准/已拒绝), 创建时间

2. API端点 (routes.py)
POST /api/login - 用户登录

GET /api/bookings - 获取预约列表(支持日期筛选)

POST /api/bookings - 创建新预约

PUT /api/bookings/<id> - 更新预约状态(仅管理员)

GET /api/availability - 检查时间段可用性

GET /api/stats - 获取统计信息(仅管理员)

3. 核心功能
时间冲突检测：确保同一时间段内没有重复预约

自动审批逻辑：非211会议室可自动批准(如需扩展)

工作日计算：只考虑周一到周五

数据验证：确保时间合理性(开始时间不能晚于结束时间等)

4. 认证系统 (auth.py)
基于会话或JWT的认证

管理员账号: zy/自定义密码

普通用户无需注册，预约时填写姓名即可

5. 定时任务 (scheduler.py)
每日清理过期预约

服务时间控制(8:00-17:00)

前端功能需求
1. 预约表单 (BookingForm.vue)
字段：预约人姓名、开始时间(日期时间选择器)、结束时间(日期时间选择器)

实时可用性检查

提交后显示等待审批状态

2. 管理员面板 (AdminPanel.vue)
登录界面

预约审批界面：列表显示待审批请求，支持批准/拒绝操作

数据可视化：近5天预约情况日历视图

用户活动追踪：显示谁提交了预约申请

3. 日历视图 (CalendarView.vue)
以日历形式展示211会议室近5个工作日的预约情况

不同颜色区分已批准、待审批、已拒绝状态

点击预约项显示详细信息

4. 响应式设计
同时支持PC端和移动端访问

使用Flexbox/Grid布局

触摸友好的界面元素

5. 状态提示与轮询
提交后显示处理状态

短轮询检查审批状态更新(每30秒)

友好的加载和错误提示

数据库设计
使用SQLite数据库，包含三张表：

users (id, username, password_hash, role)

rooms (id, room_number, capacity, facilities)

bookings (id, user_name, room_id, start_time, end_time, status, created_at)

部署与运行
后端启动命令: python main.py

前端部署: 使用轻量级HTTP服务器(如http-server)

局域网访问: 绑定到0.0.0.0，端口8080(前端)和5000(后端)

二维码生成: 硬编码包含内网IP地址的二维码(如http://192.168.1.100:8080)

特别注意事项
时间处理使用UTC并在前端转换时区显示

输入验证防止SQL注入和XSS攻击

适当的错误处理和日志记录

服务时间控制(8:00-17:00)可配置

数据库备份机制(定期备份SQLite文件)

扩展性考虑
模块化设计方便添加新会议室

API设计支持未来移动端App

配置系统允许调整参数而不修改代码

请基于以上提示词生成完整的Python和Vue.js代码实现。