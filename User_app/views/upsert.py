from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from User_app.models import payroll  
from django.core.files.storage import default_storage
import csv
import pandas as pd




@csrf_exempt
def upsert_payroll_details_api(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']  
        file_name = file.name  
        updated_payrolls = []
        added_payrolls = []

        try:
            # Load data from file
            if file_name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                df = pd.read_excel(file)
            else:
                return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

            # Iterate through DataFrame rows
            for _, row in df.iterrows():
                payroll = payroll.objects.filter(
                    cid=row['cid'], 
                    eeid=row['eeid'], 
                    payroll_date=row['payroll_date']
                ).first()

                if payroll:
                    # Check for changes
                    has_changes = (
                        payroll.pay_date != row['pay_date'] or
                        payroll.gross_pay != row['gross_pay'] or
                        payroll.net_pay != row['net_pay'] or
                        payroll.taxes_federal_income_tax != row['taxes_federal_income_tax'] or
                        payroll.taxes_state_tax != row['taxes_state_tax'] or
                        payroll.taxes_local_tax != row['taxes_local_tax'] or
                        payroll.taxes_medicare_tax != row['taxes_medicare_tax'] or
                        payroll.taxes_sdi != row['taxes_sdi'] or
                        payroll.deductions != row['deductions'] or
                        payroll.type != row['type'] or
                        payroll.amount != row['amount']
                    )

                    if has_changes:
                        # Update payroll details
                        payroll.pay_date = row['pay_date']
                        payroll.gross_pay = row['gross_pay']
                        payroll.net_pay = row['net_pay']
                        payroll.taxes_federal_income_tax = row['taxes_federal_income_tax']
                        payroll.taxes_state_tax = row['taxes_state_tax']
                        payroll.taxes_local_tax = row['taxes_local_tax']
                        payroll.taxes_medicare_tax = row['taxes_medicare_tax']
                        payroll.taxes_sdi = row['taxes_sdi']
                        payroll.deductions = row['deductions']
                        payroll.type = row['type']
                        payroll.amount = row['amount']
                        payroll.save()
                        updated_payrolls.append(payroll.id)
                else:
                    # Add new payroll entry
                    payroll.objects.create(
                        cid=row['cid'],
                        eeid=row['eeid'],
                        payroll_date=row['payroll_date'],
                        pay_date=row['pay_date'],
                        gross_pay=row['gross_pay'],
                        net_pay=row['net_pay'],
                        taxes_federal_income_tax=row['taxes_federal_income_tax'],
                        taxes_state_tax=row['taxes_state_tax'],
                        taxes_local_tax=row['taxes_local_tax'],
                        taxes_medicare_tax=row['taxes_medicare_tax'],
                        taxes_sdi=row['taxes_sdi'],
                        deductions=row['deductions'],
                        type=row['type'],
                        amount=row['amount']
                    )
                    added_payrolls.append(row['cid'])

            # Prepare response
            response_data = []
            if added_payrolls:
                response_data.append({
                    'message': 'Payroll details imported successfully',
                    'added_payrolls': added_payrolls
                })
            if updated_payrolls:
                response_data.append({
                    'message': 'Payroll details updated successfully',
                    'updated_payrolls': updated_payrolls
                })

            return JsonResponse({'responses': response_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


from User_app.models import garnishment_order
@csrf_exempt
def upsert_garnishment_order_api(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']  
        file_name = file.name  
        updated_orders = []
        added_orders = []
        no_change = []

        try:
            # Load data from file
            if file_name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file_name.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb', '.odf', '.ods', '.odt')):
                df = pd.read_excel(file)
            else:
                return JsonResponse({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=400)

            # Iterate through DataFrame rows
            for _, row in df.iterrows():
                order = garnishment_order.objects.filter(cid=row['cid'], eeid=row['eeid']).first()

                if order:
                    # Check for changess
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
                        # Update garnishment order details
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
                        updated_orders.append(order.cid)
                    else:
                        # No changes
                        no_change.append(order.cid)
                else:
                    # Add new garnishment order
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
                    added_orders.append(row['cid'])

            # Prepare response
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
            if no_change and not added_orders and not updated_orders:
                response_data = {'message': 'No change in data'}
            elif no_change:
                response_data.append({
                    'message': 'No change for certain orders',
                    'no_change_orders': no_change
                })

            return JsonResponse({'responses': response_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


#garnishment_data
#27/01 at 2:51 
#1






#.................................................................
# # class payroll(models.Model):
# #     cid= models.CharField(max_length=255)
#     eeid= models.CharField(max_length=255)
#     payroll_date=models.DateField()
#     pay_date= models.DateField()
#     gross_pay=models.DecimalField(max_digits=250,decimal_places=2)
#     net_pay=models.DecimalField(max_digits=250,decimal_places=2)
#     tax_federal_income_tax=models.DecimalField(max_digits=250,decimal_places=2)
#     tax_state_tax=models.DecimalField(max_digits=250,decimal_places=2)
#     tax_local_tax=models.DecimalField(max_digits=250,decimal_places=2)
#     tax_medicare_tax=models.DecimalField(max_digits=250,decimal_places=2)
#     tax_social_security = models.CharField(max_length=255)
#     deduction_sdi=models.DecimalField(max_digits=250,decimal_places=2)
#     deduction_medical_insurance=models.DecimalField(max_digits=250,decimal_places=2)
#     deduction_401k=models.DecimalField(max_digits=250,decimal_places=2)
#     deduction_union_dues=models.DecimalField(max_digits=250,decimal_places=2)
#     deduction_voluntary=models.DecimalField(max_digits=250,decimal_places=2)
#     type=models.CharField(max_length=255)
#     amount=models.DecimalField(max_digits=250,decimal_places=2)

#     [amount, type,deduction_voluntary, deduction_union_dues, deduction_medical_insurance, deduction_401k, deduction_sdi, tax_social_security,
#     gross_pay,pay_date, payroll_date, pay_date, eeid, cid,
#      tax_medicare_tax, tax_local_tax,  tax_state_tax,  tax_federal_income_tax, net_pay  ]