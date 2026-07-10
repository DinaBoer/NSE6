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

# Load pickle file from 'NSE_get_data_from_ESDL'
filename = 'NSE_get_data_from_ESDL.pkl'
with open(filename, 'rb') as f:
    variables = pickle.load(f)

esdl_variables = {key: variables[key] for key in ['drop_scenarios', 'asset_parameters']}
globals().update(esdl_variables)


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

# Choose electrolyser size of 100MW or 500MW
electrolyser_unit_size = '100MW'

# =============================================================================
# Load operational analysis data
# =============================================================================

#type 'yes' to update the variables retrieved from Operation_analysis_OWF_EL.ipynb. Else, the stored variables in the Pickle file will be used. The latter helps to run the program faster
update_operation_analysis = 'no'

if update_operation_analysis == 'yes':
    from importnb import Notebook
    with Notebook():
        import Operation_analysis_OWF_EL as OA  # Alias as needed

    start_year = OA.start_year
    electrolyser_capacity = OA.electrolyser_capacity
    electricity_grid_capacity = OA.electricity_grid_capacity

    margin_2030 = OA.rev_H2_PPA_2030 - OA.costs_E_PPA_2030 - OA.costs_E_market_2030 - OA.storage_costs_2030 # define the margin to order scenarios on
    df_2030 = pd.concat([margin_2030, OA.rev_H2_PPA_2030, OA.costs_E_PPA_2030, OA.costs_E_market_2030, OA.storage_costs_2030, OA.H2_sold_2030])
    df_2030 = df_2030[df_2030.iloc[0].sort_values().index]
    rev_H2_PPA_2030 = df_2030.iloc[1].tolist()
    costs_E_PPA_2030 = df_2030.iloc[2].tolist()
    costs_E_market_2030 = df_2030.iloc[3].tolist()
    storage_costs_2030 = df_2030.iloc[4].tolist()
    H2_sold_2030 = df_2030.iloc[5].tolist()

    margin_2040 = OA.rev_H2_PPA_2040 - OA.costs_E_PPA_2040 - OA.costs_E_market_2040 - OA.storage_costs_2040 # define the margin to order scenarios on
    df_2040 = pd.concat([margin_2040, OA.rev_H2_PPA_2040, OA.costs_E_PPA_2040, OA.costs_E_market_2040, OA.storage_costs_2040, OA.H2_sold_2040])
    df_2040 = df_2040[df_2040.iloc[0].sort_values().index]
    rev_H2_PPA_2040 = df_2040.iloc[1].tolist()
    costs_E_PPA_2040 = df_2040.iloc[2].tolist()
    costs_E_market_2040 = df_2040.iloc[3].tolist()
    storage_costs_2040 = df_2040.iloc[4].tolist()
    H2_sold_2040 = df_2040.iloc[5].tolist()

    margin_2050 = OA.rev_H2_PPA_2050 - OA.costs_E_PPA_2050 - OA.costs_E_market_2050 - OA.storage_costs_2050 # define the margin to order scenarios on
    df_2050 = pd.concat([margin_2050, OA.rev_H2_PPA_2050, OA.costs_E_PPA_2050, OA.costs_E_market_2050, OA.storage_costs_2050, OA.H2_sold_2050])
    df_2050 = df_2050[df_2050.iloc[0].sort_values().index]
    rev_H2_PPA_2050 = df_2050.iloc[1].tolist()
    costs_E_PPA_2050 = df_2050.iloc[2].tolist()
    costs_E_market_2050 = df_2050.iloc[3].tolist()
    storage_costs_2050 = df_2050.iloc[4].tolist()
    H2_sold_2050 = df_2050.iloc[5].tolist()

else:
    # Load the Pickle file with stored data from Operation_analysis
    filename = 'Operation_Analysis_variables.pkl'
    with open(filename, 'rb') as f:
        variables = pickle.load(f)

    # Select the variables that are needed for this Business Case
    specific_vars = {key: variables[key] for key in ['start_year', 'electrolyser_capacity', 'electricity_grid_capacity', 'lhv_h2_kwh_kg',
                                                     'E_purchased_by_EL_2030', 'E_purchased_by_EL_2040', 'E_purchased_by_EL_2050',
                                                     'E_purchased_by_EL_from_market_2030', 'E_purchased_by_EL_from_market_2040', 'E_purchased_by_EL_from_market_2050',
                                                     'E_purchased_by_EL_from_PPA_2030', 'E_purchased_by_EL_from_PPA_2040', 'E_purchased_by_EL_from_PPA_2050',
                                                     'costs_E_market_2030', 'costs_E_PPA_2030', 'rev_H2_PPA_2030', 'storage_costs_2030', 'H2_sold_2030',
                                                     'costs_E_market_2040', 'costs_E_PPA_2040', 'rev_H2_PPA_2040', 'storage_costs_2040', 'H2_sold_2040',
                                                     'costs_E_market_2050', 'costs_E_PPA_2050', 'rev_H2_PPA_2050', 'storage_costs_2050', 'H2_sold_2050'] if key in variables}

    # Use the specific variables in the current environment
    globals().update(specific_vars)
    
    margin_2030 = rev_H2_PPA_2030 - costs_E_PPA_2030 - costs_E_market_2030 - storage_costs_2030 # define the margin to order scenarios on
    df_2030 = pd.concat([margin_2030, rev_H2_PPA_2030, costs_E_PPA_2030, costs_E_market_2030, storage_costs_2030, H2_sold_2030])
    df_2030 = df_2030[df_2030.iloc[0].sort_values().index]
    rev_H2_PPA_2030 = df_2030.iloc[1].tolist()
    costs_E_PPA_2030 = df_2030.iloc[2].tolist()
    costs_E_market_2030 = df_2030.iloc[3].tolist()
    storage_costs_2030 = df_2030.iloc[4].tolist()
    H2_sold_2030 = df_2030.iloc[5].tolist()

    margin_2040 = rev_H2_PPA_2040 - costs_E_PPA_2040 - costs_E_market_2040 - storage_costs_2040 # define the margin to order scenarios on
    df_2040 = pd.concat([margin_2040, rev_H2_PPA_2040, costs_E_PPA_2040, costs_E_market_2040, storage_costs_2040, H2_sold_2040])
    df_2040 = df_2040[df_2040.iloc[0].sort_values().index]
    rev_H2_PPA_2040 = df_2040.iloc[1].tolist()
    costs_E_PPA_2040 = df_2040.iloc[2].tolist()
    costs_E_market_2040 = df_2040.iloc[3].tolist()
    storage_costs_2040 = df_2040.iloc[4].tolist()
    H2_sold_2040 = df_2040.iloc[5].tolist()

    margin_2050 = rev_H2_PPA_2050 - costs_E_PPA_2050 - costs_E_market_2050 - storage_costs_2050 # define the margin to order scenarios on
    df_2050 = pd.concat([margin_2050, rev_H2_PPA_2050, costs_E_PPA_2050, costs_E_market_2050, storage_costs_2050, H2_sold_2050])
    df_2050 = df_2050[df_2050.iloc[0].sort_values().index]
    rev_H2_PPA_2050 = df_2050.iloc[1].tolist()
    costs_E_PPA_2050 = df_2050.iloc[2].tolist()
    costs_E_market_2050 = df_2050.iloc[3].tolist()
    storage_costs_2050 = df_2050.iloc[4].tolist()
    H2_sold_2050 = df_2050.iloc[5].tolist()


# =============================================================================
# Input data - from Mapeditor
# =============================================================================


# el_capex?
# el_opex?
#el_general_wacc = asset_parameters.loc['Electrolyzer','wacc']/100      # from % to decimal #commented for now, can be updated in mapeditor later
el_general_wacc_list = [0.095, 0.095, 0.07]                             # similar to OnEL
# el_efficiency = asset_parameters['efficiency']['Electrolyzer']        # decimal, i.e., 60% # use factsheet info for now

# =============================================================================
# Input data - from factsheet
# =============================================================================

# Used factsheet: Electrolysis_PEM_100MW  & Electrolysis_PEM_500MW
# Date: 22-08-2024

# format: [2030[pes-ml-opt], 2040[pes-ml-opt], 2050[pes-ml-opt]]

# In factsheet capex is given more detailed: electrolyser + bop + compressor + indirect cost and owner cost + unforseen cost

# 100 MW electrolyser
capex_total_100mw = [[7299,4178,2493],[6836,3910,2348],[6836,3910,2348]]        # EUR/kW    excludes stack replacement and contingency
stack_replacement_100mw = [[1500,810,450],[1390,752,421],[1390,752,421]]        # EUR/kW (15% of total CAPEX)   
opex_100mw = [[484,311,86],[436,233,52],[436,233,52]]                           # EUR/kW/yr  CHECK UNIT FROM UPDATED FACTSHEET!!  

# 500 MW electrolyser
# factsheet does not contain 2030 data, because it is expected not to exist at that time
# here, we use the 2040 data for all years up to and including 2040. 

capex_total_500mw = [[6200,3534,2119],[6200,3534,2119],[6200,3534,2119]]        # EUR/kW  excludes stack replacement and contingency
stack_replacement_500mw = [[1092,585,333],[1092,585,333],[1092,585,333]]        # EUR/kW (15% of total CAPEX)  
opex_500mw = [[339,187,43],[339,187,43],[339,187,43]]                           # EUR/kW/yr   CHECK UNIT FROM UPDATED FACTSHEET!!   

# HWI price - from CE Delft report 'Toetsing beleidsontwikkelingen waterstof' 2024
hwi_price = [[5.12, 5.16, 5.20],[5.12,5.16,5.20],[5.12,5.16,5.20]]              # EUR/kgH2

# costs and revenues
el_electricity_costs_ppa = [costs_E_PPA_2030, costs_E_PPA_2040, costs_E_PPA_2050]               # EUR/year
el_electricity_costs_grid = [costs_E_market_2030, costs_E_market_2040, costs_E_market_2050]     # EUR/year
h2_revenues_hpa = [rev_H2_PPA_2030, rev_H2_PPA_2040, rev_H2_PPA_2050]                           # EUR/year
h2_storage_costs = [storage_costs_2030, storage_costs_2040, storage_costs_2050]                 # EUR/year
h2_sold_to_hpa = [H2_sold_2030, H2_sold_2040, H2_sold_2050]                                     # MWh/year
h2_sold_to_hpa_kg = np.array(h2_sold_to_hpa) * 1000 / lhv_h2_kwh_kg                             # kg/year   

electricity_tax = [[1.88, 1.88, 1.88],[1.88, 1.88, 1.88],[1.88, 1.88, 1.88]]                    # Eur/MWh, 2024 values from belastingdienst

E_purchased_by_EL_2030 = E_purchased_by_EL_2030.values.flatten().tolist()                       # GWh
E_purchased_by_EL_2040 = E_purchased_by_EL_2040.values.flatten().tolist()                       # GWh
E_purchased_by_EL_2050 = E_purchased_by_EL_2050.values.flatten().tolist()                       # GWh
E_purchased_by_EL = [E_purchased_by_EL_2030, E_purchased_by_EL_2040, E_purchased_by_EL_2050]    # GWh

E_purchased_by_EL_from_market_2030 = E_purchased_by_EL_from_market_2030.values.flatten().tolist()
E_purchased_by_EL_from_market_2040 = E_purchased_by_EL_from_market_2040.values.flatten().tolist()
E_purchased_by_EL_from_market_2050 = E_purchased_by_EL_from_market_2050.values.flatten().tolist()
E_purchased_by_EL_from_market = [E_purchased_by_EL_from_market_2030, E_purchased_by_EL_from_market_2040, E_purchased_by_EL_from_market_2050]

E_purchased_by_EL_from_PPA_2030 = E_purchased_by_EL_from_PPA_2030.values.flatten().tolist()
E_purchased_by_EL_from_PPA_2040 = E_purchased_by_EL_from_PPA_2040.values.flatten().tolist()
E_purchased_by_EL_from_PPA_2050 = E_purchased_by_EL_from_PPA_2050.values.flatten().tolist()
E_purchased_by_EL_from_PPA = [E_purchased_by_EL_from_PPA_2030, E_purchased_by_EL_from_PPA_2040, E_purchased_by_EL_from_PPA_2050]


# =============================================================================
# Select active scenario and interpolate to get yearly data
# =============================================================================

# Define all factsheet data in a dictionary
# If new parameters are added with format: [2030[pes-ml-opt], 2040[pes-ml-opt], 2050[pes-ml-opt]], they should be added in this dictionary
raw_factsheet_data = {
    'electricity_tax': electricity_tax,
    'capex_total_100mw': capex_total_100mw,
    'stack_replacement_100mw': stack_replacement_100mw,
    'opex_100mw': opex_100mw,
    'capex_total_500mw': capex_total_500mw,
    'stack_replacement_500mw': stack_replacement_500mw,
    'opex_500mw': opex_500mw,
    'hwi_price': hwi_price,
    'el_electricity_costs_ppa': el_electricity_costs_ppa,
    'el_electricity_costs_grid': el_electricity_costs_grid,
    'h2_revenues_hpa': h2_revenues_hpa,
    'h2_storage_costs': h2_storage_costs,
    'h2_sold_to_hpa': h2_sold_to_hpa,
    'h2_sold_to_hpa_kg': h2_sold_to_hpa_kg,
    'E_purchased_by_EL': E_purchased_by_EL,
    'E_purchased_by_EL_from_market': E_purchased_by_EL_from_market,
    'E_purchased_by_EL_from_PPA': E_purchased_by_EL_from_PPA
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
# Make df for electrolyser sizes
# =============================================================================

# here we make a df with just the opex numbers, so we can let the model use 100MW or 500MW electrolyser

# Opex 100 MW electrolyser 
df_el_opex_100mw = pd.DataFrame(columns=all_years)
df_el_opex_100mw.loc['opex'] = np.array(df_yearly_data.loc['opex_100mw'] * 1000 * electrolyser_capacity / 1E6) # check units from factsheet, probably a mistake in factsheet!

# Stack replacement 100 MW electrolyser
df_stack_replacement_100mw = pd.DataFrame(columns=all_years)
df_stack_replacement_100mw.loc['stack_replacement'] = np.array(df_yearly_data.loc['stack_replacement_100mw'] * 1000 * electrolyser_capacity / 1E6)

# Opex 500 MW electrolyser
df_el_opex_500mw = pd.DataFrame(columns=all_years)
df_el_opex_500mw.loc['opex'] = np.array(df_yearly_data.loc['opex_500mw'] * 1000 * electrolyser_capacity / 1E6) # check units from factsheet, probably a mistake in factsheet!

# Stack replacement 500 MW electrolyser
df_stack_replacement_500mw = pd.DataFrame(columns=all_years)
df_stack_replacement_500mw.loc['stack_replacement'] = np.array(df_yearly_data.loc['stack_replacement_500mw'] * 1000 * electrolyser_capacity / 1E6)



# =============================================================================
# Cashflow revenues and costs
# =============================================================================

################ Comment this section if you want to run the BC without the operation analysis file
el_annual_electricity_costs_ppa = pd.DataFrame(columns=all_years)
el_annual_electricity_costs_grid = pd.DataFrame(columns=all_years)
el_h2_storage_costs = pd.DataFrame(columns=all_years)
el_h2_revenues = pd.DataFrame(columns=all_years)
el_h2_sold_to_hpa = pd.DataFrame(columns=all_years)
el_hwi_revenues = pd.DataFrame(columns=all_years)
el_electricity_tax = pd.DataFrame(columns=all_years)
el_fraction_e_from_market = pd.DataFrame(columns=all_years)

el_annual_electricity_costs_ppa.loc['el_annual_electricity_costs_ppa'] = np.array(df_yearly_data.loc['el_electricity_costs_ppa']) / 1E6         #in MEUR
el_annual_electricity_costs_grid.loc['el_annual_electricity_costs_grid'] = np.array(df_yearly_data.loc['el_electricity_costs_grid']) / 1E6      #in MEUR
el_h2_storage_costs.loc['el_h2_storage_costs'] = np.array(df_yearly_data.loc['h2_storage_costs']) / 1E6                                         #in MEUR
el_h2_revenues.loc['el_h2_revenues'] = np.array(df_yearly_data.loc['h2_revenues_hpa']) / 1E6                                                    #in MEUR
el_h2_sold_to_hpa.loc['el_h2_sold_to_hpa'] = np.array(df_yearly_data.loc['h2_sold_to_hpa'])
el_electricity_tax.loc['el_electricity_tax'] = np.array(df_yearly_data.loc['electricity_tax']) * np.array(df_yearly_data.loc['E_purchased_by_EL']) * 1000 / 1E6   # MEUR
el_fraction_e_from_market.loc['fraction_e_from_market'] = np.array(df_yearly_data.loc['E_purchased_by_EL_from_market']) / np.array(df_yearly_data.loc['E_purchased_by_EL_from_PPA'])    # so this fraction of the electricity input in the electrolyser is not green, and thus that amount of H2 will not be green so won't be able to sell HWI's for this!
el_hwi_revenues.loc['el_hwi_revenues'] = np.array(df_yearly_data.loc['h2_sold_to_hpa_kg']) * np.array(df_yearly_data.loc['hwi_price']) * np.array(1-el_fraction_e_from_market.loc['fraction_e_from_market']) / 1E6    #MEUR

# =============================================================================
# Input data from Excel
# =============================================================================

# Data format: [pessimistic, most_likely, optimistic]

# General data: business case length
el_lifetime_list = [20, 25, 30]                             # years 
duration_construction_list = [3, 3, 3]
duration_operation_list = el_lifetime_list                  # amount of operational years is equal to lifetime of the investment
duration_decommissioning_list = [2, 2, 2]
tender_year_list = [start_year-duration_construction_list[0], start_year-duration_construction_list[1], start_year-duration_construction_list[2]]                       # year at which business case is 0, 
                                                            # i.e. year before start construction
# Cost data from 'inflation-WACC' sheet
el_income_tax_rate_list = [0.258, 0.258, 0.258]             # in %
el_inflation_list = [0.02, 0.02, 0.02]                      # in %
el_loan_interest_rate_list = [0.065, 0.05, 0.035]           # in %
el_length_of_loan_list = [15, 15, 15]                       # years
el_loan_type = 'annuity'
el_depreciation_list = el_lifetime_list                     # years 
el_stacks_depreciation_list = [5, 5, 5]                     # years


# Cost data from 'cost data OWF' sheet
el_contingency_list = [0.1, 0.1, 0.1]                                   # in %
el_loan_percentage_list = [0.50, 0.50, 0.50]                            # in %
el_decommissioning_percentage_list = [0.02, 0.02, 0.02]                 # in %
el_electricity_grid_connection_tariff_list = [144.3, 144.3, 144.3]      # EUR/kW

# Cost data from 'PPA Electrolyser sheet. Uncomment to run without 'Operation analysis file'
#ppa_price_electricity_list = [69.67, 55.74, 41.80]          # EUR/MWh
#grid_price_electricity_list = [102.32, 81.86, 61.39]        # EUR/MWh
#purchased_from_ppa_list = owf_sold_to_electrolyser_list     # MWh/yr
#purchased_from_grid_list = [157536, 157536, 157536]         # MWh/yr
#h2_storage_tariff_list = [3.24, 4.32, 5.40]                 # EUR/MWh
#h2_storage_need_list = [346530.12, 315027.38, 283524.64]    # MWh/yr
#h2_price_hpa_list = [61.50, 82.00, 102.50]                  # EUR/MWh

# =============================================================================
# Get active scenario for Excel data
# =============================================================================

# define all Excel inputs in a dictionary
# If new inputs are added in format: [pessimistic, most_likely, optimistic], they should be added in this dictionary

raw_cost_inputs = {
    'el_general_wacc': el_general_wacc_list,
    'el_lifetime': el_lifetime_list,
    'duration_construction': duration_construction_list,
    'duration_operation': duration_operation_list,
    'duration_decommissioning': duration_decommissioning_list,
    'tender_year': tender_year_list,
    'el_income_tax_rate': el_income_tax_rate_list,
    'el_inflation': el_inflation_list,
    'el_loan_interest_rate': el_loan_interest_rate_list,
    'el_length_of_loan': el_length_of_loan_list,
    'el_depreciation': el_depreciation_list,
    'el_stack_depreciation': el_stacks_depreciation_list,
    'el_contingency': el_contingency_list,
    'el_loan_percentage': el_loan_percentage_list,
    'el_decommissioning_percentage': el_decommissioning_percentage_list,
    'el_electricity_grid_connection_tariff': el_electricity_grid_connection_tariff_list
}


# Extract active index values into a clean temporary dictionary
cost_data_active = {name: data_list[active_index] for name, data_list in raw_cost_inputs.items()}

# Automatically unpack all keys as standalone variables
globals().update(cost_data_active)



# =============================================================================
# Calculate cost data
# =============================================================================

el_capex_100mw = df_yearly_data.loc['capex_total_100mw',tender_year] * electrolyser_capacity * 1000 / 1E6
el_capex_500mw = df_yearly_data.loc['capex_total_500mw',tender_year] * electrolyser_capacity * 1000 / 1E6

el_loan_100mw = el_capex_100mw * el_loan_percentage
el_loan_500mw = el_capex_500mw * el_loan_percentage


# numpy financial calculates the annuity payment for the loan. Same as the PMT function in Excel (but slightly different arguments). See 'Cost data OWF' cell C9.
el_annuity_loan_100mw = -npf.pmt(el_loan_interest_rate, el_length_of_loan, el_loan_100mw, fv=0, when='end')
el_annuity_loan_500mw = -npf.pmt(el_loan_interest_rate, el_length_of_loan, el_loan_500mw, fv=0, when='end')

# calculate electricity grid costs
el_electricity_grid_connection = el_electricity_grid_connection_tariff * electricity_grid_capacity * 1000 / 1E6

#uncomment this section to use input data without operation analysis
# electricity costs
#el_annual_electricity_costs_ppa = el_ppa_price_electricity * el_purchased_from_ppa / 1E6
#el_annual_electricity_costs_grid = el_grid_price_electricity * el_purchased_from_grid / 1E6

# h2 storage costs
#el_h2_storage_costs = el_h2_storage_tariff * el_h2_stoarge_need / 1E6

# h2 sold to HPA
#el_h2_sold_to_hpa = (el_purchased_from_ppa + el_purchased_from_grid) * el_efficiency
#el_h2_revenues = el_h2_price_hpa * el_h2_sold_to_hpa / 1E6

# construction years
year_construction_start = tender_year + 1
construction_years_list = list(range(year_construction_start, year_construction_start + duration_construction))



# Choose the relevant numbers based on electrolyser size configuration
if electrolyser_unit_size == '100MW':
    el_capex = el_capex_100mw
    df_el_opex = df_el_opex_100mw
    df_stack_replacement = df_stack_replacement_100mw
    el_loan = el_loan_100mw
    el_annuity_loan = el_annuity_loan_100mw

else: 
    el_capex = el_capex_500mw
    df_el_opex = df_el_opex_500mw
    df_stack_replacement = df_stack_replacement_500mw
    el_loan = el_loan_500mw
    el_annuity_loan = el_annuity_loan_500mw


# =============================================================================
# PARAMETER DICTIONARY
# =============================================================================

el_parameters = {
    # General Business Case Data
    "lifetime_investment": el_lifetime,
    "duration_construction": duration_construction,
    "duration_operation": duration_operation,
    "duration_decommissioning": duration_decommissioning,
    "tender_year": tender_year,
    
    # Financial & Cost Parameters
    "wacc": el_general_wacc,
    "income_tax_rate": el_income_tax_rate,
    "inflation": el_inflation,
    "loan_interest_rate": el_loan_interest_rate,
    "loan_percentage": el_loan_percentage,
    "decommissioning_percentage": el_decommissioning_percentage, 
    
    # Capital & Operational Expenditures (CAPEX / OPEX)
    "capex": el_capex,             # Or el_capex_500mw depending on configuration
    "opex_df": df_el_opex,         # Dataframe with yearly opex values
    "electricity_grid_connection": el_electricity_grid_connection,
    "df_stack_replacement_costs": df_stack_replacement, # Dataframe with yearly stack replacement
    
    # Technology Specific: Annual Cost and Revenue Dataframes
    "annual_electricity_costs_ppa": el_annual_electricity_costs_ppa,
    "annual_electricity_costs_grid": el_annual_electricity_costs_grid,
    "h2_storage_costs": el_h2_storage_costs,
    "hydrogen_revenues": el_h2_revenues,
    "hwi_revenues": el_hwi_revenues
}
