from User_app.models import *
from django.contrib.auth import  login as auth_login ,get_user_model
from User_app.serializers import *
import json
import os
from auth_project import settings
import re



class federal_tax_calculation():
    """ Calculate Federal Tax based on the given filing status and number of exceptions """

    def get_file_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def get_total_exemption_self(self, request):
      age = request.get('age')
        
      is_blind = request.get('is_blind')
      number_of_exemption = 0

      if (age>=65 and is_blind==True) :
          number_of_exemption=2
      elif (age<65 and is_blind==True) :
          number_of_exemption=1
      elif(age>=65 and is_blind==False) :
          number_of_exemption=1
      return number_of_exemption

    def get_total_exemption_dependent(self, request):  

      is_spouse_blind= request.get('is_spouse_blind')
      spouse_age = request.get('spouse_age')
      number_of_exemption = 0
      if (spouse_age>=65 and is_spouse_blind==True) :
          number_of_exemption=2
      elif (spouse_age<65 and is_spouse_blind==True):
          number_of_exemption=1
      elif(spouse_age>=65 and is_spouse_blind==False):
          number_of_exemption=1
      return number_of_exemption  




    def get_additional_exempt_for_self(self, record):
        pay_period=record.get('pay_period').lower()
        filing_status=record.get('filing_status')

        no_of_exemption=self.get_total_exemption_self(record)

        file_path=os.path.join(settings.BASE_DIR, 'User_app', 'configuration files/federal tables/additional_exempt_amount.json')
        result = 0
        with open(file_path, 'r') as file:
            data = json.load(file)


        data = data["additional_exempt_amt"]
        no_of_exemption_list=[]
        for item in data:
          if item.get("no_of_exemption") == no_of_exemption:
            no_of_exemption_list.append(item)
        single_filing_status_list=[]
        head_of_household_list=[]
        any_other_filing_status=[]
        for item in no_of_exemption_list:
          if "single_filing_status" == item.get("filing_status"):
            single_filing_status_list.append(item)
          elif "head_of_household" == item.get("filing_status"):
             head_of_household_list.append(item)
          else:
              any_other_filing_status.append(item)
        # print("single_filing_status_list",single_filing_status_list)
        # print("head_of_household_list",head_of_household_list)
        # print("any_other_filing_status",any_other_filing_status)
        # print("filing_status",filing_status)
        if filing_status == "single_filing_status":
          result = single_filing_status_list[0].get(pay_period)

        elif filing_status == "head_of_household":
          result = head_of_household_list[0].get(pay_period)

        else:
          result = any_other_filing_status[0].get(pay_period)
        return result



    def get_additional_exempt_for_dependent(self, record):
        pay_period=record.get('pay_period').lower()
        filing_status=record.get('filing_status')
        no_of_exemption=self.get_total_exemption_dependent(record)
        file_path=os.path.join(settings.BASE_DIR, 'User_app', 'configuration files/federal tables/additional_exempt_amount.json')

        result = 0
        with open(file_path, 'r') as file:
            data = json.load(file)


        data = data["additional_exempt_amt"]
        no_of_exemption_list=[]
        for item in data:
          if item.get("no_of_exemption") ==no_of_exemption:
            no_of_exemption_list.append(item)
        single_filing_status_list=[]
        head_of_household_list=[]
        any_other_filing_status=[]
        for item in no_of_exemption_list:
          if "single_filing_status" == item.get("filing_status"):
            single_filing_status_list.append(item)
          elif "head_of_household" == item.get("filing_status"):
             head_of_household_list.append(item)
          else:
              any_other_filing_status.append(item)

        if filing_status == "single_filing_status":
          result = single_filing_status_list[0].get(pay_period)

        elif filing_status == "head_of_household":
          result = head_of_household_list[0].get(pay_period)

        else:
          result = any_other_filing_status[0].get(pay_period)
        return result


    def get_standard_exempt_amt(self, record):

        filing_status=record.get('filing_status')
        no_of_exemption_for_self=record.get('no_of_exemption_for_self')
        pay_period=record.get('pay_period')


        # Check if the number of exceptions is greater than 5
        exempt= 6 if no_of_exemption_for_self >5 else no_of_exemption_for_self

        file_path=os.path.join(settings.BASE_DIR, 'User_app', f'configuration files/federal tables/{filing_status}.json')

        data = self.get_file_data(file_path)
        status_data = data.get(filing_status, [])


        # Accessing federal tax data
        if no_of_exemption_for_self <=5:
            semimonthly_data = next((item for item in status_data if item["Pay Period"].lower() == pay_period.lower()), None)
            exempt_amount = semimonthly_data.get(str(exempt))
        elif no_of_exemption_for_self >5:
            semimonthly_data = next((item for item in status_data if item["Pay Period"].lower() == pay_period.lower()), None)
            # print("semimonthly_data",semimonthly_data)
            exemp_amt = semimonthly_data.get(str(exempt))
            # print("exemp_amt",exemp_amt)
            exempt_amount  = re.findall(r'\d+\.?\d*',exemp_amt)
            exempt1=float(exempt_amount[0])
            exempt2=float(exempt_amount[1])
            exempt_amount=round((exempt1+(exempt2*no_of_exemption_for_self)),2)
            # print("Single exempt_amount",exempt_amount)
        return exempt_amount


class federal_tax(federal_tax_calculation):

    def calculate(self, record):

        net_pay = record.get('net_pay')
        is_blind=record.get('is_blind')
        is_spouse_blind=record.get('is_spouse_blind')
        age=record.get('age')
        spouse_age=record.get('spouse_age')

        #Calculate Standard exempt
        standard_exempt_amt=self.get_standard_exempt_amt(record)
        # print("standaerd_exmpt_amt",standard_exempt_amt)


        # Initialize exempt_amount_self and exempt_amount_dependent to 0 
        exempt_amount_self = 0  
        exempt_amount_dependent = 0

        if (age>=65 and is_blind==True) or (age<65 and is_blind==True) or(age>=65 and is_blind==False): 
            exempt_amount_self = self.get_additional_exempt_for_self(record)
            # print("exempt_amount_self", exempt_amount_self)
        if (spouse_age>=65 and is_spouse_blind==True) or (spouse_age<65 and is_spouse_blind==True) or (spouse_age>=65 and is_spouse_blind==False):
            exempt_amount_dependent = self.get_additional_exempt_for_dependent(record)

            # print("dependent_exempt_amt", exempt_amount_dependent)
        

        # Calculate the amount to deduct
        total_exempt_amt=standard_exempt_amt+exempt_amount_self+exempt_amount_dependent
        # print("total_exempt_amt",total_exempt_amt)

        amount_deduct = round((net_pay-total_exempt_amt), 2)
        # print("amount_deduct",amount_deduct)

        amount_deduct = amount_deduct if amount_deduct > 0 else 0
        return (round(amount_deduct,2))








# record =    {
#           "ee_id": "EE005114",
#           "gross_pay": 1000,
#           "state": "Texas",
#           "no_of_exemption_for_self": 1,
#           "pay_period": "Weekly",
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
#           "support_second_family": "Yes",
#           "no_of_student_default_loan": 1,
#           "arrears_greater_than_12_weeks": "No",
#           "garnishment_data": [
#             {
#               "type": "student default loan",
#               "data": [
#                 {
#                   "case_id": "C13278",
#                   "amount": 128.82,
#                   "arrear": 0
#                 }
#               ]
#             }
#           ]
#         }





# print("amt",federal_tax().calculate(record))
