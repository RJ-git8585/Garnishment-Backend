# Generated by Django 5.0.9 on 2024-09-17 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='single_student_loan_data',
            old_name='federal_income',
            new_name='federal_income_tax',
        ),
    ]