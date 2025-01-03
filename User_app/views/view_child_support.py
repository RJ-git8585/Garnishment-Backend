from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from User_app.models import *
from rest_framework.response import Response
from ..serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from auth_project.garnishment_library import gar_resused_classes as gc
from django.utils.decorators import method_decorator



def calculate_ccpa_limit(support_second_family,arrears_greater_than_12_weeks):
    # Calculate the CCPA limit based on conditions
    if support_second_family and arrears_greater_than_12_weeks:
        return 0.55
    elif not support_second_family and not arrears_greater_than_12_weeks:
        return 0.60
    elif not support_second_family and arrears_greater_than_12_weeks:
        return 0.65
    return 0.50

def calculate_minimum_wage_rule(pay_period):
    # Calculate the minimum wage rule based on pay period
    federal_minimum_wage = 7.25
    if pay_period == "weekly":
        return 30 * federal_minimum_wage
    elif pay_period == "biweekly":
        return 60 * federal_minimum_wage
    return 0
@method_decorator(csrf_exempt, name='dispatch')
class CalculationDataView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            batch_id = data.get("batch_id")
            rows = data.get("rows", [])
            
            # Validate batch number
            if not batch_id:
                return Response({"error": "batch_id is required"}, status=400)

            if not rows:
                return Response({"error": "No rows provided"}, status=400)

            # Process each result
            for record in rows:
                user = Garcalculation_data.objects.create(**record)
                employee_id = record.get("employee_id")
                employer_id = record.get("employer_id")
                amount_to_withhold_child1 = record.get('amount_to_withhold_child1', 0)
                amount_to_withhold_child2 = record.get('amount_to_withhold_child2', 0)
                amount_to_withhold_child3 = record.get('amount_to_withhold_child3', 0)
                amount_to_withhold_child4 = record.get('amount_to_withhold_child4', 0)  # Using get to avoid KeyError
                amount_to_withhold_child5 = record.get('amount_to_withhold_child5', 0)
                arrears_amt_Child1 = record.get('arrears_amt_Child1', 0)
                arrears_amt_Child2 = record.get('arrears_amt_Child2', 0)
                arrears_amt_Child3 = record.get('arrears_amt_Child3', 0)
                arrears_amt_Child4 = record.get('arrears_amt_Child4', 0)
                arrears_amt_Child5 = record.get('arrears_amt_Child5', 0)
                arrears_greater_than_12_weeks = record.get('arrears_greater_than_12_weeks')
                support_second_family = record.get('support_second_family')
                number_of_child_support_order = record.get('number_of_child_support_order')
                number_of_arrear = record.get('number_of_arrear')
                garnishment_fees = record.get('garnishment_fees')
                pay_period = record.get('pay_period')
                state=record.get('state')
                disposable_income = record.get('disposable_income')
                # ccpa_limit=ccpa_limit(support_second_family,arrears_greater_than_12_weeks)

                # Calculate ccpa_limit based on conditions
                ccpa_limit=calculate_ccpa_limit(support_second_family,arrears_greater_than_12_weeks)
                    
                # Calculate allowable disposable earnings
                allowable_disposable_earnings = round(disposable_income * ccpa_limit, 2)
                print("allowable_disposable_earnings",allowable_disposable_earnings)
                withholding_available = round(allowable_disposable_earnings - garnishment_fees, 2)
                print("withholding_available",withholding_available)
                other_garnishment_amount = round(disposable_income * 0.25, 2)
    
                # Federal Minimum Wage calculation
                fmw=calculate_minimum_wage_rule(pay_period)
                print("fmv",fmw)
                
                Disposable_Income_minus_Minimum_Wage_rule = round(disposable_income - fmw, 2)
                print("Disposable_Income_minus_Minimum_Wage_rule",Disposable_Income_minus_Minimum_Wage_rule)
                Minimum_amt = min(Disposable_Income_minus_Minimum_Wage_rule, withholding_available)

                allocation_method_for_garnishment  = gc.StateMethodIdentifiers(state).get_allocation_method()
                print("allocation_method_for_garnishment",allocation_method_for_garnishment)
                
                # Determine the allowable garnishment amount
                allowed_amount_for_garnishment = max(0, Minimum_amt)                
                amount_to_withhold = amount_to_withhold_child1 + amount_to_withhold_child2 + amount_to_withhold_child3+amount_to_withhold_child4+amount_to_withhold_child5
                print("amount_to_withhold",amount_to_withhold)
                # Determine the allowable garnishment amount
                amount_to_withhold_childs1=gc.CalculateAmountToWithhold(allowed_amount_for_garnishment, amount_to_withhold, allocation_method_for_garnishment,number_of_child_support_order).calculate(amount_to_withhold_child1)
                print("amount_to_withhold_child1",amount_to_withhold_childs1)
                amount_to_withhold_childs2=gc.CalculateAmountToWithhold(allowed_amount_for_garnishment, amount_to_withhold, allocation_method_for_garnishment,number_of_child_support_order).calculate(amount_to_withhold_child2)
                print("amount_to_withhold_child2",amount_to_withhold_childs2)
                amount_to_withhold_childs3=gc.CalculateAmountToWithhold(allowed_amount_for_garnishment, amount_to_withhold, allocation_method_for_garnishment,number_of_child_support_order).calculate(amount_to_withhold_child3)
                print("amount_to_withhold_child3",amount_to_withhold_childs3)
                amount_to_withhold_childs4=gc.CalculateAmountToWithhold(allowed_amount_for_garnishment, amount_to_withhold, allocation_method_for_garnishment,number_of_child_support_order).calculate(amount_to_withhold_child4)
                amount_to_withhold_childs5=gc.CalculateAmountToWithhold(allowed_amount_for_garnishment, amount_to_withhold, allocation_method_for_garnishment,number_of_child_support_order).calculate(amount_to_withhold_child5)
                
                # Calculate the amount left for arrears
                if allowed_amount_for_garnishment > 0 and (allowed_amount_for_garnishment - amount_to_withhold) > 0:
                    amount_left_for_arrears = round(allowed_amount_for_garnishment - amount_to_withhold, 2)
                else:
                    amount_left_for_arrears = 0
                print("amount_left_for_arrears",amount_left_for_arrears)
                
                allocation_method_for_arrears=allocation_method_for_garnishment
                print("allocation_method_for_arrears",allocation_method_for_arrears)
                # Determine allowed amount for other garnishment
                allowed_child_support_arrear = arrears_amt_Child1 + arrears_amt_Child2 + arrears_amt_Child3+amount_to_withhold_child4+amount_to_withhold_child5
                arrears_amt_Childs1=gc.CalculateArrearAmountForChild(amount_left_for_arrears, allowed_child_support_arrear,allocation_method_for_arrears,number_of_arrear).calculate(arrears_amt_Child1)
                print("arrears_amt_Childs1",arrears_amt_Childs1)
                arrears_amt_Childs2=gc.CalculateArrearAmountForChild(amount_left_for_arrears, allowed_child_support_arrear,allocation_method_for_arrears,number_of_arrear).calculate(arrears_amt_Child2)
                print("arrears_amt_Childs2")
                arrears_amt_Childs3=gc.CalculateArrearAmountForChild(amount_left_for_arrears, allowed_child_support_arrear,allocation_method_for_arrears,number_of_arrear).calculate(arrears_amt_Child3)
                arrears_amt_Childs4=gc.CalculateArrearAmountForChild(amount_left_for_arrears, allowed_child_support_arrear,allocation_method_for_arrears,number_of_arrear).calculate(arrears_amt_Child4)
                arrears_amt_Childs5=gc.CalculateArrearAmountForChild(amount_left_for_arrears, allowed_child_support_arrear,allocation_method_for_arrears,number_of_arrear).calculate(arrears_amt_Child5)
                
                if (amount_left_for_arrears - allowed_child_support_arrear) <= 0:
                    allowed_amount_for_other_garnishment = 0
                else:
                    allowed_amount_for_other_garnishment = round(amount_left_for_arrears - allowed_child_support_arrear, 2)
                print("allowed_amount_for_other_garnishment",allowed_amount_for_other_garnishment)
                net_pay = max(0, (disposable_income - allowed_amount_for_other_garnishment))

                # Create CalculationResult object
                CalculationResult.objects.create(
                    employee_id=employee_id,
                    employer_id=employer_id,
                    result=allowed_amount_for_other_garnishment,
                    amount_to_withhold_child1=amount_to_withhold_childs1,
                    amount_to_withhold_child2=amount_to_withhold_childs2,
                    amount_to_withhold_child3=amount_to_withhold_childs3,
                    amount_to_withhold_child4=amount_to_withhold_childs4,
                    amount_to_withhold_child5=amount_to_withhold_childs5,
                    arrears_amt_Child1=arrears_amt_Childs1,
                    arrears_amt_Child2=arrears_amt_Childs2,
                    arrears_amt_Child3=arrears_amt_Childs3,
                    arrears_amt_Child4=arrears_amt_Childs4,
                    arrears_amt_Child5=arrears_amt_Childs5,
                    net_pay=net_pay,
                    batch_id=batch_id
                )
                LogEntry.objects.create(
                    action='Calculation data Added',
                    details=f'Calculation data Added successfully with employer ID {employer_id} and employee ID {employee_id}'
                )
                return Response({'message': 'Child Support Calculations Details Successfully Registered', "status code":status.HTTP_200_OK})
        except Employee_Details.DoesNotExist:
            return Response({"error": "Employee details not found"}, status=status.HTTP_404_NOT_FOUND)
        except Employer_Profile.DoesNotExist:
            return Response({"error": "Employer profile not found", "status code":status.HTTP_404_NOT_FOUND})
        except Exception as e:
            return Response({"error":{str(e)}, "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})

class SingleCalculationDetailView(APIView):
    def get(self, request, employer_id, employee_id):
        employees = CalculationResult.objects.filter(employer_id=employer_id, employee_id=employee_id).order_by('-timestamp')[0:1]
        if employees.exists():
            try:
                serializer = ResultSerializer(employees, many=True)
                response_data = {
                    'success': True,
                    'message': 'Data fetched successfully',
                    'status code': status.HTTP_200_OK,
                    'data': serializer.data
                }
                return JsonResponse(response_data)
            except CalculationResult.DoesNotExist:
                return JsonResponse({'message': 'Data not found', 'status code': status.HTTP_404_NOT_FOUND})
            except Exception as e:
                return Response({"error": str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})
        else:
            return JsonResponse({'message': 'Employer ID not found', 'status code': status.HTTP_404_NOT_FOUND})


class AllGarnishmentResultDetailView(APIView):
    def get(self, request, employer_id):
        employees = CalculationResult.objects.filter(employer_id=employer_id).order_by('-timestamp')
        if employees.exists():
            try:
                serializer = ResultSerializer(employees, many=True)
                response_data = {
                    'success': True,
                    'message': 'Data retrieved successfully',
                    'status code': status.HTTP_200_OK,
                    'data': serializer.data
                }
                return JsonResponse(response_data)
            except CalculationResult.DoesNotExist:
                return JsonResponse({'message': 'Data not found', 'status code': status.HTTP_404_NOT_FOUND})
            except Exception as e:
                return Response({"error": str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})
        else:
            return JsonResponse({'message': 'Employer ID not found', 'status code': status.HTTP_404_NOT_FOUND})

class ChildSupportGarnishmentBatchResult(APIView):
    def get(self, request, batch_id):
        employees = CalculationResult.objects.filter(batch_id=batch_id)
        if employees.exists():
            try:
                employee= employees.order_by('-timestamp')
                serializer = ResultSerializer(employee, many=True)
                response_data = {
                    'success': True,
                    'message': 'Data retrieved successfully',
                    'status code': status.HTTP_200_OK,
                    'data': serializer.data
                }
                return JsonResponse(response_data)
            except CalculationResult.DoesNotExist:
                return JsonResponse({'message': 'Data not found', 'status code': status.HTTP_404_NOT_FOUND})
            except Exception as e:
                return Response({"error": str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})
        else:
            return JsonResponse({'message': 'Employer ID not found', 'status code': status.HTTP_404_NOT_FOUND})




class get_child_garnishment_case_data_and_result(APIView):
    def get(self, request, employer_id,employee_id):
        employees = Calculation_data_results.objects.filter(employer_id=employer_id,employee_id=employee_id).order_by('-timestamp')[0:1]
        if employees.exists():
            try:
                serializer = Calculation_data_results_Serializer(employees,many=True)
                response_data = {
                    'success': True,
                    'message': 'Garnishment Result Data retrieved successfully',
                    'status code': status.HTTP_200_OK,
                    'data': serializer.data
                }
                return JsonResponse(response_data)
            except federal_tax_data_and_result.DoesNotExist:
                return JsonResponse({'message': 'Data not found', 'status code': status.HTTP_404_NOT_FOUND})
            except Exception as e:
                return Response({"error": str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})  
        else:
            return JsonResponse({'message': 'Employee ID not found', 'status code': status.HTTP_404_NOT_FOUND})
  