import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import  EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import render_to_string

from news.models import Category, Post  # замените на ваш реальный путь к моделям



logger = logging.getLogger(__name__)


def send_weekly_newsletter():
    last_week = timezone.now() - timezone.timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        if not subscribers:
            continue

        new_posts = Post.objects.filter(
            category=category,
            date_add__gte=last_week
        )

        if new_posts.exists():
            subject = f'Новые статьи в категории {category.name} за неделю'
            from_email = 'django.emailsender@yandex.ru'

            for subscriber in subscribers:
                html_content = render_to_string('weekly_newsletter.html', {
                    'category': category,
                    'posts': new_posts
                })
                text_content = f'Новые статьи в категории {category.name} за неделю:\n\n' + \
                               '\n'.join([post.title for post in new_posts])

                msg = EmailMultiAlternatives(subject, text_content, from_email, [subscriber.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            logger.info(f"Sent weekly newsletter to {subscribers.count()} subscribers in category {category.name}.")

# функция, которая будет удалять неактуальные задачи
# def delete_old_job_executions(max_age=604_800):
#     """This job deletes all apscheduler job executions older than `max_age` from the database."""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_weekly_newsletter,
            trigger=CronTrigger(
                # day_of_week="mon", hour="08", minute="00"  # Запуск каждую неделю в понедельник в 8 утра
                second="*/500",  # test
            ),
            id="send_weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'send_weekly_newsletter'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

        # scheduler.add_job(
        #     delete_old_job_executions,
        #     trigger=CronTrigger(
        #         day_of_week="mon", hour="00", minute="00"
        #     ),
        #     # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
        #     id="delete_old_job_executions",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info(
        #     "Added weekly job: 'delete_old_job_executions'."
        # )
        #
        # try:
        #     logger.info("Starting scheduler...")
        #     scheduler.start()
        # except KeyboardInterrupt:
        #     logger.info("Stopping scheduler...")
        #     scheduler.shutdown()
        #     logger.info("Scheduler shut down successfully!")

