# Generated by Django 4.2.2 on 2023-06-26 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_rename_first_name_member_firstname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='joined_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
