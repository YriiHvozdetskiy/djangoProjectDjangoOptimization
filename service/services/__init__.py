from celery_app import app as celery_app

# __all__ = ('celery_app',) - щоб наша celery_app стартувала з нашим приложенієм django
__all__ = ('celery_app',)
