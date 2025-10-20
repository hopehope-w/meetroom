from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from models import delete_past_bookings, cleanup_database

scheduler = BackgroundScheduler()


def start_scheduler():
    # 每5天凌晨2点清理过期预约（已结束的会议）
    scheduler.add_job(
        lambda: delete_past_bookings(datetime.utcnow().isoformat()),
        "interval",
        days=5,
        start_date="2025-08-26 02:00:00",  # 从今天开始，每5天执行一次
        id="cleanup_expired_bookings",
    )

    # 每周日凌晨3点清理1个月前的历史数据
    scheduler.add_job(
        cleanup_database,
        "cron",
        day_of_week=6,  # 周日
        hour=3,
        minute=0,
        id="cleanup_old_data",
    )

    print("数据清理调度器已配置:")
    print("- 每5天凌晨2点清理已结束的会议")
    print("- 每周日凌晨3点清理超过30天的历史数据")

    if not scheduler.running:
        scheduler.start()
