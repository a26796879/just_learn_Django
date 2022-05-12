from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "just_learn.settings")

#app = Celery("just_learn")
app = Celery('just_learn', broker='amqp://niceguy:niceguy@35.227.175.4:5672')
app.conf.update(worker_pool_restarts=True)
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

