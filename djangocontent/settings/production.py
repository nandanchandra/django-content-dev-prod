from .dev import *
from .dev import env


DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Chandra Nandan <chandranandan.chandrakar@gmail.com>",
)

