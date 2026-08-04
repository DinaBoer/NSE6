# In this file we define the functions to calculate:
# present value cashflows
# cumulative equity and debt cash flows


# We need to construct the timelines, so we import from utils-construct_timelines
from set_up.construct_timelines import (
    construct_calendar_year_list,
    construct_business_case_year_list,
    construct_operations_years_list,
    construct_decommissioning_years_list
)

import pandas as pd
import numpy as np

# present value cashflows
def present_value_cashflows(df_construction_phase,
                            df_operational_phase,
                            df_decommissioning_phase,
                            df_equity_funding,
                            **kwargs):
    ''' This function creates a dataframe that contains all present value cashflows '''

    # 1. Get the parameters we need
    wacc = kwargs['wacc']

    # 2. Get the timelines
    calendar_years = construct_calendar_year_list(**kwargs)
    business_case_years = construct_business_case_year_list(**kwargs)

    # 3. Construct df
    row_names = [
        'sum_net_project_cash_flows',
        'present_value_net_cashflows',
        'cumulative_value_net_cashflows', 
        'present_value_equity_cashflows'
    ]
    df_present_value = pd.DataFrame(0.0, index = row_names, columns=calendar_years)
    df_present_value.columns.name = "present_value"
    
    # 4. Get the dfs constructed in previous steps
    df_construction = df_construction_phase
    df_operational = df_operational_phase
    df_decommissioning = df_decommissioning_phase
    df_equity = df_equity_funding

    # 5. Calculate sum of the net project cashflows and add to df  
    df_present_value.loc['sum_net_project_cash_flows'] = (
        df_construction.loc['total_cashflow_investment'] +
        df_operational.loc['net_cashflow_operations'] + 
        df_decommissioning.loc['total_cashflow_decommissioning']
    )
    
    # 6. Create the discount factors
    discount_factors = (1 + wacc) ** np.array(business_case_years)

    # 7. Calculate present value of net cashflows
    df_present_value.loc['present_value_net_cashflows'] = (
        df_present_value.loc['sum_net_project_cash_flows'] / discount_factors
    )

    # 8. Calculate cumulative value of net cashflows 
    df_present_value.loc['cumulative_value_net_cashflows'] = (
        df_present_value.loc['present_value_net_cashflows'].cumsum()
    )

    # 9. Calculate present value of equity cashflows
    equity_cash_flow_result = df_equity.loc['equity_cash_flow_result']
    df_present_value.loc['present_value_equity_cashflows'] = equity_cash_flow_result / discount_factors
    

    return df_present_value


# Cumulative equity and debt cashflows
def cumulative_equity_and_debt_cashflows(df_equity_funding,
                                         df_debt_and_loan_part1,
                                         **kwargs):
    '''This function creates a dataframe that contains the cumulative equity and debt cashflows'''

    # 1. Get the timelines
    calendar_years = construct_calendar_year_list(**kwargs)

    # 2. Construct df
    row_names = ['cumulative_equity_cashflow', 'cumulative_debt_cashflow']
    df_cumulative_equity_and_debt = pd.DataFrame(0.0, index= row_names, columns=calendar_years)
    df_cumulative_equity_and_debt.columns.name = "cumulative equity and debt"
    
    # 3. Get the dfs constructed in previous steps
    df_equity = df_equity_funding
    df_debt_and_loan = df_debt_and_loan_part1

    # 4. Calculate cumulative equity cashflow
    df_cumulative_equity_and_debt.loc['cumulative_equity_cashflow'] = (
        df_equity.loc['equity_cash_flow_result'].cumsum()
    )

    # 5. Calculate the cumulative debt cashflow
    df_cumulative_equity_and_debt.loc['cumulative_debt_cashflow'] = (
        -df_debt_and_loan.loc['end_of_year']
    )
   
    return df_cumulative_equity_and_debt