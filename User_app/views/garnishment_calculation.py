from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from User_app.models import *
from rest_framework.response import Response
from User_app.serializers import *
from rest_framework.views import APIView
from auth_project.garnishment_library import gar_resused_classes as gc
from auth_project.garnishment_library.child_support import ChildSupport,MultipleChild,SingleChild 
from auth_project.garnishment_library.student_loan import student_loan_calculate
from django.utils.decorators import method_decorator
from auth_project.garnishment_library.federal_case import federal_tax




@method_decorator(csrf_exempt, name='dispatch')
class CalculationDataView(APIView):
    """
    API View to handle Garnishment calculations and save data to the database.
    """
    def post(self, request, *args, **kwargs):
        try:
            # Use request.data directly
            data = request.data
            batch_id = data.get("batch_id")
            cid_data = data.get("cid", {})
            output = []
    
            # Validate batch_id
            if not batch_id:
                return Response({"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
            # Validate rows
            if not cid_data:
                return Response({"error": "No rows provided"}, status=status.HTTP_400_BAD_REQUEST)
    
            for cid, cid_info in cid_data.items():
                cid_summary = {"cid": cid, "employees": []}
    
                for record in cid_info.get("employees", []):

                    garnishment_results=[]
                    garnishment_data = record.get("garnishment_data", [])
    
                    for garnishment in garnishment_data:
                        garnishment_type = list(garnishment.values())[0]
    
                        if garnishment_type.lower() == "child support":
                            # Validate child support fields
                            required_fields = [
                                "arrears_greater_than_12_weeks",
                                "support_second_family", "gross_pay", "payroll_taxes"
                            ]
                            missing_fields = [field for field in required_fields if field not in record]
    
                            if not missing_fields:
                                tcsa = ChildSupport().get_list_supportAmt(record)
                                result = (
                                    MultipleChild().calculate(record)
                                    if len(tcsa) > 1
                                    else SingleChild().calculate(record)
                                )
                                child_support_data = result[0]
                                print("child_support_data",child_support_data)
                                print("l",len(result))
 
                                arrear_amount_data = result[1]
                                print("arrear_amount_data",arrear_amount_data)

                                case_id_get=garnishment_data[0]["data"]

                                 # Transform data into the desired format
                                # if len(result)==1:
                                        
                                #         garnishment_results.append({
                                #             "case_id":list(garnishment_data[0]["data"][0].values())[0],
                                #             "garnishment_type": garnishment_type,
                                #             "child_support_withhold_amt": child_support_data[f'child support amount1'],
                                #             "arrear_amount": arrear_amount_data[f'arrear amount1']
                                #         })

                                # else:
                                for i in range(1, len(child_support_data) + 1):
                                    garnishment_results.append({
                                        "case_id":case_id_get[i-1]["case_id"],
                                        "garnishment_type": garnishment_type,
                                        "child_support_withhold_amt": child_support_data[f'child support amount{i}'],
                                        "arrear_amount": arrear_amount_data[f'arrear amount{i}']
                                    })

                            else:
                                result = {"error": f"Missing fields in record: {', '.join(missing_fields)}"}
    
                        elif garnishment_type.lower() == "federal tax levy":
                            # Validate federal tax fields
                            required_fields = ["filing_status", "pay_period", "net_pay", "age", "is_blind"]
                            missing_fields = [field for field in required_fields if field not in record]
    
                            if not missing_fields:
                                result = federal_tax().calculate(record)
                                garnishment_results.append({
                                        "case_id":list(garnishment_data[0]["data"][0].values())[0],
                                        "garnishment_type": garnishment_type,
                                        "federal_tax_withhold_amt": result,
                                    })

                            else:
                                result = {"error": f"Missing fields in record: {', '.join(missing_fields)}"}
    
                        elif garnishment_type.lower() == "student default loan":
                            # Validate student loan fields
                            required_fields = ["gross_pay", "pay_period", "no_of_student_default_loan", "payroll_taxes"]
                            missing_fields = [field for field in required_fields if field not in record]
    
                            if not missing_fields:
                                result = student_loan_calculate().calculate(record)
                                
                                case_id_get=garnishment_data[0]["data"] 
                                # print("case_id_get",case_id_get)

                                case_id_get.append({"case_id": "C13278"})
                                                  
                                # Transform data into the desired format
                                if len(result)==1:
                                    garnishment_results.append({
                                        "case_id":list(garnishment_data[0]["data"][0].values())[0],
                                        "garnishment_type":garnishment_type,
                                        "student_loan_withhold_amt": result['student_loan_amt'],
                                    })
                                else:
                                    for i in range(1, len(result) + 1):
                                        garnishment_results.append({
                                            "case_id":case_id_get[i-1]["case_id"],
                                            "garnishment_type":garnishment_type,
                                            "student_loan_withhold_amt": result[f'student_loan_amt{i}'],
                                        })
    
                            else:
                                result = {"error": f"Missing fields in record: {', '.join(missing_fields)}"}
    
                        else:
                            return Response(
                                {"error": f"Unsupported garnishment_type: {garnishment_type}"},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        


    
                        # # Append each order to the orders list
                        # garnishment_results.append({
                        #     "order_id": record.get("order_id"),
                        #     "garnishment_type": garnishment_type,
                        #     "withholding_amt": result
                        # })
    
                    # Append employee data with all their orders
                    
                    cid_summary["employees"].append({
                        "ee_id": record.get("ee_id"),
                        "garnishment": garnishment_results
                    })
    
                output.append(cid_summary)
    
                # Log the action
                LogEntry.objects.create(
                    action="Calculation data added",
                    details=(
                        f"Calculation data added successfully with employer ID "
                        f"{record.get('batch_id')} and employee ID {record.get('ee_id')}"
                    )
                )
    
            return Response(
                {
                    "message": "Result Generated Successfully",
                    "status_code": status.HTTP_200_OK,
                    "batch_id": batch_id,
                    "results": output
                },
                status=status.HTTP_200_OK
            )
    
        except Employee_Detail.DoesNotExist:
            return Response(
                {"error": "Employee details not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




# record=   {
#       "ee_id": "EMP009",
#       "employer_id" :"EMP001",
#       "gross_pay": 600,
#       "employee_name": "Michael Johnson",
#       "garnishment_fees": 5,
#       "arrears_greater_than_12_weeks": "Yes",
#       "support_second_family": "Yes",
#       "child_support" : [ {"amount": 200, "arrear": 6}, {"amount": 300, "arrear": 0}],
#       "taxs":[{"fit":200 },{"sst":10} ,{"mct":20}, {"st":10} , {"lt":5}],
#       "state": "Florida",
#       "arrears_amount1": 99,
#       "pay_period" : "weekly",
#       "mandatory_deductions":10.0,
#        "garnishment_type":"child_support"
# } 

# print("calculate_twa",ChildSupport().calculate_twa(record))
# print("calculate_de_rule",ChildSupport().calculate_de_rule(record))
# print("calculate_md",ChildSupport().calculate_md(record))
# print("calculate_wl",ChildSupport().calculate_wl(record))
# print("calculate_tcsa",ChildSupport().get_list_supportAmt(record))
# print("calculate_tcsa_sum",sum(ChildSupport().get_list_supportAmt(record)))
# print("calculate_taa",ChildSupport().get_list_support_arrearAmt(record))
# print("calculate_ade",ChildSupport().calculate_ade(record))
# print("calculate_wa",ChildSupport().calculate_wa(record))


    
                    # elif len(garnishment_data)>1:
                    #     # Validate student loan fields
                    #     required_student_loan_fields = ["gross_pay", "pay_period","no_of_student_default_loan","taxes"]
                    #     missing_student_loan_fields = [
                    #         field for field in required_student_loan_fields if field not in record
                    #     ]
                        
                    #     if not missing_student_loan_fields:
                    #          result = multiple_garnishment_case().calculate(record)
                    #     else:
                    #         result = {"error": f"Missing fields in record: {', '.join(missing_student_loan_fields)}"}    


                            #             if not missing_fields:
                            #     tcsa = ChildSupport().get_list_supportAmt(record)
                            #     result = (
                            #         MultipleChild().calculate(record)
                            #         if len(tcsa) > 1
                            #         else ChildSupport().calculate(record)
                            #     )
                            #     for idx, item in enumerate(result):
                            #         garnishment_results.append({
                            #             "order_id": f"{record.get('order_id', 'DE')}-{idx + 1}",
                            #             "garnishment_type": garnishment_type,
                            #             "withholding_amt": item
                            #         })
                            # else:
                            #     garnishment_results.append({
                            #         "error": f"Missing fields in record: {', '.join(missing_fields)}"
                            #     })



# {
#           "ee_id": "EE005254",
#           "gross_pay": 1600,
#           "state": "Massachusetts",
#           "no_of_exemption_for_self": 1,
#           "pay_period": "Semimonthly",
#           "filing_status": "single_filing_status",
#           "net_pay": 1369.5,
#           "payroll_taxes": [
#             {
#               "federal_income_tax": 160.0
#             },
#             {
#               "social_security_tax": 45.0
#             },
#             {
#               "medicare_tax": 10.5
#             },
#             {
#               "state_tax": 15.0
#             },
#             {
#               "local_tax": 0.0
#             }
#           ],
#           "payroll_deductions": {
#             "medical_insurance": 0
#           },
#           "age": 41,
#           "is_blind": false,
#           "is_spouse_blind": true,
#           "spouse_age": 46,
#           "support_second_family": "No",
#           "no_of_student_default_loan": 0,
#           "arrears_greater_than_12_weeks": "Yes",
#           "garnishment_data": [
#             {
#               "type": "Federal Tax Levy",
#               "data": [
#                 {
#                   "case_id": "C72296",
#                   "amount1": 0,
#                   "arrear1": 0
#                 },
#                 {
#                   "case_id": "C72296",
#                   "amount2": 0,
#                   "arrear2": 0
#                 }
#               ]
#             }
#           ]
#         }