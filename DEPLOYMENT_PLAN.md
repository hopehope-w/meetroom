# 会议室预约系统 0 成本上线闭环计划

## Summary
目标是先把系统从“本地可跑的 demo”收敛成“可公开访问、前后端分离、能完成预约到审批闭环”的线上版本，优先使用 `Vercel + Render`，保留现有 `SQLite`，第一阶段补 `飞书机器人群通知`，不做大幅产品重构。

当前已确认的关键阻塞点：
- 前端线上 API 地址策略不适用于 `Vercel -> Render`，现在是按浏览器 hostname 拼 `http://<host>:5000`，上线后会直接请求错误地址。
- 后端启动方式依赖在 `backend` 目录内运行，Render 必须显式指定工作目录或启动命令。
- `SQLite` 文件位于 `backend/database.db`，在 Render 免费实例下不能视为可靠持久化存储，只能接受“演示级持久性”。
- 仓库里没有飞书通知实现，当前不是“未打通完”，而是“尚未接入”。
- `frontend` 作为主站保留，`oldfrontend` 不参与第一阶段线上入口。

## Key Changes
### 1. 前后端部署收口
- 前端只部署 `frontend` 到 Vercel，`oldfrontend` 保留在仓库但不作为线上入口。
- 前端新增明确的环境变量式 API 基址配置：
  - 本地开发默认走 `localhost:5000`
  - 生产环境改为读取 `VITE_API_BASE_URL`
  - 移除基于 `location.hostname + :5000` 的线上推断逻辑
- 后端部署到 Render Web Service，固定以 `backend` 为服务目录。
- 后端启动命令明确为可在 Render 执行的一条命令，避免依赖本地目录假设。
- 后端补生产环境所需配置说明：
  - `SECRET_KEY`
  - `ADMIN_USERNAME`
  - `ADMIN_PASSWORD`
  - `CORS_ORIGINS` 指向 Vercel 域名
  - `FEISHU_WEBHOOK_URL`（第一阶段仅群机器人通知）
- 若继续保留后端静态目录，仅作为本地或兜底，不作为线上主入口；线上以 Vercel 托管前端为准。

### 2. 后端最小上线改造
- 把配置集中为“本地默认可跑 + 线上全靠环境变量覆盖”的模式，避免硬编码生产值。
- 校正 API 约定不一致问题：
  - `/api/availability` 当前是 `GET`，前端有一处按 `POST` 调用，需统一为单一协议。
- 明确 Render 下调度器行为：
  - 保留 APScheduler 仅做轻量清理
  - 不把它当成可靠定时基础设施
  - 清理失败不影响核心预约链路
- 登录、审批、查询、统计、清理接口保持现有 shape，不在本轮做权限体系扩展。
- 增加基础生产健检：
  - `/api/health` 保留用于 Render 健康检查
  - 启动日志打印环境模式和数据库路径，但不打印敏感信息

### 3. SQLite 的上线策略
- 第一阶段继续使用 `backend/database.db`，接受免费 Render 上“实例休眠/重建后数据可能丢失”的前提。
- 明确产品定位为“演示闭环版”，不承诺正式生产级持久化。
- 增加最小备份策略文档：
  - 如何从 Render 下载或导出 SQLite
  - 如何本地恢复
  - 何时建议升级到外部 Postgres
- 本轮不迁移数据库，不引入付费资源，不做复杂 ORM 改造。

### 4. 飞书机器人通知接入
- 第一阶段只接“群机器人 Webhook 通知”，不做飞书登录、用户映射、待办卡片或双向审批。
- 通知触发点固定为两类：
  - 新预约提交成功后通知群
  - 管理员审批通过/拒绝后通知群
- 通知内容包含最小必要字段：
  - 预约人
  - 部门
  - 会议室
  - 开始/结束时间
  - 当前状态
  - 操作时间
- 失败策略：
  - 飞书通知失败不回滚主业务
  - 后端记录错误日志
  - API 仍返回业务成功
- 通知实现封装成独立服务函数，避免散落在路由中，方便后续升级到 richer message 或审批流。

### 5. 前端第一阶段整理
- 只保留一套路由入口和一套线上文案，避免 `frontend` 与 `oldfrontend` 的心智分叉。
- 优先修正“能影响闭环”的问题，不在本轮追求惊艳重设计：
  - API 调用统一
  - 登录/审批/冲突检查/我的预约链路一致
  - 生产环境错误提示清晰
  - 管理员入口可稳定使用
- 若存在明显构建或运行不一致，以“能稳定部署到 Vercel”的结构优先，减少本地专用逻辑。
- UI 优化只做轻量收束：
  - 首页价值表达更明确
  - 管理页层次更清楚
  - 移动端不出布局错乱
  - 不再继续同时维护两套视觉实现

## Public Interfaces / Config Changes
- 前端新增环境变量：
  - `VITE_API_BASE_URL`
- 后端新增或明确环境变量：
  - `SECRET_KEY`
  - `ADMIN_USERNAME`
  - `ADMIN_PASSWORD`
  - `CORS_ORIGINS`
  - `FEISHU_WEBHOOK_URL`
- 飞书通知不新增对外 API；仅作为后端内部服务层能力。
- 现有 API 保持主路径不变：
  - `POST /api/login`
  - `GET/POST /api/bookings`
  - `GET /api/my-bookings`
  - `GET /api/availability`
  - `PUT /api/bookings/:id`
  - `GET /api/stats`
  - `POST /api/cleanup`
  - `GET /api/database-info`
  - `GET /api/health`

## Test Plan
- 本地联调：
  - 前端使用环境变量直连本地后端
  - 预约提交成功
  - 时间冲突校验正确
  - 管理员登录成功
  - 审批通过/拒绝后列表与状态更新正确
- 飞书通知：
  - 新预约时群机器人收到消息
  - 审批通过时收到消息
  - 审批拒绝时收到消息
  - Webhook 失效时业务接口仍返回成功，日志可见错误
- 部署验证：
  - Vercel 页面可正常加载
  - 跨域允许来自 Vercel 域名的请求
  - Render 健康检查正常
  - 前端生产环境请求命中 Render 域名而不是当前 hostname:5000
- 演示级数据验证：
  - 新增预约后可在管理端看到
  - 实例重启后若数据仍在则记录现状，若丢失则符合已知风险说明
- 回归检查：
  - `/admin` 登录态可用
  - 统计页、数据库信息页仍能正常返回
  - 旧前端不影响新前端构建与部署

## Assumptions
- 第一阶段目标是“跑通部署闭环”，不是做正式生产版。
- 主站只使用 `frontend`，`oldfrontend` 暂不下线但不参与线上入口。
- 数据库继续使用 `SQLite`，并明确接受免费 Render 上的持久化风险。
- 飞书只接机器人群通知，不做账号体系、审批回写或组织架构集成。
- Render 和 Vercel 账号已就绪，后续实现时只需补仓库内配置与平台环境变量。
