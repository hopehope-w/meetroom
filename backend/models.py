import sqlite3
from contextlib import contextmanager
from datetime import datetime
from config import DB_PATH


@contextmanager
def get_db(readonly: bool = False):
    uri = f"file:{DB_PATH}?mode={'ro' if readonly else 'rwc'}"
    conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        if not readonly:
            conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin','user'))
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY,
                room_number TEXT UNIQUE NOT NULL,
                capacity INTEGER,
                facilities TEXT
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                department TEXT,
                room_id INTEGER NOT NULL,
                start_time TEXT NOT NULL,  -- ISO8601 UTC
                end_time TEXT NOT NULL,    -- ISO8601 UTC
                status TEXT NOT NULL CHECK(status IN ('pending','approved','rejected')) DEFAULT 'pending',
                created_at TEXT NOT NULL,
                FOREIGN KEY(room_id) REFERENCES rooms(id)
            )
            """
        )


def seed_admin_and_room(
    admin_username: str, password_hash: str, default_rooms: list[dict]
):
    with get_db() as conn:
        c = conn.cursor()
        # admin
        c.execute("SELECT id FROM users WHERE username=?", (admin_username,))
        if not c.fetchone():
            c.execute(
                "INSERT INTO users(username, password_hash, role) VALUES (?,?,?)",
                (admin_username, password_hash, "admin"),
            )
        # rooms
        for r in default_rooms:
            c.execute("SELECT id FROM rooms WHERE id=?", (r["id"],))
            if not c.fetchone():
                c.execute(
                    "INSERT INTO rooms(id, room_number, capacity, facilities) VALUES (?,?,?,?)",
                    (r["id"], r["room_number"], r.get("capacity"), r.get("facilities")),
                )


def add_booking(
    user_name: str,
    room_id: int,
    start_iso: str,
    end_iso: str,
    status: str = "pending",
    department: str | None = None,
) -> int:
    with get_db() as conn:
        c = conn.cursor()
        created_at = datetime.utcnow().isoformat()
        c.execute(
            "INSERT INTO bookings(user_name, department, room_id, start_time, end_time, status, created_at) VALUES (?,?,?,?,?,?,?)",
            (user_name, department, room_id, start_iso, end_iso, status, created_at),
        )
        return c.lastrowid or 0


def list_bookings(start_from_iso: str | None = None, end_before_iso: str | None = None):
    with get_db(True) as conn:
        c = conn.cursor()
        query = "SELECT * FROM bookings"
        params = []
        clauses = []
        if start_from_iso:
            clauses.append("end_time >= ?")
            params.append(start_from_iso)
        if end_before_iso:
            clauses.append("start_time <= ?")
            params.append(end_before_iso)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY start_time ASC"
        rows = c.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def get_booking(bid: int):
    with get_db(True) as conn:
        row = (
            conn.cursor()
            .execute("SELECT * FROM bookings WHERE id=?", (bid,))
            .fetchone()
        )
        return dict(row) if row else None


def update_booking_status(bid: int, status: str):
    with get_db() as conn:
        conn.cursor().execute("UPDATE bookings SET status=? WHERE id=?", (status, bid))


def check_conflict(
    room_id: int, start_iso: str, end_iso: str, exclude_booking_id: int | None = None
) -> bool:
    # overlap if (start < other_end) and (end > other_start)
    with get_db(True) as conn:
        c = conn.cursor()
        query = (
            "SELECT COUNT(*) as cnt FROM bookings "
            "WHERE room_id=? AND status IN ('pending','approved') AND "
            "(? < end_time) AND (? > start_time)"
        )
        params = [room_id, start_iso, end_iso]
        if exclude_booking_id is not None:
            query += " AND id != ?"
            params.append(exclude_booking_id)
        row = c.execute(query, params).fetchone()
        return row["cnt"] > 0


def delete_past_bookings(now_iso: str):
    """删除结束时间超过当前时间的预约（即时清理）"""
    with get_db() as conn:
        conn.cursor().execute("DELETE FROM bookings WHERE end_time < ?", (now_iso,))


def delete_old_bookings(cutoff_iso: str):
    """删除创建时间超过1个月的预约数据"""
    with get_db() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM bookings WHERE created_at < ?", (cutoff_iso,))
        deleted_count = c.rowcount
        return deleted_count


def cleanup_database():
    """数据库清理：删除1个月前的数据"""
    from datetime import datetime, timedelta

    now = datetime.utcnow()
    # 删除1个月前创建的预约
    one_month_ago = now - timedelta(days=30)
    cutoff_iso = one_month_ago.isoformat()

    deleted_count = delete_old_bookings(cutoff_iso)

    # 记录清理信息
    print(
        f"[{now.isoformat()}] 数据库清理完成，删除了 {deleted_count} 条超过30天的预约记录"
    )
    return deleted_count
