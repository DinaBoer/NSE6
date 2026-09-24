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

#from OWF_input_data import owf_sold_to_grid_list
#from EL_input_data import purchased_from_grid_list

#### Consider to make an option
#type 'yes' to update the variables retrieved from Operation_analysis_OWF_EL.ipynb. Else, the stored variables in the Pickle file will be used. This latter helps to run the program faster
update_operation_analysis = 'no'

if update_operation_analysis == 'yes':
    from importnb import Notebook
    with Notebook():
        import Operation_analysis_OWF_EL as OA  # Alias as needed

    start_year = OA.start_year

    H2_sold_2030 = OA.H2_sold_2030[OA.H2_sold_2030.iloc[0].sort_values().index].iloc[0].tolist()
    H2_sold_2040 = OA.H2_sold_2040[OA.H2_sold_2040.iloc[0].sort_values().index].iloc[0].tolist()
    H2_sold_2050 = OA.H2_sold_2050[OA.H2_sold_2050.iloc[0].sort_values().index].iloc[0].tolist()

else:
    # Load the Pickle file with stored data from Operation_analysis
    filename = 'Operation_Analysis_variables.pkl'
    with open(filename, 'rb') as f:
        variables = pickle.load(f)

    # Select the variables that are needed for this Business Case
    specific_vars = {key: variables[key] for key in ['start_year', 'electrolyser_capacity', 'lhv_h2_kwh_kg', 'efficiency_electrolyser_LHV',
                                                     'H2_sold_2030', 'H2_sold_2040', 'H2_sold_2050'] if key in variables}

    # Use the specific variables in the current environment
    globals().update(specific_vars)
    
    H2_sold_2030 = H2_sold_2030[H2_sold_2030.iloc[0].sort_values().index].iloc[0].tolist()
    H2_sold_2040 = H2_sold_2040[H2_sold_2040.iloc[0].sort_values().index].iloc[0].tolist()
    H2_sold_2050 = H2_sold_2050[H2_sold_2050.iloc[0].sort_values().index].iloc[0].tolist()


from Prices_input_data import (electricity_price_profiles_2030, electricity_price_profiles_2040, electricity_price_profiles_2050)

e_price_profiles_2030 = (np.array([electricity_price_profiles_2030['Pessimistic'].sum(), electricity_price_profiles_2030["Most likely"].sum(), electricity_price_profiles_2030['Optimistic'].sum()]) / 8760).tolist()
e_price_profiles_2040 = (np.array([electricity_price_profiles_2040['Pessimistic'].sum(), electricity_price_profiles_2040["Most likely"].sum(), electricity_price_profiles_2040['Optimistic'].sum()]) / 8760).tolist()
e_price_profiles_2050 = (np.array([electricity_price_profiles_2050['Pessimistic'].sum(), electricity_price_profiles_2050["Most likely"].sum(), electricity_price_profiles_2050['Optimistic'].sum()]) / 8760).tolist()

HT_e_price = [e_price_profiles_2030,e_price_profiles_2040,e_price_profiles_2050]          # EUR/MWh

########## Get cost data from Mapeditor

# HT_capex = asset_parameters['investment_costs']['TNVDW']         # in MEUR
# HT_fixed_opex = asset_parameters['fixed_opex']['TNVDW']/100      # converted 2 percent to 0.02
# HT_var_opex = asset_parameters['variable_opex']['TNVDW']         # in Eur/MWh
#HT_general_WACC = asset_parameters.loc['TNVDW','wacc']/100          # from % to decimal
# action: should be changed into offshore hydrogen transport WACC


pipeline_distance_new = 111694/1000     # km, original value  =111694/1000
pipeline_distance_reuse = 0             # km, original value = 111694/1000
pipeline_distance = pipeline_distance_new + pipeline_distance_reuse # km

pipeline_type = 'new'       # choose between 'new', 'reuse' or 'both'

if pipeline_type == 'new':
    if pipeline_distance_reuse > 0:
        print("Error: you selected 'new' pipelines but the distance of reused pipelines was not set to 0. Please set the distance of reused pipelines to 0 to obtain trustworthy results, or set pipeline type to 'both' if you want to calculate costs for a network combining new and reused pipelines")
        raise SystemExit("Stopping the program") #stop program if no suitable pipeline capacity has been chosen
if pipeline_type == 'reuse':
    if pipeline_distance_new > 0:
        print("Error: you selected 'reuse' pipelines but the distance of new pipelines was not set to 0. Please set the distance of new pipelines to 0 to obtain trustworthy results, or set pipeline type to 'both' if you want to calculate costs for a network combining new and reused pipelines")
        raise SystemExit("Stopping the program") #stop program if no suitable pipeline capacity has been chosen



# action: we should get the pipeline distance from mapeditor
# revenue data data from 'cost data HT' sheet
HT_connections = [[700,1400,2100],[700,1400,2100],[700,1400,2100]]            # number of connections (MW) (dummy)
HT_connection_tariff = [[0.00,0.00,0.00],[0.00,0.00,0.00],[0.00,0.00,0.00]]   # MEUR/year/MW number of connections (dummy)

HT_hydrogen_volume = np.array([H2_sold_2030, H2_sold_2040, H2_sold_2050]) 


########## Cost data from factsheet

# Used factsheet: TYNDP datasheet on hydrogen transport 
# Date: 16-10-2024

# format: [2030[high-mid-low], 2040[high-mid-low], 2050[high-mid-low]]

tot_transport_capacity = 7000                                                         # MW, based on typical pipeline capacity, original value = 10000
#note that costs scale linearly so if very small volumes are used these cost won't make any sense
if tot_transport_capacity < 7000:
    print("Error: please select a suitable pipeline capacity, cost represent linear scale so if pipeline sizes smaller than 7GW are chosen, the costs will be underestimated.")
    raise SystemExit("Stopping the program") #stop program if no suitable pipeline capacity has been chosen

tot_connected_capacity = electrolyser_capacity                # We use the connected capacity based on the electrolysers considered in the analysis, so 500MW for DEMO2 
                                                            # Because compressors are a very significant cost and they will not be installed before the actualisation of projects
                                                            # It is also not clear yet who will have to bear the costs for compression -> THe electrolyser operator or the transport operator
                                                            # For now, it is assumed that it is for the transport operator.

# this cost data origins from the NSWPH Pathway Databook v10

# https://365tno.sharepoint.com/:x:/r/teams/P060.52589/_layouts/15/Doc.aspx?sourcedoc=%7B90188303-F7DA-4A1A-AD40-62311171B925%7D&file=Compression_H2%20-%20Final.xlsx&action=default&mobileredirect=true
# Compressor data is from the 'Compression_H2 - Final' factsheet. 
# Data for compression based on Pathway Databook has been removed after discussions with Suriya (WP1)


capex_pipeline_offshore_new = [[443*2,443,443],[430*2,430,430],[418*2,418,418]]                                       # EUR/MWth_LHV/km
capex_compressor_offshore_new = np.array([[1789,1789,1789],[1789,1789,1789],[1789,1789,1789]]) * 1000           # EUR/MW

capex_pipeline_offshore_reuse = [[443*2*0.2,443*0.2,443*0.2],[430*2*0.2,430*0.2,430*0.2],[418*2*0.2,418*0.2,418*0.2]]                                 # EUR/MWth_LHV/km
capex_compressor_offshore_reuse = np.array([[1789*0.2,1789*0.2,1789*0.2],[1789*0.2,1789*0.2,1789*0.2],[1789*0.2,1789*0.2,1789*0.2]])*1000       # EUR/MW


opex_offshore = np.array([[11,11,11],[11,11,11],[10,10,10]]) * (0.97)       # EUR/MWth_LHV/km/year - Decreased by 3% to take compression OPEX out of this general OPEX number. We now use a specific OPEX for compression. 
opex_compressor = [[0.05,0.05,0.05],[0.05,0.05,0.05],[0.05,0.05,0.05]]      # 5% of compression CAPEX


factsheet_parameters = [capex_pipeline_offshore_new, capex_compressor_offshore_new, capex_pipeline_offshore_reuse, capex_compressor_offshore_reuse, opex_offshore, opex_compressor, HT_connections, HT_connection_tariff, HT_hydrogen_volume, HT_e_price]
index_names = ['capex_pipeline_offshore_new', 'capex_compressor_offshore_new', 'capex_pipeline_offshore_reuse', 'capex_compressor_offshore_reuse', 'opex_offshore', 'opex_compressor', 'number_connections', 'connection_tariff', 'HT_hydrogen_volume', 'HT_e_price']

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

all_years = range(2025,2100,1)
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

########## Input data from Excel

# Data format: [pessimistic, most_likely, optimistic]

# General data: business case length
HT_lifetime_list = [40, 40, 40]                            # years
compressor_lifetime_list = [15, 15, 20]                    # years 
duration_construction_list = [5, 5, 5]
duration_operation_list = HT_lifetime_list                 # amount of operational years is equal to lifetime of the investment
duration_decommissioning_list = [2, 2, 2]
tender_year_list = [start_year-duration_construction_list[0], start_year-duration_construction_list[1], start_year-duration_construction_list[2]]                       # year at which business case is 0, 
                       # year at which business case is 0, 
                                                            # i.e. year before start construction

# Cost data from 'inflation-WACC' sheet
HT_income_tax_rate_list = [0.258, 0.258, 0.258]            # in %
HT_inflation_list = [0.02, 0.02, 0.02]                     # in %
HT_general_WACC_list = [0.045, 0.04, 0.035]           # in %
HT_loan_interest_rate_list = [0.04, 0.03, 0.02]            # in % Based on rents of Dutch state loans over 2024
HT_length_of_loan_list = [30, 30, 30]                      # years
HT_loan_type = 'annuity'
HT_depreciation_list = HT_lifetime_list                    # years  
HT_compressor_depreciation_list = compressor_lifetime_list      # years
# Cost data from 'cost data ET' sheet
HT_contingency_list = [0.05, 0.05, 0.05]                   # in %
HT_loan_percentage_list = [0.75, 0.75, 0.75]               # in %
HT_decomissioning_percentage_list = [0.02, 0.02, 0.02]     # in %

# hydrogen transport tariff
HT_transport_tariff_list = np.array([0, 0, 0])/3000 #np.array([15, 10.8, 7.2])/3000      # in EUR/MWh/km  NZTC report has based tariff on a length of 3000, so we divide it by 3000 to get a value per km
# used to be: [0.1, 0.2, 0.3]     # in EUR/GWh (currently dummy numbers are included)


HT_compressor_power_consumption_list = [1.9, 1.9, 1.9]                 # in kWh/kg H2


# Construct a dataframe with the input from above
df_cost_data = pd.DataFrame(columns=['pessimistic','most_likely','optimistic'])

df_cost_data.loc['HT_lifetime'] = HT_lifetime_list
df_cost_data.loc['compressor_lifetime'] = compressor_lifetime_list
df_cost_data.loc['duration_construction'] = duration_construction_list
df_cost_data.loc['duration_operation'] = duration_operation_list
df_cost_data.loc['duration_decommissioning'] = duration_decommissioning_list
df_cost_data.loc['tender_year'] = tender_year_list

df_cost_data.loc['income_tax_rate'] = HT_income_tax_rate_list
df_cost_data.loc['inflation'] = HT_inflation_list
df_cost_data.loc['wacc'] = HT_general_WACC_list
df_cost_data.loc['loan_interest_rate'] = HT_loan_interest_rate_list
df_cost_data.loc['length_of_loan'] = HT_length_of_loan_list
df_cost_data.loc['depreciation'] = HT_depreciation_list
df_cost_data.loc['compressor_depreciation'] = HT_compressor_depreciation_list

df_cost_data.loc['contingency'] = HT_contingency_list
df_cost_data.loc['loan_percentage'] = HT_loan_percentage_list
df_cost_data.loc['decommissioning_percentage'] = HT_decomissioning_percentage_list

#df_cost_data.loc['hydrogen_volume'] = np.add(owf_sold_to_grid_list, purchased_from_grid_list).tolist()          # total number of MWh transported over the grid
df_cost_data.loc['hydrogen_transport_tariff'] = HT_transport_tariff_list                        
df_cost_data.loc['compressor_power_consumption'] = HT_compressor_power_consumption_list

df_cost_data

# the scenario is chosen, by dropping the other two scenario's from the dataframe

df_cost_data.drop(columns=drop_scenarios,axis=1,inplace=True)
df_cost_data.style.format(precision=3)

# get cost data for the correct scenario
# in the df we can see that we have the most_likely scenario
# we can get the parameters from the df by using the row index
# using df_cost_data.loc['parameter'] not only gives the value, but also column name, dtype etc.
# therefore, we use .item() to get the desired value

HT_lifetime = int(df_cost_data.loc['HT_lifetime'].item())
HT_compressor_lifetime = int(df_cost_data.loc['compressor_lifetime'].item())
duration_construction = int(df_cost_data.loc['duration_construction'].item())
duration_operation = int(df_cost_data.loc['duration_operation'].item())
duration_decommissioning = int(df_cost_data.loc['duration_decommissioning'].item())
tender_year = int(df_cost_data.loc['tender_year'].item())

HT_income_tax_rate = df_cost_data.loc['income_tax_rate'].item()
HT_inflation = df_cost_data.loc['inflation'].item()                 
HT_general_WACC = df_cost_data.loc['wacc'].item()
HT_loan_interest_rate = df_cost_data.loc['loan_interest_rate'].item()
HT_length_of_loan = int(df_cost_data.loc['length_of_loan'].item())
HT_depreciation = int(df_cost_data.loc['depreciation'].item())
HT_compressor_depreciation = int(df_cost_data.loc['compressor_depreciation'].item())

HT_contingency = df_cost_data.loc['contingency'].item()
HT_loan_percentage = df_cost_data.loc['loan_percentage'].item()
HT_decomissioning_percentage = df_cost_data.loc['decommissioning_percentage'].item()

#HT_hydrogen_volume = df_cost_data.loc['hydrogen_volume'].item()
HT_hydrogen_transport_tariff = df_cost_data.loc['hydrogen_transport_tariff'].item()
HT_compressor_power_consumption = df_cost_data.loc['compressor_power_consumption'].item()

########## Calculate cost data

if pipeline_type == 'new':
    pipeline_capex = (df_yearly_data.loc['capex_pipeline_offshore_new', tender_year] * tot_transport_capacity) / 1000000 #divided by 1E6 to present capex in MEUR
    compression_capex = (df_yearly_data.loc['capex_compressor_offshore_new', tender_year] * (HT_compressor_power_consumption / lhv_h2_kwh_kg) * (tot_connected_capacity*efficiency_electrolyser_LHV)) / 1000000 #divided by 1E6 to present capex in MEUR
elif pipeline_type == 'reuse':
    pipeline_capex = (df_yearly_data.loc['capex_pipeline_offshore_reuse', tender_year] * tot_transport_capacity) / 1000000 #divided by 1E6 to present capex in MEUR
    compression_capex = (df_yearly_data.loc['capex_compressor_offshore_reuse', tender_year] * (HT_compressor_power_consumption / lhv_h2_kwh_kg) * (tot_connected_capacity*efficiency_electrolyser_LHV)) / 1000000 #divided by 1E6 to present capex in MEUR
elif pipeline_type == 'both':
    pipeline_capex = ((df_yearly_data.loc['capex_pipeline_offshore_new', tender_year] * tot_transport_capacity * pipeline_distance_new) + (df_yearly_data.loc['capex_pipeline_offshore_reuse', tender_year] * tot_transport_capacity * pipeline_distance_reuse))/pipeline_distance/1000000 # in order to create an average cost for the reuse/new pipe ratio
    compression_capex = (df_yearly_data.loc['capex_compressor_offshore_new', tender_year] * (HT_compressor_power_consumption / lhv_h2_kwh_kg) * (tot_connected_capacity*efficiency_electrolyser_LHV)) / 1000000 #divided by 1E6 to present capex in MEUR. For new/reuse mixes only new compressors assumed
else:
    print("Error: please select a suitable pipeline type, choose between 'new' or 'reuse'.")
    raise SystemExit("Stopping the program") #stop program if no suitable location has been chosen

opex = df_yearly_data.loc['opex_offshore'] * tot_transport_capacity / 1000000 #divided by 1E6 to present capex in MEUR

revenue_connections = df_yearly_data.loc['number_connections'] * df_yearly_data.loc['connection_tariff']

HT_hydrogen_volume = pd.DataFrame(columns=all_years)
HT_hydrogen_volume.loc['HT_hydrogen_volume'] = np.array(df_yearly_data.loc['HT_hydrogen_volume']) #in Mwh
df_HT_revenues_transport = pd.DataFrame(columns=all_years)
df_HT_revenues_transport.loc['revenue_transport'] = np.array(HT_hydrogen_volume.loc['HT_hydrogen_volume']) * HT_hydrogen_transport_tariff * (pipeline_distance) / 1E6


HT_e_price = pd.DataFrame(columns=all_years)
HT_e_price.loc['HT_e_price'] = np.array(df_yearly_data.loc['HT_e_price'])   # in EUR / MWh
df_HT_compressor_power_costs = pd.DataFrame(columns=all_years)
df_HT_compressor_power_costs.loc['compressor_power_costs'] = (((((np.array(df_yearly_data.loc['HT_hydrogen_volume']) * 1000) / lhv_h2_kwh_kg) * 
                                                              HT_compressor_power_consumption) /1000) * np.array(df_yearly_data.loc['HT_e_price'])) / 1E6    # in MEUR 

# here we make a df with just the opex numbers, so we can use this for the sensitivity later on
df_HT_opex = pd.DataFrame(columns=all_years)
df_HT_opex.loc['opex_km'] = np.array(opex)
df_HT_opex

df_opex_compressor = pd.DataFrame(columns=all_years)
df_opex_compressor.loc['opex_compressor'] = np.array(df_yearly_data.loc['opex_compressor']) * compression_capex    

# here we make a df with just the revenue numbers, so we can use this for the sensitivity later on
df_HT_revenues_connections = pd.DataFrame(columns=all_years)
df_HT_revenues_connections.loc['revenue_connections'] = np.array(revenue_connections)
df_HT_revenues_connections

# # calcualte cost data

# HT_loan = (pipeline_capex + compression_capex) * HT_loan_percentage  #This excludes loan for pipelines

# # numpy financial calculates the annuity payment for the loan. Same as the PMT function in Excel (but slightly different arguments). See 'Cost data ET' cell C9.
# HT_annuity_loan = -npf.pmt(HT_loan_interest_rate, HT_length_of_loan, (pipeline_capex + compression_capex)*HT_loan_percentage, fv=0, when='end')


# construction years
year_construction_start = tender_year + 1
construction_years_list = list(range(year_construction_start, year_construction_start + duration_construction))


########## Input variables used for business case HT
# This is a list of all the input variables used in the business case. 
# Make sure to always use the same order in functions
# These are all the factors that we do sensitivity analysis on

input_variables_list = [
                        # 'HT_total_capex',
                        'pipeline_capex_variable',
                        'compression_capex_variable',
                        # 'empty_capex_variable',
                        'df_opex_variable',
                        'df_opex_compressor_variable',
                        'df_compressor_power_costs_variable',
                        'inflation_variable',
                        'df_revenues_transport_tariffs',
                        'df_revenues_connection_tariffs',
                        'decomissioning_variable',
                        'loan_percentage_variable',
                        'loan_interest_rate_variable',
                        'income_tax_rate_variable',
                        'wacc_variable',
                        #'duration_operation_variable',
                        'lifetime_investment_variable',
                        'pipeline_length_variable']

