# Generated by Django 2.2 on 2020-03-23 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='message',
            new_name='quote_message',
        ),
    ]
