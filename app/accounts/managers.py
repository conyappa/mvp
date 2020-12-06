from django.contrib.auth.base_user import BaseUserManager
from app.base import BaseManagerMixin


class UserManager(BaseManagerMixin, BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username=username, password=password, **extra_fields)
