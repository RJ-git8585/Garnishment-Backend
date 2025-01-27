# Generated by Django 5.1.5 on 2025-01-24 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0046_alter_employer_profile_employer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer_profile',
            name='cid',
            field=models.CharField(default='C00001', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employer_profile',
            name='email',
            field=models.EmailField(default='rjj@gmail.com', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='employer_profile',
            name='employer_name',
            field=models.CharField(max_length=255),
        ),
    ]
