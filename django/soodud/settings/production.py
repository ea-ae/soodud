"""Production settings."""

from decouple import config

from .base import DATABASES, BASE_REST_FRAMEWORK


DEBUG = False
ALLOWED_HOSTS: list[str] = ['django']
CORS_ORIGIN_ALLOW_ALL = True


DB_HOST = config('DB_HOST')
DATABASES['default']['HOST'] = 'db' if DB_HOST == 'default' else DB_HOST


REST_FRAMEWORK = BASE_REST_FRAMEWORK | {
    'MAX_LIMIT': 100,
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'product': '60/minute',
        'search': '240/minute',
    },
}
