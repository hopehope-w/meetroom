import datetime as dt
import hashlib
from functools import wraps

import jwt
from flask import jsonify, request

from config import JWT_EXPIRE_MINUTES, SECRET_KEY


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def generate_token(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": dt.datetime.utcnow() + dt.timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            payload = decode_token(token)
            if payload.get("role") != "admin":
                return jsonify({"error": "Forbidden"}), 403
        except Exception as exc:
            return jsonify({"error": "Unauthorized", "detail": str(exc)}), 401

        return func(*args, **kwargs)

    return wrapper
