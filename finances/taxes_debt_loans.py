# In this file we define the functions to calculate:
# Taxes & profits
# Debts & loans

# We need to construct the timelines, so we import from utils-construct_timelines
from set_up.construct_timelines import (
    construct_calendar_year_list,
    construct_business_case_year_list,
    construct_operations_years_list,
    construct_decommissioning_years_list
)

import pandas as pd
import numpy as np

# Taxes and profits part 1: 
def taxes_and_profits_part1(df_operational_phase,**kwargs):
    ''' This function creates a dataframe that contains all cashflows for taxes & profits
        It consists of two parts, as it is dependent on the debt and loan calculations'''
    
    # 1. Get the parameters we need
    capex = kwargs['capex']
    depreciation = kwargs['depreciation']

    # 2. Get the timelines
    calendar_years = construct_calendar_year_list(**kwargs)
    operational_years = construct_operations_years_list(**kwargs)

    # 3. Get the results from construction and operational phases
    df_operations = df_operational_phase
    ebitda = df_operations.loc['net_cashflow_operations']

    # 4. Construct df
    row_names = ['depreciation', 'ebit']
    df_taxes_profits = pd.DataFrame(0.0, index=row_names, columns=calendar_years)
    df_taxes_profits.columns.name = "taxes_and_profits"
    
    # 5. Calculate depreciation
    yearly_depreciation = capex/depreciation

    df_taxes_profits.loc['depreciation'] = np.where(
        df_taxes_profits.columns.isin(operational_years), 
        -yearly_depreciation, 0.0
    )
    
    # 5. Calculate EBIT = EBITDA + depreciation 
    df_taxes_profits.loc['ebit'] = ebitda + df_taxes_profits.loc['depreciation']

    
    return df_taxes_profits

# To continue the taxes and profits calculations, the interest costs are needed
# Therefore we first go to debt & loan calculations

def debt_and_loan_part1(**kwargs):
    ''' This function creates a dataframe that contains all cashflows for debt and loans
        It consists of two parts because it is dependent on the taxes & profits calculations'''

    # Using **kwargs we can pass the dictionary of parameters from the input data file into the function here

    # 1. Get the parameters we need
    capex = kwargs['capex']
    loan_percentage = kwargs['loan_percentage']
    loan_interest_rate = kwargs['loan_interest_rate']
    tender_year = kwargs['tender_year']
    annuity_loan = kwargs['annuity_loan']
    construction_years_list = kwargs['construction_years_list']

    # 2. Get the timelines
    calendar_years = construct_calendar_year_list(**kwargs)
    operational_years = construct_operations_years_list(**kwargs)
    construction_years = construction_years_list

    # 3. Construct df
    row_names = [
        "begin_of_year", "drawdown", "repayment_capital",
    "end_of_year", "repayment_interest",
    ]
    df_debt_and_loan = pd.DataFrame(0.0, index=row_names, columns=calendar_years)
    df_debt_and_loan.columns.name = "debt_and_loan"

    # 4. Calculate loan drawdown
    total_loan = capex * loan_percentage
    yearly_drawdown = total_loan / len(construction_years)

    df_debt_and_loan.loc["drawdown"] = np.where(
        df_debt_and_loan.columns.isin(construction_years_list),
        yearly_drawdown, 0.0
    )

    # 5. Debt calculations
    for x in calendar_years:
      
        # begin of year
        if x == tender_year:
            df_debt_and_loan.loc['begin_of_year',x] = 0
        else:
            df_debt_and_loan.loc['begin_of_year',x] = df_debt_and_loan.loc['end_of_year',x-1]
        
        # repayment interest
        if x in operational_years:
            current_debt = df_debt_and_loan.loc['begin_of_year',x] + df_debt_and_loan.loc['drawdown',x]

            interest_payment = -current_debt * loan_interest_rate
            df_debt_and_loan.loc['repayment_interest',x] = interest_payment
    
        # repayment capital
        if x in operational_years:

            # the min-function returns the lowest item, so min(5,10) will return 5
            df_debt_and_loan.loc['repayment_capital',x] = -min(
                    current_debt, 
                    annuity_loan + interest_payment
                    )
       
        # end of year
        df_debt_and_loan.loc['end_of_year',x] = (
            df_debt_and_loan.loc['begin_of_year',x] + 
            df_debt_and_loan.loc['drawdown',x] + 
            df_debt_and_loan.loc['repayment_capital',x])

    return df_debt_and_loan


# For the cash flow available for debt service, we need the tax expenses. 
# So we go back to Taxes & profits, and after that is finished we go back to Debt & loan - part 2

def taxes_and_profits_part2(df_operational_phase,
                            df_taxes_and_profits_part1,
                            df_debt_and_loan_part1,
                            **kwargs):
    ''' This function creates a dataframe that contains all cashflows for taxes and profits
        This is the second part of the taxes and profits calculations.'''
    
    # 1. Get the parameters we need
    income_tax_rate = kwargs['income_tax_rate']

    # 2. Get the dataframes constructed in the previous steps
    df_taxes_profits = df_taxes_and_profits_part1.copy()

    # 3. Import interest costs from the debt and loan df and add to taxes & profits df
    interest_costs = df_debt_and_loan_part1.loc['repayment_interest']  
    df_taxes_profits.loc['interest_costs'] = interest_costs

    # 4. Calculate EBT = EBIT + interest_costs 
    df_taxes_profits.loc['ebt'] = df_taxes_profits.loc['ebit'] + interest_costs

    # 5. Calculate tax expenses
    # If EBT>0, calculate tax, else 0

    ebt_series = df_taxes_profits.loc['ebt']
    df_taxes_profits.loc['tax_expenses'] = np.where(ebt_series > 0, -ebt_series * income_tax_rate, 0.0)

    # 6. Calculate net profits by adding tax expenses to ebt
    df_taxes_profits.loc['net_profits'] = df_taxes_profits.loc['ebt'] + df_taxes_profits.loc['tax_expenses']

    return df_taxes_profits


# still to do for debt & loan: 
# cash flow available for debt service
# debt service (capital + interest)
# cash flow after debt service

def debt_and_loan_part2(df_operational_phase,
                        df_debt_and_loan_part1,
                        df_taxes_and_profits_part2,
                        **kwargs):
    ''' This function creates a dataframe that contains all cashflows for debt and loans
        This is the second part of the debt and loans calculations.'''

    # 1. Get the dfs constructed in the previous steps
    df_debt_and_loan = df_debt_and_loan_part1.copy()
    df_operational = df_operational_phase

    # 2. Extract the specific rows we need from previous dfs
    tax_expenses = df_taxes_and_profits_part2.loc['tax_expenses']
    net_cashflow_operations = df_operational.loc['net_cashflow_operations']

    # 3. Calculate cash flow available for debt service
    # tax expenses is already negative, net cashflow operations is positive
    df_debt_and_loan.loc['cash_flow_for_debt'] = net_cashflow_operations + tax_expenses

    # 4. Calculate debt service (capital + interest repayments)
    df_debt_and_loan.loc['debt_service'] = df_debt_and_loan.loc['repayment_capital'] + df_debt_and_loan.loc['repayment_interest']

    # 5. Calculate cash after debt service 
    df_debt_and_loan.loc['cash_after_debt_service'] = df_debt_and_loan.loc['cash_flow_for_debt'] + df_debt_and_loan.loc['debt_service']
    
    return df_debt_and_loan