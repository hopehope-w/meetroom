import os
from datetime import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
JWT_EXPIRE_MINUTES = int(os.environ.get('JWT_EXPIRE_MINUTES', '480'))

SERVICE_START = time(8, 0)
SERVICE_END = time(17, 0)


def normalize_url(value: str) -> str:
    value = (value or '').strip()
    if not value:
        return ''
    return value.rstrip('/')


raw_cors_origins = os.environ.get('CORS_ORIGINS', '*').strip()
if raw_cors_origins == '*':
    CORS_ORIGINS = '*'
else:
    CORS_ORIGINS = [normalize_url(origin) for origin in raw_cors_origins.split(',') if normalize_url(origin)]

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'zy')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

FEISHU_WEBHOOK_URL = os.environ.get('FEISHU_WEBHOOK_URL', '').strip()
APP_BASE_URL = normalize_url(os.environ.get('APP_BASE_URL', ''))

DEFAULT_ROOM_ID = int(os.environ.get('DEFAULT_ROOM_ID', '1'))
DEFAULT_ROOM_NUMBER = os.environ.get('DEFAULT_ROOM_NUMBER', '207').strip() or '207'
DEFAULT_ROOMS = [
    {
        'id': DEFAULT_ROOM_ID,
        'room_number': DEFAULT_ROOM_NUMBER,
        'capacity': 12,
        'facilities': 'Projector, Whiteboard',
    }
]
