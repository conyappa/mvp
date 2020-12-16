# pylint: disable=import-error,wildcard-import,unused-wildcard-import
from .settings import *  # noqa: F401,F403


# Secrets.
SECRET_KEY = "m[4xQ]go~21)h6'HWh@Xz4ydn8X]H1vON4E8~`'>zv+cf+rZww"
TWILIO_ACCOUNT_SID = "Z9RhuwLgtVPZlyf6ei9H6nVXYYeBbzeDjg"
TWILIO_AUTH_TOKEN = "iLskXIhauahGmtTHzze5iDH6vIZdDXhF"
TWILIO_PHONE_NUMBER = "+0123456789"


# Other environmental variables.
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


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


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = "gmail.com"
EMAIL_HOST_PASSWORD = "password"
EMAIL_HOST_USER = "example"
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
