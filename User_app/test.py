from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status



# class calculationTest(APITestCase):
#     def test_calculation(self):
#         _data={
#             "batch_id": "B101",
#             "CID": {
#               "C021": {
#             "employees": [
#               {
#                 "employee_id": "EMP009",
#                 "gross_pay": 800,
#                 "employee_name": "Michael Johnson",
#                 "garnishment_fees": 5,
#                 "support_second_family": "Yes",
#                 "arrears_greater_than_12_weeks": "No",
#                 "state": "Florida",
#                 "child_support": [
#                   { "amount": 150, "arrear": 0 },
#                   { "amount": 10, "arrear": 10 }
#                 ],
#                 "taxes": [
#                   { "federal_income_tax": 10 },
#                   { "social_security_tax": 20 },
#                   { "medicare_tax": 5 },
#                   { "state_tax": 5 },
#                   { "local_tax": 10 }
#                 ],
#                 "pay_period": "weekly",
#                 "garnishment_type": "child_support",
#                 "result": [
#                   { "child support amount1": 150, "child support amount2": 10 },
#                   { "arrear amount1": 0, "arrear amount2": 10 }
#                 ]
#               },
#               {
#                 "employee_id": "EMP0010",
#                 "gross_pay": 900,
#                 "employee_name": "Michael Johnson",
#                 "garnishment_fees": 5,
#                 "arrears_greater_than_12_weeks": "Yes",
#                 "support_second_family": "Yes",
#                 "child_support": [
#                   { "amount": 50, "arrear": 10 },
#                   { "amount": 150, "arrear": 10 }
#                 ],
#                 "taxes": [
#                   { "federal_income_tax": 10 },
#                   { "social_security_tax": 20 },
#                   { "medicare_tax": 15 },
#                   { "state_tax": 10 },
#                   { "local_tax": 10 }
#                 ],
#                 "state": "Indiana",
#                 "pay_period": "weekly",
#                 "garnishment_type": "child_support",
#                 "result": [
#                   { "child support amount1": 50, "child support amount2": 150 },
#                   { "arrear amount1": 10, "arrear amount2": 10 }
#                 ]
#               },
#               {
#                 "employee_id": "EE009",
#                 "employee_name": "Nick Rode",
#                 "pay_period": "weekly",
#                 "no_of_exception_for_Self": 1,
#                 "filing_status": "single_filing_status",
#                 "net_pay": 169330.17,
#                 "order_id": "B101",
#                 "age": 64,
#                 "blind": True,
#                 "dependent_disability": False,
#                 "garnishment_type": "federal_tax",
#                 "result": 168866.71
#               }
#             ]
#           }
#         }
#            }      
      
#         _response=self.client.post('/User/garnishment_calculate/' ,data=_data,format="json")
#         _data=_response.json()
#         self.assertEqual(_response.status_code,status.HTTP_200_OK)
#         #   self.assertEqual()


class BasicTest(APITestCase):
    def test_basic(self):
        response = self.client.get('/User/Getallemployerdetail')
        self.assertEqual(response.status_code, status.HTTP_200_OK)