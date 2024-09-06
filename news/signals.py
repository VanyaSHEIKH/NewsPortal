from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import *
from django.conf import settings
from django.core.mail import send_mail

@receiver(post_save, sender=Subscription)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscriptions = Subscription.objects.filter(category=instance.category)
        for subscription in subscriptions:
            mail_managers(
                'Новая статья в вашей категории',
                f'Новая статья: {instance.title}\n\n{instance.content}',
                settings.DEFAULT_FROM_EMAIL,
                [subscription.user.email],

            )