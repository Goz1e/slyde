# Generated by Django 4.1.7 on 2023-03-17 21:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0014_room_allow_anon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='message',
            name='author',
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ManyToManyField(related_name='messages', related_query_name='messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
