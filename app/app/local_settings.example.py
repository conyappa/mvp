# pylint: disable=import-error,wildcard-import,unused-wildcard-import
from .settings import *  # noqa: F401,F403


# Secrets.
SECRET_KEY = "m[4xQ]go~21)h6'HWh@Xz4ydn8X]H1vON4E8~`'>zv+cf+rZww"


# Other environmental variables.
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Database: https://docs.djangoproject.com/en/2.2/ref/settings/#databases.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": 5432,
    }
}


# Mailer: https://docs.djangoproject.com/en/2.2/topics/email/.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
