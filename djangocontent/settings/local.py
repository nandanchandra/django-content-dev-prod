from .dev import *
from .dev import env

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY',default='django-insecure-bomhcbhc#rmqp9&4k$_0sse4rc(a$#8jrahz(h%m!ud_so66$x')

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "chandranandan.chandrakar@gmail.com"
DOMAIN = env("DOMAIN")
SITE_NAME = "Django Content"