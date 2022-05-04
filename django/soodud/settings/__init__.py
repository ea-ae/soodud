"""Settings initialization."""

from decouple import config

from .base import *


PRODUCTION = config('PRODUCTION', cast=bool)

if PRODUCTION:
    from .production import *
else:
    from .development import *
