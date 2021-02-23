# Generated by Django 3.1.4 on 2021-02-23 22:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_alias'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailListEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last updated at')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
            ],
            options={
                'verbose_name_plural': 'Email list entries',
            },
        ),
    ]
