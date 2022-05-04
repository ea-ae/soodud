"""Production settings."""

from decouple import config

from .base import DATABASES, BASE_REST_FRAMEWORK


DEBUG = False

DOMAIN = config('DOMAIN')
ALLOWED_HOSTS: list[str] = ['django', f'https://{DOMAIN}']
CSRF_TRUSTED_ORIGINS = [f'https://{DOMAIN}']
CORS_ALLOWED_ORIGINS = [f'https://{DOMAIN}']
CORS_ORIGIN_ALLOW_ALL = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


STATIC_ROOT = '/static'  # noqa
STATIC_URL = 'django/'


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
