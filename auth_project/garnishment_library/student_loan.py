from requests import Response
from User_app.models import *
from User_app.serializers import *
from auth_project.garnishment_library.child_support import ChildSupport
import os
import json 
from django.conf import settings
import json
from rest_framework import status
class StudentLoan():
    """ Calculate Student Loan garnishment amount based on the provided data."""


    def calculate_disposable_earnings(self,record):
        """
        Calculate Disposable Earnings (DE) based on state and rules.
        """
        # Define file paths
        de_rules_file = os.path.join(settings.BASE_DIR, 'User_app', 'configuration files/child support tables/disposable earning rules.json')
        ccpa_rules_file = os.path.join(settings.BASE_DIR, 'User_app', 'configuration files/child support tables/ccpa_rules.json')
    
        def _load_json_file(file_path):
            """Helper function to load a JSON file."""
            try:
                with open(file_path, 'r') as file:
                    return json.load(file)
            except FileNotFoundError:
                raise Exception(f"File not found: {file_path}")
            except json.JSONDecodeError:
                raise Exception(f"Invalid JSON format in file: {file_path}")
    
        # Extract values from the record
        state = record.get("state")
        gross_pay = record.get("gross_pay")
        payroll_taxes = record.get("payroll_taxes")
    
        if not state:
            raise ValueError("State information is missing in the record.")
        if gross_pay is None or payroll_taxes is None:
            raise ValueError("Record must include 'gross_pay', 'state', and 'taxes' fields.")
    
        # Load DE rules
        de_data = _load_json_file(de_rules_file)
        de_rules = de_data.get("de", [])
        de_rule = None
    
        # Find matching state in DE rules
        for rule in de_rules:
            if rule['State'] == state:
                de_rule = rule['Disposable Earnings']
                break
        if de_rule is None:
            raise ValueError(f"No DE rule found for state: {state}")
    
        # Load CCPA rules
        ccpa_data = _load_json_file(ccpa_rules_file)
        ccpa_rules = ccpa_data.get("CCPA_Rules", {})
    
        # Calculate mandatory deductions
        mandatory_deductions = 0
        if de_rule.lower() == "ccpa":
            mandatory_tax_keys = ccpa_rules.get("Mandatory_deductions", [])
            tax_amt = [tax.get(k, 0) for tax in payroll_taxes for k in mandatory_tax_keys if k in tax]
            mandatory_deductions = sum(tax_amt)

    
        # Calculate and return disposable earnings
        return gross_pay - mandatory_deductions
    

    
    def get_fmw(self,record):
      pay_period=record.get("pay_period")
      if pay_period.lower()=="weekly":
        return 7.25*30
      elif pay_period.lower()=="biweekly" or pay_period.lower()=="bi-weekly":
        return 7.25*60
      elif pay_period.lower()=="semimonthly" or pay_period.lower()=="semi-monthly":
        return 7.25*65
      elif pay_period.lower()=="monthly":
        return 7.25*130

    def get_single_student_amount(self, record):
        # Calculate disposable earnings
        disposable_earning = self.calculate_disposable_earnings(record)

        # Calculate percentages earnings
        fifteen_percent_of_earning = disposable_earning *.15
        twentyfive_percent_of_earning =disposable_earning*.25

        fmw =self.get_fmw(record)
        difference_of_de_and_fmw=disposable_earning-fmw
        
        if  fmw>=disposable_earning:
            loan_amt = "Student loan withholding cannot be applied because Disposable Earnings are less than or equal to $217.5, the exempt amount."
        elif fmw<disposable_earning:
            loan_amt=min(fifteen_percent_of_earning,twentyfive_percent_of_earning,difference_of_de_and_fmw)
        elif difference_of_de_and_fmw<0:
            loan_amt = 0
        
        if isinstance(loan_amt, (float,int)):
            loan_amt=round(loan_amt,2)
        else:
            loan_amt=loan_amt
        

        return ({"student_loan_amt":loan_amt})
    

    def get_multiple_student_amount(self, record):

        fmw = self.get_fmw(record)
        disposable_earning = self.calculate_disposable_earnings(record)

        difference_of_de_and_fmw = disposable_earning - fmw


        if fmw >= disposable_earning:
            student_loan_amt1 = "Student loan withholding cannot be applied because Disposable Earnings are less than or equal to $217.5, the exempt amount."
            student_loan_amt2 = "Student loan withholding cannot be applied because Disposable Earnings are less than or equal to $217.5, the exempt amount."
        elif difference_of_de_and_fmw < 0:
            student_loan_amt1 = 0
            student_loan_amt2 = 0
        elif disposable_earning > fmw:
            student_loan_amt1 = .15* disposable_earning
            student_loan_amt2 = .10* disposable_earning

        return ({"student_loan_amt1": round(student_loan_amt1,2), "student_loan_amt2": round(student_loan_amt2,2)})
    
class student_loan_calculate():
        
    def calculate(self, record):
        try:
            no_of_student_default_loan=record.get("no_of_student_default_loan")
            if no_of_student_default_loan==1:
                student_loan_amt=StudentLoan().get_single_student_amount(record)
            elif no_of_student_default_loan>1:
                student_loan_amt=StudentLoan().get_multiple_student_amount(record)
            return student_loan_amt
        except Exception as e:
            return Response(
                {"error": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,"ee_id":record.get("ee_id")}
            )



# record=        {
#           "ee_id": "EE005114",
#           "gross_pay": 1000,
#           "state": "Alabama",
#           "pay_period": "Weekly",
#           "no_of_exception_for_self": 1,
#           "filing_status": "single_filing_status",
#           "net_pay": 858.8,
#           "payroll_taxes": [
#             {
#               "federal_income_tax": 80
#             },
#             {
#               "social_security_tax": 49.6
#             },
#             {
#               "medicare_tax": 11.6
#             },
#             {
#               "state_tax": 0
#             },
#             {
#               "local_tax": 0
#             }
#           ],
#           "payroll_deductions": {
#             "medical_insurance": 0
#           },
#           "age": 50,
#           "is_blind": True,
#           "is_spouse_blind": True,
#           "spouse_age": 39,
#           "support_second_family": True,
#           "arrears_greater_than_12_weeks": 0,
#           "garnishment_data": [
#             {
#               "type": "student default loan",
#               "data": [
#                 {
#                   "amount": 200,
#                   "arrear": 0,
#                   "case_id": "C13278"
#                 }
#               ]
#             }
#           ]
#         }

# # # print("get_percentages:",StudentLoan().get_percentage)
# # print("get_single_student_amount",StudentLoan().get_single_student_amount(record))
# # print("get_multiple_student_amount",StudentLoan().get_multiple_student_amount(record))
# print("student_loan",student_loan_calculate().calculate( record ))
