# pylint: disable=import-error,wildcard-import,unused-wildcard-import
from .settings import *  # noqa: F401,F403


# Secrets.
SECRET_KEY = "m[4xQ]go~21)h6'HWh@Xz4ydn8X]H1vON4E8~`'>zv+cf+rZww"


# Twilio.
TWILIO_ACCOUNT_SID = "Z9RhuwLgtVPZlyf6ei9H6nVXYYeBbzeDjg"
TWILIO_AUTH_TOKEN = "iLskXIhauahGmtTHzze5iDH6vIZdDXhF"
TWILIO_PHONE_NUMBER = "+0123456789"


# Telegram.
TELEGRAM_TOKEN = "6381479124:AAGB3tTjASAHxGnO-QVMoUNIRbNq2Oe8154"


# Email.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_PASSWORD = "password"
EMAIL_HOST_USER = "example@gmail.com"
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False


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
