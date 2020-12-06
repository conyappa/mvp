"""
WSGI configuration for the App project.
It exposes the WSGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from .set_settings_module import set_settings_module


set_settings_module()

application = get_wsgi_application()
