"""Production settings."""

from .base import BASE_REST_FRAMEWORK


DEBUG = False
ALLOWED_HOSTS: list[str] = ['django']
CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = BASE_REST_FRAMEWORK | {
    'MAX_LIMIT': 100,
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'product': '60/minute',
        'search': '240/minute',
    },
}
