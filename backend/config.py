import os
from datetime import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
JWT_EXPIRE_MINUTES = int(os.environ.get('JWT_EXPIRE_MINUTES', '480'))

SERVICE_START = time(8, 0)
SERVICE_END = time(17, 0)

raw_cors_origins = os.environ.get('CORS_ORIGINS', '*').strip()
if raw_cors_origins == '*':
    CORS_ORIGINS = '*'
else:
    CORS_ORIGINS = [origin.strip() for origin in raw_cors_origins.split(',') if origin.strip()]

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'zy')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

FEISHU_WEBHOOK_URL = os.environ.get('FEISHU_WEBHOOK_URL', '').strip()
APP_BASE_URL = os.environ.get('APP_BASE_URL', '').strip()

ROOM_211_ID = 1
ROOM_211_NUMBER = '211'
DEFAULT_ROOMS = [
    {
        'id': ROOM_211_ID,
        'room_number': ROOM_211_NUMBER,
        'capacity': 12,
        'facilities': 'Projector, Whiteboard',
    }
]
