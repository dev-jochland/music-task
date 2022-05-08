from .base import *

DATABASES = {
        'default': {

            'ENGINE': "django.db.backends.postgresql",
            'NAME': config('POSTGRES_DB'),
            'USER': config('POSTGRES_USER'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': '127.0.0.1',
            'PORT': 5432,
        }
}

ALLOWED_HOSTS += ['*']
