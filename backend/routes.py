from datetime import datetime

from flask import Blueprint, jsonify, request

from auth import admin_required
from config import DEFAULT_ROOM_ID, DEFAULT_ROOM_NUMBER
from notify import send_booking_notification
from repositories import BookingRepository
from services import BookingService

api = Blueprint("api", __name__, url_prefix="/api")
booking_service = BookingService(BookingRepository())


def parse_iso(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def serialize_booking(booking: dict) -> dict:
    return {
        "id": booking["id"],
        "user_name": booking["user_name"],
        "department": booking.get("department"),
        "room_id": booking["room_id"],
        "start_time": booking["start_time"],
        "end_time": booking["end_time"],
        "status": booking["status"],
        "created_at": booking["created_at"],
    }


@api.get("/bookings")
def get_bookings():
    start = request.args.get("start")
    end = request.args.get("end")
    return jsonify(booking_service.list_bookings(start, end))


@api.post("/bookings")
def create_booking():
    data = request.get_json(force=True)
    user_name = (data.get("user_name") or "").strip()
    department = (data.get("department") or "").strip()
    start_iso = data.get("start_time")
    end_iso = data.get("end_time")

    if not user_name or not start_iso or not end_iso:
        return jsonify({"error": "Missing required fields"}), 400

    start_dt = parse_iso(start_iso)
    end_dt = parse_iso(end_iso)
    if not start_dt or not end_dt or end_dt <= start_dt:
        return jsonify({"error": "Invalid time range"}), 400

    if booking_service.has_conflict(DEFAULT_ROOM_ID, start_iso, end_iso):
        return jsonify({"error": f"Time conflict for room {DEFAULT_ROOM_NUMBER}"}), 409

    booking_id = booking_service.create_booking(
        user_name=user_name,
        department=department or None,
        room_id=DEFAULT_ROOM_ID,
        start_iso=start_iso,
        end_iso=end_iso,
    )

    booking = booking_service.get_booking(booking_id)
    if booking:
        send_booking_notification("新预约提交", serialize_booking(booking))

    return jsonify({"id": booking_id, "status": "pending"}), 201


@api.get("/availability")
def availability():
    start_iso = request.args.get("start")
    end_iso = request.args.get("end")
    if not start_iso or not end_iso:
        return jsonify({"error": "start and end required"}), 400

    conflict = booking_service.has_conflict(DEFAULT_ROOM_ID, start_iso, end_iso)
    return jsonify({"available": not conflict, "conflict": conflict})


@api.get("/my-bookings")
def get_my_bookings():
    user_name = (request.args.get("user_name") or "").strip()
    if not user_name:
        return jsonify({"error": "user_name required"}), 400

    return jsonify(booking_service.get_recent_user_bookings(user_name))


@api.put("/bookings/<int:booking_id>")
@admin_required
def update_booking(booking_id: int):
    data = request.get_json(force=True)
    status = data.get("status")
    if status not in ("approved", "rejected"):
        return jsonify({"error": "Invalid status"}), 400

    booking = booking_service.get_booking(booking_id)
    if not booking:
        return jsonify({"error": "Not found"}), 404

    booking_service.update_booking_status(booking_id, status)
    booking["status"] = status
    send_booking_notification(f"预约已{status}", serialize_booking(booking))
    return jsonify({"ok": True})


@api.get("/stats")
@admin_required
def stats():
    return jsonify(booking_service.get_stats_summary())


@api.post("/cleanup")
@admin_required
def manual_cleanup():
    try:
        deleted_count = booking_service.cleanup_database()
        return jsonify(
            {
                "success": True,
                "message": f"Cleanup finished, removed {deleted_count} old booking records",
                "deleted_count": deleted_count,
            }
        )
    except Exception as exc:
        return jsonify({"success": False, "error": f"Cleanup failed: {exc}"}), 500


@api.get("/database-info")
@admin_required
def database_info():
    try:
        return jsonify(booking_service.get_database_info())
    except Exception as exc:
        return jsonify({"error": f"Failed to load database info: {exc}"}), 500
