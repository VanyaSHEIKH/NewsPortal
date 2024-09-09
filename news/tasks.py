from celery import shared_task
from django.core.mail import send_mail

from news.views import send_weekly_post_notifications


@shared_task
def task_1():
    send_weekly_post_notifications()