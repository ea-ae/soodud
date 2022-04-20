"""Development settings."""

from .base import BASE_REST_FRAMEWORK


DEBUG = True
ALLOWED_HOSTS: list[str] = []

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8001',
    'http://localhost:8002',
    'http://127.0.0.1:8001',
    'http://127.0.0.1:8002',
]

REST_FRAMEWORK = BASE_REST_FRAMEWORK | {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30000/minute',
        'product': '6000/minute',
        'search': '30000/minute',
    },
}
