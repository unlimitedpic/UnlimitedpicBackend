# Generated by Django 2.1 on 2019-11-24 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unlimited_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sociallogin',
            name='user',
        ),
        migrations.DeleteModel(
            name='SocialLogin',
        ),
    ]
