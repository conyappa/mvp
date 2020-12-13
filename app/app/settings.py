"""
Django settings for the App project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# Build paths inside the project like this: os.path.join(BASE_DIR, ...).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Secrets.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")


# Other environmental variables.
TEST = "test" in sys.argv
DEBUG = os.getenv("DJANGO_ENV") == "development"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")


# Constants.
MAX_TICKETS = 4
TICKET_COST = 2500
TICKET_PICK_RANGE = range(1, 31)
DRAW_BEGINNING_WEEKDAY = 3
DRAW_RESULTS_HOUR = 12
DRAW_RESULTS_MINUTE = 0
PRIZES = [0, 50, 100, 200, 400, 800, 1600, 3200]


# Application definition.
INSTALLED_APPS = [
    # Third party.
    "rest_framework",
    "corsheaders",
    "whitenoise.runserver_nostatic",
    "phonenumber_field",
    # First party.
    "bot.apps.BotConfig",  # Load this app first!
    "accounts.apps.AccountsConfig",
    "lottery.apps.LotteryConfig",
    "scheduler.apps.SchedulerConfig",  # Load this app last!
    # Built-in.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "app.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "app", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


WSGI_APPLICATION = "app.wsgi.application"


# CORS: https://github.com/adamchainz/django-cors-headers#cors_origin_whitelist.
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = [
#     # In order to the app's endpoints from local docs.
#     "http://localhost:8000",
# ]


# Database: https://docs.djangoproject.com/en/2.2/ref/settings/#databases.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}
# Configure `DATABASE_URL` as the main database in production.
if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(ssl_require=True)


# Django REST framework.
REST_FRAMEWORK = {}


# Authentication.
AUTH_USER_MODEL = "accounts.User"


# Internationalization: https://docs.djangoproject.com/en/2.2/topics/i18n/.
LANGUAGE_CODE = "en"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_L10N = True
USE_TZ = True


PROPAGATE_EXCEPTIONS = True


# Sentry: https://sentry.io/for/django/.
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN", ""), integrations=[DjangoIntegration()])


# pylint: disable=line-too-long
# Static files (CSS, JavaScript, Images): https://docs.djangoproject.com/en/2.2/howto/static-files/.  # noqa=E501
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


# Whitenoise.
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
