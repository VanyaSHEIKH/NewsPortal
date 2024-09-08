from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import *

def send_weekly_updates():
    now = timezone.now()
    last_week = now - timedelta(days=7)

    subscribers = User.objects.filter(subscribed_posts__isnull=False).distinct()

    for subscriber in subscribers:
        new_posts = Post.objects.filter(
            category__in=subscriber.subscribed_posts.all(),
            date_in__gte=last_week
        )

        if new_posts.exists():
            post_links = [
                f"{post.title}: {settings.SITE_URL}{post.get_absolute_url()}"
                for post in new_posts
            ]
            message = (
                f'Здравствуйте, {subscriber.username}!\n\n'
                f'Вот новые статьи за последнюю неделю:\n'
                + '\n'.join(post_links) +
                '\n\nСпасибо за вашу подписку!'
            )
            try:
                send_mail(
                    subject='Новые статьи за неделю',
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                )
                print(f'Уведомление отправлено {subscriber.email}')
            except Exception as e:
                print(f'Ошибка при отправке уведомления {subscriber.email}: {e}')

# Настройка планировщика
scheduler = BackgroundScheduler()
scheduler.add_job(send_weekly_updates, 'cron', day_of_week='mon', hour=0, minute=0)  # Каждый понедельник в полночь
scheduler.start()