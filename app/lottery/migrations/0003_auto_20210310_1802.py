# Generated by Django 3.1.4 on 2021-03-10 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0002_auto_20201227_2334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='draw',
            options={'ordering': ['-created_at']},
        ),
    ]