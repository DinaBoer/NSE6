from decimal import Decimal, ROUND_HALF_UP
from OWF_input_data import *
from NSE_get_data_from_ESDL import *


def owf_run_all_functions(capex_variable,
                          df_opex_variable,
                          inflation_variable,
                          revenues_to_electrolyser_variable,
                          revenues_to_market_variable,
                          loan_percentage_variable,
                          loan_interest_rate_variable,
                          income_tax_rate_variable,
                          wacc_variable,
                          duration_operation_variable):    
    

    # Here we import all the functions from the working file
    from ipynb.fs.defs.OWF_working_file import (construct_calendar_year_list, 
                                                construct_business_case_year_list, 
                                                construct_operations_years_list, 
                                                construct_decomissioning_years_list, 
                                                construction_phase,
                                                operational_phase,
                                                decommissioning_phase,
                                                taxes_and_profits_part1,
                                                debt_and_loan_part1,
                                                taxes_and_profits_part2,
                                                debt_and_loan_part2,
                                                project_reserves,
                                                equity_funding,
                                                present_value_cashflows,
                                                cumulative_equity_and_debt_cashflows,
                                                discounted_cashflows_for_levelized_cost,
                                                levelized_cost_and_revenues,
                                                project_kpi,
                                                equity_kpi,
                                                output_kpi)

    construct_calendar_year_list(duration_operation_variable)
    construct_business_case_year_list(duration_operation_variable)
    construct_operations_years_list(duration_operation_variable)
    construct_decomissioning_years_list(duration_operation_variable)

    construction_phase(capex_variable,duration_operation_variable)

    operational_phase(df_opex_variable,
                      inflation_variable,
                      revenues_to_electrolyser_variable,
                      revenues_to_market_variable,
                      duration_operation_variable)

    decommissioning_phase(capex_variable,inflation_variable,duration_operation_variable)

    taxes_and_profits_part1(capex_variable,
                            df_opex_variable,
                            inflation_variable,
                            revenues_to_electrolyser_variable,
                            revenues_to_market_variable,
                            duration_operation_variable)

    debt_and_loan_part1(capex_variable,loan_percentage_variable,loan_interest_rate_variable,duration_operation_variable)

    taxes_and_profits_part2(capex_variable,
                            df_opex_variable,
                            inflation_variable,
                            revenues_to_electrolyser_variable,
                            revenues_to_market_variable,
                            loan_percentage_variable,
                            loan_interest_rate_variable,
                            income_tax_rate_variable,
                            duration_operation_variable)

    debt_and_loan_part2(capex_variable,
                        df_opex_variable,
                        inflation_variable,
                        revenues_to_electrolyser_variable,
                        revenues_to_market_variable,
                        loan_percentage_variable,
                        loan_interest_rate_variable,
                        income_tax_rate_variable,
                        duration_operation_variable)

    project_reserves(capex_variable,duration_operation_variable)

    equity_funding(capex_variable,
                   df_opex_variable,
                   inflation_variable,
                   revenues_to_electrolyser_variable,
                   revenues_to_market_variable,
                   loan_percentage_variable,
                   loan_interest_rate_variable,
                   income_tax_rate_variable,
                   duration_operation_variable)

    present_value_cashflows(capex_variable,
                            df_opex_variable,
                            inflation_variable,
                            revenues_to_electrolyser_variable,
                            revenues_to_market_variable,
                            loan_percentage_variable,
                            loan_interest_rate_variable,
                            income_tax_rate_variable,
                            wacc_variable,
                            duration_operation_variable)

    cumulative_equity_and_debt_cashflows(capex_variable,
                                         df_opex_variable,
                                         inflation_variable,
                                         revenues_to_electrolyser_variable,
                                         revenues_to_market_variable,
                                         loan_percentage_variable,
                                         loan_interest_rate_variable,
                                         income_tax_rate_variable,
                                         duration_operation_variable)

    discounted_cashflows_for_levelized_cost(capex_variable,
                                            df_opex_variable,
                                            inflation_variable,
                                            revenues_to_electrolyser_variable,
                                            revenues_to_market_variable,
                                            loan_percentage_variable,
                                            loan_interest_rate_variable,
                                            income_tax_rate_variable,
                                            wacc_variable,
                                            duration_operation_variable)

    levelized_cost_and_revenues(capex_variable,
                                df_opex_variable,
                                inflation_variable,
                                revenues_to_electrolyser_variable,
                                revenues_to_market_variable,
                                loan_percentage_variable,
                                loan_interest_rate_variable,
                                income_tax_rate_variable,
                                wacc_variable,
                                duration_operation_variable)


    project_kpi(capex_variable,
                df_opex_variable,
                inflation_variable,
                revenues_to_electrolyser_variable,
                revenues_to_market_variable,
                loan_percentage_variable,
                loan_interest_rate_variable,
                income_tax_rate_variable,
                wacc_variable,
                duration_operation_variable)

    equity_kpi(capex_variable,
               df_opex_variable,
               inflation_variable,
               revenues_to_electrolyser_variable,
               revenues_to_market_variable,
               loan_percentage_variable,
               loan_interest_rate_variable,
               income_tax_rate_variable,
               wacc_variable,
               duration_operation_variable)

    output_kpi(capex_variable,
               df_opex_variable,
               inflation_variable,
               revenues_to_electrolyser_variable,
               revenues_to_market_variable,
               loan_percentage_variable,
               loan_interest_rate_variable,
               income_tax_rate_variable,
               wacc_variable,
               duration_operation_variable)