from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def everything(self):
        super().get_queryset()

    def create_user(self, username, email, phone, password, **extra_fields):
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username=username, email=email, phone=phone, password=password, **extra_fields)
