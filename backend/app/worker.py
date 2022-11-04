"""
Script to run on a celery worekr
"""

from raven import Client

from app.core.celery_app import celery_app
from app.core.config import SETTINGS

client_sentry = Client(SETTINGS.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    """Test for celery worker"""
    return f"test task return {word}"
