from decouple import config

if config("CELERY", cast=bool, default=False):
    from .celery import app as celery_app

    __all__ = ("celery_app",)
