# Generated by Django 4.1.1 on 2024-08-14 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0020_federal_loan_case_data_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_loan_data',
            name='employee_name',
            field=models.CharField(default='John', max_length=255),
            preserve_default=False,
        ),
    ]
