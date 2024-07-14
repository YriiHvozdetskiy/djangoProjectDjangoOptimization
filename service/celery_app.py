import os
import time

from celery import Celery
from django.conf import settings

# environ - отримуємо доступ до переменої середовища
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')

app = Celery('service')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
# autodiscover_tasks - автоматично celery перевіряє які таски є в нашому проєкті
app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(20)
    print('Hello from debug_task!')
