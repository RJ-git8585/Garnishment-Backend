import json
import os
from django.contrib.staticfiles import finders
from django.conf import settings 

class DisposableIncomeCalculator:
    def __init__(self, x=0.25):
        self.x = x

    def calculate(self, gross_income):
        disposable_earnings = round(gross_income, 2)
        monthly_garnishment_amount = disposable_earnings * self.x
        return monthly_garnishment_amount

class AllocationMethodIdentifiers:
    def __init__(self, state):
        self.state = state.lower()  

    def get_allocation_method(self):

        file_path = os.path.join(settings.BASE_DIR, 'User_app', 'configuration files/child support tables/withholding_rules.json')


        # Reading the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Accessing child support data
        child_support_data = data.get("WithholdingRules", [])
        
        # Searching for the matching state
        for record in child_support_data:
            if record['State'].lower() == self.state:
                return record['AllocationMethod'].lower()
        
        # If no matching record is found
        return f"No allocation method found for the state: {self.state.capitalize()}."
    


class CalculateAmountToWithhold:
    def __init__(self, allowed_amount_for_garnishment, amount_to_withhold,allocation_method_for_garnishment,number_of_child_support_order):
        self.allowed_amount_for_garnishment = allowed_amount_for_garnishment
        self.amount_to_withhold = amount_to_withhold
        self.allocation_method_for_garnishment = allocation_method_for_garnishment
        self.number_of_child_support_order = number_of_child_support_order

    def calculate(self, amount_to_withhold_child):
        if (self.allowed_amount_for_garnishment - self.amount_to_withhold) >= 0:
            return amount_to_withhold_child
        elif self.allocation_method_for_garnishment == "Prorate":
            ratio = amount_to_withhold_child / self.amount_to_withhold
            return self.allowed_amount_for_garnishment * ratio
        elif amount_to_withhold_child > 0:
            return self.allowed_amount_for_garnishment / self.number_of_child_support_order
        else:
            return 0


class CalculateArrearAmountForChild:
    def __init__(self, amount_left_for_arrears, allowed_child_support_arrear,allocation_method_for_arrears,number_of_arrear):
        self.amount_left_for_arrears = amount_left_for_arrears
        self.allowed_child_support_arrear = allowed_child_support_arrear
        self.allocation_method_for_arrears = allocation_method_for_arrears
        self.number_of_arrear = number_of_arrear

    def calculate(self, arrears_amt_Child):
        if (self.amount_left_for_arrears - self.allowed_child_support_arrear) >= 0:
            return arrears_amt_Child
        elif self.allocation_method_for_arrears == "Prorate":
            ratio = arrears_amt_Child / self.allowed_child_support_arrear
            return self.amount_left_for_arrears * ratio
        elif self.amount_left_for_arrears > 0:
            return self.amount_left_for_arrears / self.number_of_arrear
        else:
            return 0        

class WLIdentifier:
    def get_state_rules(self, state):
        file_path = os.path.join(settings.BASE_DIR, 'User_app', 'configuration files/child support tables/withholding_rules.json')

        # Reading the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Accessing child support data
        ccpa_rules_data = data.get("WithholdingRules", [])
        
        # Searching for the matching state
        for record in ccpa_rules_data:
            if record['State'].lower() == state.lower():
                return record['Rule']  

        # If no matching record is found
        return f"No allocation method found for the state: {state.capitalize()}." 

    def find_wl_value(self, de,state, employee_id, supports_2nd_family, arrears_of_more_than_12_weeks, de_gt_145, order_gt_one):
        file_path = os.path.join(settings.BASE_DIR, 'User_app', 'configuration files/child support tables/withholding_limits.json')
        state_rule = self.get_state_rules(state)

        # Reading the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Accessing child support data
        ccpa_limits_data = data.get("Rules", [])
        for rule in ccpa_limits_data:
            if rule["Rule"] == state_rule:
                for detail in rule["Details"]:
                    if ((detail["Supports_2nd_family"] == "" and detail["Arrears_of_more_than_12_weeks"] == "") or
                        (detail["Supports_2nd_family"] == supports_2nd_family and
                         detail["Arrears_of_more_than_12_weeks"] == arrears_of_more_than_12_weeks and
                         detail["de_gt_145"] == de_gt_145 and
                         detail["order_gt_one"] == order_gt_one)):
                        result = int(detail["WL"].replace("%", "")) / 100
                        return result
        
        return f"No matching WL found for this employee: {employee_id}"


# class ChangeResultStructure:
#     def __init__(self,result,case_id,garnishment_type):
#         self.result=result
#         self.case_id=case_id
#         self.garnishment_type=garnishment_type
#         pass
#     def structurechange(self):
#         garnishment={}
#         if len(self.result)>1:
#             for i in range(len(self.result)):
#                 garnishment[f"withholding_amt_SL{i+1}"] =self.result[i]
            



#             garnishment
