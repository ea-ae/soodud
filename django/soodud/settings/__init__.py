"""Settings initialization."""

from decouple import config

from .base import *


if config('PRODUCTION', cast=bool):
    from .production import *
else:
    from .development import *
