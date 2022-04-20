"""Production settings."""

from .base import BASE_REST_FRAMEWORK


DEBUG = False
ALLOWED_HOSTS: list[str] = []

REST_FRAMEWORK = BASE_REST_FRAMEWORK | {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'product': '60/minute',
        'search': '240/minute',
    },
}
