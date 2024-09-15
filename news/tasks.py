from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

# from news.views import send_weekly_post_notifications
from django.conf import settings
from .models import *
from datetime import *
from celery import *
from django.utils import timezone

# @shared_task
# def task_1():
#     send_weekly_post_notifications()

# @shared_task
# def send_email_task(pk):
#     post = Post.objects.get(pk=pk)
#     categories = post.category.all()
#     title = post.title
#     subscribers_emails = []
#
#     for cats in categories:
#         subscribers_users = cats.subscribers.all()
#         for sub_users in subscribers_users:
#             subscribers_emails.append(sub_users.email)
#     html_content = render_to_string(
#         'celery_send_message_new.html',
#         {
#             'text': f'{post.title}',
#             'link': f'{settings.SITE_URL}/news/{pk}',
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers_emails,
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()

@shared_task
def send_notification(subscriber_email, subscriber_username, categories, post_title, post_url):
    message = (
        f'Здравствуйте, {subscriber_username}!\n\n'
        f'В категории "{", ".join(categories)}" добавлена новая новость: {post_title}.\n\n'
        f'Вы можете прочитать статью по следующей ссылке: {settings.SITE_URL}{post_url}'
    )
    try:
        send_mail(
            subject='Новая новость в вашей категории',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscriber_email],
        )
        print(f'Уведомление отправлено {subscriber_email}')
    except Exception as e:
        print(f'Ошибка при отправке уведомления {subscriber_email}: {e}')


@shared_task
def send_weekly_celery():
    today = timezone.now()
    last_week = today - timezone.timedelta(days=7)
    posts = Post.objects.filter(date_in__gte=last_week)
    categories = posts.values_list('category__name_category', flat=True).distinct()
    subscribers = set(
        Category.objects.filter(name_category__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string('account/email/week_post.html', {
        'link': settings.SITE_URL,
        'posts': posts,
    })
    msg = EmailMultiAlternatives(
        subject='Статьи в любимой категории за неделю',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(subscribers),
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()