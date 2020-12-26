from django.contrib import admin
from .models import Draw, Ticket

@admin.register(Draw)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ["start_date", "pool", "results"]


@admin.register(Ticket)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ["picks", "draw", "user"]
