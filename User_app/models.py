# models.py
from django.contrib.auth.models import AbstractUser ,AbstractBaseUser ,BaseUserManager
from django.db import models



# # Employer_Profile details
# class Employer_Profile(AbstractBaseUser):
#     employer_id = models.CharField(max_length=100,primary_key=True)
#     company_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     registered_address = models.CharField(max_length=100, unique=True)
#     zipcode = models.CharField(max_length=10, null=True, blank=True)
#     ein = models.IntegerField()
#     bank_name = models.CharField(max_length=255, null=True, blank=True)
#     bank_account_number = models.CharField(max_length=255, null=True, blank=True)
#     location = models.CharField(max_length=255, null=True, blank=True)


#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'employer_name']

#     def __str__(self):
#         return self.username

class Employer_Profile(AbstractBaseUser):
    employer_id = models.AutoField(primary_key=True)
    cid=models.CharField(max_length=100,default="ABS")
    employer_name = models.CharField(max_length=100,default="ABS")
    email = models.EmailField(unique=True,default="rtt@gmail.com")
    username = models.CharField(max_length=100, unique=True,default="USN")
    street_name = models.CharField(max_length=255, null=True, blank=True)
    federal_employer_identification_number = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    number_of_employees = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'employer_name']

    def __str__(self):
        return self.username

class peo_table(AbstractBaseUser):
    peo_id= models.AutoField(primary_key=True)
    peo_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    password1=models.CharField(max_length=255)
    password2=models.CharField(max_length=255)

    
class Calculation_data_results(models.Model):
    employee_id=models.CharField(max_length=255)
    cid=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    support_second_family=models.BooleanField()
    disposable_income =models.FloatField()
    garnishment_fees=models.FloatField()
    arrears_greater_than_12_weeks=models.BooleanField()
    amount_to_withhold_child1=models.FloatField(null=True, blank=True)
    amount_to_withhold_child2 =models.FloatField(null=True, blank=True)
    amount_to_withhold_child3=models.FloatField(null=True, blank=True)
    amount_to_withhold_child4=models.FloatField(null=True, blank=True)
    amount_to_withhold_child5=models.FloatField(null=True, blank=True)
    arrears_amt_Child1=models.FloatField(null=True, blank=True)
    arrears_amt_Child2 =models.FloatField(null=True, blank=True)
    arrears_amt_Child3 =models.FloatField(null=True, blank=True)
    arrears_amt_Child4 =models.FloatField(null=True, blank=True)
    arrears_amt_Child5 =models.FloatField(null=True, blank=True)
    number_of_arrear= models.IntegerField(null=True, blank=True)
    number_of_child_support_order=models.IntegerField()
    allowable_disposable_earnings=models.FloatField()
    withholding_available=models.FloatField()
    other_garnishment_amount=models.FloatField()
    amount_left_for_arrears=models.FloatField()
    allowed_amount_for_other_garnishment=models.FloatField()


class Employee_Detail(models.Model):
    ee_id = models.CharField(max_length=255)
    cid=models.CharField(max_length=255)
    age = models.IntegerField()
    social_security_number = models.CharField(max_length=255)
    is_blind = models.BooleanField(null=True, blank=True)
    home_state=models.CharField(max_length=255)
    work_state=models.CharField(max_length=255)
    gender=models.CharField(max_length=255,null=True, blank=True)
    pay_period = models.CharField(max_length=255)
    number_of_exemptions = models.IntegerField()
    filing_status = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=255)
    number_of_student_default_loan = models.IntegerField()
    support_second_family = models.BooleanField()
    spouse_age = models.IntegerField(null=True, blank=True)
    is_spouse_blind = models.BooleanField(null=True, blank=True)


    
# # Employer_Profile details
# class Employer_Profile(models.Model):
#     employer_id = models.AutoField(primary_key=True)
#     employer_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=100, unique=True)
#     street_name = models.CharField(max_length=255, null=True, blank=True)
#     federal_employer_identification_number = models.CharField(max_length=255, null=True, blank=True)
#     city = models.CharField(max_length=255, null=True, blank=True)
#     state = models.CharField(max_length=255, null=True, blank=True)
#     country = models.CharField(max_length=255, null=True, blank=True)
#     zipcode = models.CharField(max_length=10, null=True, blank=True)
#     number_of_employees = models.IntegerField(null=True, blank=True)
#     department = models.CharField(max_length=255, null=True, blank=True)
#     location = models.CharField(max_length=255, null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'employer_name']

    def __str__(self):
        return self.username
class Tax_details(models.Model):
    tax_id = models.AutoField(primary_key=True)
    employer_id=models.IntegerField(unique=True)
    fedral_income_tax =models.FloatField()
    social_and_security =models.FloatField()
    medicare_tax= models.FloatField()
    state_tax =models.FloatField()
    SDI_tax=models.FloatField()
    mexico_tax=models.FloatField()
    workers_compensation=models.FloatField()
    medical_insurance=models.FloatField()
    contribution=models.FloatField()
    united_way_contribution=models.FloatField()


class IWOPDFFile(models.Model):
    pdf_name = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='pdfs/')
    employer_id=models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
 
 
class IWO_Details_PDF(models.Model):
    IWO_ID = models.AutoField(primary_key=True)
    employer_id=models.IntegerField(unique=True)
    employee_id=models.IntegerField()
    IWO_Status =models.CharField(max_length=250)


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name=models.CharField(max_length=250)
    employer_id=models.IntegerField(unique=True)

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    employer_id=models.IntegerField(unique=True)
    state=models.CharField(max_length=250)
    city=models.CharField(max_length=250)
    # street=models.CharField(max_length=250)

class Garcalculation_data(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    batch_id=models.CharField(max_length=255)
    employee_name=models.CharField(max_length=255)
    garnishment_fees = models.FloatField()
    pay_period = models.CharField(max_length=255)
    support_second_family = models.BooleanField()
    arrears_greater_than_12_weeks = models.BooleanField(null=True, blank=True)
    amount_to_withhold_child1=models.FloatField(null=True, blank=True)
    amount_to_withhold_child2 =models.FloatField(null=True, blank=True)
    amount_to_withhold_child3=models.FloatField( null=True, blank=True)
    amount_to_withhold_child4=models.FloatField(null=True, blank=True )
    amount_to_withhold_child5=models.FloatField( null=True, blank=True)
    arrears_amt_Child1=models.FloatField(null=True, blank=True)
    arrears_amt_Child2 =models.FloatField(null=True, blank=True)
    arrears_amt_Child3 =models.FloatField(null=True, blank=True)
    arrears_amt_Child4 =models.FloatField(null=True, blank=True)
    arrears_amt_Child5 =models.FloatField(null=True, blank=True)
    number_of_child_support_order= models.IntegerField()
    number_of_arrear= models.IntegerField()
    order_id=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    gross_pay =models.FloatField()
    mandatory_deductions=models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class CalculationResult(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    batch_id=models.CharField(max_length=255)
    result = models.FloatField()  
    net_pay = models.FloatField()
    amount_to_withhold_child1=models.FloatField(null=True, blank=True)
    amount_to_withhold_child2 =models.FloatField(null=True, blank=True)
    amount_to_withhold_child3=models.FloatField( null=True, blank=True)
    amount_to_withhold_child4=models.FloatField(null=True, blank=True )
    amount_to_withhold_child5=models.FloatField( null=True, blank=True)
    arrears_amt_Child1=models.FloatField(null=True, blank=True)
    arrears_amt_Child2 =models.FloatField(null=True, blank=True)
    arrears_amt_Child3 =models.FloatField(null=True, blank=True)
    arrears_amt_Child4 =models.FloatField(null=True, blank=True)
    arrears_amt_Child5 =models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class LogEntry(models.Model):
    action = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.timestamp} - {self.user} - {self.action}'
    
class application_activity(models.Model):
    action = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class single_student_loan_result(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    net_pay = models.FloatField()  
    garnishment_amount= models.FloatField()
    batch_id=models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class multiple_student_loan_result(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    net_pay = models.FloatField()  
    garnishment_amount= models.FloatField()
    batch_id=models.CharField(max_length=255)
    StudentLoanAmount1= models.FloatField()
    StudentLoanAmount2= models.FloatField()
    StudentLoanAmount3= models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class single_student_loan_data(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    employee_name=models.CharField(max_length=255)
    garnishment_fees= models.IntegerField()
    order_id=models.CharField(max_length=255)
    batch_id=models.CharField(max_length=255)
    disposable_income =models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class multiple_student_loan_data(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    employee_name=models.CharField(max_length=255)
    garnishment_fees= models.FloatField()
    order_id=models.CharField(max_length=255)
    batch_id=models.CharField(max_length=255,null=True, blank=True)
    disposable_income =models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class multiple_student_loan_data_and_result(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    employee_name=models.CharField(max_length=255)
    garnishment_fees= models.FloatField()
    batch_id=models.CharField(max_length=255)
    disposable_income= models.FloatField()
    allowable_disposable_earning= models.FloatField()
    twentyfive_percent_of_earning= models.FloatField()
    fmw= models.FloatField()
    garnishment_amount= models.FloatField()
    StudentLoanAmount1= models.FloatField()
    StudentLoanAmount2= models.FloatField()
    StudentLoanAmount3= models.FloatField()
    net_pay= models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class single_student_loan_data_and_result(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    employee_name=models.CharField(max_length=255)
    batch_id=models.CharField(max_length=255)    
    garnishment_fees= models.FloatField()
    disposable_income= models.FloatField()
    allowable_disposable_earning= models.FloatField()
    fifteen_percent_of_eraning= models.FloatField()
    fmw= models.FloatField()
    difference=models.FloatField()
    garnishment_amount= models.FloatField()
    net_pay= models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class federal_loan_case_data(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    employee_name=models.CharField(max_length=255)
    batch_id=models.CharField(max_length=255)
    disposable_income =models.FloatField()
    garnishment_fees= models.FloatField()
    pay_period = models.CharField(max_length=255)
    filing_status = models.CharField(max_length=255)
    no_of_exception = models.IntegerField()
    order_id=models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class federal_tax_data_and_result(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    batch_id=models.CharField(max_length=255)
    employee_name=models.CharField(max_length=255)
    garnishment_fees= models.IntegerField()
    pay_period = models.CharField(max_length=255)
    filing_status = models.CharField(max_length=255)
    no_of_exception = models.IntegerField()
    disposable_income=models.FloatField()
    exempt_amount=models.FloatField()
    amount_deduct=models.FloatField()
    net_pay=models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class setting(models.Model):
    employer_id=models.IntegerField()
    modes=models.BooleanField()
    visibilitys=models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

class APICallLog(models.Model):
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.path} - {self.method} - {self.timestamp}'

class State_tax_data(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    employee_name=models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    gross_income = models.FloatField()  
    garnishment_fees= models.FloatField()
    disposable_income =models.FloatField()
    debt=models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


# class APICallLog(models.Model):
#     endpoint = models.CharField(max_length=255)
#     date = models.DateField(auto_now_add=True)
#     count = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f'{self.endpoint} - {self.date} - {self.count}'

class state_tax_result(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    disposable_income=models.FloatField()
    monthly_garnishment_amount=models.FloatField()
    net_pay = models.FloatField()  
    gross_income = models.FloatField()
    duration_of_levies= models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)



class multiple_garnishment_data(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    batch_id=models.CharField(max_length=255,null=True, blank=True)
    employee_name = models.CharField(max_length=255)
    garnishment_fees = models.FloatField()
    support_second_family = models.BooleanField()
    arrears_greater_than_12_weeks = models.BooleanField(null=True, blank=True)
    amount_to_withhold_child1 = models.FloatField(null=True, blank=True)
    amount_to_withhold_child2 = models.FloatField(null=True, blank=True)
    amount_to_withhold_child3 = models.FloatField(null=True, blank=True)
    amount_to_withhold_child4 = models.FloatField(null=True, blank=True)
    amount_to_withhold_child5 = models.FloatField(null=True, blank=True)
    arrears_amt_Child1 = models.FloatField(null=True, blank=True)
    arrears_amt_Child2 = models.FloatField(null=True, blank=True)
    arrears_amt_Child3 = models.FloatField(null=True, blank=True)
    arrears_amt_Child4 = models.FloatField(null=True, blank=True)
    arrears_amt_Child5 = models.FloatField(null=True, blank=True)
    number_of_child_support_order = models.IntegerField()
    number_of_arrear = models.IntegerField()
    order_id = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    disposable_income = models.FloatField()
    pay_period = models.CharField(max_length=255)
    filing_status = models.CharField(max_length=255)
    no_of_exception = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Adding garnishment_order field as a JSONField
    garnishment_order = models.JSONField(default=list)

    def __str__(self):
        return f"Garnishment Data for Employee: {self.employee_name}, Order ID: {self.order_id}"
    

class multiple_garnishment_case_result(models.Model):
    employee_id = models.CharField(max_length=255)
    employer_id = models.CharField(max_length=255)
    batch_id=models.CharField(max_length=255,null=True, blank=True)
    garnishment_priority_order= models.CharField(max_length=255)
    garnishment_amount= models.FloatField()
    net_pay = models.FloatField()  
    timestamp = models.DateTimeField(auto_now_add=True)




class company_details(models.Model):
    cid= models.CharField(max_length=255) 
    ein = models.IntegerField() 
    company_name = models.CharField(max_length=255)
    registered_address= models.CharField(max_length=255, null=True, blank=True)
    zipcode= models.IntegerField()
    state= models.CharField(max_length=255)
    dba_name= models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    bank_account_number = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

#garnishment_order_table
# class garnishment_order(models.Model):
#     garid= models.CharField(max_length=255)
#     cid = models.IntegerField()
#     eeid= models.IntegerField()
#     case_id= models.CharField(max_length=255, null=True, blank=True)
#     state= models.CharField(max_length=255)
#     type= models.CharField(max_length=255)
#     sdu= models.CharField(max_length=255, null=True, blank=True)
#     start_date= models.DateField(max_length=255, null=True, blank=True)
#     end_date= models.DateField(max_length=255, null=True, blank=True)
#     amount= models.DecimalField()
#     arrear_greater_than_12_weeks= models.BooleanField(default=False, blank=False)
#     arrear_amount= models.DecimalField()

# class payroll

# class payroll(models.Model):
#     cid= models.CharField(max_length=255)
#     eeid= models.CharField(max_length=255)
#     payroll_date=models.DateField()
#     pay_date= models.DateField()
#     gross_pay=models.DecimalField()
#     net_pay=models.DecimalField()
#     taxes_federal_income_tax=models.DecimalField()
#     taxes_state_tax=models.DecimalField()
#     taxes_local_tax=models.DecimalField()
#     taxes_medicare_tax=models.DecimalField()
#     taxes_sdi=models.DecimalField()
#     deductions=models.DecimalField()
#     type=models.CharField(max_length=255)
#     amount=models.DecimalField()


