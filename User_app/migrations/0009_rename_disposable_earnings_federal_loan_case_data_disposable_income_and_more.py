# Generated by Django 5.0.9 on 2024-12-14 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0008_rename_disposable_earnings_garcalculation_data_disposable_income'),
    ]

    operations = [
        migrations.RenameField(
            model_name='federal_loan_case_data',
            old_name='disposable_earnings',
            new_name='disposable_income',
        ),
        migrations.RenameField(
            model_name='federal_tax_data_and_result',
            old_name='disposable_earnings',
            new_name='disposable_income',
        ),
        migrations.RenameField(
            model_name='multiple_student_loan_data_and_result',
            old_name='disposable_earnings',
            new_name='disposable_income',
        ),
        migrations.RenameField(
            model_name='single_student_loan_data_and_result',
            old_name='disposable_earnings',
            new_name='disposable_income',
        ),
        migrations.RenameField(
            model_name='state_tax_data',
            old_name='disposable_earnings',
            new_name='disposable_income',
        ),
        migrations.RenameField(
            model_name='state_tax_result',
            old_name='disposable_earnings',
            new_name='disposable_income',
        ),
    ]
