# In this file we define the functions to calculate:
# project reserves
# equity funding


# We need to construct the timelines, so we import from utils-construct_timelines
from set_up.construct_timelines import (
    construct_calendar_year_list,
    construct_business_case_year_list,
    construct_operations_years_list,
    construct_decommissioning_years_list
)

import pandas as pd


# Project reserves
def project_reserves(**kwargs):
    '''This function creates a dataframe that contains all cashflows for project reserves (i.e., contingency) '''

    # 1. Get the parameters we need
    tender_year = kwargs['tender_year']
    capex = kwargs['capex']
    contingency_percentage = kwargs['contingency_percentage']

    # 2. Get the timelines
    calendar_years = construct_calendar_year_list(**kwargs)
    last_year = calendar_years[-1]

    # 3. Construct df
    row_names = [
        "contingency_injection", "contingency_reserve_balance",
        "contingency_reserve_to_dividents",
        ]

    df_project_reserves = pd.DataFrame(0.0, index=row_names, columns=calendar_years)
    df_project_reserves.columns.name = "project_reserves"

    # 4. Calculate contingency injection
    df_project_reserves.loc['contingency_injection', tender_year] = -capex * contingency_percentage

    # 5. Loop to calculate contingency balance and divident payout
    for x in calendar_years: 

        # Calculate the balance first
        if x == tender_year:
            # At the start of the project the balance is equal to the contingency injection
            df_project_reserves.loc['contingency_reserve_balance',x] = -df_project_reserves.loc['contingency_injection',x]
        else:
            # During the project 
            df_project_reserves.loc['contingency_reserve_balance',x] = (
                df_project_reserves.loc['contingency_reserve_balance',x-1] +
                df_project_reserves.loc['contingency_injection',x]
                )

        # Calculate divident payout (only in the last year of the timeline, i.e. after the project is finished)
        if x == last_year:
            available_balance = df_project_reserves.loc['contingency_reserve_balance',x]

            if available_balance > 0:
            
                # Payout of the full available balance
                df_project_reserves.loc['contingency_reserve_to_dividents', x] = available_balance

                # After paying out the divident, the balance will go to 0
                df_project_reserves.loc['contingency_reserve_balance', x] -= available_balance


    return df_project_reserves


# Equity funding
def equity_funding(df_decommissioning_phase,
                   df_debt_and_loan_part2,
                   df_construction_phase,
                   **kwargs):
    '''This function creates a dataframe that contains all cashflows for equity funding '''

    # 1. Get the parameters we need
    loan_percentage = kwargs['loan_percentage']

    # 2. Get the timelines
    calendar_years = construct_calendar_year_list(**kwargs)

    # 3. Construct df
    row_names = ['equity_injection', 'dividents_results', 'equity_cash_flow_result']
    df_equity_funding = pd.DataFrame(0.0, index=row_names, columns=calendar_years)
    df_equity_funding.columns.name = "equity_funding"

    # 4. Get the dfs constructed in previous steps
    df_reserves = project_reserves(**kwargs)
    df_decommissioning = df_decommissioning_phase
    df_debt_and_loan = df_debt_and_loan_part2
    df_construction = df_construction_phase

    # 5. Extract specific rows from the dfs
    contingency_injection = df_reserves.loc['contingency_injection']
    total_cashflow_decommissioning = df_decommissioning.loc['total_cashflow_decommissioning']
    cash_after_debt_service = df_debt_and_loan.loc['cash_after_debt_service']
    capex = df_construction.loc['capex']
    contingency_reserve_to_dividents = df_reserves.loc['contingency_reserve_to_dividents']

    # 6. Calculate equity injection
    equity_injection = contingency_injection + (capex *(1-loan_percentage)) + total_cashflow_decommissioning
    df_equity_funding.loc['equity_injection'] = equity_injection

    # 7. Calculate dividents results 
    df_equity_funding.loc['dividents_results'] = cash_after_debt_service + contingency_reserve_to_dividents

    # 8. Calculate equity cash flow result 
    df_equity_funding.loc['equity_cash_flow_result'] = df_equity_funding.loc['equity_injection'] + df_equity_funding.loc['dividents_results']

    return df_equity_funding