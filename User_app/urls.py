from django.urls import path
from . import views
from .views import UserUpdateAPIView,EmployerProfileEditView,UserDeleteAPIView,TaxDetails,EmployeeDetailsUpdateAPIView,DepartmentViewSet,get_Tax_details,EmployeeDeleteAPIView
from django.urls import include, path
from rest_framework import routers





urlpatterns = [
    path("register", views.register, name="register"),
    path("login",views.login, name="login"),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout',views.logout,name='logout'),
    path('employer-profile/', views.EmployerProfile, name='employer_profile'),
    path('TaxDetails/', views.TaxDetails, name='Tax_details'),
    path('employee_details/', views.EmployeeDetails, name='employee_details'),
    path('employee_details/<int:employee_id>/',EmployeeDetailsUpdateAPIView.as_view(), name='Employee_Details_UpdateAPIView'),
    path('<str:username>/', UserUpdateAPIView.as_view(),name='User-Update-API-View'),
    path('employer-profile/<int:employer_id>/',EmployerProfileEditView.as_view(),name='Employer_Profile_UpdateAPIView'),
    path('delete/<str:username>/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('upload', views.upload_pdf, name='upload_pdf'),
    path('getemployeedetails/<int:employer_id>/', views.get_employee_by_employer_id, name='employee-by-employer-id'),
    path('getemployerdetails/<int:employer_id>/', views.get_employer_details, name='employer-detail-by-employer-id'),
    path('DashboardData',views.get_dashboard_data, name='iwo_dashboard'),
    path('IWO_Data',views.insert_iwo_detail, name='iwo_pdf_data'),
    path('Department',DepartmentViewSet, name='Department'),
    path('Location',views.LocationViewSet, name='Location'),  
    path('GetTaxDetails/<int:employer_id>/',views.get_Tax_details, name='GetTaxDetails'),  
    path('GetDepartmentDetails/<int:employer_id>/',views.get_Department_details, name='GetDepartmentDetails'), 
    path('GetLocationDetails/<int:employer_id>/',views.get_Location_details, name='Get-Location-Details'),    
    path('EmployeeDeleteAPIView/<int:employee_id>/',EmployeeDeleteAPIView.as_view(), name='Employee-Delete-APIView'),
    path('ExportEmployees/<int:employer_id>/', views.export_employee_data, name='export-employee-data'),       
]



