import datetime as dt
import hashlib
from functools import wraps
from flask import request, jsonify
import jwt
from config import SECRET_KEY, JWT_EXPIRE_MINUTES
from models import get_db


def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


def generate_token(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": dt.datetime.utcnow() + dt.timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401
        token = auth_header.split(" ", 1)[1]
        try:
            payload = decode_token(token)
            if payload.get("role") != "admin":
                return jsonify({"error": "Forbidden"}), 403
        except Exception as e:
            return jsonify({"error": "Unauthorized", "detail": str(e)}), 401
        return f(*args, **kwargs)

    return wrapper
