"""Development settings."""

from decouple import config

from .base import DATABASES, BASE_REST_FRAMEWORK


DEBUG = True
ALLOWED_HOSTS: list[str] = []
CORS_ALLOW_ALL_ORIGINS = True


DB_HOST = config('DB_HOST')
DATABASES['default']['HOST'] = 'localhost' if DB_HOST == 'default' else DB_HOST


REST_FRAMEWORK = BASE_REST_FRAMEWORK | {
    'MAX_LIMIT': 5000,
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30000/minute',
        'product': '6000/minute',
        'search': '30000/minute',
    },
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
