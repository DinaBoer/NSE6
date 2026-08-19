import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def run_oat_sensitivity(working_module, runner_module, base_parameters):
    """
    Runs a One-At-A-Time sensitivity analysis over all parameters in our dictionary.
    Calcualtes the impact of -10% en +10% on the chosen KPI's.
    """
    # We don't need to do the sensitivity over the general business case data
    excluded_keys = [
        "duration_construction", 
        "duration_operation", 
        "duration_decommissioning", 
        "tender_year",
        "depreciation",
        "annuity_loan",
        "construction_years_list",
        "contingency_percentage"
    ]

    sensitivity_results = []

    for key, original_value in base_parameters.items():

        if key in excluded_keys:
            continue

        row_data = {"Variable": key}

        # Calculate scenarios: -10% and +10%
        scenarios = (
            ("Minus_10", 0.9), 
            ("Plus_10", 1.1),
        )

        for factor_name, factor in scenarios:
            
            # 1. Create a clean deep copy of the base parameters
            scen_params = copy.deepcopy(base_parameters)
            
            # 2. Apply multiplication (works automatically for both numbers and DataFrames!)
            scen_params[key] = original_value * factor
            
            # 3. Run the business case using the runner
            project_kpi_df, equity_kpi_df, output_kpi_df = runner_module.run_business_case(working_module, scen_params)
                
            # 4. Extract results (ensure row labels match your exact output tables)
            row_data[f"Project_NPV_{factor_name}"] = project_kpi_df.loc['net_present_value'].iloc[0]
            row_data[f"Equity_NPV_{factor_name}"]  = equity_kpi_df.loc['net_present_value'].iloc[0]
            row_data[f"LCOH_{factor_name}"]        = output_kpi_df.loc['levelized_cost'].iloc[0]
            row_data[f"Gap_{factor_name}"]         = output_kpi_df.loc['levelized_profits'].iloc[0]
                
        sensitivity_results.append(row_data)

    # Convert collected data into the 4 dataframes
    df_sens = pd.DataFrame(sensitivity_results)

    # Helper function to clean up the dfs, set the index
    def finalize_table(df, value_cols):
        # Select target columns, rename them, and set 'Variable' as the clean index
        table = df[["Variable"] + value_cols].copy()
        table.rename(columns={value_cols[0]: "-10%", value_cols[1]: "+10%"}, inplace=True)
        table.set_index("Variable", inplace=True)

        # Return values into numeric floats for future use
        return table.apply(pd.to_numeric, errors='coerce')
    
    table_project_npv = finalize_table(df_sens, ["Project_NPV_Minus_10", "Project_NPV_Plus_10"])
    table_equity_npv  = finalize_table(df_sens, ["Equity_NPV_Minus_10", "Equity_NPV_Plus_10"])
    table_lco         = finalize_table(df_sens, ["LCOH_Minus_10", "LCOH_Plus_10"])
    table_gap         = finalize_table(df_sens, ["Gap_Minus_10", "Gap_Plus_10"])
    
    return table_project_npv, table_equity_npv, table_lco, table_gap




def get_base_case_values(working_module, runner_module, parameters):
    """
    Extracts baseline KPIs from any business case module
    """
    
    # Let the runner execute the business case
    project_df, equity_df, output_df = runner_module.run_business_case(working_module, parameters)

    # Get the numbers from the dfs
    return {
        'Project NPV':       project_df.loc['net_present_value'].iloc[0],
        'Equity NPV':        equity_df.loc['net_present_value'].iloc[0],
        'Levelized Cost':    output_df.loc['levelized_cost'].iloc[0],
        'Unprofitable Gap':  output_df.loc['levelized_profits'].iloc[0]
    }







def tornado_plot(df_sa, base_case, sa_type):

    # Create percentage change from the NPV values
    df_sensitivity_analysis_percentage = -(df_sa - base_case)/base_case*100

    # Sort the values. Here we use ascending=True because the default behavior of matplotlib's barh() function (which creates horizontal bar charts) 
    # is to plot the first entry at the bottom and the last entry at the top.
    df_sensitivity_analysis_percentage.sort_values(by='-10%', key=abs, ascending=True, inplace=True)

    # Data for the tornado plot
    variables = df_sensitivity_analysis_percentage.index.tolist()

    negative_changes = df_sensitivity_analysis_percentage['-10%'].tolist()
    positive_changes = df_sensitivity_analysis_percentage['+10%'].tolist()

    # Create the tornado plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Define bar positions
    y_pos = np.arange(len(variables))

    # Create horizontal bars
    ax.barh(y_pos, negative_changes, align='center', color='red', label='-10%')
    ax.barh(y_pos, positive_changes, align='center', color='blue', label='+10%')

    # Add a vertical line at the base value (0)
    ax.axvline(x=0, color='black', linestyle='--')

    # Remove underscore from variables for the figure names
    cleaned_variables = [var.replace("_", " ")
                        .replace("variable", "")
                        .replace("df", "")
                        .strip()
                        .capitalize()
                        .replace("Capex", "CAPEX")
                        .replace("Opex", "OPEX")
                        .replace("Hwi", "HWI")
                        .replace("Wacc", "WACC") for var in variables]

    # Set y-axis labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(cleaned_variables)

    # Add labels and title
    ax.set_xlabel(f'Change in {sa_type} (%)')
    ax.set_title('Sensitivity Analysis')

    # Add grey horizontal grid lines
    ax.grid(True, axis='y', color='grey', linestyle='-', linewidth=0.5, alpha=0.3)

    # Show legend
    ax.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()






        