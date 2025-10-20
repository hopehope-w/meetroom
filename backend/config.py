import os
from datetime import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
JWT_EXPIRE_MINUTES = int(os.environ.get('JWT_EXPIRE_MINUTES', '480'))  # 8 hours

# Service window 08:00-17:00
SERVICE_START = time(8, 0)
SERVICE_END = time(17, 0)

# CORS allowed origins - for LAN testing allow all; tighten in production
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

# Predefined admin credentials
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'zy')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')  # change via env

ROOM_211_ID = 1
ROOM_211_NUMBER = '211'
DEFAULT_ROOMS = [
    {"id": ROOM_211_ID, "room_number": ROOM_211_NUMBER, "capacity": 12, "facilities": "Projector, Whiteboard"}
]

