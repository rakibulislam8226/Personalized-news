import os
from celery import Celery

from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# for worker retries to connect to the broker on startup.
app.conf.broker_connection_retry_on_startup = True

# Schedule tasks
app.conf.beat_schedule = {
    "fetch-news-for-all-users": {
        "task": "apps.articlesio.tasks.fetch_news_for_all_users",
        "schedule": crontab(minute="*/10"),
    },
}
