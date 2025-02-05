from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import *
import pandas
import math
from User_app.models import *
from django.contrib.auth import  login as auth_login ,get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count
from django.shortcuts import get_object_or_404
import json
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.generics import DestroyAPIView ,RetrieveUpdateAPIView
from ..serializers import *
from django.http import HttpResponse
from ..forms import PDFUploadForm
from django.db import transaction
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken ,AccessToken, TokenError
import csv
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from User_app.models import Employee_Detail
import pandas as pd
import os
from auth_project import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from User_app.models import garnishment_order, Employee_Detail, company_details


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON',
                'status code': status.HTTP_400_BAD_REQUEST
            })

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({
                'success': False,
                'message': 'Email and password are required',
                'status code': status.HTTP_400_BAD_REQUEST
            })

        try:
            user = Employer_Profile.objects.get(email=email)
        except Employer_Profile.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials',
                'status code': status.HTTP_400_BAD_REQUEST
            })
        employee = get_object_or_404(Employer_Profile, employer_name=user.employer_name, employer_id=user.employer_id,cid=user.cid)
        if check_password(password, user.password):
            auth_login(request, user)
            user_data = {
                "employer_id":employee.employer_id,
                "cid":employee.cid,
                'username': user.username,
                'name': user.employer_name,
                'email': user.email,
            }
            try:
                refresh = RefreshToken.for_user(user)

# <<<<<<< HEAD
                employee = get_object_or_404(Employer_Profile, employer_name=user.employer_name, cid=user.cid)
# =======

# >>>>>>> fc265ed477e089b2d584ad39b9de3885c44763a1
                application_activity.objects.create(
                action='Employer Login',
                details=f'Employer {employee.employer_name} Login successfully with ID {employee.cid}. '
            )
                response_data = {
                    'success': True,
                    'message': 'Login successfully',
# <<<<<<< HEAD
                    "cid":employee.cid,
# =======
                   
# >>>>>>> fc265ed477e089b2d584ad39b9de3885c44763a1
                    'user_data': user_data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'expire_time' : refresh.access_token.payload['exp'],
                    'status code': status.HTTP_200_OK,
                }
                return JsonResponse(response_data)
            except AttributeError as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error generating tokens: {str(e)}',
                    'status code': status.HTTP_500_INTERNAL_SERVER_ERROR
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials',
                'status code': status.HTTP_400_BAD_REQUEST
            })
    else:
        return JsonResponse({
            'message': 'Please use POST method for login',
            'status code': status.HTTP_400_BAD_REQUEST
        })


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON', 'status code': status.HTTP_400_BAD_REQUEST})

        employer_name = data.get('name')
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        street_name = data.get('street_name')
        federal_employer_identification_number = data.get('federal_employer_identification_number')
        city = data.get('city')
        state = data.get('state')
        country = data.get('country')
        zipcode = data.get('zipcode')
        number_of_employees = data.get('number_of_employees')
        department = data.get('department')
        location = data.get('location')

        if not all([employer_name, username, email, password1, password2]):
            return JsonResponse({'error': 'All required fields are mandatory', 'status_code': status.HTTP_400_BAD_REQUEST})

        if password1 != password2:
            return JsonResponse({'error': 'Passwords do not match', 'status_code': status.HTTP_400_BAD_REQUEST})

        if not (len(password1) >= 8 and any(c.isupper() for c in password1) and any(c.islower() for c in password1) and any(c.isdigit() for c in password1) and any(c in '!@#$%^&*()_+' for c in password1)):
            return JsonResponse({'error': 'Password must meet complexity requirements', 'status code': status.HTTP_400_BAD_REQUEST})

        User = get_user_model()
        if Employer_Profile.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already used', 'status code': status.HTTP_400_BAD_REQUEST})
        if Employer_Profile.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email taken', 'status code': status.HTTP_400_BAD_REQUEST})

        try:
            user = Employer_Profile.objects.create(
                employer_name=employer_name, 
                email=email, 
                username=username, 
                password=make_password(password1),  # Hash the password
                federal_employer_identification_number=federal_employer_identification_number,
                street_name=street_name, 
                city=city, 
                state=state, 
                country=country, 
                zipcode=zipcode, 
                number_of_employees=number_of_employees, 
                department=department, 
                location=location
            )
            user.save()

            employee = get_object_or_404(Employer_Profile, employer_id=user.employer_id)
            application_activity.objects.create(
                action='Employer Register',
                details=f'Employer {employee.employer_name} registered successfully with ID {employee.employer_id}.'
            )
            return JsonResponse({'message': 'Successfully registered', 'status code': status.HTTP_201_CREATED})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status code': status.HTTP_500_INTERNAL_SERVER_ERROR})
    else:
        return JsonResponse({'message': 'Please use POST method for registration', 'status code': status.HTTP_400_BAD_REQUEST})
    

@csrf_exempt
def EmployerProfile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if len(str(data['federal_employer_identification_number'])) != 9:
                return JsonResponse({'error': 'Federal Employer Identification Number must be exactly 9 characters long', 'status_code':status.HTTP_400_BAD_REQUEST})
            
            if Employer_Profile.objects.filter(email=data['email']).exists():
                return JsonResponse({'error': 'Email already registered', 'status_code':status.HTTP_400_BAD_REQUEST})
            
            user = Employer_Profile.objects.create(**data)

            employee = get_object_or_404(Employer_Profile, cid=user.employer_id)
            LogEntry.objects.create(
                action='Employer details added',
                details=f'Employer details with ID {employee.employer_id}'
            )
            return JsonResponse({'message': 'Employer Detail Successfully Registered', "status code" :status.HTTP_201_CREATED})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    else:
        return JsonResponse({'message': 'Please use POST method','status code':status.HTTP_400_BAD_REQUEST})


class EmployeeDetailsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Deserialize and validate data using the serializer
            serializer = EmployeeDetailsSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': 'Validation error', 'details': serializer.errors,
                    "status":status.HTTP_400_BAD_REQUEST }
                )
            
            # Save validated data to the database
            employee = serializer.save()
            
            # Log the action
            LogEntry.objects.create(
                action='Employee details added',
                details=f'Employee details added successfully with employee ID {employee.ee_id}'
            )
            
            return Response(
                {'message': 'Employee Details Successfully Registered',
                "status":status.HTTP_201_CREATED}
            )
        
        except Exception as e:  # Handle general errors
            return Response(
                {'error': str(e),
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR}
            )


@csrf_exempt
def TaxDetails(request):
    if request.method == 'POST' :
        try:
            data = json.loads(request.body)
            required_fields = ['state_tax','employer_id','fedral_income_tax','social_and_security','medicare_tax']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            
            if missing_fields:
                return JsonResponse({'error': f'Required fields are missing: {", ".join(missing_fields)}', 'status code':status.HTTP_400_BAD_REQUEST})
            
            user=Tax_details.objects.create(**data)
            user.save()
            # employee = get_object_or_404(Tax_details, tax_id=user.tax_id)
            LogEntry.objects.create(
                action='Tax details added',
                details=f'Tax details added successfully for tax ID {user.tax_id}'
            )
            return JsonResponse({'message': 'Tax Details Successfully Registered', 'status code':status.HTTP_200_OK})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format','status code':status.HTTP_400_BAD_REQUEST})
        
        except Exception as e:
            return JsonResponse({'error': str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})
    else:
        return JsonResponse({'message': 'Please use POST method ', 'status code':status.HTTP_400_BAD_REQUEST})





#for Updating the Employer Profile data
class EmployerProfileEditView(RetrieveUpdateAPIView):
    queryset = Employer_Profile.objects.all()
    serializer_class = EmployerProfileSerializer
    lookup_field = 'employer_id'
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            data = request.data
    
            # Check for missing fields
            # required_fields = ['employer_name', 'street_name', 'federal_employer_identification_number', 'city', 'state', 'country', 'zipcode', 'email', 'number_of_employees', 'department', 'location']
            # missing_fields = [field for field in required_fields if field not in data or not data[field]]
            # if missing_fields:
            #     return JsonResponse({'error': f'Required fields are missing: {", ".join(missing_fields)}', 'status_code':status.HTTP_400_BAD_REQUEST})
    
            # Validate length of federal_employer_identification_number
            if 'federal_employer_identification_number' in data and len(str(data['federal_employer_identification_number'])) != 9:
                return JsonResponse({'error': 'Federal Employer Identification Number must be exactly 9 characters long', 'status_code':status.HTTP_400_BAD_REQUEST})
    
            # Validate email if it's being updated
            if 'email' in data and Employer_Profile.objects.filter(email=data['email']).exclude(employer_id=instance.employer_id).exists():
                return JsonResponse({'error': 'Email already registered', 'status_code':status.HTTP_400_BAD_REQUEST})
    
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            LogEntry.objects.create(
                    action='Employer details Updated',
                    details=f'Employer details Updated successfully with ID {instance.employer_id}'
                )
    
            response_data = {
                'success': True,
                'message': 'Data Updated successfully',
                'status code': status.HTTP_200_OK
            }
        except Exception as e:
            return JsonResponse({'error': str(e), "status code":status.HTTP_500_INTERNAL_SERVER_ERROR}) 
        return JsonResponse(response_data)
    
#update employee Details
@method_decorator(csrf_exempt, name='dispatch')
class EmployeeDetailsUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Employee_Detail.objects.all()
    serializer_class = EmployeeDetailsSerializer
    lookup_fields = ('ee_id', 'cid')  # Corrected to a tuple for multiple fields

    def get_object(self):
        """
        Overriding `get_object` to fetch the instance based on multiple fields.
        """
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {field: self.kwargs[field] for field in self.lookup_fields}
        obj = queryset.filter(**filter_kwargs).first()
        if not obj:
            raise Exception(f"Object not found with {filter_kwargs}")
        return obj

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Logging the update action
            LogEntry.objects.create(
                action='Employee details updated',
                details=f'Employee details updated successfully for Employee ID {instance.ee_id}'
            )

            # Preparing the response data
            response_data = {
                'success': True,
                'message': 'Data updated successfully',
                'status_code': status.HTTP_200_OK
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse(
                {'error': str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



    
#update employee Details
@method_decorator(csrf_exempt, name='dispatch')
class CompanyDetailsUpdateAPIView(RetrieveUpdateAPIView):
    queryset = company_details.objects.all()
    serializer_class = company_details_serializer
    lookup_fields = ('cid')

    def get_object(self):
        """
        Overriding `get_object` to fetch the instance based on multiple fields.
        """
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {field: self.kwargs[field] for field in self.lookup_fields}
        obj = queryset.filter(**filter_kwargs).first()
        if not obj:
            raise Exception(f"Object not found with {filter_kwargs}")
        return obj

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Logging the update action
            LogEntry.objects.create(
                action='Company details updated',
                details=f'Company details updated successfully for Employee ID {instance.cid}'
            )

            # Preparing the response data
            response_data = {
                'success': True,
                'message': 'Data updated successfully',
                'status_code': status.HTTP_200_OK
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse(
                {'error': str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(csrf_exempt, name='dispatch')
class CompanyDetailsUpdateAPIView(RetrieveUpdateAPIView):
    queryset = company_details.objects.all()
    serializer_class = company_details_serializer
    lookup_fields = ('cid')

    def get_object(self):
        """
        Overriding `get_object` to fetch the instance based on multiple fields.
        """
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {field: self.kwargs[field] for field in self.lookup_fields}
        obj = queryset.filter(**filter_kwargs).first()
        if not obj:
            raise Exception(f"Object not found with {filter_kwargs}")
        return obj

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Logging the update action
            LogEntry.objects.create(
                action='Company details updated',
                details=f'Company details updated successfully for Employee ID {instance.cid}'
            )

            # Preparing the response data
            response_data = {
                'success': True,
                'message': 'Data updated successfully',
                'status_code': status.HTTP_200_OK
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse(
                {'error': str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#PDF upload view
@transaction.atomic
def PDFFileUploadView(request, employer_id):
    try:
        if request.method == 'POST':
            form = PDFUploadForm(request.POST, request.FILES)
            if form.is_valid():
                pdf_file = form.cleaned_data['pdf_file']
                pdf_name = pdf_file.name
    
                # Store PDF file data in the database with the correct model fields
                pdf_record = IWOPDFFile(pdf_name=pdf_name, pdf=pdf_file, employer_id=employer_id)
                pdf_record.save()
                LogEntry.objects.create(
                action='IWO PDF file Uploaded',
                details=f'IWO PDF file has been successfully Uploaded for Employer ID {employer_id}')
                return HttpResponse("File uploaded successfully.")      
        else:
            form = PDFUploadForm()
    except Exception as e:
        return JsonResponse({'error': str(e), status:status.HTTP_500_INTERNAL_SERVER_ERROR})  
    
    return render(request, 'upload_pdf.html', {'form': form})




# #Get Employer Details on the bases of Employer_ID
# @api_view(['GET'])
# def get_employee_by_employer_id(self, employer_id):
#     employees=Employee_Detail.objects.filter(employer_id=employer_id)
#     instance = self.get_object()
#     if employees.exists():
#         try:
#             serializer = EmployeeDetailsSerializer(employees, many=True)
#             response_data = {
#                     'success': True,
#                     'message': 'Data Get successfully',
#                     'status code': status.HTTP_200_OK}
#             response_data['data'] = serializer.data
#             return JsonResponse(response_data)

#         except Employee_Detail.DoesNotExist:
#             return JsonResponse({'message': 'Data not found', 'status code':status.HTTP_404_NOT_FOUND})
#     else:
#         return JsonResponse({'message': 'Employer ID not found', 'status code':status.HTTP_404_NOT_FOUND})



# @api_view(['GET'])
# def get_employee_by_employer_id(request, cid):
# # <<<<<<< HEAD
#     try:
#         # Check if employer_id is valid and query the database
#         employees = Employee_Detail.objects.filter(cid=cid)
        
#         if employees.exists():
# # =======
#     employees=Employee_Detail.objects.filter(cid=cid)
#     if employees.exists():
#         try:
#             serializer = EmployeeDetailsSerializer(employees, many=True)
#             response_data = {
#                 'success': True,
#                 'message': 'Data retrieved successfully',
#                 'status_code': status.HTTP_200_OK,
#                 'data': serializer.data,
#             }
#             return JsonResponse(response_data, status=status.HTTP_200_OK)
#         else:
#             return JsonResponse(
#                 {'success': False, 'message': 'Employer ID not found', 'status_code': status.HTTP_404_NOT_FOUND},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#     except ValueError:
#         # Handle the case where employer_id is invalid
#         return JsonResponse(
#             {'success': False, 'message': 'Invalid Employer ID format', 'status_code': status.HTTP_400_BAD_REQUEST},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#     except Exception as e:
#         # Catch any other unexpected errors
#         return JsonResponse(
#             {'success': False, 'message': f'An error occurred: {str(e)}', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR


        # )


@api_view(['GET'])
def get_employee_by_employer_id(request, cid):
    employees=Employee_Detail.objects.filter(cid=cid)
    if employees.exists():
        try:
            serializer = EmployeeDetailsSerializer(employees, many=True)
            response_data = {
                    'success': True,
                    'message': 'Data Get successfully',
                    'status code': status.HTTP_200_OK}
            response_data['data'] = serializer.data
            return JsonResponse(response_data)
        except Employee_Detail.DoesNotExist:
            return JsonResponse({'message': 'Data not found', 'status code':status.HTTP_404_NOT_FOUND})
    else:
        return JsonResponse({'message': 'Employer ID not found', 'status code':status.HTTP_404_NOT_FOUND})
    

@api_view(['GET'])
def get_order_details(request, cid):
    employees=garnishment_order.objects.filter(cid=cid)
    if employees.exists():
        try:
            serializer = garnishment_order_serializer(employees, many=True)
            response_data = {
                    'success': True,
                    'message': 'Data Get successfully',
                    'status code': status.HTTP_200_OK}
            response_data['data'] = serializer.data
            return JsonResponse(response_data)
        except Employee_Detail.DoesNotExist:
            return JsonResponse({'message': 'Data not found', 'status code':status.HTTP_404_NOT_FOUND})
        except Exception as e:
            return JsonResponse({'error': str(e), status:status.HTTP_500_INTERNAL_SERVER_ERROR})  

    else:
        return JsonResponse({'message': 'Company ID not found', 'status code':status.HTTP_404_NOT_FOUND})



@api_view(['GET'])
def get_single_employee_details(request, cid,ee_id):
    employees=Employee_Detail.objects.filter(cid=cid,ee_id=ee_id)
    if employees.exists():
        try:
            serializer = EmployeeDetailsSerializer(employees, many=True)
            response_data = {
                    'success': True,
                    'message': 'Data Get successfully',
                    'status code': status.HTTP_200_OK}
            response_data['data'] = serializer.data
            return JsonResponse(response_data)
        except Employee_Detail.DoesNotExist:
            return JsonResponse({'message': 'Data not found', 'status code':status.HTTP_404_NOT_FOUND})
    else:
        return JsonResponse({'message': 'Employer ID not found', 'status code':status.HTTP_404_NOT_FOUND})


#Get Employer Details from employer ID
@api_view(['GET'])
def get_employer_details(request, employer_id):
    employees=Employer_Profile.objects.filter(employer_id=employer_id)
    if employees.exists():
        try:
            serializer = GetEmployerDetailsSerializer(employees, many=True)
            response_data = {
                    'success': True,
                    'message': 'Data Get successfully',
                    'status code': status.HTTP_200_OK}
            response_data['data'] = serializer.data
            return JsonResponse(response_data)
        except Employer_Profile.DoesNotExist:
            return JsonResponse({'message': 'Data not found', 'status code':status.HTTP_404_NOT_FOUND})
    else:
        return JsonResponse({'message': 'Employer ID not found', 'status code':status.HTTP_404_NOT_FOUND})
    


@csrf_exempt
def insert_iwo_detail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cid = data.get('cid')
            ee_id = data.get('ee_id')
            IWO_Status = data.get('IWO_Status')

            # Validate required fields
            if cid is None or ee_id is None or IWO_Status is None:
                return JsonResponse({'error': 'Missing required fields','code':status.HTTP_400_BAD_REQUEST})

            # Create a new IWO_Details_PDF instance and save it to the database
            iwo_detail = IWO_Details_PDF(
                cid=cid,
                ee_id=ee_id,
                IWO_Status=IWO_Status
            )
            iwo_detail.save()
            return JsonResponse({'message': 'IWO detail inserted successfully', 'code' :status.HTTP_201_CREATED})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON', 'status_code':status.HTTP_400_BAD_REQUEST})
        except Exception as e:
            return JsonResponse({'error': str(e),'status code': status.HTTP_500_INTERNAL_SERVER_ERROR})

    return JsonResponse({'error': 'Invalid request method', 'status code': status.HTTP_405_METHOD_NOT_ALLOWED})


@csrf_exempt
def get_dashboard_data(request):
    try:
        total_iwo = IWO_Details_PDF.objects.count()
    
        employees_with_single_iwo = IWO_Details_PDF.objects.values('cid').annotate(iwo_count=Count('cid')).filter(iwo_count=1).count()
    
        employees_with_multiple_iwo = IWO_Details_PDF.objects.values('cid').annotate(iwo_count=Count('cid')).filter(iwo_count__gt=1).count()
    
        active_employees = IWO_Details_PDF.objects.filter(IWO_Status='active').count()
    
        data = {
            'Total_IWO': total_iwo,
            'Employees_with_Single_IWO': employees_with_single_iwo,
            'Employees_with_Multiple_IWO': employees_with_multiple_iwo,
            'Active_employees': active_employees,
        }
    except Exception as e:
        return JsonResponse({'error': str(e), "status code":status.HTTP_500_INTERNAL_SERVER_ERROR}) 
    response_data = {
        'success': True,
        'message': 'Data Get successfully',
        'status code': status.HTTP_200_OK,
        'data' : data}
    return JsonResponse(response_data)


@csrf_exempt
def DepartmentViewSet(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['department_name', 'employer_id']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            if missing_fields:
                return JsonResponse({'error': f'Required fields are missing: {", ".join(missing_fields)}','status_code':status.HTTP_400_BAD_REQUEST})
            if Department.objects.filter(department_name=data['department_name']).exists():
                 return JsonResponse({'error': 'Department already exists', 'status_code':status.HTTP_400_BAD_REQUEST})            
            user = Department.objects.create(**data)
            LogEntry.objects.create(
            action='Department details added',
            details=f'Department details added successfully for Department ID{user.department_id}'
            ) 
            return JsonResponse({'message': 'Department Details Successfully Registered'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'error': str(e), "status code":status.HTTP_500_INTERNAL_SERVER_ERROR}) 
    else:
        return JsonResponse({'message': 'Please use POST method','status code':status.HTTP_400_BAD_REQUEST})


@csrf_exempt
def LocationViewSet(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['employer_id','state','city']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            if missing_fields:
                return JsonResponse({'error': f'Required fields are missing: {", ".join(missing_fields)}','status_code':status.HTTP_400_BAD_REQUEST})
            user = Location.objects.create(**data)
            LogEntry.objects.create(
            action='Location details added',
            details=f'Location details added successfully for Location ID{user.location_id}'
            ) 
            return JsonResponse({'message': 'Location Details Successfully Registered', "status code" :status.HTTP_201_CREATED})
        except Exception as e:
            return JsonResponse({'error': str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR}) 
    else:
        return JsonResponse({'message': 'Please use POST method','status code':status.HTTP_400_BAD_REQUEST})
    


# For  Deleting the Employee Details
@method_decorator(csrf_exempt, name='dispatch')
class EmployeeDeleteAPIView(DestroyAPIView):

        queryset = Employee_Detail.objects.all()
        lookup_field = 'ee_id'

        def get_object(self):
            ee_id = self.kwargs.get('ee_id')
            cid = self.kwargs.get('cid')
            return Employee_Detail.objects.get(ee_id=ee_id, cid=cid)

        @csrf_exempt
        def delete(self, request, *args, **kwargs):
            instance = self.get_object()
            self.perform_destroy(instance)
            LogEntry.objects.create(
                action='Employee details Deleted',
                details=f'Employee details Deleted successfully with Employee ID {instance.ee_id} and Employer ID {instance.cid}'
            )
            response_data = {
                'success': True,
                'message': 'Employee Data Deleted successfully',
                'status code': status.HTTP_200_OK
            }
            return JsonResponse(response_data)
        

           
# For Deleting the Tax Details
@method_decorator(csrf_exempt, name='dispatch')
class CompanyDeleteAPIView(DestroyAPIView):
    queryset = company_details.objects.all()
    lookup_field = 'cid'
    @csrf_exempt
    def get_object(self):
        cid = self.kwargs.get('cid')

        return company_details.objects.get(cid=cid)
    
    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        LogEntry.objects.create(
        action='Company details deleted',
        details=f'Company details Deleted successfully with Company ID {instance.cid}'
            ) 
        response_data = {
                'success': True,
                'message': 'Company Data Deleted successfully',
                'status code': status.HTTP_200_OK}
        return JsonResponse(response_data)
    


# For Deleting the Location Details
@method_decorator(csrf_exempt, name='dispatch')
class GarOrderDeleteAPIView(DestroyAPIView):
    queryset = garnishment_order.objects.all()
    lookup_field = 'case_id'
    @csrf_exempt
    def get_object(self):
        case_id = self.kwargs.get('case_id')
        return self.queryset.filter(case_id=case_id)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        LogEntry.objects.create(
            action='Garnishment order details Deleted',
            details=f'Garnishment order deleted successfully with Case ID'
        )
        response_data = {
            'success': True,
            'message': 'Garnishment order Data Deleted successfully',
            'status code': status.HTTP_200_OK
        }
        return JsonResponse(response_data)
    


# For Deleting the Department Details
@method_decorator(csrf_exempt, name='dispatch')
class DepartmentDeleteAPIView(DestroyAPIView):
    queryset = Department.objects.all()
    lookup_field = 'department_id' 

    def get_object(self):
        department_id = self.kwargs.get('department_id')
        employer_id = self.kwargs.get('employer_id')  
        return self.queryset.filter(department_id=department_id, employer_id=employer_id).first()  
    
    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        LogEntry.objects.create(
        action='Department details Deleted',
        details=f'Department details Deleted successfully with ID {instance.department_id} and Employer ID {instance.employer_id}'
            ) 
        response_data = {
                'success': True,
                'message': 'Department Data Deleted successfully',
                'status code': status.HTTP_200_OK}
        return JsonResponse(response_data)
    

# Export employee details into the csv
@api_view(['GET'])
def export_employee_data(request, cid):
    try:
        employees = Employee_Detail.objects.filter(cid=cid)
        if not employees.exists():
            return JsonResponse({'detail': 'No employees found for this employer ID', 'status': status.HTTP_404_NOT_FOUND})

        serializer = EmployeeDetailsSerializer(employees, many=True)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="employees_{cid}.csv"'

        writer = csv.writer(response)

        # Updated header fields
        header_fields = [
            'ee_id', 'cid', 'age', 'social_security_number',
            'is_blind', 'home_state', 'work_state', 'gender', 'pay_period',
            'number_of_exemptions', 'filing_status', 'marital_status',
            'number_of_student_default_loan', 'support_second_family',
            'spouse_age', 'is_spouse_blind'
        ]
        writer.writerow(header_fields)

        # Write rows dynamically
        for employee in serializer.data:
            row = [employee.get(field, '') for field in header_fields]
            writer.writerow(row)

        return response

    except Exception as e:
        return JsonResponse({'detail': str(e), 'status code ': status.HTTP_500_INTERNAL_SERVER_ERROR})


@api_view(['GET'])
def export_company_data(request):
    try:
        employees = company_details.objects.all()
        if not employees.exists():
            return JsonResponse({'detail': 'No employees found for this employer ID', 'status': status.HTTP_404_NOT_FOUND})

        serializer = company_details_serializer(employees, many=True)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="company_data.csv"'

        writer = csv.writer(response)

        # Updated header fields
        header_fields = ['cid','ein','company_name','registered_address','zipcode','state','dba_name','bank_name','bank_account_number','location']
        writer.writerow(header_fields)

        # Write rows dynamically
        for employee in serializer.data:
            row = [employee.get(field, '') for field in header_fields]
            writer.writerow(row)

        return response

    except Exception as e:
        return JsonResponse({'detail': str(e), 'status code ': status.HTTP_500_INTERNAL_SERVER_ERROR})




#Import employee details using the Excel file
class EmployeeImportView(APIView):
    def post(self, request, employer_id):
        try:
            if 'file' not in request.FILES:
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            file = request.FILES['file']
            file_name = file.name
    
            # Check the file extension
            if file_name.endswith('.csv'):
                df = pandas.read_csv(file)
            elif file_name.endswith(('.xlsx','.xls', '.xlsm', '.xlsb', '.odf', '.ods','.odt')):
                df = pandas.read_excel(file)
            else:
                return Response({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=status.HTTP_400_BAD_REQUEST)
            df['employer_id'] = employer_id        
            employees = []
            for _, row in df.iterrows():
                employee_data={
                'employee_name':row['employee_name'],
                'department':row['department'],
                'pay_cycle':row['pay_cycle'],
                'number_of_child_support_order':row['number_of_child_support_order'],
                'location':row['location'],
                'employer_id': row['employer_id'] 
                }
                # employer = get_object_or_404(Employee_Detail, employer_id=employer_id)
    
                serializer = EmployeeDetailsSerializer(data=employee_data)
                if serializer.is_valid():
                    employees.append(serializer.save())   
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            LogEntry.objects.create(
            action='Employee details Imported',
            details=f'Employee details Imported successfully using excel file with empployer ID {employer_id}')
        except Exception as e:
            return JsonResponse({'error': str(e), "status code":status.HTTP_500_INTERNAL_SERVER_ERROR}) 
        
        return Response({"message": "File processed successfully", "status code" :status.HTTP_201_CREATED})


#Extracting the Last Five record from the Log Table
class LastFiveLogsView(APIView):
    def get(self, request, format=None):
        try:
           logs = LogEntry.objects.order_by('-timestamp')[:5]
           serializer = LogSerializer(logs, many=True)
           response_data = {
                       'success': True,
                       'message': 'Data Get successfully',
                       'status code': status.HTTP_200_OK,
                      'data' : serializer.data}
           return JsonResponse(response_data)
        except Exception as e:
            return Response({"error": str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})


#Extracting the ALL Employer Detials  
class EmployerProfileList(APIView):
    def get(self, request, format=None):
        try:
            employees = Employer_Profile.objects.all()
            serializer = EmployerProfileSerializer(employees, many=True)
            response_data = {
                'success': True,
                'message': 'Data retrieved successfully',
                'status_code': status.HTTP_200_OK,
                'data': serializer.data
            }
            return JsonResponse(response_data)
        except Exception as e:
            return Response({"error": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})


#Extracting the ALL Employee Details 
class EmployeeDetailsList(APIView):
    def get(self, request, format=None):
        try:
            employees = Employee_Detail.objects.all()
            serializer = EmployeeDetailsSerializer(employees, many=True)
            response_data = {
                        'success': True,
                        'message': 'Data Get successfully',
                        'status code': status.HTTP_200_OK,
                        'data' : serializer.data}
            return JsonResponse(response_data)
        except Exception as e:
            return Response({"error": str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})



class GETGarnishmentFeesStatesRule(APIView):
    def get(self, request, format=None):
        try:
            employees = garnishment_fees_states_rule.objects.all()
            serializer = garnishment_fees_states_rule_serializer(employees, many=True)
            response_data = {
                        'success': True,
                        'message': 'Data Get successfully',
                        'status code': status.HTTP_200_OK,
                        'data' : serializer.data}
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

class GarFeesRulesUpdateAPIView(APIView):
    def put(self, request, rule):
        try:
            # Get the object to update
            employees = garnishment_fees_rules.objects.filter(rule=rule)
            
            if not employees.exists():
                return Response(
                    {
                        "success": False,
                        "message": "No records found for the given rule",
                        "status_code": status.HTTP_404_NOT_FOUND,
                    }
                )

            # Use first() to get the single instance
            serializer = garnishment_fees_rules_serializer(
                employees.first(), data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Data updated successfully",
                        "status_code": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



@api_view(['GET'])
def GETGarnishmentFeesRules(request,rule):
    employees=garnishment_fees_rules.objects.filter(rule=rule)

    if employees.exists():
        try:
            serializer = garnishment_fees_rules_serializer(employees, many=True)
            response_data = {
                        'success': True,
                        'message': 'Data Get successfully',
                        'status code': status.HTTP_200_OK,
                        'data' : serializer.data}
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Rule not found', 'status code':status.HTTP_404_NOT_FOUND})





@api_view(['GET'])
def garnishment_fees_rules_based_on_state(request, state):
    state = state.lower()
    employees = garnishment_fees_states_rule.objects.filter(state=state)

    if employees:
        try:
            serializer = garnishment_fees_states_rule_serializer(employees, many=True)
            response_data = {
                'success': True,
                'message': 'Data retrieved successfully',
                'status_code': status.HTTP_200_OK,
                'data': serializer.data
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred while processing your request',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JsonResponse({
        'success': False,
        'message': 'Rule not found',
        'status_code': status.HTTP_404_NOT_FOUND
    }, status=status.HTTP_404_NOT_FOUND)


class CompanyDetails(APIView):
    def get(self, request, format=None):
        try:
            employees = company_details.objects.all()
            serializer = company_details_serializer(employees, many=True)
            response_data = {
                        'success': True,
                        'message': 'Data Get successfully',
                        'status code': status.HTTP_200_OK,
                        'data' : serializer.data}
            return JsonResponse(response_data)
        except Exception as e:
            return Response({"error": str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})




@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = Employer_Profile.objects.get(email=email)
        except Employer_Profile.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        token = RefreshToken.for_user(user).access_token
        # Change this URL to point to your frontend
        reset_url = f'https://garnishment-react-main.vercel.app/reset-password/{str(token)}'
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_url}',
            'your-email@example.com',
            [email],
        )
        return Response({"message": "Password reset link sent.", "status code":status.HTTP_200_OK})



class PasswordResetConfirmView(APIView):
    def post(self, request, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['password']
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = Employer_Profile.objects.get(employer_id=user_id)
            user.set_password(new_password)
            user.save()
            employee = get_object_or_404(Employer_Profile, employer_name=user.employer_name, employer_id=user.employer_id)
            application_activity.objects.create(
                action='Forget Pasword',
                details=f'Employer {employee.employer_name} successfully forget password with ID {employee.employer_id}. '
            )
        except (Employer_Profile.DoesNotExist, TokenError) as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR})
        return Response({"message": "Password reset successful.", "status code":status.HTTP_200_OK})




@csrf_exempt
def SettingPostAPI(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['modes','visibilitys','employer_id']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            if missing_fields:
                return JsonResponse({'error': f'Required fields are missing: {", ".join(missing_fields)}','status_code':status.HTTP_400_BAD_REQUEST})
            
            user = setting.objects.create(**data)
            LogEntry.objects.create(
            action='setting details added',
            details=f'setting details added successfully'
            ) 
            return JsonResponse({'message': 'Setting Details Successfully Registered', "status code" :status.HTTP_201_CREATED})
        except Exception as e:
            return JsonResponse({'error': str(e), "status code" :status.HTTP_500_INTERNAL_SERVER_ERROR}) 
    else:
        return JsonResponse({'message': 'Please use POST method','status code':status.HTTP_400_BAD_REQUEST})

class GETSettingDetails(APIView):
    def get(self, request, employer_id):
        employees = setting.objects.filter(employer_id=employer_id)
        if employees.exists():
            try:
                employee = employees.first() 
                serializer = setting_Serializer(employee)
                response_data = {
                    'success': True,
                    'message': 'Data retrieved successfully',
                    'status code': status.HTTP_200_OK,
                    'data' : serializer.data
                    }
                return JsonResponse(response_data)
            except setting.DoesNotExist:
                return JsonResponse({'message': 'Data not found', 'status code': status.HTTP_404_NOT_FOUND})
        else:
            return JsonResponse({'message': 'Employee ID not found', 'status code': status.HTTP_404_NOT_FOUND})




class convert_excel_to_json(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        try:
            if not file:
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

            # try:
            # Load the Excel workbook

            employee_details = pd.read_excel(file, sheet_name='Employee Details ')
            garnishment_order_details = pd.read_excel(file, sheet_name='Garnishment Order details')
            payroll_batch_details = pd.read_excel(file, sheet_name='Payroll Batch Details', header=[0, 1])
            # Concatenate the DataFrames
            concatenated_df = pd.concat([employee_details, garnishment_order_details, payroll_batch_details], axis=1)
            # Column cleanup
            concatenated_df.columns = concatenated_df.columns.map(
                lambda x: '_'.join(str(i) for i in x) if isinstance(x, tuple) else x
            )

            concatenated_df.rename(columns={
                "Deductions 401K": 'Deductions 401(K)',
                "Deductions_MedicalInsurance": 'medical_insurance',
                "Deductions_SDI": 'SDI',
                "Deductions_UnionDues": 'union_dues',
                "Deductions_Voluntary": 'voluntary',
                "GrossPay_Unnamed: 6_level_1": 'gross_pay',
                "NetPay_Unnamed: 17_level_1": 'net_pay',
                "PayPeriod_Unnamed: 3_level_1": 'Pay cycle',
                "PayPeriod": "pay_period",
                "PayDate_Unnamed: 5_level_1": 'Pay Date',
                "PayrollDate_Unnamed: 4_level_1": 'Payroll Date',
                "State Unnamed: 2_level_1": 'state',
                'Taxes_FederalIncomeTax': 'federal_income_tax',
                'Taxes_StateTax': 'state_tax',
                'Taxes_LocalTax': 'local_tax',
                "FilingStatus":'filing_status',

                'Taxes_SocialSecurityTax': 'social_security_tax',
                'Taxes_MedicareTax': 'medicare_tax',
            }, inplace=True)


            # Create a dictionary mapping merged_df column names to JSON keys
            column_mapping = {
                'EEID': 'ee_id',
                "CID": 'cid',
                'IsBlind': 'is_blind',
                'Age': 'age',
                'FilingStatus': 'filing_status',
                'SupportSecondFamily': 'support_second_family',
                'SpouseAge ': 'spouse_age',
                'IsSpouseBlind': 'is_spouse_blind',
                'Amount': 'amount',
                'ArrearsGreaterThan12Weeks': 'arrears_greater_than_12_weeks',
                "CaseID":'case_id',
                'TotalExemptions':'no_of_exception_for_self',
                'WorkState':'Work State',
                'HomeState':'Home State',
                'NumberofStudentLoan' : 'no_of_student_default_loan',
                'No.OFExemptionIncludingSelf':'no_of_exception_for_self',
                "Type":"garnishment_type",
                "ArrearAmount":"arrear",
                "State":"state"
            }
            concatenated_df = concatenated_df.rename(columns=column_mapping)
            concatenated_df = concatenated_df.loc[:, ~concatenated_df.columns.duplicated(keep='first')] 


            # print(concatenated_df.columns)
            # Data preparation
            concatenated_df['filing_status'] = concatenated_df['filing_status'].str.lower().str.replace(' ', '_')
            concatenated_df['batch_id'] = "B001A"
            concatenated_df['arrears_greater_than_12_weeks'] = concatenated_df['arrears_greater_than_12_weeks'].replace(
                {True: "Yes", False: "No"}
            )
            concatenated_df['support_second_family'] = concatenated_df['support_second_family'].replace(
                {True: "Yes", False: "No"}
            )
            concatenated_df['garnishment_type'] = concatenated_df['garnishment_type'].replace(
                {'Student Loan': "student default loan"}
            )
            concatenated_df['filing_status'] = concatenated_df['filing_status'].apply(
                lambda x: 'married_filing_separate' if x == 'married_filing_separate_return' else x
            )
            concatenated_df = concatenated_df.fillna(0)
            # print(concatenated_df.columns)
            # Create JSON structure
            output_json = {}
            for (batch_id, cid), group in concatenated_df.groupby(["batch_id", "cid"]):
                employees = []
                for _, row in group.iterrows():
                    employee = {
                        "ee_id": row["ee_id"],
                        "gross_pay": row["gross_pay"],
                        "state": row["state"],
                        "no_of_exemption_for_self": row["no_of_exception_for_self"],
                        "pay_period": row["pay_period"],
                        "filing_status": row["filing_status"],
                        "net_pay": row["net_pay"],
                        "payroll_taxes": [
                            {"federal_income_tax": row["federal_income_tax"]},
                            {"social_security_tax": row["social_security_tax"]},
                            {"medicare_tax": row["medicare_tax"]},
                            {"state_tax": row["state_tax"]},
                            {"local_tax": row["local_tax"]}
                        ],
                        "payroll_deductions": {
                            "medical_insurance": row["medical_insurance"]
                        },
                        "age": row["age"],
                        "is_blind": row["is_blind"],
                        "is_spouse_blind": row["is_spouse_blind"],
                        "spouse_age": row["spouse_age"],
                        "support_second_family": row["support_second_family"],
                        "no_of_student_default_loan": row["no_of_student_default_loan"],
                        "arrears_greater_than_12_weeks": row["arrears_greater_than_12_weeks"],
                        "garnishment_data": [
                            {
                                "type": row["garnishment_type"],
                                "data": [
                                    {
                                        "case_id": row["case_id"],
                                        "amount": row["amount"],
                                        "arrear": row["arrear"]
                                    }
                                ]
                            }
                        ]
                    }
                    employees.append(employee)

                output_json["batch_id"] = batch_id  # Add batch_id key as a top-level key
                if "cid" not in output_json:
                    output_json["cid"] = {}  # Create "cid" as a top-level key
                output_json["cid"][cid] = {"employees": employees}
            return Response(output_json, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class APICallCountView(APIView):
    def get(self, request):
        logs = APICallLog.objects.values('date', 'endpoint', 'count')
        return Response(logs)


# @csrf_exempt
# def import_employees_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  # Uploaded file
#         file_name = file.name  # Get the name of the uploaded file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Handle file formats
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Process the data from DataFrame
#             for _, row in df.iterrows():
#                 # Check if the employee exists
#                 employee = Employee_Detail.objects.filter(ee_id=row['ee_id']).first()

#                 if employee:
#                     # Detect changes in employee data
#                     has_changes = (
#                         employee.cid != row['cid'] or
#                         employee.age != int(row['age']) or
#                         employee.social_security_number != row['social_security_number'] or
#                         employee.blind != (str(row['blind']).lower() == 'true') or
#                         employee.home_state != row['home_state'] or
#                         employee.work_state != row['work_state'] or
#                         employee.gender != row.get('gender', None) or
#                         employee.pay_period != row['pay_period'] or
#                         employee.number_of_exemptions != int(row['number_of_exemptions']) or
#                         employee.filing_status != row['filing_status'] or
#                         employee.marital_status != row['marital_status'] or
#                         employee.number_of_student_default_loan != int(row['number_of_student_default_loan']) or
#                         employee.support_second_family != (str(row['support_second_family']).lower() == 'true') or
#                         employee.spouse_age != int(row.get('spouse_age', 0)) or
#                         employee.is_spouse_blind != (str(row.get('is_spouse_blind', '')).lower() == 'true')
#                     )

#                     if has_changes:
#                         # Update employee details
#                         employee.cid = row['cid']
#                         employee.age = int(row['age'])
#                         employee.social_security_number = row['social_security_number']
#                         employee.blind = str(row['blind']).lower() == 'true'
#                         employee.home_state = row['home_state']
#                         employee.work_state = row['work_state']
#                         employee.gender = row.get('gender', None)
#                         employee.pay_period = row['pay_period']
#                         employee.number_of_exemptions = int(row['number_of_exemptions'])
#                         employee.filing_status = row['filing_status']
#                         employee.marital_status = row['marital_status']
#                         employee.number_of_student_default_loan = int(row['number_of_student_default_loan'])
#                         employee.support_second_family = str(row['support_second_family']).lower() == 'true'
#                         employee.spouse_age = int(row.get('spouse_age', 0))
#                         employee.is_spouse_blind = str(row.get('is_spouse_blind', '')).lower() == 'true'
#                         employee.save()
#                         updated_employees.append(employee.ee_id)
#                 else:
#                     # Add new employee
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=int(row['age']),
#                         social_security_number=row['social_security_number'],
#                         blind=str(row['blind']).lower() == 'true',
#                         home_state=row['home_state'],
#                         work_state=row['work_state'],
#                         gender=row.get('gender', None),
#                         pay_period=row['pay_period'],
#                         number_of_exemptions=int(row['number_of_exemptions']),
#                         filing_status=row['filing_status'],
#                         marital_status=row['marital_status'],
#                         number_of_student_default_loan=int(row['number_of_student_default_loan']),
#                         support_second_family=str(row['support_second_family']).lower() == 'true',
#                         spouse_age=int(row.get('spouse_age', 0)),
#                         is_spouse_blind=str(row.get('is_spouse_blind', '')).lower() == 'true'
#                     )
#                     added_employees.append(row['ee_id'])

#             # Prepare response
#             response_data = []
#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })
#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
#WORKING
#new logic for data insertation in the employee table
# @csrf_exempt
# def import_employees_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  # Uploaded file
#         file_name = file.name  # Get the name of the uploaded file
#         updated_employees = []
#         added_employees = []
#         no_changes = []


#         try:
#             # Handle file formats
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Process the data from DataFrame
#             for _, row in df.iterrows():
#                 # Check if the employee exists
#                 employee = Employee_Detail.objects.filter(ee_id=row['ee_id']).first()

#                 if employee:
#                     # Detect changes in employee data
#                     has_changes = (
#                         employee.cid != row['cid'] or
#                         employee.age != int(row['age']) or
#                         employee.social_security_number != row['social_security_number'] or
#                         employee.blind != (str(row['blind']).lower() == 'true') or
#                         employee.home_state != row['home_state'] or
#                         employee.work_state != row['work_state'] or
#                         employee.gender != row.get('gender', None) or
#                         employee.pay_period != row['pay_period'] or
#                         employee.number_of_exemptions != int(row['number_of_exemptions']) or
#                         employee.filing_status != row['filing_status'] or
#                         employee.marital_status != row['marital_status'] or
#                         employee.number_of_student_default_loan != int(row['number_of_student_default_loan']) or
#                         employee.support_second_family != (str(row['support_second_family']).lower() == 'true') or
#                         employee.spouse_age != int(row.get('spouse_age', 0)) or
#                         employee.is_spouse_blind != (str(row.get('is_spouse_blind', '')).lower() == 'true')
#                     )

#                     if has_changes:
#                         # Update employee details
#                         employee.cid = row['cid']
#                         employee.age = int(row['age'])
#                         employee.social_security_number = row['social_security_number']
#                         employee.blind = str(row['blind']).lower() == 'true'
#                         employee.home_state = row['home_state']
#                         employee.work_state = row['work_state']
#                         employee.gender = row.get('gender', None)
#                         employee.pay_period = row['pay_period']
#                         employee.number_of_exemptions = int(row['number_of_exemptions'])
#                         employee.filing_status = row['filing_status']
#                         employee.marital_status = row['marital_status']
#                         employee.number_of_student_default_loan = int(row['number_of_student_default_loan'])
#                         employee.support_second_family = str(row['support_second_family']).lower() == 'true'
#                         employee.spouse_age = int(row.get('spouse_age', 0))
#                         employee.is_spouse_blind = str(row.get('is_spouse_blind', '')).lower() == 'true'
#                         employee.save()
#                         updated_employees.append(employee.ee_id)
#                     else:
#                         #No_changes_detected
#                         no_changes.append(employee.ee_id)
#                 else:
#                     # Add new employee
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=int(row['age']),
#                         social_security_number=row['social_security_number'],
#                         blind=str(row['blind']).lower() == 'true',
#                         home_state=row['home_state'],
#                         work_state=row['work_state'],
#                         gender=row.get('gender', None),
#                         pay_period=row['pay_period'],
#                         number_of_exemptions=int(row['number_of_exemptions']),
#                         filing_status=row['filing_status'],
#                         marital_status=row['marital_status'],
#                         number_of_student_default_loan=int(row['number_of_student_default_loan']),
#                         support_second_family=str(row['support_second_family']).lower() == 'true',
#                         spouse_age=int(row.get('spouse_age', 0)),
#                         is_spouse_blind=str(row.get('is_spouse_blind', '')).lower() == 'true'
#                     )
#                     added_employees.append(row['ee_id'])

#             # Prepare response
#             response_data = []
#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })
#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })
#             if no_changes:
#                 response_data.append({
#                     'message': 'No changes detected for existing employees',
#                     'unchanged_employees': no_changes
#                 })

#             # Check if no data was added, updated, or unchanged
#             if not added_employees and not updated_employees and not no_changes:
#                 return JsonResponse({'message': 'No data was processed.'}, status=200)

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)

#update logic where the data is actually updated
# @csrf_exempt
# def import_employees_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  # Uploaded file
#         file_name = file.name  # Get the name of the uploaded file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Handle file formats
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Process the data from DataFrame
#             for _, row in df.iterrows():
#                 # Check if the employee exists
#                 employee = Employee_Detail.objects.filter(ee_id=row['ee_id']).first()

#                 if employee:
#                     # Detect changes in employee data
#                     has_changes = False
#                     fields_to_update = {}

#                     # Compare fields and add to update list if changed
#                     if employee.cid != row['cid']:
#                         fields_to_update['cid'] = row['cid']
#                     if employee.age != int(row['age']):
#                         fields_to_update['age'] = int(row['age'])
#                     if employee.social_security_number != row['social_security_number']:
#                         fields_to_update['social_security_number'] = row['social_security_number']
#                     if employee.blind != (str(row['blind']).lower() == 'true'):
#                         fields_to_update['blind'] = str(row['blind']).lower() == 'true'
#                     if employee.home_state != row['home_state']:
#                         fields_to_update['home_state'] = row['home_state']
#                     if employee.work_state != row['work_state']:
#                         fields_to_update['work_state'] = row['work_state']
#                     if employee.gender != row.get('gender', None):
#                         fields_to_update['gender'] = row.get('gender', None)
#                     if employee.pay_period != row['pay_period']:
#                         fields_to_update['pay_period'] = row['pay_period']
#                     if employee.number_of_exemptions != int(row['number_of_exemptions']):
#                         fields_to_update['number_of_exemptions'] = int(row['number_of_exemptions'])
#                     if employee.filing_status != row['filing_status']:
#                         fields_to_update['filing_status'] = row['filing_status']
#                     if employee.marital_status != row['marital_status']:
#                         fields_to_update['marital_status'] = row['marital_status']
#                     if employee.number_of_student_default_loan != int(row['number_of_student_default_loan']):
#                         fields_to_update['number_of_student_default_loan'] = int(row['number_of_student_default_loan'])
#                     if employee.support_second_family != (str(row['support_second_family']).lower() == 'true'):
#                         fields_to_update['support_second_family'] = str(row['support_second_family']).lower() == 'true'
#                     if employee.spouse_age != int(row.get('spouse_age', 0)):
#                         fields_to_update['spouse_age'] = int(row.get('spouse_age', 0))
#                     if employee.is_spouse_blind != (str(row.get('is_spouse_blind', '')).lower() == 'true'):
#                         fields_to_update['is_spouse_blind'] = str(row.get('is_spouse_blind', '')).lower() == 'true'

#                     # Update only if changes exist
#                     if fields_to_update:
#                         has_changes = True
#                         for field, value in fields_to_update.items():
#                             setattr(employee, field, value)
#                         employee.save()
                    
#                     if has_changes:
#                         updated_employees.append(employee.ee_id)
#                 else:
#                     # Add new employee
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=int(row['age']),
#                         social_security_number=row['social_security_number'],
#                         blind=str(row['blind']).lower() == 'true',
#                         home_state=row['home_state'],
#                         work_state=row['work_state'],
#                         gender=row.get('gender', None),
#                         pay_period=row['pay_period'],
#                         number_of_exemptions=int(row['number_of_exemptions']),
#                         filing_status=row['filing_status'],
#                         marital_status=row['marital_status'],
#                         number_of_student_default_loan=int(row['number_of_student_default_loan']),
#                         support_second_family=str(row['support_second_family']).lower() == 'true',
#                         spouse_age=int(row.get('spouse_age', 0)),
#                         is_spouse_blind=str(row.get('is_spouse_blind', '')).lower() == 'true'
#                     )
#                     added_employees.append(row['ee_id'])

#             # Prepare response
#             response_data = {}
#             if updated_employees:
#                 response_data['updated_employees'] = updated_employees
#             if added_employees:
#                 response_data['added_employees'] = added_employees

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)

#above code is to see only the emp where the data is updated
#new code for no updates
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from User_app.models import Employee_Detail  # Import your Employee_Detail model
# from django.core.files.storage import default_storage
# import csv
# import pandas as pd

# @csrf_exempt
# def import_employees_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         file_path = default_storage.save(file.name, file)  # Temporarily save the file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Determine the file type
#             if file.name.endswith('.csv'):
#                 # Process CSV file
#                 with open(file_path, 'r') as csvfile:
#                     reader = csv.DictReader(csvfile)
#                     data = list(reader)
#             elif file.name.endswith(('.xls', '.xlsx')):
#                 # Process Excel file
#                 df = pd.read_excel(file_path)
#                 data = df.to_dict(orient='records')  # Convert to list of dictionaries
#             else:
#                 return JsonResponse({'error': 'Unsupported file format. Please upload a CSV or Excel file.'}, status=400)

#             # Process each row
#             for row in data:
#                 try:
#                     # Retrieve the existing employee (if any)
#                     employee = Employee_Detail.objects.get(ee_id=row['ee_id']) 

#                     # Check if any field differs from the incoming data
#                     has_changes = False
#                     for field_name in [
#                         'cid', 'age', 'social_security_number', 'blind', 'home_state', 'work_state',
#                         'gender', 'pay_period', 'number_of_exemptions', 'filing_status', 'marital_status',
#                         'number_of_student_default_loan', 'support_second_family', 'spouse_age', 'is_spouse_blind'
#                     ]: 
#                         if getattr(employee, field_name) != row[field_name]:
#                             has_changes = True
#                             break

#                     if has_changes:
#                         # Update the employee record
#                         employee.cid = row['cid']
#                         employee.age = row['age']
#                         employee.social_security_number = row['social_security_number']
#                         employee.blind = row['blind'] 
#                         employee.home_state = row['home_state']
#                         employee.work_state = row['work_state']
#                         employee.gender = row['gender']
#                         employee.pay_period = row['pay_period']
#                         employee.number_of_exemptions = row['number_of_exemptions']
#                         employee.filing_status = row['filing_status']
#                         employee.marital_status = row['marital_status']
#                         employee.number_of_student_default_loan = row['number_of_student_default_loan']
#                         employee.support_second_family = row['support_second_family']
#                         employee.spouse_age = row['spouse_age']
#                         employee.is_spouse_blind = row['is_spouse_blind']
#                         employee.save()
#                         updated_employees.append(employee.ee_id)
#                 except Employee_Detail.DoesNotExist:
#                     # Add new employee
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=row['age'],
#                         social_security_number=row['social_security_number'],
#                         blind=row['blind'],
#                         home_state=row['home_state'],
#                         work_state=row['work_state'],
#                         gender=row['gender'],
#                         pay_period=row['pay_period'],
#                         number_of_exemptions=row['number_of_exemptions'],
#                         filing_status=row['filing_status'],
#                         marital_status=row['marital_status'],
#                         number_of_student_default_loan=row['number_of_student_default_loan'],
#                         support_second_family=row['support_second_family'],
#                         spouse_age=row['spouse_age'],
#                         is_spouse_blind=row['is_spouse_blind']
#                     )
#                     added_employees.append(row['ee_id'])

#             # Check if any updates or insertions occurred
#             if not updated_employees and not added_employees:
#                 return JsonResponse({'message': 'No data was updated or inserted.'}, status=200)

#             response_data = []

#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })

#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
# #new code for no updates

# ##new1 6:20
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from ..models import Employee_Detail  # Import your Employee_Detail model
# from django.core.files.storage import default_storage
# import csv
# import pandas as pd

# @csrf_exempt
# def import_employees_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         file_path = default_storage.save(file.name, file)  # Temporarily save the file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Determine the file type
#             if file.name.endswith('.csv'):
#                 # Process CSV file
#                 with open(file_path, 'r') as csvfile:
#                     reader = csv.DictReader(csvfile)
#                     data = list(reader)
#             elif file.name.endswith(('.xls', '.xlsx')):
#                 # Process Excel file
#                 df = pd.read_excel(file_path)
#                 data = df.to_dict(orient='records')  # Convert to list of dictionaries
#             else:
#                 return JsonResponse({'error': 'Unsupported file format. Please upload a CSV or Excel file.'}, status=400)

#             # Process each row
#             for row in data:
#                 try:
#                     # Retrieve the existing employee (if any)
#                     employee = Employee_Detail.objects.get(ee_id=row['ee_id']) 

#                     # Check if any field differs from the incoming data
#                     has_changes = False
#                     for field_name in [
#                         'cid', 'age', 'social_security_number', 'home_state', 'work_state',
#                         'pay_period', 'number_of_exemptions', 'filing_status', 'marital_status',
#                         'number_of_student_default_loan', 'support_second_family', 'spouse_age' 
#                     ]: 
#                         if getattr(employee, field_name) != row[field_name]:
#                             has_changes = True
#                             break

#                     # Handle boolean fields separately
#                     if employee.blind != (row['blind'].lower() == 'true' or row['blind'].lower() == 'false'): 
#                         has_changes = True
#                     if employee.is_spouse_blind != (row['is_spouse_blind'].lower() == 'true' or row['is_spouse_blind'].lower() == 'false'):
#                         has_changes = True

#                     if has_changes:
#                         # Update the employee record
#                         employee.cid = row['cid']
#                         employee.age = row['age']
#                         employee.social_security_number = row['social_security_number']
#                         employee.blind = row['blind'].lower() == 'true' 
#                         employee.home_state = row['home_state']
#                         employee.work_state = row['work_state']
#                         employee.gender = row['gender'] 
#                         employee.pay_period = row['pay_period']
#                         employee.number_of_exemptions = row['number_of_exemptions']
#                         employee.filing_status = row['filing_status']
#                         employee.marital_status = row['marital_status']
#                         employee.number_of_student_default_loan = row['number_of_student_default_loan']
#                         employee.support_second_family = row['support_second_family'].lower() == 'true' 
#                         employee.spouse_age = row['spouse_age']
#                         employee.is_spouse_blind = row['is_spouse_blind'].lower() == 'true' 
#                         employee.save()
#                         updated_employees.append(employee.ee_id)
#                 except Employee_Detail.DoesNotExist:
#                     # Add new employee
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=row['age'],
#                         social_security_number=row['social_security_number'],
#                         blind=row['blind'].lower() == 'true', 
#                         home_state=row['home_state'],
#                         work_state=row['work_state'],
#                         gender=row['gender'],
#                         pay_period=row['pay_period'],
#                         number_of_exemptions=row['number_of_exemptions'],
#                         filing_status=row['filing_status'],
#                         marital_status=row['marital_status'],
#                         number_of_student_default_loan=row['number_of_student_default_loan'],
#                         support_second_family=row['support_second_family'].lower() == 'true', 
#                         spouse_age=row['spouse_age'],
#                         is_spouse_blind=row['is_spouse_blind'].lower() == 'true' 
#                     )
#                     added_employees.append(row['ee_id'])

#             # Check if any updates or insertions occurred
#             if not updated_employees and not added_employees:
#                 return JsonResponse({'message': 'No data was updated or inserted.'}, status=200)

#             response_data = []

#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })

#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
# ##new1 6:20
# company data correct working
#code.upsert_file 
# @csrf_exempt
# def upsert_company_details_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  
#         file_name = file.name  
#         updated_companies = []
#         added_companies = []

#         try:
#             # Load data from file
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Iterate through DataFrame rows
#             for _, row in df.iterrows():
#                 company = company_details.objects.filter(cid=row['cid']).first()

#                 if company:
#                     # Check for changes
#                     has_changes = (
#                         company.ein != row['ein'] or
#                         company.company_name != row['company_name'] or
#                         company.zipcode != row['zipcode'] or
#                         company.state != row['state'] or
#                         company.dba_name != row['dba_name'] or
#                         company.bank_name != row.get('bank_name', None) or
#                         company.bank_account_number != row.get('bank_account_number', None) or
#                         company.location != row.get('location', None) or
#                         company.registered_address != row.get('registered_address', None)
#                     )

#                     if has_changes:
#                         # Update company details
#                         company.ein = row['ein']
#                         company.company_name = row['company_name']
#                         company.zipcode = row['zipcode']
#                         company.state = row['state']
#                         company.dba_name = row['dba_name']
#                         company.bank_name = row.get('bank_name', None)
#                         company.bank_account_number = row.get('bank_account_number', None)
#                         company.location = row.get('location', None)
#                         company.registered_address = row.get('registered_address', None)
#                         company.save()
#                         updated_companies.append(company.cid)
#                 else:
#                     # Add new company
#                     company_details.objects.create(
#                         cid=row['cid'],
#                         ein=row['ein'],
#                         company_name=row['company_name'],
#                         zipcode=row['zipcode'],
#                         state=row['state'],
#                         dba_name=row['dba_name'],
#                         bank_name=row.get('bank_name', None),
#                         bank_account_number=row.get('bank_account_number', None),
#                         location=row.get('location', None),
#                         registered_address=row.get('registered_address', None)
#                     )
#                     added_companies.append(row['cid'])

#             # Prepare response
#             response_data = []
#             if added_companies:
#                 response_data.append({
#                     'message': 'Company details imported successfully',
#                     'added_companies': added_companies
#                 })
#             if updated_companies:
#                 response_data.append({
#                     'message': 'Company details updated successfully',
#                     'updated_companies': updated_companies
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)

#code above this line working!

#garnishment_data
#27/01 at 2:51 
#1

# upsert the garnishment data


#friday_11:45 #2
#well working and functional_____________________________
# @csrf_exempt
# def upsert_employees_data_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  # Uploaded file
#         file_name = file.name  # Get the name of the uploaded file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Handle file formats
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Process the data from DataFrame
#             for _, row in df.iterrows():
#                 # Check if the employee exists
#                 employee = Employee_Detail.objects.filter(ee_id=row['ee_id']).first()

#                 if employee:
#                     # Detect changes in employee data
#                     has_changes = (
#                         employee.cid != row['cid'] or
#                         employee.age != int(row['age']) or
#                         employee.social_security_number != row['social_security_number'] or
#                         employee.blind != (str(row['blind']).lower() == 'true') or
#                         employee.home_state != row['home_state'] or
#                         employee.work_state != row['work_state'] or
#                         employee.gender != row.get('gender', None) or
#                         employee.pay_period != row['pay_period'] or
#                         employee.number_of_exemptions != int(row['number_of_exemptions']) or
#                         employee.filing_status != row['filing_status'] or
#                         employee.marital_status != row['marital_status'] or
#                         employee.number_of_student_default_loan != int(row['number_of_student_default_loan']) or
#                         employee.support_second_family != (str(row['support_second_family']).lower() == 'true') or
#                         employee.spouse_age != int(row.get('spouse_age', 0)) or
#                         employee.is_spouse_blind != (str(row.get('is_spouse_blind', '')).lower() == 'true')
#                     )

#                     if has_changes:
#                         # Update employee details
#                         employee.cid = row['cid']
#                         employee.age = int(row['age'])
#                         employee.social_security_number = row['social_security_number']
#                         employee.blind = str(row['blind']).lower() == 'true'
#                         employee.home_state = row['home_state']
#                         employee.work_state = row['work_state']
#                         employee.gender = row.get('gender', None)
#                         employee.pay_period = row['pay_period']
#                         employee.number_of_exemptions = int(row['number_of_exemptions'])
#                         employee.filing_status = row['filing_status']
#                         employee.marital_status = row['marital_status']
#                         employee.number_of_student_default_loan = int(row['number_of_student_default_loan'])
#                         employee.support_second_family = str(row['support_second_family']).lower() == 'true'
#                         employee.spouse_age = int(row.get('spouse_age', 0))
#                         employee.is_spouse_blind = str(row.get('is_spouse_blind', '')).lower() == 'true'
#                         employee.save()
#                         updated_employees.append(employee.ee_id)
#                 else:
#                     # Add new employee
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=int(row['age']),
#                         social_security_number=row['social_security_number'],
#                         blind=str(row['blind']).lower() == 'true',
#                         home_state=row['home_state'],
#                         work_state=row['work_state'],
#                         gender=row.get('gender', None),
#                         pay_period=row['pay_period'],
#                         number_of_exemptions=int(row['number_of_exemptions']),
#                         filing_status=row['filing_status'],
#                         marital_status=row['marital_status'],
#                         number_of_student_default_loan=int(row['number_of_student_default_loan']),
#                         support_second_family=str(row['support_second_family']).lower() == 'true',
#                         spouse_age=int(row.get('spouse_age', 0)),
#                         is_spouse_blind=str(row.get('is_spouse_blind', '')).lower() == 'true'
#                     )
#                     added_employees.append(row['ee_id'])

#             # Prepare response
#             if not added_employees and not updated_employees:
#                 return JsonResponse({'message': 'No data is inserted or updated.'}, status=200)

#             response_data = []
#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })
#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
##____________________________________________________
#11:45
#new code 3:21 on 24 
#3
# @csrf_exempt
# def import_employees_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  # Uploaded file
#         file_name = file.name  # Get the name of the uploaded file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Handle file formats
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Process the data from DataFrame
#             for _, row in df.iterrows():
#                 # Check if the employee exists
#                 employee = Employee_Detail.objects.filter(ee_id=row['ee_id']).first()

#                 if employee:
#                     # Detect changes in employee data
#                     existing_data = {
#                         'cid': employee.cid,
#                         'age': employee.age,
#                         'social_security_number': employee.social_security_number,
#                         'blind': employee.blind,
#                         'home_state': employee.home_state,
#                         'work_state': employee.work_state,
#                         'gender': employee.gender,
#                         'pay_period': employee.pay_period,
#                         'number_of_exemptions': employee.number_of_exemptions,
#                         'filing_status': employee.filing_status,
#                         'marital_status': employee.marital_status,
#                         'number_of_student_default_loan': employee.number_of_student_default_loan,
#                         'support_second_family': employee.support_second_family,
#                         'spouse_age': employee.spouse_age,
#                         'is_spouse_blind': employee.is_spouse_blind,
#                     }

#                     provided_data = {
#                         'cid': row['cid'],
#                         'age': int(row['age']),
#                         'social_security_number': row['social_security_number'],
#                         'blind': str(row['blind']).lower() == 'true',
#                         'home_state': row['home_state'],
#                         'work_state': row['work_state'],
#                         'gender': row.get('gender', None),
#                         'pay_period': row['pay_period'],
#                         'number_of_exemptions': int(row['number_of_exemptions']),
#                         'filing_status': row['filing_status'],
#                         'marital_status': row['marital_status'],
#                         'number_of_student_default_loan': int(row['number_of_student_default_loan']),
#                         'support_second_family': str(row['support_second_family']).lower() == 'true',
#                         'spouse_age': int(row.get('spouse_age', 0)),
#                         'is_spouse_blind': str(row.get('is_spouse_blind', '')).lower() == 'true',
#                     }

#                     if existing_data != provided_data:
#                         # Update employee details
#                         for key, value in provided_data.items():
#                             setattr(employee, key, value)
#                         employee.save()
#                         updated_employees.append(employee.ee_id)
#                 else:
#                     # Add new employee
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=int(row['age']),
#                         social_security_number=row['social_security_number'],
#                         blind=str(row['blind']).lower() == 'true',
#                         home_state=row['home_state'],
#                         work_state=row['work_state'],
#                         gender=row.get('gender', None),
#                         pay_period=row['pay_period'],
#                         number_of_exemptions=int(row['number_of_exemptions']),
#                         filing_status=row['filing_status'],
#                         marital_status=row['marital_status'],
#                         number_of_student_default_loan=int(row['number_of_student_default_loan']),
#                         support_second_family=str(row['support_second_family']).lower() == 'true',
#                         spouse_age=int(row.get('spouse_age', 0)),
#                         is_spouse_blind=str(row.get('is_spouse_blind', '')).lower() == 'true'
#                     )
#                     added_employees.append(row['ee_id'])

#             # Prepare response
#             if not added_employees and not updated_employees:
#                 return JsonResponse({'message': 'No data is inserted or updated.'}, status=200)

#             response_data = []
#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })
#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)

# #3 end
# #4 3:25 new1 start
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import pandas as pd
# import numpy as np  # For NaN handling

# @csrf_exempt
# def import_employees_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  # Uploaded file
#         file_name = file.name  # Get the name of the uploaded file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Handle file formats
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Process the data from DataFrame
#             for _, row in df.iterrows():
#                 # Check if the employee exists
#                 employee = Employee_Detail.objects.filter(ee_id=row['ee_id']).first()

#                 if employee:
#                     # Detect changes in employee data, handling NaN comparisons
#                     existing_data = {
#                         'cid': employee.cid,
#                         'age': employee.age,
#                         'social_security_number': employee.social_security_number,
#                         'blind': employee.blind,
#                         'home_state': employee.home_state,
#                         'work_state': employee.work_state,
#                         'gender': employee.gender,
#                         'pay_period': employee.pay_period,
#                         'number_of_exemptions': employee.number_of_exemptions,
#                         'filing_status': employee.filing_status,
#                         'marital_status': employee.marital_status,
#                         'number_of_student_default_loan': employee.number_of_student_default_loan,
#                         'support_second_family': employee.support_second_family,
#                         'spouse_age': employee.spouse_age,
#                         'is_spouse_blind': employee.is_spouse_blind,
#                     }

#                     provided_data = {
#                         'cid': row['cid'],
#                         'age': int(row['age']) if not pd.isna(row['age']) else None,
#                         'social_security_number': row['social_security_number'],
#                         'blind': str(row['blind']).lower() == 'true' if not pd.isna(row['blind']) else None,
#                         'home_state': row['home_state'],
#                         'work_state': row['work_state'],
#                         'gender': row.get('gender', None),
#                         'pay_period': row['pay_period'],
#                         'number_of_exemptions': int(row['number_of_exemptions']) if not pd.isna(row['number_of_exemptions']) else None,
#                         'filing_status': row['filing_status'],
#                         'marital_status': row['marital_status'],
#                         'number_of_student_default_loan': int(row['number_of_student_default_loan']) if not pd.isna(row['number_of_student_default_loan']) else None,
#                         'support_second_family': str(row['support_second_family']).lower() == 'true' if not pd.isna(row['support_second_family']) else None,
#                         'spouse_age': int(row.get('spouse_age', 0)) if not pd.isna(row.get('spouse_age', None)) else None,
#                         'is_spouse_blind': str(row.get('is_spouse_blind', '')).lower() == 'true' if not pd.isna(row.get('is_spouse_blind', '')) else None,
#                     }

#                     # Compare existing and provided data, handling NaN equivalence
#                     has_changes = any(
#                         (existing_value != provided_value and not (pd.isna(existing_value) and pd.isna(provided_value)))
#                         for existing_value, provided_value in zip(existing_data.values(), provided_data.values())
#                     )

#                     if has_changes:
#                         # Update employee details
#                         for key, value in provided_data.items():
#                             setattr(employee, key, value)
#                         employee.save()
#                         updated_employees.append(employee.ee_id)
#                 else:
#                     # Add new employee
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=int(row['age']) if not pd.isna(row['age']) else None,
#                         social_security_number=row['social_security_number'],
#                         blind=str(row['blind']).lower() == 'true' if not pd.isna(row['blind']) else None,
#                         home_state=row['home_state'],
#                         work_state=row['work_state'],
#                         gender=row.get('gender', None),
#                         pay_period=row['pay_period'],
#                         number_of_exemptions=int(row['number_of_exemptions']) if not pd.isna(row['number_of_exemptions']) else None,
#                         filing_status=row['filing_status'],
#                         marital_status=row['marital_status'],
#                         number_of_student_default_loan=int(row['number_of_student_default_loan']) if not pd.isna(row['number_of_student_default_loan']) else None,
#                         support_second_family=str(row['support_second_family']).lower() == 'true' if not pd.isna(row['support_second_family']) else None,
#                         spouse_age=int(row.get('spouse_age', 0)) if not pd.isna(row.get('spouse_age', None)) else None,
#                         is_spouse_blind=str(row.get('is_spouse_blind', '')).lower() == 'true' if not pd.isna(row.get('is_spouse_blind', '')) else None
#                     )
#                     added_employees.append(row['ee_id'])

#             # Prepare response
#             if not added_employees and not updated_employees:
#                 return JsonResponse({'message': 'No data is inserted or updated.'}, status=200)

#             response_data = []
#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })
#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)

# #4 end 
#5 START
# new logic to get data from db and match it with current data to return no changes.
# @csrf_exempt
# def import_employees_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  # Uploaded file
#         file_name = file.name  # Get the name of the uploaded file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Handle file formats
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Process the data from DataFrame
#             for _, row in df.iterrows():
#                 # Check if the employee exists
#                 employee = Employee_Detail.objects.filter(ee_id=row['ee_id']).first()

#                 if employee:
#                     # Detect changes in employee data
#                     has_changes = (
#                         employee.cid != row['cid'] or
#                         employee.age != int(row['age']) or
#                         employee.social_security_number != row['social_security_number'] or
#                         employee.blind != (str(row['blind']).lower() == 'true') or
#                         employee.home_state != row['home_state'] or
#                         employee.work_state != row['work_state'] or
#                         employee.gender != row.get('gender', None) or
#                         employee.pay_period != row['pay_period'] or
#                         employee.number_of_exemptions != int(row['number_of_exemptions']) or
#                         employee.filing_status != row['filing_status'] or
#                         employee.marital_status != row['marital_status'] or
#                         employee.number_of_student_default_loan != int(row['number_of_student_default_loan']) or
#                         employee.support_second_family != (str(row['support_second_family']).lower() == 'true') or
#                         employee.spouse_age != int(row.get('spouse_age', 0)) or
#                         employee.is_spouse_blind != (str(row.get('is_spouse_blind', '')).lower() == 'true')
#                     )

#                     if has_changes:
#                         # Update employee details
#                         employee.cid = row['cid']
#                         employee.age = int(row['age'])
#                         employee.social_security_number = row['social_security_number']
#                         employee.blind = str(row['blind']).lower() == 'true'
#                         employee.home_state = row['home_state']
#                         employee.work_state = row['work_state']
#                         employee.gender = row.get('gender', None)
#                         employee.pay_period = row['pay_period']
#                         employee.number_of_exemptions = int(row['number_of_exemptions'])
#                         employee.filing_status = row['filing_status']
#                         employee.marital_status = row['marital_status']
#                         employee.number_of_student_default_loan = int(row['number_of_student_default_loan'])
#                         employee.support_second_family = str(row['support_second_family']).lower() == 'true'
#                         employee.spouse_age = int(row.get('spouse_age', 0))
#                         employee.is_spouse_blind = str(row.get('is_spouse_blind', '')).lower() == 'true'
#                         employee.save()
#                         updated_employees.append(employee.ee_id)
#                 else:
#                     # Add new employee
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=int(row['age']),
#                         social_security_number=row['social_security_number'],
#                         blind=str(row['blind']).lower() == 'true',
#                         home_state=row['home_state'],
#                         work_state=row['work_state'],
#                         gender=row.get('gender', None),
#                         pay_period=row['pay_period'],
#                         number_of_exemptions=int(row['number_of_exemptions']),
#                         filing_status=row['filing_status'],
#                         marital_status=row['marital_status'],
#                         number_of_student_default_loan=int(row['number_of_student_default_loan']),
#                         support_second_family=str(row['support_second_family']).lower() == 'true',
#                         spouse_age=int(row.get('spouse_age', 0)),
#                         is_spouse_blind=str(row.get('is_spouse_blind', '')).lower() == 'true'
#                     )
#                     added_employees.append(row['ee_id'])

#             # Prepare response
#             response_data = []
#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })
#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
# #5

#changes detect here
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from User_app.models import Employee_Detail
# @csrf_exempt
# def import_employees_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  # Uploaded file
#         file_name = file.name  # Get the name of the uploaded file

#         try:
#             # Handle file formats
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Initialize variables to track changes
#             has_changes = False

#             # Process the data from DataFrame
#             for _, row in df.iterrows():
#                 # Check if the employee exists
#                 employee = Employee_Detail.objects.filter(ee_id=row['ee_id']).first()

#                 if employee:
#                     # Check for differences in employee data
#                     if (
#                         employee.cid != row['cid'] or
#                         employee.age != int(row['age']) or
#                         employee.social_security_number != row['social_security_number'] or
#                         employee.blind != (str(row['blind']).lower() == 'true') or
#                         employee.home_state != row['home_state'] or
#                         employee.work_state != row['work_state'] or
#                         employee.gender != row.get('gender', None) or
#                         employee.pay_period != row['pay_period'] or
#                         employee.number_of_exemptions != int(row['number_of_exemptions']) or
#                         employee.filing_status != row['filing_status'] or
#                         employee.marital_status != row['marital_status'] or
#                         employee.number_of_student_default_loan != int(row['number_of_student_default_loan']) or
#                         employee.support_second_family != (str(row['support_second_family']).lower() == 'true') or
#                         employee.spouse_age != int(row.get('spouse_age', 0)) or
#                         employee.is_spouse_blind != (str(row.get('is_spouse_blind', '')).lower() == 'true')
#                     ):
#                         has_changes = True
#                         break
#                 else:
#                     # New employee found, indicating changes
#                     has_changes = True
#                     break

#             # Return response based on changes
#             if not has_changes:
#                 return JsonResponse({"message": "No changes found."}, status=200)
#             else:
#                 return JsonResponse({"message": "Changes detected in the data."}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#changes detect here
#2 start
#for insertation only

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from ..models import Employee_Detail  # Import your updated model
# from django.core.files.storage import default_storage
# import csv
# import pandas as pd

# @csrf_exempt
# def upsert_employees_data_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         file_path = default_storage.save(file.name, file)  # Temporarily save the file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Determine the file type
#             if file.name.endswith('.csv'):
#                 # Process CSV file
#                 with open(file_path, 'r') as csvfile:
#                     reader = csv.DictReader(csvfile)
#                     data = list(reader)
#             elif file.name.endswith(('.xls', '.xlsx')):
#                 # Process Excel file
#                 df = pd.read_excel(file_path)
#                 data = df.to_dict(orient='records')  # Convert to list of dictionaries
#             else:
#                 return JsonResponse({'error': 'Unsupported file format. Please upload a CSV or Excel file.'}, status=400)

#             # Process each row
#             for row in data:
#                 try:
#                     # Retrieve the existing employee details (if any)
#                     employee_detail = Employee_Detail.objects.get(ee_id=row['ee_id'], cid=row['cid'])

#                     # Check if any field differs from the incoming data
#                     has_changes = False
#                     for field_name in [
#                         'age', 'social_security_number', 'blind', 'home_state', 'work_state', 'gender', 'pay_period',
#                         'number_of_exemptions', 'filing_status', 'marital_status', 'number_of_student_default_loan',
#                         'support_second_family', 'spouse_age', 'is_spouse_blind'
#                     ]:
#                         # Safely handle boolean and string conversions
#                         incoming_value = row.get(field_name)
#                         if isinstance(getattr(employee_detail, field_name), bool) and isinstance(incoming_value, str):
#                             incoming_value = incoming_value.lower() in ['true', '1', 'yes']
#                         elif isinstance(getattr(employee_detail, field_name), bool):
#                             incoming_value = bool(incoming_value)  # Ensure incoming value is boolean
#                         if getattr(employee_detail, field_name) != incoming_value:
#                             has_changes = True
#                             break

#                     if has_changes:
#                         # Update the employee detail record
#                         for field_name in [
#                             'age', 'social_security_number', 'blind', 'home_state', 'work_state', 'gender', 'pay_period',
#                             'number_of_exemptions', 'filing_status', 'marital_status', 'number_of_student_default_loan',
#                             'support_second_family', 'spouse_age', 'is_spouse_blind'
#                         ]:
#                             # Safely handle boolean and string conversions
#                             incoming_value = row.get(field_name)
#                             if isinstance(getattr(employee_detail, field_name), bool) and isinstance(incoming_value, str):
#                                 incoming_value = incoming_value.lower() in ['true', '1', 'yes']
#                             elif isinstance(getattr(employee_detail, field_name), bool):
#                                 incoming_value = bool(incoming_value)  # Ensure incoming value is boolean
#                             setattr(employee_detail, field_name, incoming_value)
#                         employee_detail.save()
#                         updated_employees.append(employee_detail.ee_id)
#                 except Employee_Detail.DoesNotExist:
#                     # Add new employee detail
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=row.get('age'),
#                         social_security_number=row.get('social_security_number'),
#                         blind=row.get('blind').lower() in ['true', '1', 'yes'] if isinstance(row.get('blind'), str) else row.get('blind'),
#                         home_state=row.get('home_state'),
#                         work_state=row.get('work_state'),
#                         gender=row.get('gender'),
#                         pay_period=row.get('pay_period'),
#                         number_of_exemptions=row.get('number_of_exemptions'),
#                         filing_status=row.get('filing_status'),
#                         marital_status=row.get('marital_status'),
#                         number_of_student_default_loan=row.get('number_of_student_default_loan'),
#                         support_second_family=row.get('support_second_family').lower() in ['true', '1', 'yes'] if isinstance(row.get('support_second_family'), str) else row.get('support_second_family'),
#                         spouse_age=row.get('spouse_age'),
#                         is_spouse_blind=row.get('is_spouse_blind').lower() in ['true', '1', 'yes'] if isinstance(row.get('is_spouse_blind'), str) else row.get('is_spouse_blind')
#                     )
#                     added_employees.append(row['ee_id'])

#             # Check if any updates or insertions occurred
#             if not updated_employees and not added_employees:
#                 return JsonResponse({'message': 'No data was updated or inserted.'}, status=200)

#             response_data = []

#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })

#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)


#insertation file
#7:27 PM on 24  START
#working well only problem is with the "nan" row value else working correct.
#IMPLEMENTING THE LOGIC OF EMPTY VALUE IN SSN..... START
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Employee_Detail  # Import your updated model
from django.core.files.storage import default_storage
import csv
import pandas as pd
import math

# @csrf_exempt
# def upsert_employees_data_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         print("called")
#         file = request.FILES['file']
#         file_path = default_storage.save(file.name, file)  # Temporarily save the file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Determine the file type
#             if file.name.endswith('.csv'):
#                 # Process CSV file
#                 with open(file_path, 'r') as csvfile:
#                     reader = csv.DictReader(csvfile)
#                     data = list(reader)
#             elif file.name.endswith(('.xls', '.xlsx')):
#                 # Process Excel file
#                 df = pd.read_excel(file_path)
#                 data = df.to_dict(orient='records')  # Convert to list of dictionaries
#             else:
#                 return JsonResponse({'error': 'Unsupported file format. Please upload a CSV or Excel file.'}, status=400)
#             # Process each row
#             for row in data:
#                 # Filter out irrelevant keys like unnamed columns
#                 row = {k: v for k, v in row.items() if k and not k.startswith('Unnamed:')}
#                 updated_row = {}

#                 for k,v in row.items():
#                     if k == "social_security_number" and type(v) == float and  math.isnan(v):
#                         updated_row[k] = ""
#                     else:
#                         updated_row[k] = v

#                 try:
#                     # Retrieve the existing employee details (if any)
#                     employee_detail = Employee_Detail.objects.get(ee_id=row['ee_id'], cid=row['cid'])

#                     # Check if any field differs from the incoming data
#                     has_changes = False
#                     for field_name in [
#                         'age', 'social_security_number', 'blind', 'home_state', 'work_state', 'gender', 'pay_period',
#                         'number_of_exemptions', 'filing_status', 'marital_status', 'number_of_student_default_loan',
#                         'support_second_family', 'spouse_age', 'is_spouse_blind'
#                     ]:
#                         # Safely handle boolean and string conversions
#                         incoming_value = row.get(field_name)

#                         if isinstance(getattr(employee_detail, field_name), bool) and isinstance(incoming_value, str):
#                             incoming_value = incoming_value.lower() in ['true', '1', 'yes']
#                         elif isinstance(getattr(employee_detail, field_name), bool):
#                             incoming_value = bool(incoming_value)  # Ensure incoming value is boolean
#                         if getattr(employee_detail, field_name) != incoming_value:
#                             has_changes = True
#                             break

#                     if has_changes:
#                         # Update the employee detail record
#                         for field_name in [
#                             'age', 'social_security_number', 'blind', 'home_state', 'work_state', 'gender', 'pay_period',
#                             'number_of_exemptions', 'filing_status', 'marital_status', 'number_of_student_default_loan',
#                             'support_second_family', 'spouse_age', 'is_spouse_blind'
#                         ]:
#                             # Safely handle boolean and string conversions
#                             incoming_value = row.get(field_name)
#                             if isinstance(getattr(employee_detail, field_name), bool) and isinstance(incoming_value, str):
#                                 incoming_value = incoming_value.lower() in ['true', '1', 'yes']
#                             elif isinstance(getattr(employee_detail, field_name), bool):
#                                 incoming_value = bool(incoming_value)  # Ensure incoming value is boolean
#                             setattr(employee_detail, field_name, incoming_value)
#                         employee_detail.save()
#                         updated_employees.append(employee_detail.ee_id)
#                 except Employee_Detail.DoesNotExist:
#                     # Add new employee detail
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=row.get('age'),
#                         social_security_number=row.get('social_security_number'),
#                         blind=row.get('blind').lower() in ['true', '1', 'yes'] if isinstance(row.get('blind'), str) else row.get('blind'),
#                         home_state=row.get('home_state'),
#                         work_state=row.get('work_state'),
#                         gender=row.get('gender'),
#                         pay_period=row.get('pay_period'),
#                         number_of_exemptions=row.get('number_of_exemptions'),
#                         filing_status=row.get('filing_status'),
#                         marital_status=row.get('marital_status'),
#                         number_of_student_default_loan=row.get('number_of_student_default_loan'),
#                         support_second_family=row.get('support_second_family').lower() in ['true', '1', 'yes'] if isinstance(row.get('support_second_family'), str) else row.get('support_second_family'),
#                         spouse_age=row.get('spouse_age'),
#                         is_spouse_blind=row.get('is_spouse_blind').lower() in ['true', '1', 'yes'] if isinstance(row.get('is_spouse_blind'), str) else row.get('is_spouse_blind')
#                     )
#                     added_employees.append(row['ee_id'])
                    
#                     #
#                     #added_row = {}



#             # Check if any updates or insertions occurred
#             if not updated_employees and not added_employees:
#                 return JsonResponse({'message': 'No data was updated or inserted.'}, status=200)

#             response_data = []

#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })

#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
#IMPLEMENTING THE LOGIC OF EMPTY VALUE IN SSN..... END

#insertation file
#7:27 PM on 24  END...................
#working well only problem is with the "nan" row value else working correct.

# FINAL CODE For handling the "nan" value and other stuff
#begninning

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from ..models import Employee_Detail  # Import your updated model
# from django.core.files.storage import default_storage
# import csv
# import pandas as pd

# @csrf_exempt
# def upsert_employees_data_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         file_path = default_storage.save(file.name, file)  # Temporarily save the file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Determine the file type
#             if file.name.endswith('.csv'):
#                 # Process CSV file
#                 with open(file_path, 'r') as csvfile:
#                     reader = csv.DictReader(csvfile)
#                     data = list(reader)
#             elif file.name.endswith(('.xls', '.xlsx')):
#                 # Process Excel file
#                 df = pd.read_excel(file_path)
#                 data = df.to_dict(orient='records')  # Convert to list of dictionaries
#             else:
#                 return JsonResponse({'error': 'Unsupported file format. Please upload a CSV or Excel file.'}, status=400)

#             # Process each row
#             for row in data:
                
#                 row = {k: v for k, v in row.items() if k and not k.startswith('Unnamed:')}

#                 try:
                    
#                     employee_detail = Employee_Detail.objects.get(ee_id=row['ee_id'], cid=row['cid'])

                    
#                     has_changes = False
#                     for field_name in [
#                         'age', 'social_security_number', 'blind', 'home_state', 'work_state', 'gender', 'pay_period',
#                         'number_of_exemptions', 'filing_status', 'marital_status', 'number_of_student_default_loan',
#                         'support_second_family', 'spouse_age', 'is_spouse_blind'
#                     ]:
#                         #bool field handling
#                         existing_value = getattr(employee_detail, field_name)
#                         incoming_value = row.get(field_name)

                        
#                         if pd.isna(existing_value):
#                             existing_value = None
#                         if pd.isna(incoming_value) or incoming_value == '':
#                             incoming_value = None

#                         if isinstance(existing_value, bool) and isinstance(incoming_value, str):
#                             incoming_value = incoming_value.lower() in ['true', '1', 'yes']
#                         elif isinstance(existing_value, bool):
#                             incoming_value = bool(incoming_value)  # Ensure incoming value is boolean

#                         if existing_value != incoming_value:
#                             has_changes = True
#                             break

#                     if has_changes:
#                         #update the data
#                         for field_name in [
#                             'age', 'social_security_number', 'blind', 'home_state', 'work_state', 'gender', 'pay_period',
#                             'number_of_exemptions', 'filing_status', 'marital_status', 'number_of_student_default_loan',
#                             'support_second_family', 'spouse_age', 'is_spouse_blind'
#                         ]:
#                             incoming_value = row.get(field_name)

#                             # Treat None, empty strings, and NaN as equivalent
#                             if pd.isna(incoming_value) or incoming_value == '':
#                                 incoming_value = None

#                             if isinstance(getattr(employee_detail, field_name), bool) and isinstance(incoming_value, str):
#                                 incoming_value = incoming_value.lower() in ['true', '1', 'yes']
#                             elif isinstance(getattr(employee_detail, field_name), bool):
#                                 incoming_value = bool(incoming_value)  # Ensure incoming value is boolean

#                             setattr(employee_detail, field_name, incoming_value)
#                         employee_detail.save()
#                         updated_employees.append(employee_detail.ee_id)
#                 except Employee_Detail.DoesNotExist:
#                     # Add new employee detail
#                     Employee_Detail.objects.create(
#                         ee_id=row['ee_id'],
#                         cid=row['cid'],
#                         age=row.get('age'),
#                         social_security_number=row.get('social_security_number'),
#                         blind=row.get('blind').lower() in ['true', '1', 'yes'] if isinstance(row.get('blind'), str) else row.get('blind'),
#                         home_state=row.get('home_state'),
#                         work_state=row.get('work_state'),
#                         gender=row.get('gender'),
#                         pay_period=row.get('pay_period'),
#                         number_of_exemptions=row.get('number_of_exemptions'),
#                         filing_status=row.get('filing_status'),
#                         marital_status=row.get('marital_status'),
#                         number_of_student_default_loan=row.get('number_of_student_default_loan'),
#                         support_second_family=row.get('support_second_family').lower() in ['true', '1', 'yes'] if isinstance(row.get('support_second_family'), str) else row.get('support_second_family'),
#                         spouse_age=row.get('spouse_age'),
#                         is_spouse_blind=row.get('is_spouse_blind').lower() in ['true', '1', 'yes'] if isinstance(row.get('is_spouse_blind'), str) else row.get('is_spouse_blind')
#                     )
#                     added_employees.append(row['ee_id'])

#             # Check if any updates or insertions occurred
#             if not updated_employees and not added_employees:
#                 return JsonResponse({'message': 'No data was updated or inserted.'}, status=200)

#             response_data = []

#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })

#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)


#ending

#INSERTING THE DATA WIHT THE SAME LOGIC
# @csrf_exempt
# def upsert_employees_data_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         print("called")
#         file = request.FILES['file']
#         file_path = default_storage.save(file.name, file)  # Temporarily save the file
#         updated_employees = []
#         added_employees = []

#         try:
#             # Determine the file type
#             if file.name.endswith('.csv'):
#                 # Process CSV file
#                 with open(file_path, 'r') as csvfile:
#                     reader = csv.DictReader(csvfile)
#                     data = list(reader)
#             elif file.name.endswith(('.xls', '.xlsx')):
#                 # Process Excel file
#                 df = pd.read_excel(file_path)
#                 data = df.to_dict(orient='records')  # Convert to list of dictionaries
#             else:
#                 return JsonResponse({'error': 'Unsupported file format. Please upload a CSV or Excel file.'}, status=400)

#             # Process each row
#             for row in data:
#                 # Filter out irrelevant keys like unnamed columns
#                 row = {k: v for k, v in row.items() if k and not k.startswith('Unnamed:')}

#                 # Apply updated_row logic
#                 updated_row = {}
#                 for k, v in row.items():
#                     if k == "social_security_number" and isinstance(v, float) and math.isnan(v):
#                         updated_row[k] = ""
#                     else:
#                         updated_row[k] = v

#                 try:
#                     # Retrieve the existing employee details (if any)
#                     employee_detail = Employee_Detail.objects.get(ee_id=updated_row['ee_id'], cid=updated_row['cid'])

#                     # Check if any field differs from the incoming data
#                     has_changes = False
#                     for field_name in [
#                         'age', 'social_security_number', 'blind', 'home_state', 'work_state', 'gender', 'pay_period',
#                         'number_of_exemptions', 'filing_status', 'marital_status', 'number_of_student_default_loan',
#                         'support_second_family', 'spouse_age', 'is_spouse_blind'
#                     ]:
#                         incoming_value = updated_row.get(field_name)

#                         if isinstance(getattr(employee_detail, field_name), bool) and isinstance(incoming_value, str):
#                             incoming_value = incoming_value.lower() in ['true', '1', 'yes']
#                         elif isinstance(getattr(employee_detail, field_name), bool):
#                             incoming_value = bool(incoming_value)  # Ensure incoming value is boolean
#                         if getattr(employee_detail, field_name) != incoming_value:
#                             has_changes = True
#                             break

#                     if has_changes:
#                         # Update the employee detail record
#                         for field_name in [
#                             'age', 'social_security_number', 'blind', 'home_state', 'work_state', 'gender', 'pay_period',
#                             'number_of_exemptions', 'filing_status', 'marital_status', 'number_of_student_default_loan',
#                             'support_second_family', 'spouse_age', 'is_spouse_blind'
#                         ]:
#                             incoming_value = updated_row.get(field_name)
#                             if isinstance(getattr(employee_detail, field_name), bool) and isinstance(incoming_value, str):
#                                 incoming_value = incoming_value.lower() in ['true', '1', 'yes']
#                             elif isinstance(getattr(employee_detail, field_name), bool):
#                                 incoming_value = bool(incoming_value)  # Ensure incoming value is boolean
#                             setattr(employee_detail, field_name, incoming_value)
#                         employee_detail.save()
#                         updated_employees.append(employee_detail.ee_id)
#                 except Employee_Detail.DoesNotExist:
#                     # Add new employee detail
#                     Employee_Detail.objects.create(
#                         ee_id=updated_row['ee_id'],
#                         cid=updated_row['cid'],
#                         age=updated_row.get('age'),
#                         social_security_number=updated_row.get('social_security_number'),
#                         blind=updated_row.get('blind').lower() in ['true', '1', 'yes'] if isinstance(updated_row.get('blind'), str) else updated_row.get('blind'),
#                         home_state=updated_row.get('home_state'),
#                         work_state=updated_row.get('work_state'),
#                         gender=updated_row.get('gender'),
#                         pay_period=updated_row.get('pay_period'),
#                         number_of_exemptions=updated_row.get('number_of_exemptions'),
#                         filing_status=updated_row.get('filing_status'),
#                         marital_status=updated_row.get('marital_status'),
#                         number_of_student_default_loan=updated_row.get('number_of_student_default_loan'),
#                         support_second_family=updated_row.get('support_second_family').lower() in ['true', '1', 'yes'] if isinstance(updated_row.get('support_second_family'), str) else updated_row.get('support_second_family'),
#                         spouse_age=updated_row.get('spouse_age'),
#                         is_spouse_blind=updated_row.get('is_spouse_blind').lower() in ['true', '1', 'yes'] if isinstance(updated_row.get('is_spouse_blind'), str) else updated_row.get('is_spouse_blind')
#                     )
#                     added_employees.append(updated_row['ee_id'])

#             # Check if any updates or insertions occurred
#             if not updated_employees and not added_employees:
#                 return JsonResponse({'message': 'No data was updated or inserted.'}, status=200)

#             response_data = []

#             if added_employees:
#                 response_data.append({
#                     'message': 'Employee(s) imported successfully',
#                     'added_employees': added_employees
#                 })

#             if updated_employees:
#                 response_data.append({
#                     'message': 'Employee details updated successfully',
#                     'updated_employees': updated_employees
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
#working as needed and good 
#not updating the data specially the "nan"




#Upsert the company details

@csrf_exempt
def upsert_employees_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        print("called")
        file = request.FILES['file']
        updated_employees = []
        added_employees = []

        try:
            
            if file.name.endswith('.csv'):
                
                data = list(csv.DictReader(file.read().decode('utf-8').splitlines()))
            elif file.name.endswith(('.xls', '.xlsx')):
                
                df = pd.read_excel(file)
                data = df.to_dict(orient='records')  
            else:
                return JsonResponse({'error': 'Unsupported file format. Please upload a CSV or Excel file.'}, status=400)

           
            for row in data:
                
                row = {k: v for k, v in row.items() if k and not k.startswith('Unnamed:')}

                
                updated_row = {}
                for k, v in row.items():
                    if k == "social_security_number" and isinstance(v, float) and math.isnan(v):
                        updated_row[k] = ""
                    else:
                        updated_row[k] = v

                try:
                    
                    employee_detail = Employee_Detail.objects.get(ee_id=updated_row['ee_id'], cid=updated_row['cid'])

                    
                    has_changes = False
                    for field_name in [
                        'age', 'social_security_number', 'is_blind', 'home_state', 'work_state', 'gender', 'pay_period',
                        'number_of_exemptions', 'filing_status', 'marital_status', 'number_of_student_default_loan',
                        'support_second_family', 'spouse_age', 'is_spouse_blind'
                    ]:
                        incoming_value = updated_row.get(field_name)
                        if isinstance(getattr(employee_detail, field_name), bool) and isinstance(incoming_value, str):
                            incoming_value = incoming_value.lower() in ['true', '1', 'yes']
                        elif isinstance(getattr(employee_detail, field_name), bool):
                            incoming_value = bool(incoming_value)  
                        if getattr(employee_detail, field_name) != incoming_value:
                            has_changes = True
                            break

                    if has_changes:
                        
                        for field_name in [
                            'age', 'social_security_number', 'is_blind', 'home_state', 'work_state', 'gender', 'pay_period',
                            'number_of_exemptions', 'filing_status', 'marital_status', 'number_of_student_default_loan',
                            'support_second_family', 'spouse_age', 'is_spouse_blind'
                        ]:
                            incoming_value = updated_row.get(field_name)
                            if isinstance(getattr(employee_detail, field_name), bool) and isinstance(incoming_value, str):
                                incoming_value = incoming_value.lower() in ['true', '1', 'yes']
                            elif isinstance(getattr(employee_detail, field_name), bool):
                                incoming_value = bool(incoming_value)  
                            setattr(employee_detail, field_name, incoming_value)
                        employee_detail.save()
                        updated_employees.append(employee_detail.ee_id)
                except Employee_Detail.DoesNotExist:
                    
                    Employee_Detail.objects.create(
                        ee_id=updated_row['ee_id'],
                        cid=updated_row['cid'],
                        age=updated_row.get('age'),
                        social_security_number=updated_row.get('social_security_number'),
                        is_blind=updated_row.get('is_blind').lower() in ['true', '1', 'yes'] if isinstance(updated_row.get('is_blind'), str) else updated_row.get('is_blind'),
                        home_state=updated_row.get('home_state'),
                        work_state=updated_row.get('work_state'),
                        gender=updated_row.get('gender'),
                        pay_period=updated_row.get('pay_period'),
                        number_of_exemptions=updated_row.get('number_of_exemptions'),
                        filing_status=updated_row.get('filing_status'),
                        marital_status=updated_row.get('marital_status'),
                        number_of_student_default_loan=updated_row.get('number_of_student_default_loan'),
                        support_second_family=updated_row.get('support_second_family').lower() in ['true', '1', 'yes'] if isinstance(updated_row.get('support_second_family'), str) else updated_row.get('support_second_family'),
                        spouse_age=updated_row.get('spouse_age'),
                        is_spouse_blind=updated_row.get('is_spouse_blind').lower() in ['true', '1', 'yes'] if isinstance(updated_row.get('is_spouse_blind'), str) else updated_row.get('is_spouse_blind')
                    )
                    added_employees.append(updated_row['ee_id'])

           
            if not updated_employees and not added_employees:
                return JsonResponse({'message': 'No data was updated or inserted.'}, status=200)

            response_data = []

            if added_employees:
                response_data.append({
                    'message': 'Employee(s) imported successfully',
                    'added_employees': added_employees
                })

            if updated_employees:
                response_data.append({
                    'message': 'Employee details updated successfully',
                    'updated_employees': updated_employees
                })

            return JsonResponse({'responses': response_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
 
@csrf_exempt
def upsert_garnishment_order(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_name = file.name
        updated_orders = []
        added_orders = []
        no_change = []

        try:
            # Load file into a DataFrame
            if file_name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                df = pd.read_excel(file)
            else:
                return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

            # Format date columns
            date_columns = ['start_date', 'end_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    df[col] = df[col].apply(lambda x: x.date() if not pd.isna(x) else None)

            # Process each row
            for _, row in df.iterrows():
                try:
                    # Skip rows with missing 'cid' or 'eeid'
                    if pd.isna(row['cid']) or pd.isna(row['eeid']):
                        continue

                    # Retrieve existing order
                    order = garnishment_order.objects.filter(cid=row['cid'], eeid=row['eeid']).first()

                    if order:
                        # Check for changes
                        has_changes = (
                            order.case_id != row.get('case_id', None) or
                            order.state != row['state'] or
                            order.type != row['type'] or
                            order.sdu != row.get('sdu', None) or
                            order.start_date != row.get('start_date', None) or
                            order.end_date != row.get('end_date', None) or
                            float(order.amount) != float(row['amount']) or
                            order.arrear_greater_than_12_weeks != row['arrear_greater_than_12_weeks'] or
                            float(order.arrear_amount) != float(row['arrear_amount'])
                        )

                        if has_changes:
                            # Update order
                            order.case_id = row.get('case_id', None)
                            order.state = row['state']
                            order.type = row['type']
                            order.sdu = row.get('sdu', None)
                            order.start_date = row.get('start_date', None)
                            order.end_date = row.get('end_date', None)
                            order.amount = row['amount']
                            order.arrear_greater_than_12_weeks = row['arrear_greater_than_12_weeks']
                            order.arrear_amount = row['arrear_amount']
                            order.save()
                            updated_orders.append({'cid': order.cid, 'eeid': order.eeid})
                        else:
                            no_change.append({'cid': order.cid, 'eeid': order.eeid})
                    else:
                        # Create new order
                        garnishment_order.objects.create(
                            cid=row['cid'],
                            eeid=row['eeid'],
                            case_id=row.get('case_id', None),
                            state=row['state'],
                            type=row['type'],
                            sdu=row.get('sdu', None),
                            start_date=row.get('start_date', None),
                            end_date=row.get('end_date', None),
                            amount=row['amount'],
                            arrear_greater_than_12_weeks=row['arrear_greater_than_12_weeks'],
                            arrear_amount=row['arrear_amount']
                        )
                        added_orders.append({'cid': row['cid'], 'eeid': row['eeid']})

                except Exception as row_error:
                    # Error is no longer printed in terminal, only logged in exception handling
                    continue

            # Prepare response data
            if added_orders or updated_orders:
                response_data = []
                if added_orders:
                    response_data.append({
                        'message': 'Garnishment orders imported successfully',
                        'added_orders': added_orders
                    })
                if updated_orders:
                    response_data.append({
                        'message': 'Garnishment orders updated successfully',
                        'updated_orders': updated_orders
                    })
                if no_change:
                    response_data.append({
                        'message': 'No change for certain orders',
                        'no_change_orders': no_change
                    })
            else:
                response_data = {'message': 'No changes in data'}

            return JsonResponse({'responses': response_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)




@csrf_exempt
def upsert_company_details(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']  
        file_name = file.name  
        updated_companies = []
        added_companies = []
        unchanged_companies = []  
        new_data_found = False 

        try:
            
            if file_name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                df = pd.read_excel(file)
            else:
                return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

            
            for _, row in df.iterrows():
                company = company_details.objects.filter(cid=row['cid']).first()

                if company:
                    
                    existing_data = {
                        'ein': str(company.ein).strip() if company.ein else '',
                        'company_name': str(company.company_name).strip() if company.company_name else '',
                        'zipcode': str(company.zipcode).strip() if company.zipcode else '',
                        'state': str(company.state).strip() if company.state else '',
                        'dba_name': str(company.dba_name).strip() if company.dba_name else '',
                        'bank_name': str(company.bank_name).strip() if company.bank_name else '',
                        'bank_account_number': str(company.bank_account_number).strip() if company.bank_account_number else '',
                        'location': str(company.location).strip() if company.location else '',
                        'registered_address': str(company.registered_address).strip() if company.registered_address else ''
                    }

                    file_data = {
                        'ein': str(row['ein']).strip() if row['ein'] else '',
                        'company_name': str(row['company_name']).strip() if row['company_name'] else '',
                        'zipcode': str(row['zipcode']).strip() if row['zipcode'] else '',
                        'state': str(row['state']).strip() if row['state'] else '',
                        'dba_name': str(row['dba_name']).strip() if row['dba_name'] else '',
                        'bank_name': str(row.get('bank_name', '')).strip() if row.get('bank_name') else '',
                        'bank_account_number': str(row.get('bank_account_number', '')).strip() if row.get('bank_account_number') else '',
                        'location': str(row.get('location', '')).strip() if row.get('location') else '',
                        'registered_address': str(row.get('registered_address', '')).strip() if row.get('registered_address') else ''
                    }

                    
                    has_changes = any(existing_data[key] != file_data[key] for key in existing_data)

                    if has_changes:
                        
                        company.ein = row['ein']
                        company.company_name = row['company_name']
                        company.zipcode = row['zipcode']
                        company.state = row['state']
                        company.dba_name = row['dba_name']
                        company.bank_name = row.get('bank_name', None)
                        company.bank_account_number = row.get('bank_account_number', None)
                        company.location = row.get('location', None)
                        company.registered_address = row.get('registered_address', None)
                        company.save()
                        updated_companies.append(company.cid)
                    else:
                        
                        unchanged_companies.append(company.cid)
                else:
                    
                    company_details.objects.create(
                        cid=row['cid'],
                        ein=row['ein'],
                        company_name=row['company_name'],
                        zipcode=row['zipcode'],
                        state=row['state'],
                        dba_name=row['dba_name'],
                        bank_name=row.get('bank_name', None),
                        bank_account_number=row.get('bank_account_number', None),
                        location=row.get('location', None),
                        registered_address=row.get('registered_address', None)
                    )
                    added_companies.append(row['cid'])
                    new_data_found = True  

            
            response_data = []
            if added_companies:
                response_data.append({
                    'message': 'Company details imported successfully',
                    'added_companies': added_companies
                })
            
            if updated_companies:
                response_data.append({
                    'message': 'Company details updated successfully',
                    'updated_companies': updated_companies
                })
            
            
            if not added_companies and not updated_companies:
                response_data.append({'message': 'No changes are found'})

            return JsonResponse({'responses': response_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


#get the employee data with the rules
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from User_app.models import Employee_Detail, garnishment_fees_states_rule
from ..serializers import EmployeeDetailsSerializer

@api_view(['GET'])
def get_employees_with_rules(request):
    """
    API to fetch Employee_Detail data, match work_state with state in garnishment_fees_states_rule,
    and return a DataFrame response with an additional 'rule' column.
    """
    # Fetch all employees
    employees = Employee_Detail.objects.all()
    employee_data = list(employees.values())  # Convert QuerySet to List of Dicts

    # Fetch all garnishment rules
    rules = garnishment_fees_states_rule.objects.all()
    rules_data = {rule.state: rule.rule for rule in rules}  # Create a dictionary {state: rule}

    # Convert Employee data to DataFrame
    df = pd.DataFrame(employee_data)

    # Add 'rule' column based on work_state matching state
    df['rule'] = df['work_state'].map(rules_data).fillna('No Rule Found')

    # Convert DataFrame to JSON response
    return Response(df.to_dict(orient='records'), status=status.HTTP_200_OK)
