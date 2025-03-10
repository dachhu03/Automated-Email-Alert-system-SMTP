from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from celery import shared_task


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smtp.settings')

app = Celery('smtp')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_connection_retry_on_startup = True

# Set the timezone
app.conf.timezone = 'Asia/Kolkata'  # You can change this to your desired timezone, e.g., 'Asia/Kolkata'

# Auto-discover tasks from installed Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Celery Beat settings for periodic tasks
app.conf.beat_schedule = {
    'send-alert-email-every-1-minute': {
        'task': 'newapp.tasks.send_alert_email',  # Make sure this matches the task path
        'schedule': crontab(minute='*/1'),  # Execute every 1 minute
    },
}
