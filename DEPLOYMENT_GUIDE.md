# Deployment Guide

## Architecture
- Frontend: `frontend` -> Vercel
- Backend: `backend` -> Render Web Service
- Database: `backend/database.db` (`SQLite`, demo-grade persistence only)
- Notification: Feishu bot webhook

## Frontend on Vercel
- Root Directory: `frontend`
- Build Command: `npm run build`
- Output Directory: `dist`
- Environment Variables:
  - `VITE_API_BASE_URL=https://your-render-service.onrender.com`

## Backend on Render
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python main.py`
- Health Check Path: `/api/health`
- Environment Variables:
  - `SECRET_KEY`
  - `ADMIN_USERNAME`
  - `ADMIN_PASSWORD`
  - `CORS_ORIGINS=https://your-app.vercel.app`
  - `FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your-token`
  - `APP_BASE_URL=https://your-app.vercel.app`

## Local Development
### Backend
```powershell
cd backend
python main.py
```

### Frontend
```powershell
cd frontend
cmd /c npm.cmd install
cmd /c npm.cmd run dev
```

## SQLite Notes
- Current storage is suitable for demo and workflow validation only.
- Free Render instances may lose local disk state after rebuild or instance replacement.
- If you need stronger persistence later, migrate to a managed Postgres service.

## Feishu Notification Notes
- Notifications are sent when:
  - a new booking is created
  - an admin approves a booking
  - an admin rejects a booking
- Notification failure does not block booking or approval APIs.
