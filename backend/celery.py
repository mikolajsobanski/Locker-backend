import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('backend',backend='db+postgresql://mikolaj:DAWID1mikolaj1@localhost:5432/locker', broker='redis://localhost:6379/0')

#app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()