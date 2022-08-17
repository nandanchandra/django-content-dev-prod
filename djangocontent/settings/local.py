from .dev import *
from .dev import env

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY',default='django-insecure-bomhcbhc#rmqp9&4k$_0sse4rc(a$#8jrahz(h%m!ud_so66$x')

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
