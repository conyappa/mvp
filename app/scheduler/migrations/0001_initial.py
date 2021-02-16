# Generated by Django 3.1.4 on 2021-02-13 17:02

from django.db import migrations, models
import scheduler.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last updated at')),
                ('scheduled_for', models.DateTimeField(blank=True, null=True, validators=[scheduler.models.validate_scheduled_time], verbose_name='scheduled for')),
                ('job_id', models.CharField(default=None, max_length=64, null=True, verbose_name='scheduler job ID')),
                ('text', models.TextField(verbose_name='message text')),
                ('is_draft', models.BooleanField(default=False, verbose_name='draft status')),
                ('sent', models.BooleanField(default=False, verbose_name='sent status')),
            ],
            options={
                'ordering': ('scheduled_for',),
            },
        ),
    ]