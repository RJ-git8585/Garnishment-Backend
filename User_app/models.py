# models.py
from django.contrib.auth.models import AbstractUser ,AbstractBaseUser ,BaseUserManager
from django.db import models



# Employer_Profile details
class Employer_Profile(AbstractBaseUser):
    employer_id = models.AutoField(primary_key=True)
    employer_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
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
    

class Calculation_data_results(models.Model):
    employee_id=models.IntegerField()
    employer_id=models.IntegerField()
    fedral_income_tax=models.FloatField()
    social_and_security=models.FloatField()
    medicare_tax=models.FloatField()
    state=models.CharField(max_length=255)
    state_taxes=models.FloatField()
    earnings= models.FloatField()
    support_second_family=models.BooleanField()
    garnishment_fees=models.FloatField()
    arrears_greater_than_12_weeks=models.BooleanField()
    amount_to_withhold_child1=models.FloatField()
    amount_to_withhold_child2 =models.FloatField()
    amount_to_withhold_child3=models.FloatField()
    arrears_amt_Child1=models.FloatField()
    arrears_amt_Child2 =models.FloatField()
    arrears_amt_Child3 =models.FloatField()
    number_of_arrears= models.IntegerField()
    allowable_disposable_earnings=models.FloatField()
    withholding_available=models.FloatField()
    other_garnishment_amount=models.FloatField()
    amount_left_for_arrears=models.FloatField()
    allowed_amount_for_other_garnishment=models.FloatField()

class Employee_Details(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employer_id = models.IntegerField()
    employee_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    pay_cycle = models.CharField(max_length=255)
    number_of_garnishment = models.IntegerField()
    location = models.CharField(max_length=255)
    def __str__(self):
        return self.employee_name
  
class Tax_details(models.Model):
    tax_id = models.AutoField(primary_key=True)
    employer_id=models.IntegerField(unique=True)
    fedral_income_tax =models.FloatField()
    social_and_security =models.FloatField()
    medicare_tax= models.FloatField()
    state_tax =models.FloatField()
    SDI_tax=models.FloatField()


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
    employee_id = models.IntegerField()
    employer_id = models.IntegerField()
    employee_name=models.CharField(max_length=255)
    garnishment_fees = models.FloatField()
    minimum_wages = models.FloatField()
    earnings = models.FloatField()
    support_second_family = models.BooleanField()
    arrears_greater_than_12_weeks = models.BooleanField()
    amount_to_withhold_child1=models.FloatField()
    amount_to_withhold_child2 =models.FloatField()
    amount_to_withhold_child3=models.FloatField()
    arrears_amt_Child1=models.FloatField()
    arrears_amt_Child2 =models.FloatField()
    arrears_amt_Child3 =models.FloatField()
    number_of_arrears= models.IntegerField()
    order_id=models.IntegerField()
    state=models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class CalculationResult(models.Model):
    employee_id = models.IntegerField()
    employer_id = models.IntegerField()
    result = models.FloatField()  
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
    employee_id = models.IntegerField()
    employer_id = models.IntegerField()
    net_pay = models.FloatField()  
    garnishment_amount= models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class multiple_student_loan_result(models.Model):
    employee_id = models.IntegerField()
    employer_id = models.IntegerField()
    net_pay = models.FloatField()  
    garnishment_amount= models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class student_loan_data(models.Model):
    employee_id = models.IntegerField()
    employer_id = models.IntegerField()
    earnings = models.FloatField()  
    garnishment_fees= models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

