from celery import Celery
from core.config import settings
import time
import datetime

celery_app = Celery('worker',
                    broker = settings.CELERY_BROKER_URL,
                    backend = settings.CELERY_BACKEND_URL)

celery_app.conf.update(broker_connection_retry_on_startup = True,
                       timezone = "UTC",
                       beat_schedule = {
                           "print-hello-every-20-seconds": {
                               "task": "core.celery_conf.print_hello",
                               "schedule": 20.0
                           }
                       })

@celery_app.task
def print_hello():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Hello, World! - {now}")

@celery_app.task
def add_number(x, y):
    time.sleep(15)
    return x+y