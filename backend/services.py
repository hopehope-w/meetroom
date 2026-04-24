from datetime import datetime, timedelta

from repositories import BookingRepository


class BookingService:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def list_bookings(self, start_from_iso: str | None = None, end_before_iso: str | None = None) -> list[dict]:
        return self.booking_repository.list_bookings(start_from_iso, end_before_iso)

    def get_booking(self, booking_id: int) -> dict | None:
        return self.booking_repository.get_booking(booking_id)

    def create_booking(
        self,
        user_name: str,
        department: str | None,
        room_id: int,
        start_iso: str,
        end_iso: str,
    ) -> int:
        return self.booking_repository.add_booking(
            user_name=user_name,
            department=department,
            room_id=room_id,
            start_iso=start_iso,
            end_iso=end_iso,
            status="pending",
        )

    def has_conflict(self, room_id: int, start_iso: str, end_iso: str) -> bool:
        return self.booking_repository.check_conflict(room_id, start_iso, end_iso)

    def update_booking_status(self, booking_id: int, status: str) -> None:
        self.booking_repository.update_booking_status(booking_id, status)

    def get_recent_user_bookings(self, user_name: str) -> list[dict]:
        now = datetime.utcnow()
        start_date = now - timedelta(days=30)
        end_date = now + timedelta(days=30)
        return [
            booking
            for booking in self.booking_repository.list_bookings(start_date.isoformat(), end_date.isoformat())
            if (booking.get("user_name") or "").strip() == user_name
        ]

    def get_stats_summary(self) -> dict:
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
        bookings = self.booking_repository.list_bookings(start_iso, end_iso)

        by_day = {}
        for booking in bookings:
            day = booking["start_time"][:10]
            by_day.setdefault(day, []).append(booking)

        return {
            "days": [str(day) for day in days],
            "by_day": by_day,
            "total": len(bookings),
            "current_info": {
                "current_date": today.isoformat(),
                "current_time": local_now.strftime("%H:%M:%S"),
                "last_updated": local_now.isoformat(),
            },
        }

    def get_database_info(self) -> dict:
        all_bookings = self.booking_repository.list_bookings()
        now = datetime.utcnow()
        one_week_ago = now - timedelta(days=7)
        one_month_ago = now - timedelta(days=30)

        return {
            "total_bookings": len(all_bookings),
            "recent_week": len(
                [booking for booking in all_bookings if booking["created_at"] >= one_week_ago.isoformat()]
            ),
            "recent_month": len(
                [booking for booking in all_bookings if booking["created_at"] >= one_month_ago.isoformat()]
            ),
            "old_data_count": len(
                [booking for booking in all_bookings if booking["created_at"] < one_month_ago.isoformat()]
            ),
            "cleanup_threshold": "Records older than 30 days can be cleaned manually or by the scheduler.",
        }

    def cleanup_database(self) -> int:
        one_month_ago = datetime.utcnow() - timedelta(days=30)
        return self.booking_repository.delete_old_bookings(one_month_ago.isoformat())

    def delete_past_bookings(self) -> None:
        self.booking_repository.delete_past_bookings(datetime.utcnow().isoformat())
