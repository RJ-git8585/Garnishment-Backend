# Generated by Django 4.1.1 on 2024-08-20 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0029_rename_twentyfifth_percent_of_eraning_single_student_loan_data_and_result_fifteen_percent_of_eraning'),
    ]

    operations = [
        migrations.CreateModel(
            name='setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setting1', models.BooleanField()),
                ('setting2', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]