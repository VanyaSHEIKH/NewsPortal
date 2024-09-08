from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
import logging

from appointment.tasks import send_weekly_updates  # Импортируйте вашу новую функцию

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Добавляем вашу задачу для отправки новых статей каждую неделю
        scheduler.add_job(
            send_weekly_updates,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="send_weekly_updates",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'send_weekly_updates'.")

        # Остальные задачи...
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")