# This is an empty file that tells Python that this directory should be considered a Python package.

from .celery import app as celery_app

__all__ = ('celery_app',)
