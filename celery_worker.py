from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    'worker',
    broker= CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['tasks'],
)

celery_app.conf.task_routes = {
    'tasks.analyse_doc': {'queue': 'analysis'}
}
