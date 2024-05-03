from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#CONEKTA
PUBLICA_CONEKTA = config('SANDBOX_PUBLICA_CONEKTA', default='')
PRIVADA_CONEKTA = config('SANDBOX_PRIVADA_CONEKTA', default='')

SITE_URL = 'http://test.hzcode.mx/'
PROTOCOL_HTTP = 'http'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
