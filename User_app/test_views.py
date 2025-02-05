import pytest
from rest_framework.test import APIClient
from rest_framework import status


import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()



@pytest.fixture
def api_client():
    return APIClient()

def test_calculation_data_view_success(api_client):
    url = "http://127.0.0.1:8000/User/garnishment_calculate/"
    test_data = {
    "batch_id": "B001A",
    "cid": {
        "C00001": {
            "employees": [
                {
                    "ee_id": "EE005114",
                    "gross_pay": 1000.0,
                    "state": "Alabama",
                    "no_of_exemption_for_self": 1,
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
                    "no_of_student_default_loan": 1,
                    "arrears_greater_than_12_weeks": "No",
                    "garnishment_data": [
                        {
                            "type": "Student Default Loan",
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
            ]
        
        
        }
    
    }
}
    response = api_client.post(url, data=test_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.data
    assert response.data["message"] == "Result Generated Successfully"

def test_calculation_data_view_missing_batch_id(api_client):
    url = "http://127.0.0.1:8000/User/garnishment_calculate/"
    test_data = {"cid": {}}
    response = api_client.post(url, data=test_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
    assert response.data["error"] == "batch_id is required"

def test_calculation_data_view_invalid_garnishment_type(api_client):
    url = "http://127.0.0.1:8000/User/garnishment_calculate/"
    test_data = {
        "batch_id": "B001A",
        "cid": {
            "C00001": {
                "employees": [
                    {
                        "ee_id": "EE005114",
                        "garnishment_data": [{"type": "Student Default Loanss", "data": []}]
                    }
                ]
            }
        }
    }
    response = api_client.post(url, data=test_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
