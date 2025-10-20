from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from models import (
    add_booking,
    list_bookings,
    check_conflict,
    update_booking_status,
    get_booking,
    cleanup_database,
)
from config import ROOM_211_ID
from auth import admin_required

api = Blueprint("api", __name__, url_prefix="/api")


def parse_iso(s: str):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


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
        return jsonify({"error": "Missing fields"}), 400

    start_dt = parse_iso(start_iso)
    end_dt = parse_iso(end_iso)
    if not start_dt or not end_dt or end_dt <= start_dt:
        return jsonify({"error": "Invalid time range"}), 400

    # conflict check for room 211 only
    if check_conflict(ROOM_211_ID, start_iso, end_iso):
        return jsonify({"error": "Time conflict for room 211"}), 409

    booking_id = add_booking(
        user_name,
        ROOM_211_ID,
        start_iso,
        end_iso,
        status="pending",
        department=department or None,
    )
    return jsonify({"id": booking_id, "status": "pending"}), 201


@api.get("/availability")
def availability():
    start_iso = request.args.get("start")
    end_iso = request.args.get("end")
    if not start_iso or not end_iso:
        return jsonify({"error": "start and end required"}), 400
    return jsonify({"conflict": check_conflict(ROOM_211_ID, start_iso, end_iso)})


@api.get("/my-bookings")
def get_my_bookings():
    user_name = request.args.get("user_name")
    if not user_name:
        return jsonify({"error": "user_name required"}), 400

    # 获取该用户的所有预约（最近30天）
    from datetime import datetime, timedelta

    now = datetime.utcnow()
    start_date = now - timedelta(days=30)
    end_date = now + timedelta(days=30)

    all_bookings = list_bookings(start_date.isoformat(), end_date.isoformat())
    user_bookings = [
        b
        for b in all_bookings
        if b["user_name"] and b["user_name"].strip() == user_name.strip()
    ]

    return jsonify(user_bookings)


@api.put("/bookings/<int:bid>")
@admin_required
def update_booking(bid: int):
    data = request.get_json(force=True)
    status = data.get("status")
    if status not in ("approved", "rejected"):
        return jsonify({"error": "Invalid status"}), 400
    if not get_booking(bid):
        return jsonify({"error": "Not found"}), 404
    update_booking_status(bid, status)
    return jsonify({"ok": True})


@api.get("/stats")
@admin_required
def stats():
    # next 5 business days from today (including today) - 使用本地时间
    from datetime import datetime as dt
    import time

    # 获取本地时间
    local_time = dt.fromtimestamp(time.time())
    today = local_time.date()

    days = []
    added = 0
    d = today
    while added < 5:
        if d.weekday() < 5:  # Monday=0, Sunday=6, so <5 means weekdays
            days.append(d)
            added += 1
        d += timedelta(days=1)

    # 获取从今天开始到未来5个工作日的预约
    start_iso = dt.combine(today, dt.min.time()).isoformat()
    end_iso = dt.combine(days[-1], dt.max.time()).isoformat()
    bookings = list_bookings(start_iso, end_iso)

    # aggregate by day
    by_day = {}
    for b in bookings:
        day = b["start_time"][:10]
        by_day.setdefault(day, []).append(b)

    # 添加当前时间信息用于前端显示
    current_info = {
        "current_date": today.isoformat(),
        "current_time": local_time.strftime("%H:%M:%S"),
        "last_updated": local_time.isoformat(),
    }

    return jsonify(
        {
            "days": [str(x) for x in days],
            "by_day": by_day,
            "total": len(bookings),
            "current_info": current_info,
        }
    )


@api.post("/cleanup")
@admin_required
def manual_cleanup():
    """管理员手动清理超过30天的历史数据"""
    try:
        deleted_count = cleanup_database()
        return jsonify(
            {
                "success": True,
                "message": f"清理完成，删除了 {deleted_count} 条超过30天的预约记录",
                "deleted_count": deleted_count,
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": f"清理失败: {str(e)}"}), 500


@api.get("/database-info")
@admin_required
def database_info():
    """获取数据库统计信息"""
    try:
        from datetime import datetime, timedelta

        # 获取所有预约
        all_bookings = list_bookings()

        # 统计不同时间段的数据
        now = datetime.utcnow()
        one_week_ago = now - timedelta(days=7)
        one_month_ago = now - timedelta(days=30)

        total_count = len(all_bookings)
        recent_week = len(
            [b for b in all_bookings if b["created_at"] >= one_week_ago.isoformat()]
        )
        recent_month = len(
            [b for b in all_bookings if b["created_at"] >= one_month_ago.isoformat()]
        )
        old_data = len(
            [b for b in all_bookings if b["created_at"] < one_month_ago.isoformat()]
        )

        return jsonify(
            {
                "total_bookings": total_count,
                "recent_week": recent_week,
                "recent_month": recent_month,
                "old_data_count": old_data,
                "cleanup_threshold": "30天前的数据将被自动清理",
            }
        )
    except Exception as e:
        return jsonify({"error": f"获取数据库信息失败: {str(e)}"}), 500
