"""
Django settings for mdmq_motor_inferencia project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# TODO: Temporal hasta obtener fecha máxima de actualización de STL
import atexit
from pathlib import Path

import redis
from decouple import config
from django.core.cache import cache
from mongoengine import connect

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-x1cr-c426u!g6$bn8vhpl@ly$y3=2-rgc1+*mv)z276jb@vk74"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [config("HOST_PERMITIDO")]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "motorInferencia",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # CORS
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "mdmq_motor_inferencia.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mdmq_motor_inferencia.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": config("ENGINE"),
#         "NAME": config("NAME"),
#         "ENFORCE_SCHEMA": config("ENFORCE_SCHEMA"),
#         "CLIENT": {"host": config("CLIENT_HOST")},
#     }
# }

connect(
    db=config("BDD_NAME"),
    username=config("BDD_USERNAME"),
    password=config("BDD_PASSWORD"),
    authentication_source=config("BDD_AUTHENTICATION_SOURCE"),
    host=config("BDD_HOST"),
    port=int(config("BDD_PORT")),
)

# BDD Caché
redis_instance = redis.StrictRedis(
    host=config("HOST_REDIS"),
    port=config("PUERTO_REDIS"),
    db=config("DB_ALIAS_REDIS"),
    password=config("PASSWORD_REDIS"),
    decode_responses=True,
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('HOST_REDIS')}:{config('PUERTO_REDIS')}/{config('DB_ALIAS_REDIS')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config("PASSWORD_REDIS"),
        },
    }
}

CACHE_TTL = 60 * 15
CACHE_PREFIX = "default"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "es-es"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuración CORS
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [config("FRONTEND_CONSUMO")]


# TODO: temporal hasta utilizar fecha máxima de actualización en STL
def limpiar_cache_redis():
    cache.clear()


atexit.register(limpiar_cache_redis)
