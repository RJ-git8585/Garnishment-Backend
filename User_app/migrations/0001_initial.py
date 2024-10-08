# Generated by Django 5.0.9 on 2024-09-23 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APICallLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('method', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='application_activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('details', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Calculation_data_results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('fedral_income_tax', models.FloatField()),
                ('social_and_security', models.FloatField()),
                ('medicare_tax', models.FloatField()),
                ('state', models.CharField(max_length=255)),
                ('state_taxes', models.FloatField()),
                ('earnings', models.FloatField()),
                ('support_second_family', models.BooleanField()),
                ('garnishment_fees', models.FloatField()),
                ('arrears_greater_than_12_weeks', models.BooleanField()),
                ('amount_to_withhold_child1', models.FloatField(blank=True, null=True)),
                ('amount_to_withhold_child2', models.FloatField(blank=True, null=True)),
                ('amount_to_withhold_child3', models.FloatField(blank=True, null=True)),
                ('amount_to_withhold_child4', models.FloatField(blank=True, null=True)),
                ('amount_to_withhold_child5', models.FloatField(blank=True, null=True)),
                ('arrears_amt_Child1', models.FloatField(blank=True, null=True)),
                ('arrears_amt_Child2', models.FloatField(blank=True, null=True)),
                ('arrears_amt_Child3', models.FloatField(blank=True, null=True)),
                ('arrears_amt_Child4', models.FloatField(blank=True, null=True)),
                ('arrears_amt_Child5', models.FloatField(blank=True, null=True)),
                ('number_of_arrear', models.IntegerField(blank=True, null=True)),
                ('number_of_garnishment', models.IntegerField(blank=True, null=True)),
                ('allowable_disposable_earnings', models.FloatField()),
                ('withholding_available', models.FloatField()),
                ('other_garnishment_amount', models.FloatField()),
                ('amount_left_for_arrears', models.FloatField()),
                ('allowed_amount_for_other_garnishment', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CalculationResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('result', models.FloatField()),
                ('net_pay', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=250)),
                ('employer_id', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee_Details',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('employer_id', models.IntegerField()),
                ('employee_name', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=255)),
                ('pay_cycle', models.CharField(max_length=255)),
                ('number_of_garnishment', models.IntegerField()),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Employer_Profile',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('employer_id', models.AutoField(primary_key=True, serialize=False)),
                ('employer_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('street_name', models.CharField(blank=True, max_length=255, null=True)),
                ('federal_employer_identification_number', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=10, null=True)),
                ('number_of_employees', models.IntegerField(blank=True, null=True)),
                ('department', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='federal_case_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('net_pay', models.FloatField()),
                ('result', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='federal_loan_case_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('employee_name', models.CharField(max_length=255)),
                ('earnings', models.FloatField()),
                ('garnishment_fees', models.FloatField()),
                ('pay_period', models.CharField(max_length=255)),
                ('filing_status', models.CharField(max_length=255)),
                ('no_of_exception', models.IntegerField()),
                ('federal_income_tax', models.FloatField()),
                ('local_tax', models.FloatField()),
                ('social_and_security', models.FloatField()),
                ('medicare_tax', models.FloatField()),
                ('state_tax', models.FloatField()),
                ('workers_compensation', models.FloatField()),
                ('medical_insurance', models.FloatField()),
                ('contribution', models.FloatField()),
                ('united_way_contribution', models.FloatField()),
                ('order_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='federal_tax_data_and_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('employee_name', models.CharField(max_length=255)),
                ('earnings', models.FloatField()),
                ('garnishment_fees', models.IntegerField()),
                ('pay_period', models.CharField(max_length=255)),
                ('filing_status', models.CharField(max_length=255)),
                ('no_of_exception', models.IntegerField()),
                ('fedral_income_tax', models.FloatField()),
                ('social_and_security', models.FloatField()),
                ('medicare_tax', models.FloatField()),
                ('state_tax', models.FloatField()),
                ('local_tax', models.FloatField()),
                ('workers_compensation', models.FloatField()),
                ('medical_insurance', models.FloatField()),
                ('contribution', models.FloatField()),
                ('united_way_contribution', models.FloatField()),
                ('total_tax', models.FloatField()),
                ('disposable_earnings', models.FloatField()),
                ('exempt_amount', models.FloatField()),
                ('amount_deduct', models.FloatField()),
                ('net_pay', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Garcalculation_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('employee_name', models.CharField(max_length=255)),
                ('garnishment_fees', models.FloatField()),
                ('earnings', models.FloatField()),
                ('support_second_family', models.BooleanField()),
                ('arrears_greater_than_12_weeks', models.BooleanField(blank=True, null=True)),
                ('amount_to_withhold_child1', models.FloatField(blank=True, null=True)),
                ('amount_to_withhold_child2', models.FloatField(blank=True, null=True)),
                ('amount_to_withhold_child3', models.FloatField(blank=True, null=True)),
                ('amount_to_withhold_child4', models.FloatField(blank=True, null=True)),
                ('amount_to_withhold_child5', models.FloatField(blank=True, null=True)),
                ('arrears_amt_Child1', models.FloatField(blank=True, null=True)),
                ('arrears_amt_Child2', models.FloatField(blank=True, null=True)),
                ('arrears_amt_Child3', models.FloatField(blank=True, null=True)),
                ('arrears_amt_Child4', models.FloatField(blank=True, null=True)),
                ('arrears_amt_Child5', models.FloatField(blank=True, null=True)),
                ('number_of_garnishment', models.IntegerField()),
                ('number_of_arrear', models.IntegerField()),
                ('order_id', models.IntegerField()),
                ('state', models.CharField(max_length=255)),
                ('federal_income_tax', models.FloatField()),
                ('social_tax', models.FloatField()),
                ('medicare_tax', models.FloatField()),
                ('state_tax', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='head_of_household',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_period', models.CharField(max_length=255)),
                ('exemptions_1', models.FloatField()),
                ('exemptions_2', models.FloatField()),
                ('exemptions_3', models.FloatField()),
                ('exemptions_4', models.FloatField()),
                ('exemptions_5', models.FloatField()),
                ('exemptions_6', models.FloatField()),
                ('morethan7', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='IWO_Details_PDF',
            fields=[
                ('IWO_ID', models.AutoField(primary_key=True, serialize=False)),
                ('employer_id', models.IntegerField(unique=True)),
                ('employee_id', models.IntegerField()),
                ('IWO_Status', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='IWOPDFFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_name', models.CharField(max_length=100)),
                ('pdf', models.FileField(upload_to='pdfs/')),
                ('employer_id', models.IntegerField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('employer_id', models.IntegerField(unique=True)),
                ('state', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('details', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('additional_info', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='married_filing_joint_return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_period', models.CharField(max_length=255)),
                ('exemptions_1', models.FloatField()),
                ('exemptions_2', models.FloatField()),
                ('exemptions_3', models.FloatField()),
                ('exemptions_4', models.FloatField()),
                ('exemptions_5', models.FloatField()),
                ('exemptions_6', models.FloatField()),
                ('morethan7', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='married_filing_sepearte_return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_period', models.CharField(max_length=255)),
                ('exemptions_1', models.FloatField()),
                ('exemptions_2', models.FloatField()),
                ('exemptions_3', models.FloatField()),
                ('exemptions_4', models.FloatField()),
                ('exemptions_5', models.FloatField()),
                ('exemptions_6', models.FloatField()),
                ('morethan7', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='multiple_student_loan_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('employee_name', models.CharField(max_length=255)),
                ('earnings', models.FloatField()),
                ('garnishment_fees', models.FloatField()),
                ('order_id', models.IntegerField()),
                ('federal_income_tax', models.FloatField()),
                ('social_and_security_tax', models.FloatField()),
                ('medicare_tax', models.FloatField()),
                ('state_tax', models.FloatField()),
                ('SDI_tax', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='multiple_student_loan_data_and_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('employee_name', models.CharField(max_length=255)),
                ('earnings', models.FloatField()),
                ('federal_income_tax', models.FloatField()),
                ('social_and_security_tax', models.FloatField()),
                ('medicare_tax', models.FloatField()),
                ('state_tax', models.FloatField()),
                ('SDI_tax', models.FloatField()),
                ('total_tax', models.FloatField()),
                ('garnishment_fees', models.FloatField()),
                ('disposable_earnings', models.FloatField()),
                ('allowable_disposable_earning', models.FloatField()),
                ('twentyfive_percent_of_earning', models.FloatField()),
                ('fmw', models.FloatField()),
                ('garnishment_amount', models.FloatField()),
                ('StudentLoanAmount1', models.FloatField()),
                ('StudentLoanAmount2', models.FloatField()),
                ('StudentLoanAmount3', models.FloatField()),
                ('net_pay', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='multiple_student_loan_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('net_pay', models.FloatField()),
                ('garnishment_amount', models.FloatField()),
                ('StudentLoanAmount1', models.FloatField()),
                ('StudentLoanAmount2', models.FloatField()),
                ('StudentLoanAmount3', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer_id', models.IntegerField()),
                ('modes', models.BooleanField()),
                ('visibilitys', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='single_filing_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_period', models.CharField(max_length=255)),
                ('exemptions_1', models.FloatField()),
                ('exemptions_2', models.FloatField()),
                ('exemptions_3', models.FloatField()),
                ('exemptions_4', models.FloatField()),
                ('exemptions_5', models.FloatField()),
                ('exemptions_6', models.FloatField()),
                ('morethan7', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='single_student_loan_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('employee_name', models.CharField(max_length=255)),
                ('earnings', models.FloatField()),
                ('garnishment_fees', models.IntegerField()),
                ('order_id', models.IntegerField()),
                ('federal_income_tax', models.FloatField()),
                ('social_and_security_tax', models.FloatField()),
                ('medicare_tax', models.FloatField()),
                ('state_tax', models.FloatField()),
                ('SDI_tax', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='single_student_loan_data_and_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('employee_name', models.CharField(max_length=255)),
                ('earnings', models.FloatField()),
                ('federal_income_tax', models.FloatField()),
                ('social_and_security_tax', models.FloatField()),
                ('medicare_tax', models.FloatField()),
                ('state_tax', models.FloatField()),
                ('SDI_tax', models.FloatField()),
                ('total_tax', models.FloatField()),
                ('garnishment_fees', models.FloatField()),
                ('disposable_earnings', models.FloatField()),
                ('allowable_disposable_earning', models.FloatField()),
                ('fifteen_percent_of_eraning', models.FloatField()),
                ('fmw', models.FloatField()),
                ('difference', models.FloatField()),
                ('garnishment_amount', models.FloatField()),
                ('net_pay', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='single_student_loan_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('net_pay', models.FloatField()),
                ('garnishment_amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tax_details',
            fields=[
                ('tax_id', models.AutoField(primary_key=True, serialize=False)),
                ('employer_id', models.IntegerField(unique=True)),
                ('fedral_income_tax', models.FloatField()),
                ('social_and_security', models.FloatField()),
                ('medicare_tax', models.FloatField()),
                ('state_tax', models.FloatField()),
                ('SDI_tax', models.FloatField()),
                ('mexico_tax', models.FloatField()),
                ('workers_compensation', models.FloatField()),
                ('medical_insurance', models.FloatField()),
                ('contribution', models.FloatField()),
                ('united_way_contribution', models.FloatField()),
            ],
        ),
    ]
