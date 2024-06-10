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
    print('Weekly update task executed')
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)

    for category in Category.objects.all():
        posts_last_week = Post.objects.filter(
            Q(categories=category) & Q(post_date__gte=start_date, post_date__lte=end_date)
        )

        if not posts_last_week:
            continue

        subject = f'Обновления в категории "{category.category}" за неделю'

        html_content = render_to_string(
            'weekly_update.html',
            {
                'category': category.category,
                'news': posts_last_week,
            }
        )

        text_content = strip_tags(html_content)

        recipients = list(category.subscribers.all().values_list('email', flat=True))
        if recipients:
            print(f'Sending email to {recipients}')
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email='NewsPortal <django.emailsender@yandex.ru>',
                to=recipients
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print('Email sent')
        else:
            print('No recipients found')
