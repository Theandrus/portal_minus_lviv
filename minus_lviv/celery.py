import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the Celery app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minus_lviv.settings')

# Create the Celery app
app = Celery('minus_lviv')

# Load the settings from the Django project
app.config_from_object(settings, namespace='CELERY')

# Discover tasks in the Django project
app.autodiscover_tasks()

# Define the Celery beat schedule
app.conf.beat_schedule = {
    'send_new_minuses': {
        'task': 'minusstore.tasks.minus_send_new',
        'schedule': crontab(day_of_week=1),  # Change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}

app.conf.beat_schedule = {
    'check_payment_status': {
        'task': 'user.tasks.check_payment_status',
        'schedule': 10.0,
    },
}

# Set the timezone for the Celery app
app.conf.timezone = 'UTC'