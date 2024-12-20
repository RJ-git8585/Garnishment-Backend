# Generated by Django 5.0.9 on 2024-12-18 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0019_federal_case_result_batch_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculationresult',
            name='batch_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='garcalculation_data',
            name='batch_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='multiple_student_loan_data',
            name='batch_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
