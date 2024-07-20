from datetime import datetime, timedelta
import time
from celery import shared_task

import logging
logger = logging.getLogger(__name__)

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q
from django.utils import timezone

from .models import Post, PostCategory, Category


# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)


@shared_task
def notifier(instance_key):
    print('Notifier task executed')
    logger.info('Weekly update task executed')
    instance = Post.objects.get(pk=instance_key)

    html_content = render_to_string(
        'post_created.html',
        {
            'post': instance,
        }
    )
    text_content = strip_tags(html_content)

    for category in PostCategory.objects.filter(post_id=instance_key):
        msg = EmailMultiAlternatives(
            subject=f'Новая запись в категории {category.category}',
            body=text_content,
            from_email='django.emailsender@yandex.ru',
            # recipient_list=Category.objects.get(pk=instance.category.pk).subscribers.all()
            to=category.category.subscribers.all().values_list('email', flat=True)
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_update():
    logger.info('Weekly update task started')
    print('Weekly update task started')
    try:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)

        for category in Category.objects.all():
            logger.info(f'Processing category: {category}')
            print(f'Processing category: {category}')
            posts_last_week = Post.objects.filter(
                Q(category=category) & Q(date_add__gte=start_date, date_add__lte=end_date)
            )

            if not posts_last_week.exists():
                logger.info(f'No posts found for category: {category}')
                print(f'No posts found for category: {category}')
                continue

            subject = f'Обновления в категории "{category}" за неделю'

            try:
                html_content = render_to_string(
                    'weekly_update.html',
                    {
                        'category': category,
                        'news': posts_last_week,
                    }
                )
            except Exception as e:
                logger.error(f'Error rendering template: {e}', exc_info=True)
                print(f'Error rendering template: {e}')
                continue

            text_content = strip_tags(html_content)

            recipients = list(category.subscribers.all().values_list('email', flat=True))
            if recipients:
                logger.info(f'Sending email to: {recipients}')
                print(f'Sending email to: {recipients}')
                try:
                    msg = EmailMultiAlternatives(
                        subject=subject,
                        body=text_content,
                        from_email='django.emailsender@yandex.ru',
                        to=recipients
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    logger.info('Email sent successfully')
                    print('Email sent successfully')
                except Exception as e:
                    logger.error(f'Error sending email: {e}', exc_info=True)
                    print(f'Error sending email: {e}')
            else:
                logger.info('No recipients found')
                print('No recipients found')
    except Exception as e:
        logger.error(f'Error in weekly_update task: {e}', exc_info=True)
        print(f'Error in weekly_update task: {e}')
    logger.info('Weekly update task finished')
    print('Weekly update task finished')