from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = [
        "username",
        "password",
        "first_name",
        "last_name",
        "last_login",
        "date_joined",
        "telegram_id",
        "phone",
        "winnings",
        "extra_tickets_ttl",
    ]
