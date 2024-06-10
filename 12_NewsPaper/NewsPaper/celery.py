from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update_every_monday_8am': {
        'task': 'news.tasks.weekly_update',
        'schedule': crontab(minute='0', hour='8', day_of_week='monday'),
        'args': (),
    },
}

# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'news.tasks.printer',
#         'schedule': 5,
#         'args': (5,),
#     },
# }

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'news.tasks.weekly_update',
        'schedule': 20,
        'args': (),
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
