from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from models import cleanup_database, delete_past_bookings

scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(
        lambda: delete_past_bookings(datetime.utcnow().isoformat()),
        "interval",
        days=1,
        id="cleanup_expired_bookings",
        replace_existing=True,
    )

    scheduler.add_job(
        cleanup_database,
        "cron",
        day_of_week=6,
        hour=3,
        minute=0,
        id="cleanup_old_data",
        replace_existing=True,
    )

    if not scheduler.running:
        scheduler.start()
