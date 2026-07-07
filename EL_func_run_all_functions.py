from decimal import Decimal, ROUND_HALF_UP
from NSE_get_data_from_ESDL import *
from EL_input_data import *



def el_run_all_functions(capex_variable,
                         df_opex_variable,
                         inflation_variable,
                         annual_electricity_costs_ppa_variable,
                         annual_electricity_costs_grid_variable,
                         electricity_grid_connection_variable,
                         h2_storage_costs_variable,
                         df_stack_replacement_costs_variable,
                         hydrogen_revenues_variable,
                         hwi_revenues_variable,
                         decommissioning_variable,
                         loan_percentage_variable,
                         loan_interest_rate_variable,
                         income_tax_rate_variable,
                         wacc_variable,
                         lifetime_investment_variable):

        # Here we import all the functions from the working file
    from ipynb.fs.defs.EL_working_file import (construct_calendar_year_list, 
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

    
    construct_calendar_year_list(lifetime_investment_variable)
    construct_business_case_year_list(lifetime_investment_variable)
    construct_operations_years_list(lifetime_investment_variable)
    construct_decomissioning_years_list(lifetime_investment_variable)

    construction_phase(capex_variable,lifetime_investment_variable)

    operational_phase(df_opex_variable,
                      inflation_variable,
                      annual_electricity_costs_ppa_variable,
                      annual_electricity_costs_grid_variable,
                      electricity_grid_connection_variable,
                      h2_storage_costs_variable,
                      df_stack_replacement_costs_variable,
                      hydrogen_revenues_variable,
                      hwi_revenues_variable,
                      lifetime_investment_variable)

    decommissioning_phase(capex_variable,inflation_variable,decommissioning_variable,lifetime_investment_variable)

    taxes_and_profits_part1(capex_variable,
                            df_opex_variable,
                            inflation_variable,
                            annual_electricity_costs_ppa_variable,
                            annual_electricity_costs_grid_variable,
                            electricity_grid_connection_variable,
                            h2_storage_costs_variable,
                            df_stack_replacement_costs_variable,
                            hydrogen_revenues_variable,
                            hwi_revenues_variable,
                            lifetime_investment_variable)

    debt_and_loan_part1(capex_variable,
                        loan_percentage_variable,
                        loan_interest_rate_variable,
                        lifetime_investment_variable)

    taxes_and_profits_part2(capex_variable,
                            df_opex_variable,
                            inflation_variable,
                            annual_electricity_costs_ppa_variable,
                            annual_electricity_costs_grid_variable,
                            electricity_grid_connection_variable,
                            h2_storage_costs_variable,
                            df_stack_replacement_costs_variable,
                            hydrogen_revenues_variable,
                            hwi_revenues_variable,
                            loan_percentage_variable,
                            loan_interest_rate_variable,
                            income_tax_rate_variable,
                            lifetime_investment_variable)

    debt_and_loan_part2(capex_variable,
                        df_opex_variable,
                        inflation_variable,
                        annual_electricity_costs_ppa_variable,
                        annual_electricity_costs_grid_variable,
                        electricity_grid_connection_variable,
                        h2_storage_costs_variable,
                        df_stack_replacement_costs_variable,
                        hydrogen_revenues_variable,
                        hwi_revenues_variable,
                        loan_percentage_variable,
                        loan_interest_rate_variable,
                        income_tax_rate_variable,
                        lifetime_investment_variable)

    project_reserves(capex_variable,lifetime_investment_variable)

    equity_funding(capex_variable,
                   df_opex_variable,
                   inflation_variable,
                   annual_electricity_costs_ppa_variable,
                   annual_electricity_costs_grid_variable,
                   electricity_grid_connection_variable,
                   h2_storage_costs_variable,
                   df_stack_replacement_costs_variable,
                   hydrogen_revenues_variable,
                   hwi_revenues_variable,
                   decommissioning_variable,
                   loan_percentage_variable,
                   loan_interest_rate_variable,
                   income_tax_rate_variable,
                   lifetime_investment_variable)

    present_value_cashflows(capex_variable,
                            df_opex_variable,
                            inflation_variable,
                            annual_electricity_costs_ppa_variable,
                            annual_electricity_costs_grid_variable,
                            electricity_grid_connection_variable,
                            h2_storage_costs_variable,
                            df_stack_replacement_costs_variable,
                            hydrogen_revenues_variable,
                            hwi_revenues_variable,
                            decommissioning_variable,
                            loan_percentage_variable,
                            loan_interest_rate_variable,
                            income_tax_rate_variable,
                            wacc_variable,
                            lifetime_investment_variable)

    cumulative_equity_and_debt_cashflows(capex_variable,
                                         df_opex_variable,
                                         inflation_variable,
                                         annual_electricity_costs_ppa_variable,
                                         annual_electricity_costs_grid_variable,
                                         electricity_grid_connection_variable,
                                         h2_storage_costs_variable,
                                         df_stack_replacement_costs_variable,
                                         hydrogen_revenues_variable,
                                         hwi_revenues_variable,
                                         decommissioning_variable,
                                         loan_percentage_variable,
                                         loan_interest_rate_variable,
                                         income_tax_rate_variable,
                                         lifetime_investment_variable)

    discounted_cashflows_for_levelized_cost(capex_variable,
                                            df_opex_variable,
                                            inflation_variable,
                                            annual_electricity_costs_ppa_variable,
                                            annual_electricity_costs_grid_variable,
                                            electricity_grid_connection_variable,
                                            h2_storage_costs_variable,
                                            df_stack_replacement_costs_variable,
                                            hydrogen_revenues_variable,
                                            hwi_revenues_variable,
                                            decommissioning_variable,
                                            loan_percentage_variable,
                                            loan_interest_rate_variable,
                                            income_tax_rate_variable,
                                            wacc_variable,
                                            lifetime_investment_variable)

    levelized_cost_and_revenues(capex_variable,
                                df_opex_variable,
                                inflation_variable,
                                annual_electricity_costs_ppa_variable,
                                annual_electricity_costs_grid_variable,
                                electricity_grid_connection_variable,
                                h2_storage_costs_variable,
                                df_stack_replacement_costs_variable,
                                hydrogen_revenues_variable,
                                hwi_revenues_variable,
                                decommissioning_variable,
                                loan_percentage_variable,
                                loan_interest_rate_variable,
                                income_tax_rate_variable,
                                wacc_variable,
                                lifetime_investment_variable)


    project_kpi(capex_variable,
                df_opex_variable,
                inflation_variable,
                annual_electricity_costs_ppa_variable,
                annual_electricity_costs_grid_variable,
                electricity_grid_connection_variable,
                h2_storage_costs_variable,
                df_stack_replacement_costs_variable,
                hydrogen_revenues_variable,
                hwi_revenues_variable,
                decommissioning_variable,
                loan_percentage_variable,
                loan_interest_rate_variable,
                income_tax_rate_variable,
                wacc_variable,
                lifetime_investment_variable)

    equity_kpi(capex_variable,
               df_opex_variable,
               inflation_variable,
               annual_electricity_costs_ppa_variable,
               annual_electricity_costs_grid_variable,
               electricity_grid_connection_variable,
               h2_storage_costs_variable,
               df_stack_replacement_costs_variable,
               hydrogen_revenues_variable,
               hwi_revenues_variable,
               decommissioning_variable,
               loan_percentage_variable,
               loan_interest_rate_variable,
               income_tax_rate_variable,
               wacc_variable,
               lifetime_investment_variable)

    output_kpi(capex_variable,
               df_opex_variable,
               inflation_variable,
               annual_electricity_costs_ppa_variable,
               annual_electricity_costs_grid_variable,
               electricity_grid_connection_variable,
               h2_storage_costs_variable,
               df_stack_replacement_costs_variable,
               hydrogen_revenues_variable,
               hwi_revenues_variable,
               decommissioning_variable,
               loan_percentage_variable,
               loan_interest_rate_variable,
               income_tax_rate_variable,
               wacc_variable,
               lifetime_investment_variable)