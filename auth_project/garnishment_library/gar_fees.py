from User_app.models import *
from User_app.serializers import *

class gar_fees_rules_engine():
    def __init__(self):
        
        # Mapping rule names to their corresponding methods
        self.rule_map = {f'Rule_{i}': getattr(self, f'Rule_{i}') for i in range(1, 3)}
    
    def get_serialized_data(self):
        data = garnishment_fees.objects.all()
        serializer = garnishment_fees_serializer(data, many=True)
        return serializer.data


    def find_rule(self,record):
        state=record.get("state").lower()
        gar_type = record.get("garnishment_data")[0]
        type=gar_type.get('type').lower()
        pay_period=record.get('pay_period').lower()
        data = garnishment_fees.objects.all()
        serializer = garnishment_fees_serializer(data, many=True)

        for item in serializer.data:
            if (item["state"].strip().lower() == state.strip().lower() and
                item["pay_period"].strip().lower() == pay_period.strip().lower() and
                item["type"].strip().lower() == type.strip().lower()):
                return (item["rules"])
            
    def Rule_1(self,record):
        state=record.get("state").lower()
        gar_type = record.get("garnishment_data")[0]
        type=gar_type.get('type').lower()
        pay_period=record.get('pay_period').lower()
        rules_data=self.get_serialized_data()

        for item in rules_data:
            if (item["state"].strip().lower() == state.strip().lower() and
                item["pay_period"].strip().lower() == pay_period.strip().lower() and
                item["type"].strip().lower() == type.strip().lower()):
                return (item["amount"])
            
    def Rule_2(self,record):
        return ("No Provision")

    
    def apply_rule(self, record):
        rule_name=self.find_rule(record)
        """Dynamically applies the rule based on the rule name"""
        if rule_name in self.rule_map:
            return self.rule_map[rule_name](record)
        else:
            raise ValueError(f"Rule '{rule_name}' is not defined.")


record={
                "ee_id": "EE005114",
                "gross_pay": 1000.0,
                "state": "alaska",
                "no_of_exemption_for_self": 2,
                "pay_period": "Weekly",
                "filing_status": "single_filing_status",
                "net_pay": 858.8,
                "payroll_taxes": [
                    {
                        "federal_income_tax": 80.0
                    },
                    {
                        "social_security_tax": 49.6
                    },
                    {
                        "medicare_tax": 11.6
                    },
                    {
                        "state_tax": 0.0
                    },
                    {
                        "local_tax": 0.0
                    }
                ],
                "payroll_deductions": {
                    "medical_insurance": 0.0
                },
                "age": 50,
                "is_blind": True,
                "is_spouse_blind": True,
                "spouse_age": 39,
                "support_second_family": "Yes",
                "no_of_student_default_loan": 2,
                "arrears_greater_than_12_weeks": "No",
                "garnishment_data": [
                    {
                        "type": "student_default_loan",
                        "data": [
                            {
                                "case_id": "C13278",
                                "amount": 200.0,
                                "arrear": 0
                            }
                        ]
                    }
                ]
            }

print(gar_fees_rules_engine().apply_rule(record))



