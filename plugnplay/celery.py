import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plugnplay.settings')

app = Celery('plugnplay')

# Load settings from Django settings, using a CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

# Add this line (optional if using django-celery-beat's scheduler)
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'