import uuid
from django.db import models
from django.utils import timezone


class BaseManager(models.Manager):
    def all_active(self):
        return super().get_queryset().filter(is_active=True)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        serialize=False,
        unique=True,
        verbose_name="identifier",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="last updated at")
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name="last deleted at"
    )

    objects = BaseManager()

    def save(self, *args, **kwargs):
        self.clean_fields()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
