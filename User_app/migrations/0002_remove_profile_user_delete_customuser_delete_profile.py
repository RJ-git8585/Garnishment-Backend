# Generated by Django 5.0.7 on 2024-07-31 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]