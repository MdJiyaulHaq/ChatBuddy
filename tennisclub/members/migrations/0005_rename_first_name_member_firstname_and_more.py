# Generated by Django 4.2.2 on 2023-06-26 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_remove_member_joined_date_remove_member_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='last_name',
            new_name='lastname',
        ),
    ]
