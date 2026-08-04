# In this file we define the functions to calculate:
# project_kpi
# equity_kpi
# output_kpi


# We need to construct the timelines, so we import from utils-construct_timelines
from set_up.construct_timelines import (
    construct_calendar_year_list,
    construct_business_case_year_list,
    construct_operations_years_list,
    construct_decommissioning_years_list
)

import pandas as pd
import numpy as np
import numpy_financial as npf


# Project kpi
def project_kpi(df_present_value_cashflows,
                df_taxes_and_profits_part2,
                df_construction_phase,
                **kwargs):
    '''This function creates a dataframe that contains the project KPI's'''

    # Using **kwargs we can pass the dictionary of parameters from the input data file into the function here

    # 1. Get the parameters we need
    wacc = kwargs['wacc']
    lifetime_investment = kwargs['lifetime_investment']
    construction_years_list = kwargs['construction_years_list']

    # 2. Construct df
    df_project_kpi = pd.DataFrame(columns=['Value','Unit'])
    df_project_kpi.columns.name = "Project KPIs"
    
    # 3. Get the dfs constructed in previous steps
    df_present_value = df_present_value_cashflows
    df_taxes_profits = df_taxes_and_profits_part2
    df_construction = df_construction_phase

    # 4. Extract the series we need
    sum_net_project_cashflows = df_present_value.loc['sum_net_project_cash_flows']
    present_value_net_cashflows = df_present_value.loc['present_value_net_cashflows']
    net_profits = df_taxes_profits.loc['net_profits']
    total_cashflow_investment = df_construction.loc['total_cashflow_investment']

    # 5. Calculate NPV and IRR
    df_project_kpi.loc['net_present_value'] = [npf.npv(wacc,sum_net_project_cashflows), 'MEUR']
    df_project_kpi.loc['internal_rate_of_return'] = [npf.irr(sum_net_project_cashflows) * 100,'%']    # times 100 to give percentage

    # 6. Calculate ROI
    total_investment_sum = -total_cashflow_investment.sum()
    df_project_kpi.loc['return_on_investment'] = [net_profits.sum() / total_investment_sum * 100, '%']
    
    # 7. Calculate Simple Payback Period
    df_project_kpi.loc['payback_period'] = [total_investment_sum / (net_profits.sum() / lifetime_investment), 'years']

    # 7. Calculate PP 
    df_project_kpi.loc['payback_period'] = [total_investment_sum / (net_profits.sum() / lifetime_investment), 'years']

    # 8. Calculate discounted ROI and PP
    # Here we look up only the present value cashflows for the construction years
    pv_investment = present_value_net_cashflows.loc[construction_years_list].sum()

    # Here we look up the present value cashflows that are in the operational years
    pv_returns = present_value_net_cashflows.loc[construct_operations_years_list(**kwargs)].sum()

    # Discounted ROI
    discounted_roi = (pv_investment + pv_returns) / -pv_investment * 100
    df_project_kpi.loc['discounted_return_on_investment'] = [discounted_roi, '%']

    # Discounted PP
    discounted_pp = -pv_investment / (pv_returns / lifetime_investment)
    df_project_kpi.loc['discounted_payback_period'] = [discounted_pp, 'years']  
 
    return df_project_kpi


# Equity KPI's
def equity_kpi(df_equity_funding, 
               df_present_value_cashflows,
               **kwargs):
    '''This function creates a dataframe that contains the equity KPI's'''

    # 1. Get the parameters we need
    wacc = kwargs['wacc']
    lifetime_investment = kwargs['lifetime_investment']
    construction_years_list = kwargs['construction_years_list']

    # 2. construct df
    df_equity_kpi = pd.DataFrame(columns=['Value','Unit'])
    df_equity_kpi.columns.name = "Equity KPIs"
    
    # 3. Get the dataframes constructed in the previous steps
    df_equity_funding = df_equity_funding
    df_present_value = df_present_value_cashflows

    # 4. Extract the series we need
    equity_injection = df_equity_funding.loc['equity_injection']
    dividents_results = df_equity_funding.loc['dividents_results']
    equity_cash_flow_result = df_equity_funding.loc['equity_cash_flow_result']
    present_value_equity_cashflows = df_present_value.loc['present_value_equity_cashflows']

    # 5. Calculate NPV and IRR
    df_equity_kpi.loc['net_present_value'] = [npf.npv(wacc,equity_cash_flow_result), 'MEUR']
    df_equity_kpi.loc['internal_rate_of_return'] = [npf.irr(equity_cash_flow_result) * 100,'%']    # times 100 to give percentage

    # 6. Calculate ROI
    total_equity_inj = -equity_injection.sum()
    return_on_investment = [dividents_results.sum() / total_equity_inj *100,'%']
    df_equity_kpi.loc['return_of_investment'] = return_on_investment

    # 7. Calculate PP
    payback_period = [total_equity_inj / (dividents_results.sum() / lifetime_investment), 'years']
    df_equity_kpi.loc['payback_period'] = payback_period
    
    # 8. Calculate discounted ROI and PP
    # Here we look up only the present value cashflows for the construction years
    pv_investment = present_value_equity_cashflows.loc[construction_years_list].sum()

    # Here we look up the present value cashflows that are in the operational years
    pv_returns = present_value_equity_cashflows.loc[construct_operations_years_list(**kwargs)].sum()

    # Discounted ROI
    discounted_roi = (pv_investment + pv_returns) / -pv_investment * 100
    df_equity_kpi.loc['discounted_return_on_investment'] = [discounted_roi, '%']

    # Discounted Payback Period
    discounted_pp = -pv_investment / (pv_returns / lifetime_investment)
    df_equity_kpi.loc['discounted_payback_period'] = [discounted_pp, 'years'] 
   
    
    return df_equity_kpi



# Output KPI's
def output_kpi(df_levelized_cost_and_revenues,**kwargs):
    '''This function creates a dataframe that contains the output KPI's'''

    # 1. Construct df
    df_output_kpi = pd.DataFrame(columns=['Value','Unit'])
    df_output_kpi.columns.name = "Output KPIs"
    
    # 2. Get the df constructed in previous steps
    df_levelized_costs_and_revenues = df_levelized_cost_and_revenues

    # calculate levelized costs
    levelized_costs = (df_levelized_costs_and_revenues['cost'].sum() - 
                       df_levelized_costs_and_revenues.loc['profits','cost'])
    df_output_kpi.loc['levelized_cost'] = [levelized_costs, 'Eur/MWh']

    # calculate levelized revenues 
    levelized_revenues = (df_levelized_costs_and_revenues['revenues'].sum() - 
                          df_levelized_costs_and_revenues.loc['unprofitable_gap','revenues'])
    df_output_kpi.loc['levelized_revenues'] = [levelized_revenues, 'Eur/MWh']

    # calculate levelized profits
    levelized_profits = (df_output_kpi.loc['levelized_revenues','Value'] - 
                         df_output_kpi.loc['levelized_cost','Value'])
    df_output_kpi.loc['levelized_profits'] = [levelized_profits, 'Eur/MWh']

    return df_output_kpi