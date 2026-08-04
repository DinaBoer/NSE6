# Import the timelines
from set_up import construct_timelines as timelines

# Import the financial functions
from finances import taxes_debt_loans as tax_debt
from finances import project_reserves_and_equity as reserves_equity
from finances import present_value_and_cumulative_cashflows as cashflows
from finances import kpis



def run_business_case(working_module, params): 
    """
    Runs all business cases by passing the parameter dictionary into the functions

    working_module: the imported working file module containing the formula functions.
    params: a dictionary containing all required input variables. 
    """

    # step 1: Timeline construction
    timelines.construct_calendar_year_list(**params)
    timelines.construct_business_case_year_list(**params)
    timelines.construct_operations_years_list(**params)
    timelines.construct_decommissioning_years_list(**params)

    # step 2: Set up construction, operation and decommissioning phases
    df_construction_phase = working_module.construction_phase(**params)
    df_operational_phase = working_module.operational_phase(**params)
    df_decommissioning_phase = working_module.decommissioning_phase(**params)

    # step 3: Set up financial sections
    df_taxes_and_profits_part1 = tax_debt.taxes_and_profits_part1(df_operational_phase,**params)
    df_debt_and_loan_part1 = tax_debt.debt_and_loan_part1(**params)
    df_taxes_and_profits_part2 = tax_debt.taxes_and_profits_part2(df_operational_phase,
                                                                  df_taxes_and_profits_part1,
                                                                  df_debt_and_loan_part1,
                                                                  **params)
    df_debt_and_loan_part2 = tax_debt.debt_and_loan_part2(df_operational_phase,
                                                          df_debt_and_loan_part1,
                                                          df_taxes_and_profits_part2,
                                                          **params)

    reserves_equity.project_reserves(**params)
    df_equity_funding = reserves_equity.equity_funding(df_decommissioning_phase,
                                                       df_debt_and_loan_part2,
                                                       df_construction_phase,
                                                       **params)

    # step 4: Cashflow present values & cumulative cashflows
    df_present_value_cashflows = cashflows.present_value_cashflows(df_construction_phase,
                                                                   df_operational_phase,
                                                                   df_decommissioning_phase,
                                                                   df_equity_funding,
                                                                   **params)
    cashflows.cumulative_equity_and_debt_cashflows(df_equity_funding,
                                                   df_debt_and_loan_part1,
                                                   **params)

    # step 5: Levelized costs
    working_module.discounted_cashflows_for_levelized_cost(**params)
    df_levelized_cost_and_revenues = working_module.levelized_cost_and_revenues(**params)
    
    # step 5: KPIs
    project_kpi_df = kpis.project_kpi(df_present_value_cashflows,
                                      df_taxes_and_profits_part2,
                                      df_construction_phase,
                                      **params)
    equity_kpi_df = kpis.equity_kpi(df_equity_funding,
                                    df_present_value_cashflows,
                                    **params)
    output_kpi_df = kpis.output_kpi(df_levelized_cost_and_revenues,
                                    **params)

    return project_kpi_df, equity_kpi_df, output_kpi_df

