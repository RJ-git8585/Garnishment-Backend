from rest_framework import status
from django.contrib import messages
from auth_project.config import ccpa_limit
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from User_app.models import *

from django.contrib.auth import authenticate, login as auth_login ,get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count
from django.shortcuts import get_object_or_404
import json
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.generics import DestroyAPIView ,RetrieveUpdateAPIView
from rest_framework import viewsets ,generics
from ..serializers import *
from django.http import HttpResponse
from ..forms import PDFUploadForm
from django.db import transaction
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken ,AccessToken, TokenError
import csv
from rest_framework.views import APIView


class get_multiple_student_loan_case_data(APIView):
    def get(self, request, employer_id,employee_id):
        employees = multiple_student_loan_data.objects.filter(employer_id=employer_id,employee_id=employee_id).order_by('-timestamp')[0:1]
        if employees.exists():
            try:
                serializer = multiple_student_loan_data_Serializer(employees,many=True)
                response_data = {
                    'success': True,
                    'message': 'Data retrieved successfully',
                    'status code': status.HTTP_200_OK,
                    'data': serializer.data
                }
                return JsonResponse(response_data)
            except federal_loan_case_data.DoesNotExist:
                return JsonResponse({'message': 'Data not found', 'status code': status.HTTP_404_NOT_FOUND})
        else:
            return JsonResponse({'message': 'Employee ID not found', 'status code': status.HTTP_404_NOT_FOUND})


class get_multiple_student_loan_data_and_result(APIView):
    def get(self, request, employer_id,employee_id):
        employees = multiple_student_loan_data_and_result.objects.filter(employer_id=employer_id,employee_id=employee_id).order_by('-timestamp')[0:1]
        if employees.exists():
            try:
                serializer = multiple_student_loan_data_and_result_Serializer(employees,many=True)
                response_data = {
                    'success': True,
                    'message': 'Data retrieved successfully',
                    'status code': status.HTTP_200_OK,
                    'data': serializer.data
                }
                return JsonResponse(response_data)
            except multiple_student_loan_data_and_result.DoesNotExist:
                return JsonResponse({'message': 'Data not found', 'status code': status.HTTP_404_NOT_FOUND})
        else:
            return JsonResponse({'message': 'Employee ID not found', 'status code': status.HTTP_404_NOT_FOUND})



class get_multiple_student_loan_result(APIView):
    def get(self, request, employee_id, employer_id): 
        employees = multiple_student_loan_result.objects.filter(employee_id=employee_id, employer_id=employer_id)
        if employees.exists():
            try:
                employee= employees.order_by('-timestamp')[:1]
                serializer = MultipleStudentLoanSerializer(employee, many=True)
                response_data = {
                    'success': True,
                    'message': 'Data retrieved successfully',
                    'status code': status.HTTP_200_OK,
                    'data': serializer.data
                }
                return JsonResponse(response_data)
            except Employer_Profile.DoesNotExist:
                return JsonResponse({'message': 'Data not found', 'status code': status.HTTP_404_NOT_FOUND})
        else:
            return JsonResponse({'message': 'Employer ID not found', 'status code': status.HTTP_404_NOT_FOUND})

class get_all_multiple_student_loan_result(APIView):
    def get(self, request, employer_id):
        employees = multiple_student_loan_result.objects.filter(employer_id=employer_id,)
        if employees.exists():
            try:
                serializer = MultipleStudentLoanSerializer(employees,many=True)
                response_data = {
                    'success': True,
                    'message': 'Multiple Student Loan Data retrieved successfully',
                    'status code': status.HTTP_200_OK,
                    'data': serializer.data
                }
                return JsonResponse(response_data)
            except multiple_student_loan_result.DoesNotExist:
                return JsonResponse({'message': 'Data not found', 'status code': status.HTTP_404_NOT_FOUND})
        else:
            return JsonResponse({'message': 'Employee ID not found', 'status code': status.HTTP_404_NOT_FOUND})


@csrf_exempt
@api_view(['POST'])
def MultipleStudentLoanCalculationData(request):
    if request.method == 'POST':
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
                employee_id = record.get("employee_id")
                employer_id = record.get("employer_id")
                garnishment_fees = record.get("garnishment_fees", 0)
                disposable_income = record.get("disposable_income", 0)
            
                user = multiple_student_loan_data.objects.create(**record)
                allowable_disposable_earning=round(disposable_income-garnishment_fees,2)
                twentyfive_percent_of_earning= round(allowable_disposable_earning*.25,2)
                fmw=7.25*30
                
                if allowable_disposable_earning<fmw:
                    garnishment_amount=0
                else:
                    garnishment_amount=twentyfive_percent_of_earning
                difference=round(disposable_income-fmw,2)
                if difference>garnishment_amount:
                    garnishment_amount=garnishment_amount
                else:
                    garnishment_amount=difference
                if garnishment_amount<0:
                    garnishment_amount=0
                else:
                    garnishment_amount=garnishment_amount

                StudentLoanAmount1=round(allowable_disposable_earning*.15,2)
                StudentLoanAmount2=round(allowable_disposable_earning*.10,2)
                StudentLoanAmount3=round(allowable_disposable_earning*0,2)
    
                net_pay = round(disposable_income-garnishment_amount,2)
                if net_pay <0:
                    net_pay=0
                else:
                    net_pay=net_pay

                # Create Calculation_data_results object
                multiple_student_loan_data_and_result.objects.create(
                    employee_id=employee_id,
                    employer_id=employer_id,
                    garnishment_fees=garnishment_fees,
                    disposable_income=disposable_income,
                    allowable_disposable_earning=allowable_disposable_earning,
                    twentyfive_percent_of_earning=twentyfive_percent_of_earning,
                    fmw=fmw,
                    garnishment_amount=garnishment_amount,
                    StudentLoanAmount1=StudentLoanAmount1,
                    StudentLoanAmount2=StudentLoanAmount2,
                    StudentLoanAmount3=StudentLoanAmount3,
                    net_pay=net_pay
                )
    
                # Create CalculationResult object
                multiple_student_loan_result.objects.create(
                    employee_id=employee_id,
                    employer_id=employer_id,
                    garnishment_amount=garnishment_amount,
                    StudentLoanAmount1=StudentLoanAmount1,
                    StudentLoanAmount2=StudentLoanAmount2,
                    StudentLoanAmount3=StudentLoanAmount3,
                    net_pay=net_pay   ,
                    batch_id=batch_id         
                )
                LogEntry.objects.create(
                    action='Multiple Student Loan Calculation data Added',
                    details=f'Multiple Student Loan Calculation data Added successfully with employer ID {user.employer_id} and employee ID {user.employee_id}'
                )
            return Response({'message': 'Multiple Student Loan Calculations Details Successfully Registered', "status code":status.HTTP_200_OK})
        except Employee_Details.DoesNotExist:
            return Response({"error": "Employee details not found"}, status=status.HTTP_404_NOT_FOUND)
        except Employer_Profile.DoesNotExist:
            return Response({"error": "Employer profile not found", "status code":status.HTTP_404_NOT_FOUND})
        except Exception as e:
                return Response({"error": str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})
    else:
        return Response({'message': 'Please use POST method', "status_code":status.HTTP_400_BAD_REQUEST})

class MultipleStudentLoanBatchResult(APIView):
    def get(self, request, batch_id): 
        employees = multiple_student_loan_result.objects.filter(batch_id=batch_id)
        if employees.exists():
            try:
                employee= employees.order_by('-timestamp')      
                serializer = MultipleStudentLoanSerializer(employee, many=True)
                response_data = {
                    'success': True,
                    'message': 'Data retrieved successfully',
                    'status code': status.HTTP_200_OK,
                    'data': serializer.data
                }
                return JsonResponse(response_data)
            except Employer_Profile.DoesNotExist:
                return JsonResponse({'message': 'Data not found', 'status code': status.HTTP_404_NOT_FOUND})
        else:
            return JsonResponse({'message': 'Employer ID not found', 'status code': status.HTTP_404_NOT_FOUND})