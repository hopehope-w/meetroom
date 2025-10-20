from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import CORS_ORIGINS, ADMIN_USERNAME, ADMIN_PASSWORD, DEFAULT_ROOMS
from models import init_db, seed_admin_and_room
from auth import hash_password, generate_token
from routes import api
from scheduler import start_scheduler


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

    # init database
    init_db()
    seed_admin_and_room(ADMIN_USERNAME, hash_password(ADMIN_PASSWORD), DEFAULT_ROOMS)

    app.register_blueprint(api)

    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.get_json(force=True)
        username = data.get("username")
        password = data.get("password")
        if username == ADMIN_USERNAME and hash_password(password) == hash_password(
            ADMIN_PASSWORD
        ):
            token = generate_token(ADMIN_USERNAME, "admin")
            return jsonify({"token": token})
        return jsonify({"error": "Invalid credentials"}), 401

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True, "time": datetime.utcnow().isoformat()})

    return app


if __name__ == "__main__":
    # Bind to all interfaces for LAN access
    app = create_app()
    start_scheduler()
    print("启动会议预约系统后端服务...")
    print("访问地址: http://172.100.12.17:5000")
    print("API文档: http://172.100.12.17:5000/api/health")
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,  # 生产环境关闭debug
        threaded=True,  # 启用多线程支持
        processes=1,  # 单进程多线程模式
    )
