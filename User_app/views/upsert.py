from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from User_app.models import payroll  
from django.core.files.storage import default_storage
import csv
import pandas as pd
from ..models import *

#UPSERT EMPLOYEE CODE___START
 

import math
from User_app.models import Employee_Detail

@csrf_exempt
def upsert_employees_data_api(request):
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
                        is_blind=updated_row.get('blind').lower() in ['true', '1', 'yes'] if isinstance(updated_row.get('blind'), str) else updated_row.get('blind'),
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

#UPSERT EMPLOYEE CODE___END
#UPSERT COMPANY_DETAILS_CODE__START

# company data correct working
from User_app.models import company_details
#new1
##############################################################################
# @csrf_exempt
# def upsert_company_details_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  
#         file_name = file.name  
#         updated_companies = []
#         added_companies = []
#         unchanged_companies = []  
#         new_data_found = False 

#         try:
            
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

            
#             for _, row in df.iterrows():
#                 company = company_details.objects.filter(cid=row['cid']).first()

#                 if company:
                    
#                     existing_data = {
#                         'ein': str(company.ein).strip() if company.ein else '',
#                         'company_name': str(company.company_name).strip() if company.company_name else '',
#                         'zipcode': str(company.zipcode).strip() if company.zipcode else '',
#                         'state': str(company.state).strip() if company.state else '',
#                         'dba_name': str(company.dba_name).strip() if company.dba_name else '',
#                         'bank_name': str(company.bank_name).strip() if company.bank_name else '',
#                         'bank_account_number': str(company.bank_account_number).strip() if company.bank_account_number else '',
#                         'location': str(company.location).strip() if company.location else '',
#                         'registered_address': str(company.registered_address).strip() if company.registered_address else ''
#                     }

#                     file_data = {
#                         'ein': str(row['ein']).strip() if row['ein'] else '',
#                         'company_name': str(row['company_name']).strip() if row['company_name'] else '',
#                         'zipcode': str(row['zipcode']).strip() if row['zipcode'] else '',
#                         'state': str(row['state']).strip() if row['state'] else '',
#                         'dba_name': str(row['dba_name']).strip() if row['dba_name'] else '',
#                         'bank_name': str(row.get('bank_name', '')).strip() if row.get('bank_name') else '',
#                         'bank_account_number': str(row.get('bank_account_number', '')).strip() if row.get('bank_account_number') else '',
#                         'location': str(row.get('location', '')).strip() if row.get('location') else '',
#                         'registered_address': str(row.get('registered_address', '')).strip() if row.get('registered_address') else ''
#                     }

                    
#                     has_changes = any(existing_data[key] != file_data[key] for key in existing_data)

#                     if has_changes:
                        
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
#                     else:
                        
#                         unchanged_companies.append(company.cid)
#                 else:
                    
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
#                     new_data_found = True  

            
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
            
            
#             if not added_companies and not updated_companies:
#                 response_data.append({'message': 'No changes are found'})

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)

#new1

#timestamp

from django.utils import timezone

@csrf_exempt
def upsert_company_details_api(request):
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
                        company.record_updated = timezone.now()  # Store timestamp for updated records
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
                        registered_address=row.get('registered_address', None),
                        record_import=timezone.now()  # Store timestamp for newly added records
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

#timestamp


#2
#On 27/01 at 5:02
#NEW LOGIC CODE START
from User_app.models import garnishment_order
# @csrf_exempt
# def upsert_garnishment_order_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         file_name = file.name
#         updated_orders = []
#         added_orders = []
#         no_change = []

#         try:
#             # Load file into a DataFrame
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Format date columns
#             date_columns = ['start_date', 'end_date']
#             for col in date_columns:
#                 if col in df.columns:
#                     df[col] = pd.to_datetime(df[col], errors='coerce')
#                     df[col] = df[col].apply(lambda x: x.date() if not pd.isna(x) else None)

#             # Process each row
#             for _, row in df.iterrows():
#                 try:
#                     # Skip rows with missing 'cid' or 'eeid'
#                     if pd.isna(row['cid']) or pd.isna(row['eeid']):
#                         continue

#                     # Retrieve existing order
#                     order = garnishment_order.objects.filter(cid=row['cid'], eeid=row['eeid']).first()

#                     if order:
#                         # Check for changes
#                         has_changes = (
#                             order.case_id != row.get('case_id', None) or
#                             order.state != row['state'] or
#                             order.type != row['type'] or
#                             order.sdu != row.get('sdu', None) or
#                             order.start_date != row.get('start_date', None) or
#                             order.end_date != row.get('end_date', None) or
#                             float(order.amount) != float(row['amount']) or
#                             order.arrear_greater_than_12_weeks != row['arrear_greater_than_12_weeks'] or
#                             float(order.arrear_amount) != float(row['arrear_amount'])
#                         )

#                         if has_changes:
#                             # Update order
#                             order.case_id = row.get('case_id', None)
#                             order.state = row['state']
#                             order.type = row['type']
#                             order.sdu = row.get('sdu', None)
#                             order.start_date = row.get('start_date', None)
#                             order.end_date = row.get('end_date', None)
#                             order.amount = row['amount']
#                             order.arrear_greater_than_12_weeks = row['arrear_greater_than_12_weeks']
#                             order.arrear_amount = row['arrear_amount']
#                             order.save()
#                             updated_orders.append({'cid': order.cid, 'eeid': order.eeid})
#                         else:
#                             no_change.append({'cid': order.cid, 'eeid': order.eeid})
#                     else:
#                         # Create new order
#                         garnishment_order.objects.create(
#                             cid=row['cid'],
#                             eeid=row['eeid'],
#                             case_id=row.get('case_id', None),
#                             state=row['state'],
#                             type=row['type'],
#                             sdu=row.get('sdu', None),
#                             start_date=row.get('start_date', None),
#                             end_date=row.get('end_date', None),
#                             amount=row['amount'],
#                             arrear_greater_than_12_weeks=row['arrear_greater_than_12_weeks'],
#                             arrear_amount=row['arrear_amount']
#                         )
#                         added_orders.append({'cid': row['cid'], 'eeid': row['eeid']})

#                 except Exception as row_error:
#                     print(f"Error processing row: {row}. Error: {row_error}")
#                     continue

#             # Prepare response data
#             if added_orders or updated_orders:
#                 response_data = []
#                 if added_orders:
#                     response_data.append({
#                         'message': 'Garnishment orders imported successfully',
#                         'added_orders': added_orders
#                     })
#                 if updated_orders:
#                     response_data.append({
#                         'message': 'Garnishment orders updated successfully',
#                         'updated_orders': updated_orders
#                     })
#                 if no_change:
#                     response_data.append({
#                         'message': 'No change for certain orders',
#                         'no_change_orders': no_change
#                     })
#             else:
#                 response_data = {'message': 'No changes in data'}

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
###############################################################################
@csrf_exempt
def upsert_garnishment_order_api(request):
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




#On 27/01 at 5:02
#NEW LOGIC CODE END




#______________________________________________________________________________________________________________
#4
#on 27/01 at 4:26
# from User_app.models import garnishment_order
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import pandas as pd
# from django.db import transaction

# @csrf_exempt
# def upsert_garnishment_order_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         file_name = file.name

#         try:
#             # Load data from file
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Ensure date columns are parsed correctly
#             date_columns = ['start_date', 'end_date']
#             for col in date_columns:
#                 if col in df.columns:
#                     df[col] = pd.to_datetime(df[col], errors='coerce').dt.date  # Convert to date

#             # Validate and clean data
#             df = df.dropna(subset=['cid', 'eeid'])  # Drop rows with missing mandatory fields

#             # Prepare lists for bulk operations
#             updates = []
#             inserts = []
#             no_changes = []

#             # Chunk processing for large datasets
#             chunk_size = 1000  # Adjustable based on memory and system capacity
#             for chunk_start in range(0, len(df), chunk_size):
#                 chunk = df.iloc[chunk_start:chunk_start + chunk_size]

#                 # Fetch existing orders for this chunk
#                 existing_orders = garnishment_order.objects.filter(
#                     cid__in=chunk['cid'].unique(),
#                     eeid__in=chunk['eeid'].unique()
#                 )
#                 existing_orders_map = {
#                     (order.cid, order.eeid): order for order in existing_orders
#                 }

#                 for _, row in chunk.iterrows():
#                     key = (row['cid'], row['eeid'])
#                     order = existing_orders_map.get(key)

#                     if order:
#                         # Check for changes
#                         has_changes = (
#                             order.case_id != row.get('case_id', None) or
#                             order.state != row['state'] or
#                             order.type != row['type'] or
#                             order.sdu != row.get('sdu', None) or
#                             order.start_date != row.get('start_date', None) or
#                             order.end_date != row.get('end_date', None) or
#                             float(order.amount) != float(row['amount']) or
#                             order.arrear_greater_than_12_weeks != row['arrear_greater_than_12_weeks'] or
#                             float(order.arrear_amount) != float(row['arrear_amount'])
#                         )

#                         if has_changes:
#                             order.case_id = row.get('case_id', None)
#                             order.state = row['state']
#                             order.type = row['type']
#                             order.sdu = row.get('sdu', None)
#                             order.start_date = row.get('start_date', None)
#                             order.end_date = row.get('end_date', None)
#                             order.amount = row['amount']
#                             order.arrear_greater_than_12_weeks = row['arrear_greater_than_12_weeks']
#                             order.arrear_amount = row['arrear_amount']
#                             updates.append(order)
#                         else:
#                             no_changes.append({'cid': order.cid, 'eeid': order.eeid})
#                     else:
#                         # Prepare new order for insertion
#                         inserts.append(garnishment_order(
#                             cid=row['cid'],
#                             eeid=row['eeid'],
#                             case_id=row.get('case_id', None),
#                             state=row['state'],
#                             type=row['type'],
#                             sdu=row.get('sdu', None),
#                             start_date=row.get('start_date', None),
#                             end_date=row.get('end_date', None),
#                             amount=row['amount'],
#                             arrear_greater_than_12_weeks=row['arrear_greater_than_12_weeks'],
#                             arrear_amount=row['arrear_amount']
#                         ))

#             # Perform bulk insert and update operations
#             with transaction.atomic():
#                 if inserts:
#                     garnishment_order.objects.bulk_create(inserts, batch_size=chunk_size)
#                 if updates:
#                     garnishment_order.objects.bulk_update(
#                         updates,
#                         fields=[
#                             'case_id', 'state', 'type', 'sdu', 'start_date',
#                             'end_date', 'amount', 'arrear_greater_than_12_weeks', 'arrear_amount'
#                         ],
#                         batch_size=chunk_size
#                     )

#             # Prepare response
#             response_data = {
#                 'added_orders': [{'cid': order.cid, 'eeid': order.eeid} for order in inserts],
#                 'updated_orders': [{'cid': order.cid, 'eeid': order.eeid} for order in updates],
#                 'no_change_orders': no_changes
#             }

#             return JsonResponse({'status': 'success', 'data': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)



#on 27/01 at 4:26
#4

#3
#On 27/01 at 3:51

# from User_app.models import garnishment_order
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import pandas as pd
# from django.db import transaction

# @csrf_exempt
# def upsert_garnishment_order_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         file_name = file.name

#         try:
#             # Load data from file
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

#             # Ensure date columns are parsed correctly
#             date_columns = ['start_date', 'end_date']
#             for col in date_columns:
#                 if col in df.columns:
#                     df[col] = pd.to_datetime(df[col], errors='coerce').dt.date  # Convert to date

#             # Validate and clean data
#             df = df.dropna(subset=['cid', 'eeid'])  # Drop rows with missing mandatory fields

#             # Prepare lists for bulk operations
#             updates = []
#             inserts = []
#             no_changes = []

#             # Chunk processing for large datasets
#             chunk_size = 500  # Adjust based on your system's capacity
#             for chunk_start in range(0, len(df), chunk_size):
#                 chunk = df.iloc[chunk_start:chunk_start + chunk_size]

#                 # Fetch existing orders for this chunk
#                 existing_orders = garnishment_order.objects.filter(
#                     cid__in=chunk['cid'].unique(),
#                     eeid__in=chunk['eeid'].unique()
#                 )
#                 existing_orders_map = {
#                     (order.cid, order.eeid): order for order in existing_orders
#                 }

#                 for _, row in chunk.iterrows():
#                     key = (row['cid'], row['eeid'])
#                     order = existing_orders_map.get(key)

#                     if order:
#                         # Check for changes
#                         has_changes = (
#                             order.case_id != row.get('case_id', None) or
#                             order.state != row['state'] or
#                             order.type != row['type'] or
#                             order.sdu != row.get('sdu', None) or
#                             order.start_date != row.get('start_date', None) or
#                             order.end_date != row.get('end_date', None) or
#                             float(order.amount) != float(row['amount']) or
#                             order.arrear_greater_than_12_weeks != row['arrear_greater_than_12_weeks'] or
#                             float(order.arrear_amount) != float(row['arrear_amount'])
#                         )

#                         if has_changes:
#                             order.case_id = row.get('case_id', None)
#                             order.state = row['state']
#                             order.type = row['type']
#                             order.sdu = row.get('sdu', None)
#                             order.start_date = row.get('start_date', None)
#                             order.end_date = row.get('end_date', None)
#                             order.amount = row['amount']
#                             order.arrear_greater_than_12_weeks = row['arrear_greater_than_12_weeks']
#                             order.arrear_amount = row['arrear_amount']
#                             updates.append(order)
#                         else:
#                             #no_changes.append(order.cid)
#                             no_changes.append({'cid': order.cid, 'eeid': order.eeid})
#                     else:
#                         # Prepare new order for insertion
#                         inserts.append(garnishment_order(
#                             cid=row['cid'],
#                             eeid=row['eeid'],
#                             case_id=row.get('case_id', None),
#                             state=row['state'],
#                             type=row['type'],
#                             sdu=row.get('sdu', None),
#                             start_date=row.get('start_date', None),
#                             end_date=row.get('end_date', None),
#                             amount=row['amount'],
#                             arrear_greater_than_12_weeks=row['arrear_greater_than_12_weeks'],
#                             arrear_amount=row['arrear_amount']
#                         ))

#             # Perform bulk insert and update operations
#             with transaction.atomic():
#                 if inserts:
#                     garnishment_order.objects.bulk_create(inserts, batch_size=chunk_size)
#                 if updates:
#                     garnishment_order.objects.bulk_update(
#                         updates,
#                         fields=[
#                             'case_id', 'state', 'type', 'sdu', 'start_date',
#                             'end_date', 'amount', 'arrear_greater_than_12_weeks', 'arrear_amount'
#                         ],
#                         batch_size=chunk_size
#                     )

#             # Prepare response
#             response_data = []
#             if inserts:
#                 response_data.append({
#                     'message': 'New garnishment orders added successfully',
#                     'added_count': len(inserts)
#                 })
#             if updates:
#                 response_data.append({
#                     'message': 'Existing garnishment orders updated successfully',
#                     'updated_count': len(updates)
#                 })
#             if no_changes:
#                 response_data.append({
#                     'message': 'No changes for certain orders',
#                     'no_change_count': len(no_changes)
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)


#On 27/01 at 3:51
#3


# #2

# from User_app.models import garnishment_order
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import pandas as pd

# @csrf_exempt
# def upsert_garnishment_order_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         file_name = file.name
#         updated_orders = []
#         added_orders = []
#         no_change = []

#         try:
           
#             if file_name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
#                 df = pd.read_excel(file)
#             else:
#                 return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

            
#             date_columns = ['start_date', 'end_date']
#             for col in date_columns:
#                 if col in df.columns:
#                     df[col] = pd.to_datetime(df[col], errors='coerce')  
#                     #replacing with 'none'
#                     df[col] = df[col].apply(lambda x: x.date() if not pd.isna(x) else None) 

           
#             for _, row in df.iterrows():
#                 try:
                    
#                     if pd.isna(row['cid']) or pd.isna(row['eeid']):
#                         continue  

#                     order = garnishment_order.objects.filter(cid=row['cid'], eeid=row['eeid']).first()

#                     if order:
                        
#                         has_changes = (
#                             order.case_id != row.get('case_id', None) or
#                             order.state != row['state'] or
#                             order.type != row['type'] or
#                             order.sdu != row.get('sdu', None) or
#                             order.start_date != row.get('start_date', None) or
#                             order.end_date != row.get('end_date', None) or
#                             float(order.amount) != float(row['amount']) or
#                             order.arrear_greater_than_12_weeks != row['arrear_greater_than_12_weeks'] or
#                             float(order.arrear_amount) != float(row['arrear_amount'])
#                         )

#                         if has_changes:
                            
#                             order.case_id = row.get('case_id', None)
#                             order.state = row['state']
#                             order.type = row['type']
#                             order.sdu = row.get('sdu', None)
#                             order.start_date = row.get('start_date', None)
#                             order.end_date = row.get('end_date', None)
#                             order.amount = row['amount']
#                             order.arrear_greater_than_12_weeks = row['arrear_greater_than_12_weeks']
#                             order.arrear_amount = row['arrear_amount']
#                             order.save()
#                             #updated_orders.append(order.cid)
#                             updated_orders.append({'cid': order.cid, 'eeid': order.eeid})
#                         else:
                            
#                             #no_change.append(order.cid)
#                             no_change.append({'cid': order.cid, 'eeid': order.eeid})
#                     else:
                      
#                         garnishment_order.objects.create(
#                             cid=row['cid'],
#                             eeid=row['eeid'],
#                             case_id=row.get('case_id', None),
#                             state=row['state'],
#                             type=row['type'],
#                             sdu=row.get('sdu', None),
#                             start_date=row.get('start_date', None),
#                             end_date=row.get('end_date', None),
#                             amount=row['amount'],
#                             arrear_greater_than_12_weeks=row['arrear_greater_than_12_weeks'],
#                             arrear_amount=row['arrear_amount']
#                         )
#                         #added_orders.append(row['cid'])
#                         added_orders.append({'cid': order.cid, 'eeid': order.eeid})

#                 except Exception as row_error:
                    
#                     print(f"Error processing row: {row}. Error: {row_error}")
#                     continue

        
#             response_data = []
#             if added_orders:
#                 response_data.append({
#                     'message': 'Garnishment orders imported successfully',
#                     'added_orders': added_orders
#                 })
#             if updated_orders:
#                 response_data.append({
#                     'message': 'Garnishment orders updated successfully',
#                     'updated_orders': updated_orders
#                 })
#             if no_change and not added_orders and not updated_orders:
#                 response_data = {'message': 'No change in data'}
#             elif no_change:
#                 response_data.append({
#                     'message': 'No change for certain orders',
#                     'no_change_orders': no_change
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)



#garnishment_data
#27/01 at 2:51 
#1
# @csrf_exempt
# def upsert_garnishment_order_api(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']  
#         file_name = file.name  
#         updated_orders = []
#         added_orders = []
#         no_change = []

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
#                 order = garnishment_order.objects.filter(cid=row['cid'], eeid=row['eeid']).first()

#                 if order:
#                     # Check for changess
#                     has_changes = (
#                         order.case_id != row.get('case_id', None) or
#                         order.state != row['state'] or
#                         order.type != row['type'] or
#                         order.sdu != row.get('sdu', None) or
#                         order.start_date != row.get('start_date', None) or
#                         order.end_date != row.get('end_date', None) or
#                         float(order.amount) != float(row['amount']) or
#                         order.arrear_greater_than_12_weeks != row['arrear_greater_than_12_weeks'] or
#                         float(order.arrear_amount) != float(row['arrear_amount'])
#                     )

#                     if has_changes:
#                         # Update garnishment order details
#                         order.case_id = row.get('case_id', None)
#                         order.state = row['state']
#                         order.type = row['type']
#                         order.sdu = row.get('sdu', None)
#                         order.start_date = row.get('start_date', None)
#                         order.end_date = row.get('end_date', None)
#                         order.amount = row['amount']
#                         order.arrear_greater_than_12_weeks = row['arrear_greater_than_12_weeks']
#                         order.arrear_amount = row['arrear_amount']
#                         order.save()
#                         updated_orders.append(order.cid)
#                     else:
#                         # No changes
#                         no_change.append(order.cid)
#                 else:
#                     # Add new garnishment order
#                     garnishment_order.objects.create(
#                         cid=row['cid'],
#                         eeid=row['eeid'],
#                         case_id=row.get('case_id', None),
#                         state=row['state'],
#                         type=row['type'],
#                         sdu=row.get('sdu', None),
#                         start_date=row.get('start_date', None),
#                         end_date=row.get('end_date', None),
#                         amount=row['amount'],
#                         arrear_greater_than_12_weeks=row['arrear_greater_than_12_weeks'],
#                         arrear_amount=row['arrear_amount']
#                     )
#                     added_orders.append(row['cid'])

#             # Prepare response
#             response_data = []
#             if added_orders:
#                 response_data.append({
#                     'message': 'Garnishment orders imported successfully',
#                     'added_orders': added_orders
#                 })
#             if updated_orders:
#                 response_data.append({
#                     'message': 'Garnishment orders updated successfully',
#                     'updated_orders': updated_orders
#                 })
#             if no_change and not added_orders and not updated_orders:
#                 response_data = {'message': 'No change in data'}
#             elif no_change:
#                 response_data.append({
#                     'message': 'No change for certain orders',
#                     'no_change_orders': no_change
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)


#garnishment_data
#27/01 at 2:51 
#1






#.................................................................
# import openpyxl
# from ..serializers import PayrollSerializer

# @csrf_exempt
# def upsert_payroll_data(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         print("called")
#         file = request.FILES['file']
#         updated_payrolls = []
#         added_payrolls = []

#         try:
#             if file.name.endswith('.csv'):
#                 data = list(csv.DictReader(file.read().decode('utf-8').splitlines()))
#             elif file.name.endswith(('.xls', '.xlsx')):
#                 df = pd.read_excel(file)
#                 data = df.to_dict(orient='records')  
#             else:
#                 return JsonResponse({'error': 'Unsupported file format. Please upload a CSV or Excel file.'}, status=400)

#             for row in data:
#                 row = {k: v for k, v in row.items() if k and not k.startswith('Unnamed:')}
#                 updated_row = {}

#                 for k, v in row.items():
#                     if isinstance(v, float) and math.isnan(v):
#                         updated_row[k] = None
#                     else:
#                         updated_row[k] = v

#                 try:
#                     payroll_record = payroll.objects.get(cid=updated_row['cid'], eeid=updated_row['eeid'], payroll_date=updated_row['payroll_date'])
#                     has_changes = False
                    
#                     for field_name in ['pay_date', 'gross_pay', 'net_pay', 'tax_federal_income_tax', 'tax_state_tax', 'tax_local_tax',
#                                        'tax_medicare_tax', 'tax_social_security', 'deduction_sdi', 'deduction_medical_insurance',
#                                        'deduction_401k', 'deduction_union_dues', 'deduction_voluntary', 'type', 'amount']:
#                         incoming_value = updated_row.get(field_name)
#                         if getattr(payroll_record, field_name) != incoming_value:
#                             has_changes = True
#                             break
                    
#                     if has_changes:
#                         for field_name in ['pay_date', 'gross_pay', 'net_pay', 'tax_federal_income_tax', 'tax_state_tax', 'tax_local_tax',
#                                            'tax_medicare_tax', 'tax_social_security', 'deduction_sdi', 'deduction_medical_insurance',
#                                            'deduction_401k', 'deduction_union_dues', 'deduction_voluntary', 'type', 'amount']:
#                             setattr(payroll_record, field_name, updated_row.get(field_name))
#                         payroll_record.save()
#                         updated_payrolls.append(updated_row['eeid'])
#                 except payroll.DoesNotExist:
#                     payroll.objects.create(
#                         cid=updated_row['cid'],
#                         eeid=updated_row['eeid'],
#                         payroll_date=updated_row['payroll_date'],
#                         pay_date=updated_row.get('pay_date'),
#                         gross_pay=updated_row.get('gross_pay'),
#                         net_pay=updated_row.get('net_pay'),
#                         tax_federal_income_tax=updated_row.get('tax_federal_income_tax'),
#                         tax_state_tax=updated_row.get('tax_state_tax'),
#                         tax_local_tax=updated_row.get('tax_local_tax'),
#                         tax_medicare_tax=updated_row.get('tax_medicare_tax'),
#                         tax_social_security=updated_row.get('tax_social_security'),
#                         deduction_sdi=updated_row.get('deduction_sdi'),
#                         deduction_medical_insurance=updated_row.get('deduction_medical_insurance'),
#                         deduction_401k=updated_row.get('deduction_401k'),
#                         deduction_union_dues=updated_row.get('deduction_union_dues'),
#                         deduction_voluntary=updated_row.get('deduction_voluntary'),
#                         type=updated_row.get('type'),
#                         amount=updated_row.get('amount')
#                     )
#                     added_payrolls.append(updated_row['eeid'])

#             if not updated_payrolls and not added_payrolls:
#                 return JsonResponse({'message': 'No data was updated or inserted.'}, status=200)

#             response_data = []
#             if added_payrolls:
#                 response_data.append({
#                     'message': 'Payroll records imported successfully',
#                     'added_payrolls': added_payrolls
#                 })
#             if updated_payrolls:
#                 response_data.append({
#                     'message': 'Payroll records updated successfully',
#                     'updated_payrolls': updated_payrolls
#                 })

#             return JsonResponse({'responses': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
