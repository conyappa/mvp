from app.base import BaseManagerMixin

class UserManager(BaseManagerMixin, BaseUserManager):
    def create_user(self, rut, password, **extra_fields):
        user = self.model(rut=rut, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, rut, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(rut=rut, password=password, **extra_fields)
