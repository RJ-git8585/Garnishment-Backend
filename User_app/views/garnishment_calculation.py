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
from auth_project.garnishment_library import gar_fees as gar_fees
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
    
            # Validate cid_data
            if not cid_data:
                return Response({"error": "No rows provided"}, status=status.HTTP_400_BAD_REQUEST)



            for cid, cid_info in cid_data.items():
                cid_summary = {"cid": cid, "employees": []}
    
                for record in cid_info.get("employees", []):

                    garnishment_data = record.get("garnishment_data", [])
                    #Garnishment Fees 
                    gar_fees=gc.GarnishmentFeesIdentifier().calculate(record)

                    print("new",gar_fees.gar_fees_rules_engine.apply_rule(record))
    
                    gar_type = record.get("garnishment_data")[0]
                    garnishment_type=gar_type.get('type')

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
                            arrear_amount_data = result[1]
                            case_id_get=garnishment_data[0]["data"]
                            child_support=[]
                            arrears=[]
                            for i in range(1, len(child_support_data) + 1):
                                child_support.append({"child_support_withhold_amt": child_support_data[f'child support amount{i}']})
                                arrears.append({"arrear_amount": arrear_amount_data[f'arrear amount{i}']})
                            record["Agency"]=[{"withholding_amt":child_support}]
                            record['Arrear']=arrears
                            record['ER_deduction']={"garnishment_fees":gar_fees}
                        else:
                            result = {"error": f"Missing fields in record: {', '.join(missing_fields)}"}

                    elif garnishment_type.lower() == "federal tax levy":
                        
                        # Validate federal tax fields
                        required_fields = ["filing_status", "pay_period", "net_pay", "age", "is_blind"]
                        missing_fields = [field for field in required_fields if field not in record]

                        if not missing_fields:
                            result = federal_tax().calculate(record)
                            record["Agency"]=[{"withholding_amt":result}]
                            record['ER_deduction']={"garnishment_fees":gar_fees}
                          
                        else:
                            result = {"error": f"Missing fields in record: {', '.join(missing_fields)}"}

                    elif garnishment_type.lower() == "student default loan":
                        
                        # Validate student loan fields
                        required_fields = ["gross_pay", "pay_period", "no_of_student_default_loan", "payroll_taxes"]
                        missing_fields = [field for field in required_fields if field not in record]

                        if not missing_fields:
                            result = student_loan_calculate().calculate(record)
                                              
                            # Transform data into the desired format
                            if len(result)==1:
                                record["Agency"]=[{"student_loan_withhold_amt":result['student_loan_amt']}]
                                record['ER_deduction']={"Garnishment_fees":gar_fees}
                            else:
                                student_loan=[]
                                for i in range(1, len(result) + 1):
                                    student_loan.append({"student_loan_withhold_amt":result[f'student_loan_amt{i}']})
                                record["Agency"]=[{"student_loan_withhold_amt":student_loan}]
                                record['ER_deduction']={"Garnishment_fees":gar_fees}

                        else:
                            result = {"error": f"Missing fields in record: {', '.join(missing_fields)}"}

                    else:
                        return Response(
                            {"error": f"Unsupported garnishment_type: {garnishment_type}"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    cid_summary["employees"].append(record)
    
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
