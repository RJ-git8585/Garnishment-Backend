# Generated by Django 5.0.9 on 2025-01-23 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0039_peo_table_rename_cid_employer_profile_employer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_details',
            name='co_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='company_details',
            name='ein',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='company_details',
            name='zipcode',
            field=models.IntegerField(),
        ),
    ]
