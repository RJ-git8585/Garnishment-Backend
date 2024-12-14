# Generated by Django 5.0.9 on 2024-12-14 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0015_remove_calculation_data_results_amount_to_withhold_child1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='multiple_garnishment_case_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=255)),
                ('employer_id', models.CharField(max_length=255)),
                ('garnishment_priority_order', models.CharField(max_length=255)),
                ('garnishment_amount', models.FloatField()),
                ('net_pay', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='calculation_data_results',
            name='amount_to_withhold_child1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='calculationresult',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='calculationresult',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='federal_case_result',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='federal_case_result',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='federal_loan_case_data',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='federal_loan_case_data',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='federal_tax_data_and_result',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='federal_tax_data_and_result',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='garcalculation_data',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='garcalculation_data',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='multiple_garnishment_data',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='multiple_garnishment_data',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='multiple_student_loan_data',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='multiple_student_loan_data',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='multiple_student_loan_data_and_result',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='multiple_student_loan_data_and_result',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='multiple_student_loan_result',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='multiple_student_loan_result',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='single_student_loan_data',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='single_student_loan_data',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='single_student_loan_data_and_result',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='single_student_loan_data_and_result',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='single_student_loan_result',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='single_student_loan_result',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='state_tax_data',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='state_tax_data',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='state_tax_result',
            name='employee_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='state_tax_result',
            name='employer_id',
            field=models.CharField(max_length=255),
        ),
    ]
