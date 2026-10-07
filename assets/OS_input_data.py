# =============================================================================
# Imports & initialization
# =============================================================================
from esdl import esdl
from esdl.esdl_handler import EnergySystemHandler
import pandas as pd
import numpy as np
import numpy_financial as npf
from decimal import Decimal, ROUND_HALF_UP
import pickle
from pathlib import Path


# Load pickle file from 'NSE_get_data_from_ESDL'
base_dir = Path(__file__).resolve().parent.parent
filename = base_dir/'esdl_files'/'NSE_get_data_from_ESDL.pkl'
with open(filename, 'rb') as f:
    variables = pickle.load(f)

# Here we define the input variables received from the pkl file
asset_parameters = variables['asset_parameters']
drop_scenarios = variables['drop_scenarios']

# =============================================================================
# Scenario selection
# =============================================================================
# Map scenario names to their respective list index
Scenario_mapping = {
    "pessimistic": 0,
    "most_likely": 1,
    "optimistic": 2
}

# Determine which scenario is active based on what is NOT dropped
all_scenarios = {"pessimistic", "most_likely", "optimistic"}
active_scenario_name = list(all_scenarios - set(drop_scenarios))[0]
active_index = Scenario_mapping[active_scenario_name]

print(f"Active Scenario: {active_scenario_name} (Index: {active_index})")

# =============================================================================
# Load operational analysis data
# =============================================================================

#type 'yes' to update the variables retrieved from Operation_analysis_OWF_EL.ipynb. 
# Else, the stored variables in the Pickle file will be used. This latter helps to run the program faster
update_operation_analysis = 'no'

if update_operation_analysis == 'yes':
    from importnb import Notebook
    with Notebook():
        import Operation_analysis_OWF_EL as OA  # Alias as needed

    start_year = OA.start_year
    solar_capacity = OA.solar_capacity
    electricity_grid_capacity = OA.electricity_grid_capacity

    margin_2030 = OA.rev_E_market_2030_S + OA.rev_E_PPA_2030_S  # define the margin to order scenarios on
    df_2030 = pd.concat([margin_2030, OA.rev_E_market_2030_S, OA.rev_E_PPA_2030_S, OA.E_sold_2030_S])
    df_2030 = df_2030[df_2030.iloc[0].sort_values().index]
    rev_E_market_2030_S = df_2030.iloc[1].tolist()
    rev_E_PPA_2030_S = df_2030.iloc[2].tolist()
    E_sold_2030_S = df_2030.iloc[3].tolist()

    margin_2040 = OA.rev_E_market_2040_S + OA.rev_E_PPA_2040_S # define the margin to order scenarios on
    df_2040 = pd.concat([margin_2040, OA.rev_E_market_2040_S, OA.rev_E_PPA_2040_S, OA.E_sold_2040_S])
    df_2040 = df_2040[df_2040.iloc[0].sort_values().index]
    rev_E_market_2040_S = df_2040.iloc[1].tolist()
    rev_E_PPA_2040_S = df_2040.iloc[2].tolist()
    E_sold_2040_S = df_2040.iloc[3].tolist()

    margin_2050 = OA.rev_E_market_2050_S + OA.rev_E_PPA_2050_S # define the margin to order scenarios on
    df_2050 = pd.concat([margin_2050, OA.rev_E_market_2050_S, OA.rev_E_PPA_2050_S, OA.E_sold_2050_S])
    df_2050 = df_2050[df_2050.iloc[0].sort_values().index]
    rev_E_market_2050_S = df_2050.iloc[1].tolist()
    rev_E_PPA_2050_S = df_2050.iloc[2].tolist()
    E_sold_2050_S = df_2050.iloc[3].tolist()

else:
    # Load the Pickle file with stored data from Operation_analysis
    filename = 'Operation_Analysis_variables.pkl'
    with open(filename, 'rb') as f:
        oa_data = pickle.load(f)

    start_year = oa_data['start_year']
    solar_capacity = oa_data['solar_capacity']
    electricity_grid_capacity = oa_data['electricity_grid_capacity']

    rev_E_market_2030_S = oa_data['rev_E_market_2030_S']
    rev_E_PPA_2030_S = oa_data['rev_E_PPA_2030_S']
    E_sold_2030_S = oa_data['E_sold_2030_S']

    rev_E_market_2040_S = oa_data['rev_E_market_2040_S']
    rev_E_PPA_2040_S = oa_data['rev_E_PPA_2040_S']
    E_sold_2040_S = oa_data['E_sold_2040_S']

    rev_E_market_2050_S = oa_data['rev_E_market_2050_S']
    rev_E_PPA_2050_S = oa_data['rev_E_PPA_2050_S']
    E_sold_2050_S = oa_data['E_sold_2050_S']

    # Margin calculations    
    margin_2030 = rev_E_market_2030_S + rev_E_PPA_2030_S # define the margin to order scenarios on
    df_2030 = pd.concat([margin_2030, rev_E_market_2030_S, rev_E_PPA_2030_S, E_sold_2030_S])
    df_2030 = df_2030[df_2030.iloc[0].sort_values().index]
    rev_E_market_2030_S = df_2030.iloc[1].tolist()
    rev_E_PPA_2030_S = df_2030.iloc[2].tolist()
    E_sold_2030_S = df_2030.iloc[3].tolist()

    margin_2040 = rev_E_market_2040_S + rev_E_PPA_2040_S # define the margin to order scenarios on
    df_2040 = pd.concat([margin_2040, rev_E_market_2040_S, rev_E_PPA_2040_S, E_sold_2040_S])
    df_2040 = df_2040[df_2040.iloc[0].sort_values().index]
    rev_E_market_2040_S = df_2040.iloc[1].tolist()
    rev_E_PPA_2040_S = df_2040.iloc[2].tolist()
    E_sold_2040_S = df_2040.iloc[3].tolist()

    margin_2050 = rev_E_market_2050_S + rev_E_PPA_2050_S # define the margin to order scenarios on
    df_2050 = pd.concat([margin_2050, rev_E_market_2050_S, rev_E_PPA_2050_S, E_sold_2050_S])
    df_2050 = df_2050[df_2050.iloc[0].sort_values().index]
    rev_E_market_2050_S = df_2050.iloc[1].tolist()
    rev_E_PPA_2050_S = df_2050.iloc[2].tolist()
    E_sold_2050_S = df_2050.iloc[3].tolist()


# =============================================================================
# Input data - from Mapeditor
# =============================================================================

# os_capex = asset_parameters['investment_costs']['TNVDW']         # in MEUR
# os_fixed_opex = asset_parameters['fixed_opex']['TNVDW']/100      # converted 2 percent to 0.02
# os_var_opex = asset_parameters['variable_opex']['TNVDW']         # in Eur/MWh
# os_general_WACC = asset_parameters.loc['TNVDW','wacc']/100          # from % to decimal

# The cable costs depend on the length of the cables
# In Mapeditor, a straight line between OS and Eemshaven is approximately 111694 meter
#cable_distance = 111694 / 1000     # km


# =============================================================================
# Input data - from factsheet
# =============================================================================

# Used factsheet: NSE5_Factsheet_OffshoreSolar 
# Date: 14-08-2024

# format: [2030[pes-ml-opt], 2040[pes-ml-opt], 2050[pes-ml-opt]]

#solar_capacity = 700                                                       # MW, based on TNVDW                                                     
module_capacity = [[0.05,0.05,0.05],[0.01,0.1,1],[0.01,0.1,1]]              # MW 

capex = [[3,1.5,1],[3,1.5,1],[3,1.5,1]]                                     # MEUR/MWp, only 2030 numbers available in factsheet. Assumed that this is the total CAPEX of full plant
opex = [[30000,22500,20000],[30000,22500,20000],[30000,22500,20000]]        # EUR/MWp/yr   

# revenues and volumes
os_revenues_to_electrolyser = [rev_E_PPA_2030_S, rev_E_PPA_2040_S, rev_E_PPA_2050_S]      # EUR/year
os_revenues_to_market = [rev_E_market_2030_S, rev_E_market_2040_S, rev_E_market_2050_S]   # EUR/year
os_sold_electricity = [E_sold_2030_S, E_sold_2030_S, E_sold_2030_S]                       # EUR/year

# =============================================================================
# Select active scenario and interpolate to get yearly data
# =============================================================================

# Define all factsheet data in a dictionary
# If new parameters are added with format: [2030[pes-ml-opt], 2040[pes-ml-opt], 2050[pes-ml-opt]], they should be added in this dictionary
raw_factsheet_data = {
    'module_capacity': module_capacity,
    'capex': capex,
    'opex': opex,
    'os_revenues_to_electrolyser': os_revenues_to_electrolyser,
    'os_revenues_to_market': os_revenues_to_market,
    'os_sold_electricity': os_sold_electricity
}

# Set up a dataframe 
all_years = range(2027,2100,1)
df_yearly_data = pd.DataFrame(index=raw_factsheet_data.keys(), columns=all_years)

# Loop over the dictionary and interpolate between data points to create values for each year
for name, data_array in raw_factsheet_data.items():

    # first get the value for the active scenario for each year
    # data_array[0] = 2030, data_array[1] = 2040, data_array[2]=2050
    # [active_index] extracts only the chosen pessimistic/most_likely/optimistic value
    value_2030 = data_array[0][active_index]
    value_2040 = data_array[1][active_index]
    value_2050 = data_array[2][active_index]


    # Fill in the dataframe year by year
    for year in all_years:
        if year <= 2030:
            df_yearly_data.loc[name,year] = value_2030

        elif 2030 < year < 2040: 
            # linear interpolation between 2030 and 2040
            df_yearly_data.loc[name,year] = value_2030 + ((value_2040-value_2030) / 10) * (year - 2030)

        elif year == 2040:
            df_yearly_data.loc[name,year] = value_2040

        elif 2040 < year < 2050:
            df_yearly_data.loc[name, year] = value_2040 + ((value_2050-value_2040) / 10)* (year - 2040)

        elif year >= 2050:
            df_yearly_data.loc[name,year] = value_2050


# print(df_yearly_data)


# =============================================================================
# Revenues and electricity sold from operational analysis file
# =============================================================================

################ Comment this section if you want to run the BC without the operation analysis file
os_revenues_to_electrolyser = pd.DataFrame(columns=all_years)
os_revenues_to_market = pd.DataFrame(columns=all_years)
os_sold_electricity = pd.DataFrame(columns=all_years)

os_revenues_to_electrolyser.loc['os_revenues_to_electrolyser'] = np.array(df_yearly_data.loc['os_revenues_to_electrolyser']) / 1E6      #in MEUR
os_revenues_to_market.loc['os_revenues_to_market'] = np.array(df_yearly_data.loc['os_revenues_to_market']) / 1E6                        #in MEUR
os_sold_electricity.loc['os_sold_electricity'] = np.array(df_yearly_data.loc['os_sold_electricity'])                                    #in MWh


# =============================================================================
# Input data from Excel
# =============================================================================

# Data format: [pessimistic, most_likely, optimistic]

# General data: business case length
os_lifetime_list = [25, 25, 25]                            # years
duration_construction_list = [3, 3, 3]
duration_operation_list = os_lifetime_list                 # amount of operational years is equal to lifetime of the investment
duration_decommissioning_list = [2, 2, 2]
tender_year_list = [start_year-duration_construction_list[0], start_year-duration_construction_list[1], start_year-duration_construction_list[2]]                       # year at which business case is 0, 
                       # year at which business case is 0, i.e., year before start construction

# Cost data from 'inflation-WACC' sheet
os_income_tax_rate_list = [0.258, 0.258, 0.258]            # in %
os_inflation_list = [0.02, 0.02, 0.02]                     # in %
os_general_WACC_list = [0.0925, 0.085, 0.0775]             # in %   Assumption - base case is the same as OWF
os_loan_interest_rate_list = [0.065, 0.05, 0.035]          # in %
os_length_of_loan_list = [15, 15, 15]                      # years
os_loan_type = 'annuity'
os_depreciation_list = [25, 25, 30]                        # years  Possibly change to os_depreciation_list = os_lifetime_list

# Cost data from 'cost data os' sheet
os_contingency_list = [0.1, 0.1, 0.1]                      # in %
os_loan_percentage_list = [0.75, 0.75, 0.75]               # in %
os_decommissioning_percentage_list = [0.02, 0.02, 0.02]     # in %

# =============================================================================
# Get active scenario for Excel data
# =============================================================================

# Get the active scenario (i.e., pes/ml,opt) for each parameter
# If new inputs are added in format: [pessimistic, most_likely, optimistic], they should be added here

os_lifetime = os_lifetime_list[active_index]
duration_construction = duration_construction_list[active_index]
duration_operation = duration_operation_list[active_index]
duration_decommissioning = duration_decommissioning_list[active_index]
tender_year = tender_year_list[active_index]

os_income_tax_rate = os_income_tax_rate_list[active_index]
os_inflation = os_inflation_list[active_index]
os_general_WACC = os_general_WACC_list[active_index]
os_loan_interest_rate = os_loan_interest_rate_list[active_index]
os_length_of_loan = os_length_of_loan_list[active_index]
os_depreciation = os_depreciation_list[active_index]
os_contingency = os_contingency_list[active_index]
os_loan_percentage = os_loan_percentage_list[active_index]
os_decommissioning_percentage = os_decommissioning_percentage_list[active_index]

# =============================================================================
# Calculate cost data
# =============================================================================

# We need the number of modules because some of the cost data is given per module
# TWe use np.ceil to round the value up to the closest integer
# Then we multiply the rounded number with the module capacity to get a new total windfarm capacity,
# which is equal to or slightly higher than the original 700 MW capacity

number_of_modules = np.ceil(solar_capacity / df_yearly_data.loc['module_capacity', tender_year])
new_solar_capacity = number_of_modules * df_yearly_data.loc['module_capacity', tender_year]

# capex
os_capex = (df_yearly_data.loc['capex', tender_year] * new_solar_capacity)

# opex
df_os_opex = pd.DataFrame(columns=all_years)
df_os_opex.loc['opex'] = np.array(df_yearly_data.loc['opex']) * new_solar_capacity / 1E6        # in MEUR/year


# debt financing

os_loan = os_capex * os_loan_percentage

# numpy financial calculates the annuity payment for the loan. Same as the PMT function in Excel (but slightly different arguments). See 'Cost data os' cell C9.
os_annuity_loan = -npf.pmt(os_loan_interest_rate, os_length_of_loan, os_loan, fv=0, when='end')

# construction years
year_construction_start = tender_year + 1
construction_years_list = list(range(year_construction_start, year_construction_start + duration_construction))

# =============================================================================
# PARAMETER DICTIONARY
# =============================================================================
os_parameters = {
    # General business case data
    'lifetime_investment': os_lifetime,
    'duration_construction': duration_construction,
    'duration_operation': duration_operation,
    'duration_decommissioning': duration_decommissioning,
    'tender_year': tender_year,

    # Financial & cost parameters
    'wacc': os_general_WACC,
    'income_tax_rate': os_income_tax_rate,
    'inflation': os_inflation,
    'loan_interest_rate': os_loan_interest_rate,
    'loan_percentage': os_loan_percentage,
    'decommissioning_percentage': os_decommissioning_percentage,

    # CAPEX & OPEX
    'capex': os_capex,
    'opex_df': df_os_opex,

    # Technology specific
    'revenues_to_electrolyser': os_revenues_to_electrolyser,
    'revenues_to_market': os_revenues_to_market,
    # 'sold_electricity': os_sold_electricity,

    # Additional parameters required to generalize functions
    'depreciation': os_depreciation,
    'annuity_loan': os_annuity_loan,
    'construction_years_list': construction_years_list,
    'contingency_percentage': os_contingency,
}

