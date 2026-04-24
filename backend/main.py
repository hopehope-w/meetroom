import logging
import os
from datetime import datetime

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from auth import generate_token, hash_password
from config import ADMIN_PASSWORD, ADMIN_USERNAME, CORS_ORIGINS, DB_PATH, DEFAULT_ROOMS
from models import init_db, seed_admin_and_room
from routes import api
from scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

    init_db()
    seed_admin_and_room(ADMIN_USERNAME, hash_password(ADMIN_PASSWORD), DEFAULT_ROOMS)
    app.register_blueprint(api)

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(app.static_folder, 'favicon.ico')

    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.get_json(force=True)
        username = data.get("username")
        password = data.get("password")

        if username == ADMIN_USERNAME and hash_password(password) == hash_password(ADMIN_PASSWORD):
            token = generate_token(ADMIN_USERNAME, "admin")
            return jsonify({"token": token})
        return jsonify({"error": "Invalid credentials"}), 401

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True, "time": datetime.utcnow().isoformat()})

    logger.info("App initialized. Database path: %s", DB_PATH)
    logger.info("CORS origins: %s", CORS_ORIGINS)
    return app


if __name__ == "__main__":
    app = create_app()
    start_scheduler()

    port = int(os.environ.get("PORT", "5000"))

    try:
        from waitress import serve

        logger.info("Starting Waitress on 0.0.0.0:%s", port)
        serve(app, host="0.0.0.0", port=port, threads=8)
    except ImportError:
        logger.info("Waitress not installed, falling back to Flask dev server on port %s", port)
        app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
