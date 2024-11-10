import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from NEWS_PORTAL.newsapp.models import Category, Post

logger = logging.getLogger(__name__)


def my_job():
    today = datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    subscribers = Category.objects.filter(name='IT').values_list('subscribers__email', flat=True)
    html_content = ''
    for post in posts:
        html_content += f'<a href="{post.get_absolute_url()}">{post.title}</a><br>'


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="00"
            ),
            # Триггер, который запускает задание в 18:00, пятницу
            id="my_job",  # уникальное имя задания
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

