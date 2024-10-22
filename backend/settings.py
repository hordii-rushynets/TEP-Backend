"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
from enum import IntEnum
from corsheaders.defaults import default_headers
from celery.schedules import crontab


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)g_rd3*j)dnkrd!8b@mb821t0yq129hzx*!f%r97(j2$#%@it)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv("CSRF_TRUSTED_ORIGINS").split(",")]
LOCALE_PATHS = [BASE_DIR / 'locale']

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',

    'django.contrib.sites',

    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'storages',

    'common',
    'store',
    'blog',
    'tep_user',
    'cart',
    'vacancy',
    'post'
]

DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,
    'UPDATE_LAST_LOGIN': False,
}
APPEND_SLASH=False

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware'
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'tep'),
        'USER': os.getenv('POSTGRES_USER', 'tep'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'qwerty123'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = [
    'tep_user.authentication.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'real-ip',
]


class RedisDatabases(IntEnum):
    DEFAULT: int = 0
    CELERY: int = 1
    CELERY_RESULTS: int = 2
    LOGIN_CODE: int = 3
    IP_CONTROL: int = 4
    LOCK: int = 5
    CACHE: int = 6


REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or None
REDIS_USE_SSL = os.environ.get('REDIS_USE_SSL', '').upper() in ('TRUE', '1', 'Y', 'YES', 'T')

REDIS_PROTOCOL = 'rediss' if REDIS_USE_SSL else 'redis'
REDIS_AUTH = f'default:{REDIS_PASSWORD}@' if REDIS_PASSWORD else ''

REDIS_CONNECTION = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'password': REDIS_PASSWORD,
}

REDIS_CONNECTION_QUERY = '?ssl_cert_reqs=none' if REDIS_USE_SSL else ''
REDIS_CONNECTION_STRING = '{protocol}://{auth}{host}:{port}/%s{query}'.format(
    protocol=REDIS_PROTOCOL,
    auth=REDIS_AUTH,
    **REDIS_CONNECTION,
    query=REDIS_CONNECTION_QUERY,
)
print('REDIS_CONNECTION_STRING:', REDIS_CONNECTION_STRING)

CELERY_TIMEZONE = "Europe/Kiev"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 3600*3
CELERY_TASK_SOFT_TIME_LIMIT = 3500*3
CELERY_BROKER_URL = REDIS_CONNECTION_STRING % int(RedisDatabases.CELERY)

LANGUAGES = (
    ('uk', 'Ukrainian'),
    ('en', 'English'),
    ('ru', 'Russian')
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'


AUTH_USER_MODEL = 'tep_user.TEPUser'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
DEFAULT_FILE_STORAGE = 'backend.storages.MediaS3Boto3Storage'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")


NOVA_POST_API_KEY = os.getenv('NOVA_POST_API_KEY')
REF_CITY_SENDER = os.getenv('REF_CITY_SENDER')

REST_USE_JWT = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'format_tags': 'p;h1;h2;h3;pre',
        'removePlugins': 'format',
    },
}

CKEDITOR_BASEPATH = f'{STATIC_URL}ckeditor/ckeditor/'

MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
MAILCHIMP_AUDIENCE_ID = os.getenv('MAILCHIMP_AUDIENCE_ID')
MAILCHIMP_DATA_CENTER = os.getenv('MAILCHIMP_DATA_CENTER')  # The prefix of your API key (e.g., 'us1', 'us2')

LIQPAY_PUBLIC_KEY = os.getenv('LIQPAY_PUBLIC_KEY')
LIQPAY_PRIVATE_KEY = os.getenv('LIQPAY_PRIVATE_KEY')

META_PIXEL_ID = os.getenv('META_PIXEL_ID')
META_PIXEL_ACCESS_TOKEN = os.getenv('META_PIXEL_ACCESS_TOKEN')
META_GRAPH_API = os.getenv('META_GRAPH_API')

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


DATA_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{int(RedisDatabases.CACHE)}",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CELERY_BEAT_SCHEDULE = {
    'save_queryset_every_3_hours': {
        'task': 'store.tasks.save_queryset',
        'schedule': crontab(minute=0, hour='*/3'),  # Кожні 3 години
    },
}
