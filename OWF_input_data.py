# imports
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

#type 'yes' to update the variables retrieved from Operation_analysis_OWF_EL.ipynb. Else, the stored variables in the Pickle file will be used. This latter helps to run the program faster
update_operation_analysis = 'yes'

if update_operation_analysis == 'yes':
    from importnb import Notebook
    with Notebook():
        import Operation_analysis_OWF_EL as OA  # Alias as needed

    start_year = OA.start_year
    windfarm_capacity = OA.windfarm_capacity
    electricity_grid_capacity = OA.electricity_grid_capacity

    margin_2030 = OA.rev_E_market_2030_W + OA.rev_E_PPA_2030_W  # define the margin to order scenarios on
    df_2030 = pd.concat([margin_2030, OA.rev_E_market_2030_W, OA.rev_E_PPA_2030_W, OA.E_sold_2030_W])
    df_2030 = df_2030[df_2030.iloc[0].sort_values().index]
    rev_E_market_2030_W = df_2030.iloc[1].tolist()
    rev_E_PPA_2030_W = df_2030.iloc[2].tolist()
    E_sold_2030_W = df_2030.iloc[3].tolist()

    margin_2040 = OA.rev_E_market_2040_W + OA.rev_E_PPA_2040_W # define the margin to order scenarios on
    df_2040 = pd.concat([margin_2040, OA.rev_E_market_2040_W, OA.rev_E_PPA_2040_W, OA.E_sold_2040_W])
    df_2040 = df_2040[df_2040.iloc[0].sort_values().index]
    rev_E_market_2040_W = df_2040.iloc[1].tolist()
    rev_E_PPA_2040_W = df_2040.iloc[2].tolist()
    E_sold_2040_W = df_2040.iloc[3].tolist()

    margin_2050 = OA.rev_E_market_2050_W + OA.rev_E_PPA_2050_W # define the margin to order scenarios on
    df_2050 = pd.concat([margin_2050, OA.rev_E_market_2050_W, OA.rev_E_PPA_2050_W, OA.E_sold_2050_W])
    df_2050 = df_2050[df_2050.iloc[0].sort_values().index]
    rev_E_market_2050_W = df_2050.iloc[1].tolist()
    rev_E_PPA_2050_W = df_2050.iloc[2].tolist()
    E_sold_2050_W = df_2050.iloc[3].tolist()

else:
    # Load the Pickle file with stored data from Operation_analysis
    filename = 'Operation_Analysis_variables.pkl'
    with open(filename, 'rb') as f:
        variables = pickle.load(f)

    # Select the variables that are needed for this Business Case
    specific_vars = {key: variables[key] for key in ['start_year', 'windfarm_capacity', 'electricity_grid_capacity', 
                                                     'rev_E_market_2030_W', 'rev_E_PPA_2030_W', 'E_sold_2030_W',
                                                     'rev_E_market_2040_W', 'rev_E_PPA_2040_W', 'E_sold_2040_W',
                                                     'rev_E_market_2050_W', 'rev_E_PPA_2050_W', 'E_sold_2050_W'] if key in variables}

    # Use the specific variables in the current environment
    globals().update(specific_vars)
    
    margin_2030 = rev_E_market_2030_W + rev_E_PPA_2030_W # define the margin to order scenarios on
    df_2030 = pd.concat([margin_2030, rev_E_market_2030_W, rev_E_PPA_2030_W, E_sold_2030_W])
    df_2030 = df_2030[df_2030.iloc[0].sort_values().index]
    rev_E_market_2030_W = df_2030.iloc[1].tolist()
    rev_E_PPA_2030_W = df_2030.iloc[2].tolist()
    E_sold_2030_W = df_2030.iloc[3].tolist()

    margin_2040 = rev_E_market_2040_W + rev_E_PPA_2040_W # define the margin to order scenarios on
    df_2040 = pd.concat([margin_2040, rev_E_market_2040_W, rev_E_PPA_2040_W, E_sold_2040_W])
    df_2040 = df_2040[df_2040.iloc[0].sort_values().index]
    rev_E_market_2040_W = df_2040.iloc[1].tolist()
    rev_E_PPA_2040_W = df_2040.iloc[2].tolist()
    E_sold_2040_W = df_2040.iloc[3].tolist()

    margin_2050 = rev_E_market_2050_W + rev_E_PPA_2050_W # define the margin to order scenarios on
    df_2050 = pd.concat([margin_2050, rev_E_market_2050_W, rev_E_PPA_2050_W, E_sold_2050_W])
    df_2050 = df_2050[df_2050.iloc[0].sort_values().index]
    rev_E_market_2050_W = df_2050.iloc[1].tolist()
    rev_E_PPA_2050_W = df_2050.iloc[2].tolist()
    E_sold_2050_W = df_2050.iloc[3].tolist()

########## Get cost data from Mapeditor

# owf_capex = asset_parameters['investment_costs']['TNVDW']         # in MEUR
# owf_fixed_opex = asset_parameters['fixed_opex']['TNVDW']/100      # converted 2 percent to 0.02
# owf_var_opex = asset_parameters['variable_opex']['TNVDW']         # in Eur/MWh
owf_general_WACC = asset_parameters.loc['TNVDW','wacc']/100          # from % to decimal

# The cable costs depend on the length of the cables
# In Mapeditor, a straight line between OWF and Eemshaven is approximately 111694 meter
cable_distance = 111694 / 1000     # km

########## Cost data from factsheet

# Used factsheet: NSE5_Factsheet_OffshoreWind 
# Date: 14-08-2024

# format: [2030[pes-ml-opt], 2040[pes-ml-opt], 2050[pes-ml-opt]]

#windfarm_capacity = 700                                                        # MW, based on TNVDW
windturbine_capacity = [[15,17,19],[18,21,25],[18,21,25]]                       # MW 

capex_rna = [[16,12.3,9],[16,13.8,9],[16,13.8,9]]                               # MEUR/WT
capex_structure = [[10,8.3,6],[13.19,10,6],[13.19,10,6]]                        # MEUR/WT
capex_electric = [[1500,800,693],[1500,800,693],[1500,800,693]]                 # kEur/MW
capex_cables = [[2.112,2.112,2.112],[1.816,1.816,1.816],[1.816,1.816,1.816]]    # kEUR/MW/km
capex_installation = [[245,200,100],[211,200,100],[211,200,100]]                # kEUR/MW  Note that I changed the order from the factsheet to correctly represent high-mid-low
capex_project_costs = [[313,200,100],[314,200,100],[314,200,100]]               # kEUR/MW  Note that I changed the order from the factsheet to correctly represent high-mid-low
capex_abex_decex = [[211,160,80],[196,160,80],[196,160,80]]                     # kEUR/MW abandonment/decomissioning costs. Note that I changed the order from the factsheet to correctly represent high-mid-low
opex = [[70,52,30],[70,37,30],[70,37,30]]                                       # kEUR/MW/yr

# revenues and volumes
owf_revenues_to_electrolyser = [rev_E_PPA_2030_W, rev_E_PPA_2040_W, rev_E_PPA_2050_W]               # EUR/year
owf_revenues_to_market = [rev_E_market_2030_W, rev_E_market_2040_W, rev_E_market_2050_W]            # EUR/year
owf_sold_electricity = [E_sold_2030_W, E_sold_2030_W, E_sold_2030_W]                                # EUR/year

factsheet_parameters = [windturbine_capacity, capex_rna, capex_structure, capex_electric, capex_cables, capex_installation, capex_project_costs, capex_abex_decex, opex, owf_revenues_to_electrolyser, owf_revenues_to_market, owf_sold_electricity]
index_names = ['windturbine_capacity', 'capex_rna', 'capex_structure', 'capex_electric', 'capex_cables', 'capex_installation', 'capex_project_costs', 'capex_abex_decex', 'opex', 'owf_revenues_to_electrolyser', 'owf_revenues_to_market', 'owf_sold_electricity']

df_factsheet_2030 = pd.DataFrame(columns=['pessimistic','most_likely','optimistic'])
df_factsheet_2040 = pd.DataFrame(columns=['pessimistic','most_likely','optimistic'])
df_factsheet_2050 = pd.DataFrame(columns=['pessimistic','most_likely','optimistic'])

for i,name in enumerate(index_names):
    df_factsheet_2030.loc[name] = factsheet_parameters[i][0]

for i,name in enumerate(index_names):
    df_factsheet_2040.loc[name] = factsheet_parameters[i][1]

for i,name in enumerate(index_names):
    df_factsheet_2050.loc[name] = factsheet_parameters[i][2]

df_factsheet_2030.drop(columns=drop_scenarios,axis=1,inplace=True)
df_factsheet_2040.drop(columns=drop_scenarios,axis=1,inplace=True)
df_factsheet_2050.drop(columns=drop_scenarios,axis=1,inplace=True)

df_factsheet_2030_2050 = pd.concat([df_factsheet_2030,df_factsheet_2040,df_factsheet_2050], axis=1)
df_factsheet_2030_2050.columns = ['2030','2040','2050']

df_factsheet_2030_2050.style.format(precision=2)


########## Transform 2030, 2040, 2050 data from factsheet into yearly data

all_years = range(2027,2100,1)
df_yearly_data = pd.DataFrame(index=index_names, columns=all_years)

for year in all_years:
    for name in index_names:
        if year <= 2030:
            df_yearly_data.loc[name,year] = df_factsheet_2030_2050.loc[name,'2030']

for i, year in enumerate(all_years):
    for name in index_names:
        if year >2030 and year < 2040:
            df_yearly_data.loc[name,year] = (df_factsheet_2030_2050.loc[name,'2030'] + 
                                          ((df_factsheet_2030_2050.loc[name,'2040'] - 
                                          df_factsheet_2030_2050.loc[name,'2030']) / 10)*(i-3))
            
for i, year in enumerate(all_years):
    for name in index_names:
        if year == 2040:
            df_yearly_data.loc[name,year] = df_factsheet_2030_2050.loc[name,'2040']
        if year >2040 and year < 2050:
            df_yearly_data.loc[name,year] = (df_factsheet_2030_2050.loc[name,'2040'] + 
                                          ((df_factsheet_2030_2050.loc[name,'2050'] - 
                                          df_factsheet_2030_2050.loc[name,'2040']) / 10)*(i-13))

for year in all_years:
    for name in index_names:
        if year >= 2050:
            df_yearly_data.loc[name,year] = df_factsheet_2030_2050.loc[name,'2050']

df_yearly_data.style.format(precision=1)





################ Comment this section if you want to run the BC without the operation analysis file
owf_revenues_to_electrolyser = pd.DataFrame(columns=all_years)
owf_revenues_to_market = pd.DataFrame(columns=all_years)
owf_sold_electricity = pd.DataFrame(columns=all_years)

owf_revenues_to_electrolyser.loc['owf_revenues_to_electrolyser'] = np.array(df_yearly_data.loc['owf_revenues_to_electrolyser']) / 1E6 #in MEUR
owf_revenues_to_market.loc['owf_revenues_to_market'] = np.array(df_yearly_data.loc['owf_revenues_to_market']) / 1E6 #in MEUR
owf_sold_electricity.loc['owf_sold_electricity'] = np.array(df_yearly_data.loc['owf_sold_electricity']) #in MWh

########## Input data from Excel

# Data format: [pessimistic, most_likely, optimistic]

# General data: business case length
owf_lifetime_list = [25, 25, 30]                            # years
duration_construction_list = [3, 3, 3]
duration_operation_list = owf_lifetime_list                 # amount of operational years is equal to lifetime of the investment
duration_decommissioning_list = [2, 2, 2]
tender_year_list = [start_year-duration_construction_list[0], start_year-duration_construction_list[1], start_year-duration_construction_list[2]]                       # year at which business case is 0, 
                       # year at which business case is 0, 
                                                            # i.e. year before start construction

# Cost data from 'inflation-WACC' sheet
owf_income_tax_rate_list = [0.258, 0.258, 0.258]            # in %
owf_inflation_list = [0.02, 0.02, 0.02]                     # in %
# owf_general_WACC_list = [0.0925, 0.085, 0.0775]             # in %
owf_loan_interest_rate_list = [0.065, 0.05, 0.035]          # in %
owf_length_of_loan_list = [15, 15, 15]                      # years
owf_loan_type = 'annuity'
owf_depreciation_list = [25, 25, 30]                        # years  Possibly change to owf_depreciation_list = owf_lifetime_list

# Cost data from 'cost data OWF' sheet
owf_contingency_list = [0.1, 0.1, 0.1]                      # in %
owf_loan_percentage_list = [0.75, 0.75, 0.75]               # in %
owf_decomissioning_percentage_list = [0.02, 0.02, 0.02]     # in %

####### data is replaced by data from operation analysis
# Cost data from 'PPA OWF' sheet
# In 'used input data' Excel file this is linked to the draft data input EYE document
#owf_sold_to_electrolyser_list = [2849543, 2849543, 2849543]     # MWh/year 
#owf_sold_to_grid_list = [195458, 195458, 195458]                # MWh/year 
#owf_revenues_to_electrolyser_list = [119.12, 158.83, 198.54]    # MEUR 
#owf_revenues_to_market_list = [3.89, 5.19, 6.48]                # MEUR 


# Construct a dataframe with the input from above
df_cost_data = pd.DataFrame(columns=['pessimistic','most_likely','optimistic'])

df_cost_data.loc['owf_lifetime'] = owf_lifetime_list
df_cost_data.loc['duration_construction'] = duration_construction_list
df_cost_data.loc['duration_operation'] = duration_operation_list
df_cost_data.loc['duration_decommissioning'] = duration_decommissioning_list
df_cost_data.loc['tender_year'] = tender_year_list

df_cost_data.loc['income_tax_rate'] = owf_income_tax_rate_list
df_cost_data.loc['inflation'] = owf_inflation_list
# df_cost_data.loc['wacc'] = owf_general_WACC_list
df_cost_data.loc['loan_interest_rate'] = owf_loan_interest_rate_list
df_cost_data.loc['length_of_loan'] = owf_length_of_loan_list
df_cost_data.loc['depreciation'] = owf_depreciation_list

df_cost_data.loc['contingency'] = owf_contingency_list
df_cost_data.loc['loan_percentage'] = owf_loan_percentage_list
df_cost_data.loc['decommissioning_percentage'] = owf_decomissioning_percentage_list

########### Data is replaced by data from operation analysis
#df_cost_data.loc['sold_to_electrolyser'] = owf_sold_to_electrolyser_list
#df_cost_data.loc['sold_to_grid'] = owf_sold_to_grid_list
#df_cost_data.loc['revenues_to_electrolyser'] = owf_revenues_to_electrolyser_list
#df_cost_data.loc['revenues_to_market'] = owf_revenues_to_market_list

df_cost_data

# the scenario is chosen, by dropping the other two scenario's from the dataframe

df_cost_data.drop(columns=drop_scenarios,axis=1,inplace=True)
df_cost_data.style.format(precision=3)

# get cost data for the correct scenario
# in the df we can see that we have the most_likely scenario
# we can get the parameters from the df by using the row index
# using df_cost_data.loc['parameter'] not only gives the value, but also column name, dtype etc.
# therefore, we use .item() to get the desired value

owf_lifetime = int(df_cost_data.loc['owf_lifetime'].item())
duration_construction = int(df_cost_data.loc['duration_construction'].item())
duration_operation = int(df_cost_data.loc['duration_operation'].item())
duration_decommissioning = int(df_cost_data.loc['duration_decommissioning'].item())
tender_year = int(df_cost_data.loc['tender_year'].item())

owf_income_tax_rate = df_cost_data.loc['income_tax_rate'].item()
owf_inflation = df_cost_data.loc['inflation'].item()                 
# owf_general_WACC = df_cost_data.loc['wacc'].item()
owf_loan_interest_rate = df_cost_data.loc['loan_interest_rate'].item()
owf_length_of_loan = int(df_cost_data.loc['length_of_loan'].item())
owf_depreciation = int(df_cost_data.loc['depreciation'].item())

owf_contingency = df_cost_data.loc['contingency'].item()
owf_loan_percentage = df_cost_data.loc['loan_percentage'].item()
owf_decomissioning_percentage = df_cost_data.loc['decommissioning_percentage'].item()

########### data is replaced by data from operation analysis
#owf_sold_to_electrolyser = df_cost_data.loc['sold_to_electrolyser'].item()
#owf_sold_to_grid = df_cost_data.loc['sold_to_grid'].item()
#owf_revenues_to_electrolyser = df_cost_data.loc['revenues_to_electrolyser'].item()
#owf_revenues_to_market = df_cost_data.loc['revenues_to_market'].item()


########## Calculate cost data

# We need the number of turbines because some of the cost data is given per turbine
# We assume that at least 700 MW windfarm capacity is required
# Therefore we use np.ceil (or you could use math.ceil) to round the value up to the closest integer
# Then we multiply the rounded number with the turbine capacity to get a new total windfarm capacity,
# which is equal to or slightly higher than the original 700 MW capacity

number_of_turbines = np.ceil(windfarm_capacity / df_yearly_data.loc['windturbine_capacity', tender_year])
new_windfarm_capacity = number_of_turbines * df_yearly_data.loc['windturbine_capacity', tender_year]



owf_capex = (df_yearly_data.loc['capex_rna', tender_year] * number_of_turbines +
             df_yearly_data.loc['capex_structure', tender_year] * number_of_turbines +
             df_yearly_data.loc['capex_electric', tender_year] * new_windfarm_capacity / 1000 +
             #   df_yearly_data.loc['capex_cables', tender_year] * new_windfarm_capacity / 1000 * cable_distance +       # Removed cables capex (HVDC cables), Interarray cables is included by Capex electricty but is not depending on cable distance
             df_yearly_data.loc['capex_installation', tender_year] * new_windfarm_capacity / 1000 +
             df_yearly_data.loc['capex_project_costs', tender_year] * new_windfarm_capacity / 1000)


# here we make a df with just the opex numbers, so we can use this for the sensitivity later on
df_owf_opex = pd.DataFrame(columns=all_years)
df_owf_opex.loc['opex'] = np.array(df_yearly_data.loc['opex']) * new_windfarm_capacity / 1000  # in MEUR


# calcualte cost data

owf_loan = owf_capex * owf_loan_percentage

# numpy financial calculates the annuity payment for the loan. Same as the PMT function in Excel (but slightly different arguments). See 'Cost data OWF' cell C9.
owf_annuity_loan = -npf.pmt(owf_loan_interest_rate, owf_length_of_loan, owf_capex*owf_loan_percentage, fv=0, when='end')


# construction years
year_construction_start = tender_year + 1
construction_years_list = list(range(year_construction_start, year_construction_start + duration_construction))


########## Input variables used for business case OWF
# This is a list of all the input variables used in the business case. 
# Make sure to always use the same order in functions
# These are all the factors that we did a sensitivity analysis on in Excel

input_variables_list = ['capex_variable',
                        'df_opex_variable',
                        'inflation_variable',
                        'revenues_to_electrolyser_variable',
                        'revenues_to_market_variable',
                        'loan_percentage_variable',
                        'loan_interest_rate_variable',
                        'income_tax_rate_variable',
                        'wacc_variable',
                        #'duration_operation_variable',
                        'lifetime_investment_variable']
