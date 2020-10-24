import os


class Config(object):
    """Parent configuration class."""

    DEBUG = True

    TITLE = "Flask API with Celery"
    VERSION = "0.1.0"
    DESCRIPTION = "An API Skeleton with Celery."

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    BROKER_URL = CELERY_BROKER_URL