# Generated by Django 4.1.2 on 2024-08-07 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0008_student_loan_data_student_loan_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='single_student_loan_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('net_pay', models.FloatField()),
                ('garnishment_amount', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='student_loan_result',
            new_name='multiple_student_loan_result',
        ),
    ]
