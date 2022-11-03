"""
Main celery app, to execute on a celery worker
"""

from celery import Celery

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
