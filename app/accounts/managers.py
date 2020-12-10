from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def everything(self):
        super().get_queryset()

    def create_user(self, phone, **extra_fields):
        user = self.model(phone=phone, **extra_fields)
        user.save()
        return user

    def create_superuser(self, phone, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone=phone, **extra_fields)
