# Generated by Django 4.1.1 on 2024-08-18 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0025_remove_multiple_student_loan_data_and_result_order_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='multiple_student_loan_data_and_result',
            old_name='federal_income_tax_rate',
            new_name='federal_income_tax',
        ),
        migrations.RenameField(
            model_name='multiple_student_loan_data_and_result',
            old_name='medicare_tax_rate',
            new_name='medicare_tax',
        ),
        migrations.RenameField(
            model_name='multiple_student_loan_data_and_result',
            old_name='social_tax_rate',
            new_name='social_tax',
        ),
        migrations.RenameField(
            model_name='multiple_student_loan_data_and_result',
            old_name='state_tax_rate',
            new_name='state_tax',
        ),
        migrations.AddField(
            model_name='multiple_student_loan_data_and_result',
            name='total_tax',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]