from datetime import datetime

from models import get_db


class UserRepository:
    def ensure_admin(self, username: str, password_hash: str) -> None:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username=?", (username,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO users(username, password_hash, role) VALUES (?,?,?)",
                    (username, password_hash, "admin"),
                )


class RoomRepository:
    def ensure_rooms(self, rooms: list[dict]) -> None:
        with get_db() as conn:
            cursor = conn.cursor()
            for room in rooms:
                cursor.execute("SELECT id FROM rooms WHERE id=?", (room["id"],))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO rooms(id, room_number, capacity, facilities) VALUES (?,?,?,?)",
                        (room["id"], room["room_number"], room.get("capacity"), room.get("facilities")),
                    )


class BookingRepository:
    def add_booking(
        self,
        user_name: str,
        room_id: int,
        start_iso: str,
        end_iso: str,
        status: str = "pending",
        department: str | None = None,
    ) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            created_at = datetime.utcnow().isoformat()
            cursor.execute(
                "INSERT INTO bookings(user_name, department, room_id, start_time, end_time, status, created_at) VALUES (?,?,?,?,?,?,?)",
                (user_name, department, room_id, start_iso, end_iso, status, created_at),
            )
            return cursor.lastrowid or 0

    def list_bookings(self, start_from_iso: str | None = None, end_before_iso: str | None = None) -> list[dict]:
        with get_db(True) as conn:
            cursor = conn.cursor()
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
            rows = cursor.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    def get_booking(self, booking_id: int) -> dict | None:
        with get_db(True) as conn:
            row = (
                conn.cursor()
                .execute("SELECT * FROM bookings WHERE id=?", (booking_id,))
                .fetchone()
            )
            return dict(row) if row else None

    def update_booking_status(self, booking_id: int, status: str) -> None:
        with get_db() as conn:
            conn.cursor().execute("UPDATE bookings SET status=? WHERE id=?", (status, booking_id))

    def check_conflict(
        self,
        room_id: int,
        start_iso: str,
        end_iso: str,
        exclude_booking_id: int | None = None,
    ) -> bool:
        with get_db(True) as conn:
            cursor = conn.cursor()
            query = (
                "SELECT COUNT(*) as cnt FROM bookings "
                "WHERE room_id=? AND status IN ('pending','approved') AND "
                "(? < end_time) AND (? > start_time)"
            )
            params = [room_id, start_iso, end_iso]
            if exclude_booking_id is not None:
                query += " AND id != ?"
                params.append(exclude_booking_id)
            row = cursor.execute(query, params).fetchone()
            return row["cnt"] > 0

    def delete_past_bookings(self, now_iso: str) -> None:
        with get_db() as conn:
            conn.cursor().execute("DELETE FROM bookings WHERE end_time < ?", (now_iso,))

    def delete_old_bookings(self, cutoff_iso: str) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE created_at < ?", (cutoff_iso,))
            return cursor.rowcount
