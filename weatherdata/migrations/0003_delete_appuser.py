# Generated by Django 4.1.5 on 2023-02-08 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weatherdata', '0002_appuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='appUser',
        ),
    ]
