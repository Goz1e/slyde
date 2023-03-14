# Generated by Django 4.1.7 on 2023-03-12 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_room_members_alter_room_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='messages',
            field=models.ManyToManyField(blank=True, related_name='room', related_query_name='room', to='chat.message'),
        ),
    ]