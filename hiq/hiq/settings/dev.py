from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0my!vz1tbui8fx9()few^osp28m)%=de0u1yqfbr*f!%s7b_5q'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
