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
import datetime as dt
from sentry_sdk.integrations.django import DjangoIntegration


# Build paths inside the project like this: os.path.join(BASE_DIR, ...).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Secrets.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")


# Telegram.
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_WEBHOOK_DOMAIN = os.environ.get("TELEGRAM_WEBHOOK_DOMAIN")
TELEGRAM_WEBHOOK_PORT = int(os.environ.get("TELEGRAM_WEBHOOK_PORT", "8443"))
TELEGRAM_STAFF_GROUP_ID = os.environ.get("TELEGRAM_STAFF_GROUP_ID")
TELEGRAM_STAFF_GROUP_ID = None if (TELEGRAM_STAFF_GROUP_ID is None) else int(TELEGRAM_STAFF_GROUP_ID)
TELEGRAM_MAX_BULK_SIZE = int(os.environ.get("TELEGRAM_MAX_BULK_SIZE", 30))
TELEGRAM_DELAY_SECONDS = float(os.environ.get("TELEGRAM_DELAY_SECONDS", 1))


# Twilio.
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
TWILIO_MAX_BULK_SIZE = int(os.environ.get("TWILIO_MAX_BULK_SIZE", 30))
TWILIO_DELAY_SECONDS = int(os.environ.get("TWILIO_DELAY_SECONDS", 1))


# Other environmental variables.
TEST = "test" in sys.argv
DEBUG = os.environ.get("DJANGO_ENV") == "development"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")


# Constants.
MAX_TICKETS = int(os.environ.get("MAX_TICKETS", "4"))
TICKET_COST = int(os.environ.get("TICKET_COST", "5000"))
INITIAL_EXTRA_TICKETS_TTL = list(map(int, os.environ.get("INITIAL_EXTRA_TICKETS_TTL", "1").split(" ")))
PICK_RANGE = tuple(range(int(os.environ.get("MIN_PICK", "1")), int(os.environ.get("MAX_PICK", "30")) + 1))
NEW_DRAW_WEEKDAY = int(os.environ.get("NEW_DRAW_WEEKDAY", "0"))
DRAW_RESULTS_HOUR, DRAW_RESULTS_MINUTE = map(int, os.environ.get("DRAW_RESULTS_TIME", "20:00").split(":"))
NEW_DRAW_CREATION_DELTA_HOURS = int(os.environ.get("NEW_DRAW_CREATION_DELTA_HOURS", "3"))
NEW_DRAW_REMINDER_DELTA_HOURS = int(os.environ.get("NEW_DRAW_REMINDER_DELTA_HOURS", "3"))
PRIZES = tuple(map(int, os.environ.get("PRIZES", "10 20 50 100 200 500 1000 5000").split(" ")))
BANK_ACCOUNT = os.environ.get("BANK_ACCOUNT")
WEEKDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
WEEKDAYS = WEEKDAYS[NEW_DRAW_WEEKDAY:] + WEEKDAYS[:NEW_DRAW_WEEKDAY]

# Properties.
NEW_DRAW_CREATION_HOUR = DRAW_RESULTS_HOUR - NEW_DRAW_CREATION_DELTA_HOURS
NEW_DRAW_REMINDER_HOUR = NEW_DRAW_CREATION_HOUR - NEW_DRAW_REMINDER_DELTA_HOURS
FORMATTED_NEW_DRAW_CREATION_TIME = dt.time(hour=NEW_DRAW_CREATION_HOUR, minute=DRAW_RESULTS_MINUTE).isoformat(
    timespec="minutes"
)
FORMATTED_DRAW_RESULTS_TIME = dt.time(hour=DRAW_RESULTS_HOUR, minute=DRAW_RESULTS_MINUTE).isoformat(timespec="minutes")
END_DRAW_WEEKDAY = (NEW_DRAW_WEEKDAY - 1) % 7


# Application definition.
INSTALLED_APPS = [
    # Third party.
    "rest_framework",
    "corsheaders",
    "whitenoise.runserver_nostatic",
    "phonenumber_field",
    "django_extensions",
    # First party.
    "bot.apps.BotConfig",  # Load this app first!
    "lottery.apps.LotteryConfig",
    "accounts.apps.AccountsConfig",  # Load this app second to last!
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


# Logging: https://docs.djangoproject.com/en/2.2/topics/logging/.
DEFAULT_LOGGING_LEVEL = "INFO" if DEBUG else "WARNING"
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", DEFAULT_LOGGING_LEVEL)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOGGING_LEVEL,
    },
}
PROPAGATE_EXCEPTIONS = True


# Mailer: https://docs.djangoproject.com/en/2.2/topics/email/.
# Email: https://docs.djangoproject.com/en/2.2/ref/settings/#email.
ADMINS = [("Ariel Martínez", "ariel@conyappa.cl")]
MANAGERS = [("Ariel Martínez", "ariel@conyappa.cl")]
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_PORT = int(os.environ.get("EMAIL_HOST_PORT", "25"))
EMAIL_USE_TLS = bool(int(os.environ.get("EMAIL_USE_TLS", "0")))
EMAIL_USE_SSL = bool(int(os.environ.get("EMAIL_USE_SSL", "0")))
EMAIL_USE_LOCALTIME = True


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


# Sentry: https://sentry.io/for/django/.
sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN", ""), integrations=[DjangoIntegration()])


# pylint: disable=line-too-long
# Static files (CSS, JavaScript, Images): https://docs.djangoproject.com/en/2.2/howto/static-files/.
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


# Whitenoise.
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
