# Generated by Django 4.1.2 on 2024-08-10 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0015_rename_garnishment_amount_federal_case_result_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='federal_loan_case_data',
            name='employee_name',
            field=models.CharField(default='Leo', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='federal_case_result',
            name='result',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='multiple_student_loan_result',
            name='garnishment_amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='single_student_loan_result',
            name='garnishment_amount',
            field=models.FloatField(),
        ),
    ]
