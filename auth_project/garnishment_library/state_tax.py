def cal_x_disposible_income(gross_income,total_deductions,x=0.25):
    disposable_earnings = round(gross_income - total_deductions, 2)
    monthly_garnishment_amount= disposable_earnings*x
    return(monthly_garnishment_amount)



