def run_business_case(working_module, params): 
    """
    Runs all business cases by passing the parameter dictionary into the functions

    working_module: the imported working file module containing the formula functions.
    params: a dictionary containing all required input variables. 
    """

    # step 1: Timeline construction
    working_module.construct_calender_year_list(params)
    working_module.construct_business_case_year_list(params)
    working_module.construct_operations_years_list(params)
    working_module.construct_decommissioning_years_list(params)

    # step 2: Set up construction, operation and decommissioning phases
    working_module.construction_phase(params)
    working_module.operational_phase(params)
    working_module.decommissioning_phase(params)

    # step 3: Set up financial sections
    working_module.taxes_and_profits_part1(params)
    working_module.debt_and_loan_part1(params)
    working_module.taxes_and_profits_part2(params)
    working_module.debt_and_loan_part2(params)
    working_module.project_reserves(params)
    working_module.equity_funcing(params)

    # step 4: Cashflow present values & levelized costs
    working_module.present_value_cashflows(params)
    working_module.cumulative_equity_and_debt_cashflows(params)
    working_module.discounted_cashflows_for_levelized_cost(params)
    working_module.levelized_cost_and_revenues(params)
    
    # step 5: KPIs
    working_module.project_kpi(params)
    working_module.equity_kpi(params)
    working_module.output_kpi(params)



