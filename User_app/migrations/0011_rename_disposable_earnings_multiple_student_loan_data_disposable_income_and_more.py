# Generated by Django 5.0.9 on 2024-12-14 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0010_rename_disposable_earnings_calculation_data_results_disposable_income'),
    ]

    operations = [
        migrations.RenameField(
            model_name='multiple_student_loan_data',
            old_name='disposable_earnings',
            new_name='disposable_income',
        ),
        migrations.RenameField(
            model_name='single_student_loan_data',
            old_name='disposable_earnings',
            new_name='disposable_income',
        ),
    ]
