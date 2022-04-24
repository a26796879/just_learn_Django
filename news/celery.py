from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','news.settings')
app = Celery('proj', broker='amqp://guest@35.227.175.4:5672')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()