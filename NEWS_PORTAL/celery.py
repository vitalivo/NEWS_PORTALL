#celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NEWS_PORTAL.settings')

app = Celery('NEWS_PORTAL')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-weekly-news-email': {
        'task': 'tasks.send_weekly_news_email',
        'schedule': crontab(day_of_week='monday', hour=8, minute=0),
    },
}