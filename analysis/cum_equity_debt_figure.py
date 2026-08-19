import numpy as np
import matplotlib.pyplot as plt

def plot_cumulative_cashflows(working_module, runner_module, parameters):
    """
    Executes a business case scenario and generates a cumulative equity and debt figure
    """

    # Run the business case and get the details dictionary (i.e. the saved intermediate dfs of each function)
    # _, _, _, is a conventional way of saying 'I don't need this value'
    # we cannot just say 'details = ..' because run_business_case returns 4 object as a tuple, that we need to unpack
    _, _, _, details = runner_module.run_business_case(working_module, parameters, return_details=True)
    

    # Extract the timeline years from from the details dictionary
    years = details['calendar_years']

    # Get the cumulative equity and debt cashflows from the details dictionary
    df_cumulative_equity_debt = details['cumulative_equity_debt']

    # Extract rows to lists
    cumulative_equity_cashflow = df_cumulative_equity_debt.loc['cumulative_equity_cashflow'].tolist()
    cumulative_debt_cashflow = df_cumulative_equity_debt.loc['cumulative_debt_cashflow'].tolist()

    # Plot

    # Set the width of each bar
    bar_width = 0.35

    # Set the position of the bars on the x-axis
    r1 = np.arange(len(years))
    r2 = [x + bar_width for x in r1]

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bars for cumulative equity cashflow
    ax.bar(r1, cumulative_equity_cashflow, color='blue', width=bar_width, label='Equity Cashflow')

    # Create bars for cumulative debt cashflow
    ax.bar(r2, cumulative_debt_cashflow, color='red', width=bar_width, label='Debt Cashflow')

    # Add a horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1)

    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Cashflow (MEUR)')
    ax.set_title('Cumulative Equity and Debt Cashflows')

    # Add xticks on the middle of the group bars
    ax.set_xticks([r + bar_width/2 for r in range(len(years))])
    ax.set_xticklabels(years, rotation=45)

    # Add legend
    ax.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()
