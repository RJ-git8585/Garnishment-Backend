# Generated by Django 5.0.9 on 2024-12-19 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0020_calculationresult_batch_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiple_garnishment_case_result',
            name='batch_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='multiple_garnishment_data',
            name='batch_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
