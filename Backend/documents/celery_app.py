# documents/celery_app.py
from celery import Celery
import os

# Load Redis from environment or defaults
REDIS_BROKER = os.getenv("REDIS_BROKER", "redis://localhost:6379/0")
REDIS_BACKEND = os.getenv("REDIS_BACKEND", "redis://localhost:6379/1")

# Create Celery instance (NO circular imports)
celery_app = Celery(
    "nlp_tasks",
    broker=REDIS_BROKER,
    backend=REDIS_BACKEND
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)
