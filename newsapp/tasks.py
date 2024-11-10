#tasks.py
from datetime import datetime, timedelta
from celery import shared_task
from django.core.mail import send_mail
from .models import Post, Subscriber


@shared_task
def send_weekly_news_email():
    posts = Post.objects.filter(created_at__gte=datetime.now() - timedelta(days=7))

    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        send_mail(
            'Еженедельная новостная рассылка',
            'Подпишитесь на нашу новостную ленту',
            'vitalivoloshin1975@yandex.co.il',
            [subscriber.user.email],
            fail_silently=False,
        )