from django.contrib.auth import get_user_model
from django.contrib import admin


user_model = get_user_model()


admin.site.register(user_model)
