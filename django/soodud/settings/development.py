"""Development settings."""

from decouple import config

from .base import DATABASES, BASE_REST_FRAMEWORK


DEBUG = True
ALLOWED_HOSTS: list[str] = []


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8001',
    'http://localhost:8002',
    'http://127.0.0.1:8001',
    'http://127.0.0.1:8002',
]


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
