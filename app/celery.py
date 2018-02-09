from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

from django.conf import settings  # noqa

capp = Celery('app')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
capp.config_from_object('django.conf:settings')
capp.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@capp.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
