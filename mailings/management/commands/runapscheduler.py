import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from django.utils import timezone

from mailings.models import Mailing, Log
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER

logger = logging.getLogger(__name__)
scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

from django.utils import timezone


def change_status():
    for mailing in Mailing.objects.all():
        if timezone.now().time() < mailing.time_start:
            mailing.status = "created"


        elif mailing.time_start <= timezone.now().time() <= mailing.time_end:
            mailing.status = "started"

        elif mailing.time_end < timezone.now().time():
            mailing.status = "done"

        mailing.save()


def start_or_not_mailing():
    mailings_for_start = Mailing.objects.filter(status="started")
    for mailing in mailings_for_start:
        logs = Log.objects.filter(mailing=mailing)
        if not logs.exists():
            add_job(mailing)


def send_mailings(mailing):
    Log.objects.create(answer_server="Отправлено", mailing=mailing, owner=mailing.owner)
    title = mailing.message.title
    message = mailing.message.message
    from_email = EMAIL_HOST_USER
    to_emails = [client.email for client in mailing.clients.all()]

    send_mail(
        subject=title,
        message=message,
        from_email=from_email,
        recipient_list=to_emails,
    )

def add_job(mailing):
    if mailing.period == "daily":
        cron_period = CronTrigger(second="*/30")
        # cron_period = CronTrigger(day='*/1')

    elif mailing.period == "weekly":
        cron_period = CronTrigger(second="*/30")
        # cron_period = CronTrigger(week='*/1')

    else:
        cron_period = CronTrigger(second="*/30")
        # cron_period = CronTrigger(month='*/1')

    scheduler.add_job(
        send_mailings,
        trigger=cron_period,
        id=f"{mailing.pk}",
        max_instances=1,
        args=[mailing],
        replace_existing=True,
    )

class TimeIsOverError(Exception):
    """ Вызывается по истечении времени """
    pass

def time_end(mailing):
    return mailing.time_end


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):

        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            change_status,
            trigger=CronTrigger(second="*/30"),
            id="change_status",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            start_or_not_mailing,
            trigger=CronTrigger(second="*/30"),
            id="start_or_not_mailing",
            max_instances=1,
            replace_existing=True,
        )

        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()

        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
