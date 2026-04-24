from apscheduler.schedulers.background import BackgroundScheduler

from repositories import BookingRepository
from services import BookingService

scheduler = BackgroundScheduler()
booking_service = BookingService(BookingRepository())


def start_scheduler():
    scheduler.add_job(
        booking_service.delete_past_bookings,
        "interval",
        days=1,
        id="cleanup_expired_bookings",
        replace_existing=True,
    )

    scheduler.add_job(
        booking_service.cleanup_database,
        "cron",
        day_of_week=6,
        hour=3,
        minute=0,
        id="cleanup_old_data",
        replace_existing=True,
    )

    if not scheduler.running:
        scheduler.start()
