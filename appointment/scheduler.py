from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .tasks import send_weekly_updates
appointment_scheduler=BackgroundScheduler()

appointment_scheduler.add_job(
    send_weekly_updates,
    trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),  # Каждый понедельник в полночь
    id="send_weekly_updates",
    max_instances=1,
    replace_existing=True,
)
