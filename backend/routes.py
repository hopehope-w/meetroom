from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from auth import admin_required
from config import ROOM_211_ID
from models import (
    add_booking,
    check_conflict,
    cleanup_database,
    get_booking,
    list_bookings,
    update_booking_status,
)
from notify import send_booking_notification

api = Blueprint("api", __name__, url_prefix="/api")


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
    return jsonify(list_bookings(start, end))


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

    if check_conflict(ROOM_211_ID, start_iso, end_iso):
        return jsonify({"error": "Time conflict for room 211"}), 409

    booking_id = add_booking(
        user_name=user_name,
        room_id=ROOM_211_ID,
        start_iso=start_iso,
        end_iso=end_iso,
        status="pending",
        department=department or None,
    )

    booking = get_booking(booking_id)
    if booking:
        send_booking_notification("新预约提交", serialize_booking(booking))

    return jsonify({"id": booking_id, "status": "pending"}), 201


@api.get("/availability")
def availability():
    start_iso = request.args.get("start")
    end_iso = request.args.get("end")
    if not start_iso or not end_iso:
        return jsonify({"error": "start and end required"}), 400

    conflict = check_conflict(ROOM_211_ID, start_iso, end_iso)
    return jsonify({"available": not conflict, "conflict": conflict})


@api.get("/my-bookings")
def get_my_bookings():
    user_name = (request.args.get("user_name") or "").strip()
    if not user_name:
        return jsonify({"error": "user_name required"}), 400

    now = datetime.utcnow()
    start_date = now - timedelta(days=30)
    end_date = now + timedelta(days=30)

    all_bookings = list_bookings(start_date.isoformat(), end_date.isoformat())
    user_bookings = [
        booking
        for booking in all_bookings
        if (booking.get("user_name") or "").strip() == user_name
    ]
    return jsonify(user_bookings)


@api.put("/bookings/<int:bid>")
@admin_required
def update_booking(bid: int):
    data = request.get_json(force=True)
    status = data.get("status")
    if status not in ("approved", "rejected"):
        return jsonify({"error": "Invalid status"}), 400

    booking = get_booking(bid)
    if not booking:
        return jsonify({"error": "Not found"}), 404

    update_booking_status(bid, status)
    booking["status"] = status
    send_booking_notification(f"预约已{status}", serialize_booking(booking))
    return jsonify({"ok": True})


@api.get("/stats")
@admin_required
def stats():
    local_now = datetime.now()
    today = local_now.date()

    days = []
    current_day = today
    while len(days) < 5:
        if current_day.weekday() < 5:
            days.append(current_day)
        current_day += timedelta(days=1)

    start_iso = datetime.combine(today, datetime.min.time()).isoformat()
    end_iso = datetime.combine(days[-1], datetime.max.time()).isoformat()
    bookings = list_bookings(start_iso, end_iso)

    by_day = {}
    for booking in bookings:
        day = booking["start_time"][:10]
        by_day.setdefault(day, []).append(booking)

    return jsonify(
        {
            "days": [str(day) for day in days],
            "by_day": by_day,
            "total": len(bookings),
            "current_info": {
                "current_date": today.isoformat(),
                "current_time": local_now.strftime("%H:%M:%S"),
                "last_updated": local_now.isoformat(),
            },
        }
    )


@api.post("/cleanup")
@admin_required
def manual_cleanup():
    try:
        deleted_count = cleanup_database()
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
        all_bookings = list_bookings()

        now = datetime.utcnow()
        one_week_ago = now - timedelta(days=7)
        one_month_ago = now - timedelta(days=30)

        total_count = len(all_bookings)
        recent_week = len(
            [booking for booking in all_bookings if booking["created_at"] >= one_week_ago.isoformat()]
        )
        recent_month = len(
            [booking for booking in all_bookings if booking["created_at"] >= one_month_ago.isoformat()]
        )
        old_data = len(
            [booking for booking in all_bookings if booking["created_at"] < one_month_ago.isoformat()]
        )

        return jsonify(
            {
                "total_bookings": total_count,
                "recent_week": recent_week,
                "recent_month": recent_month,
                "old_data_count": old_data,
                "cleanup_threshold": "Records older than 30 days can be cleaned manually or by the scheduler.",
            }
        )
    except Exception as exc:
        return jsonify({"error": f"Failed to load database info: {exc}"}), 500
