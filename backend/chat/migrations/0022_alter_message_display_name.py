# Generated by Django 4.1.7 on 2023-03-18 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0021_message_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='display_name',
            field=models.CharField(blank=True, default='non', max_length=50),
            preserve_default=False,
        ),
    ]