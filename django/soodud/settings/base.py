"""Django settings for soodud project."""

from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # BASE_DIR / 'subdir'
SECRET_KEY = config('SECRET_KEY')
ROOT_URLCONF = 'soodud.urls'
WSGI_APPLICATION = 'soodud.wsgi.application'
STATIC_URL = 'static/'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_extensions',
    'corsheaders',

    'data.apps.DataConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

BASE_REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

BASE_LOGGING = {
    'version': 1,
    'formatters': {
        'normal': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'normal',
        },
        'client_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/client_log.log',
            'formatter': 'normal',
        },
        'client_errors': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/client_errors.log',
            'formatter': 'verbose',
        },
        'server_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/server_info.log',
            'formatter': 'normal',
        },
        'server_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/server_errors.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console', 'server_info'],
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['server_errors'],
        },
        'data': {
            'level': 'INFO',
            'handlers': ['console', 'client_info', 'client_errors'],
            'propagate': True
        },
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
