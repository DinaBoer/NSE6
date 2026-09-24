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

#type 'yes' to update the variables retrieved from Operation_analysis_OWF_EL.ipynb. Else, the stored variables in the Pickle file will be used. This latter helps to run the program faster
update_operation_analysis = 'no'

if update_operation_analysis == 'yes':
    from importnb import Notebook
    with Notebook():
        import Operation_analysis_OWF_EL as OA  # Alias as needed

    start_year = OA.start_year
    electricity_grid_capacity = OA.electricity_grid_capacity

    E_trans_2030 = OA.E_trans_2030[OA.E_trans_2030.iloc[0].sort_values().index].iloc[0].tolist()
    E_trans_2040 = OA.E_trans_2040[OA.E_trans_2040.iloc[0].sort_values().index].iloc[0].tolist()
    E_trans_2050 = OA.E_trans_2050[OA.E_trans_2050.iloc[0].sort_values().index].iloc[0].tolist()

else:
    # Load the Pickle file with stored data from Operation_analysis
    filename = 'Operation_Analysis_variables.pkl'
    with open(filename, 'rb') as f:
        variables = pickle.load(f)

    # Select the variables that are needed for this Business Case
    specific_vars = {key: variables[key] for key in ['start_year', 'electricity_grid_capacity',
                                                     'E_purchased_by_EL_2030', 'E_purchased_by_EL_2040', 'E_purchased_by_EL_2050', 
                                                     'E_trans_2030', 'E_trans_2040', 'E_trans_2050'] if key in variables}

    # Use the specific variables in the current environment
    globals().update(specific_vars)
    
    E_trans_2030 = E_trans_2030[E_trans_2030.iloc[0].sort_values().index].iloc[0].tolist()
    E_trans_2040 = E_trans_2040[E_trans_2040.iloc[0].sort_values().index].iloc[0].tolist()
    E_trans_2050 = E_trans_2050[E_trans_2050.iloc[0].sort_values().index].iloc[0].tolist()
    E_purchased_by_EL_2030 = E_purchased_by_EL_2030[E_purchased_by_EL_2030.iloc[0].sort_values().index].iloc[0].tolist()
    E_purchased_by_EL_2040 = E_purchased_by_EL_2040[E_purchased_by_EL_2040.iloc[0].sort_values().index].iloc[0].tolist()
    E_purchased_by_EL_2050 = E_purchased_by_EL_2050[E_purchased_by_EL_2050.iloc[0].sort_values().index].iloc[0].tolist()

########## Get cost data from Mapeditor

# ET_capex = asset_parameters['investment_costs']['TNVDW']              # in MEUR
# ET_fixed_opex = asset_parameters['fixed_opex']['TNVDW']/100           # converted 2 percent to 0.02
# ET_var_opex = asset_parameters['variable_opex']['TNVDW']              # in Eur/MWh
# ET_general_WACC = asset_parameters.loc['TNVDW','wacc']/100              # from % to decimal
# action: should be changed into offshore electricity transport WACC



cable_distance = 111694 / 1000     # km, original value = 111694 / 1000
if cable_distance < 80:
    current = 'AC'
else:
    current = 'DC'

# action: we should get the cable distance from mapeditor
# revenue data data from 'cost data ET' sheet
ET_connections = [[700,1400,2100],[700,1400,2100],[700,1400,2100]]                  # number of connections (MW) (dummy)
ET_connection_tariff = [[0.00,0.00,0.00],[0.00,0.00,0.00],[0.00,0.00,0.00]]         # MEUR/year/MW number of connections (dummy)

'''CHECK THE CONNECTIONS AND CONNECTION TARIFFS AND WHETHER THEY CAN BE REMOVED!!'''

########## Cost data from factsheet

# Used factsheet: TYNDP datasheet on electricity transport 
# Date: 27-09-2024

# format: [2030[pes-ml-opt]], 2040[pes-ml-opt], 2050[pes-ml-opt]]

tot_transport_capacity = electricity_grid_capacity                                     # MW, based on TNVDW , original value = electricity_grid_capacity

# this cost data origins from the NSWPH Pathway Databook v10

capex_ac_platform_offshore = [[0.158,0.158,0.158],[0.153,0.153,0.153],[0.149,0.149,0.149]]              # MEUR/MW
capex_ac_substation = [[0.032,0.032,0.032],[0.031,0.031,0.031],[0.030,0.030,0.030]]                     # MEUR/MW for both onshore and offshore

capex_ac_cables_on_ov = [[0.25,0.25,0.25],[0.24,0.24,0.24],[0.24,0.24,0.24]]                            # kEUR/km/MW  #onduidelijk waar deze data vandaan komt, niet in Pathway_databook_v10 #This is not used? Can probably be removed!                   
capex_ac_cables_on_un = [[1.181,1.181,1.181],[0.146,0.146,0.146],[0.114,0.114,0.114]]                   # kEUR/km/MW #This is not used? Can probably be removed!
capex_ac_cables_off = [[6.961,6.961,6.961],[6.752,6.752,6.752],[6.564,6.564,6.564]]                     # kEUR/km/MW

capex_dc_platform_offshore = [[0.264*2,0.264,0.264],[0.256*2,0.256,0.256],[0.249*2,0.249,0.249]]        # MEUR/MW  Multiplied pessimistic scenario by 2 based on information from Joris
capex_dc_substation = [[0.264*2,0.264,0.264],[0.256*2,0.256,0.256],[0.249*2,0.249,0.249]]               # MEUR/MW  Multiplied pessimistic scenario by 2 based on information from Joris
capex_dc_topsideadj_offshore = [[0.047*2,0.047,0.047],[0.046*2,0.046,0.046],[0.045*2,0.045,0.045]]      # MEUR/MW  Multiplied pessimistic scenario by 2 based on information from Joris

capex_dc_cables_on_ov = [[0.55,0.55,0.55],[0.54,0.54,0.54],[0.52,0.52,0.52]]                            # kEUR/km/MW #onduidelijk waar deze data vandaan komt, niet in Pathway_databook_v10  #This is not used? Can probably be removed!
capex_dc_cables_on_un = [[3.649,3.649,3.649],[3.540,3.540,3.540],[3.441,3.441,3.441]]                   # kEUR/km/MW #This is not used? Can probably be removed!
capex_dc_cables_off = [[2.109*2,2.109,2.109],[2.046*2,2.046,2.046],[1.989*2,1.989,1.989]]               # kEUR/km/MW  Multiplied pessimistic scenario by 2 based on information from Joris

opex_perc = [[0.015,0.015,0.015],[0.015,0.015,0.015],[0.015,0.015,0.015]]                               # 1.5% of CAPEX for all components and for every year

ET_electricity_volume = np.array([E_trans_2030, E_trans_2040, E_trans_2050]) 
#ET_electricity_volume = np.array([E_purchased_by_EL_2030,E_purchased_by_EL_2040,E_purchased_by_EL_2050])*1000 ## replace this only for VC analysis

print(ET_electricity_volume)

factsheet_parameters = [capex_ac_platform_offshore, capex_dc_platform_offshore, capex_ac_substation, capex_dc_substation, capex_dc_topsideadj_offshore, capex_ac_cables_on_ov, capex_ac_cables_on_un, capex_ac_cables_off, capex_dc_cables_on_ov, capex_dc_cables_on_un, capex_dc_cables_off, opex_perc, ET_connections, ET_connection_tariff, ET_electricity_volume]
index_names = ['capex_ac_platform_offshore', 'capex_dc_platform_offshore', 'capex_ac_substation', 'capex_dc_substation', 'capex_dc_topside_adjustment_offshore', 'capex_ac_cables_onshore_overhead', 'capex_ac_cables_onshore_underground', 'capex_ac_cables_submarine', 'capex_dc_cables_onshore_overhead', 'capex_dc_cables_onshore_underground', 'capex_dc_cables_submarine', 'opex_perc', 'number_connections', 'connection_tariff', 'ET_electricity_volume']

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
ET_lifetime_list = [40, 40, 40]                             # years
duration_construction_list = [5, 5, 5]
duration_operation_list = ET_lifetime_list                  # amount of operational years is equal to lifetime of the investment
duration_decommissioning_list = [2, 2, 2]
tender_year_list = [start_year-duration_construction_list[0], start_year-duration_construction_list[1], start_year-duration_construction_list[2]]          # year at which business case is 0, 
                       # year at which business case is 0, 
                                                            # i.e. year before start construction

# Cost data from 'inflation-WACC' sheet
ET_income_tax_rate_list = [0.258, 0.258, 0.258]             # in %
ET_inflation_list = [0.02, 0.02, 0.02]                      # in %
ET_general_WACC_list = [0.045, 0.04, 0.035]            # in %
ET_loan_interest_rate_list = [0.04, 0.03, 0.02]             # in % Based on rents of Dutch state loans over 2024
ET_length_of_loan_list = [30, 30, 30]                       # years
ET_loan_type = 'annuity'
ET_depreciation_list = ET_lifetime_list                     # years  

# Cost data from 'cost data ET' sheet
ET_contingency_list = [0.05, 0.05, 0.05]                    # in %
ET_loan_percentage_list = [0.75, 0.75, 0.75]                # in %
ET_decomissioning_percentage_list = [0.02, 0.02, 0.02]      # in %

# Electricity transport tariff
ET_transport_tariff_list = [0,0,0]            #[51.96, 44.75, 37.53]            # EUR/MWh, Based on report 'Electricity cost assessment for large industry in the Netherlands, Belgium, Germany and France' from E-Bridge
                                                            # It seems that the connection tariffs are already included in these transport tariffs
# used to be: [0.1, 0.2, 0.3]     # in EUR/GWh (currently dummy numbers are included)
#action: this can be made a value with 2030. 2040 and 2050 values after electricity prices are connected


# Construct a dataframe with the input from above
df_cost_data = pd.DataFrame(columns=['pessimistic','most_likely','optimistic'])

df_cost_data.loc['ET_lifetime'] = ET_lifetime_list
df_cost_data.loc['duration_construction'] = duration_construction_list
df_cost_data.loc['duration_operation'] = duration_operation_list
df_cost_data.loc['duration_decommissioning'] = duration_decommissioning_list
df_cost_data.loc['tender_year'] = tender_year_list

df_cost_data.loc['income_tax_rate'] = ET_income_tax_rate_list
df_cost_data.loc['inflation'] = ET_inflation_list
df_cost_data.loc['wacc'] = ET_general_WACC_list
df_cost_data.loc['loan_interest_rate'] = ET_loan_interest_rate_list
df_cost_data.loc['length_of_loan'] = ET_length_of_loan_list
df_cost_data.loc['depreciation'] = ET_depreciation_list

df_cost_data.loc['contingency'] = ET_contingency_list
df_cost_data.loc['loan_percentage'] = ET_loan_percentage_list
df_cost_data.loc['decommissioning_percentage'] = ET_decomissioning_percentage_list

#df_cost_data.loc['electricity_volume'] = np.add(owf_sold_to_grid_list, purchased_from_grid_list).tolist()          # total number of MWh transported over the grid
df_cost_data.loc['electricity_transport_tariff'] = ET_transport_tariff_list                        

df_cost_data

# the scenario is chosen, by dropping the other two scenario's from the dataframe

df_cost_data.drop(columns=drop_scenarios,axis=1,inplace=True)
df_cost_data.style.format(precision=3)

# get cost data for the correct scenario
# in the df we can see that we have the most_likely scenario
# we can get the parameters from the df by using the row index
# using df_cost_data.loc['parameter'] not only gives the value, but also column name, dtype etc.
# therefore, we use .item() to get the desired value

ET_lifetime = int(df_cost_data.loc['ET_lifetime'].item())
duration_construction = int(df_cost_data.loc['duration_construction'].item())
duration_operation = int(df_cost_data.loc['duration_operation'].item())
duration_decommissioning = int(df_cost_data.loc['duration_decommissioning'].item())
tender_year = int(df_cost_data.loc['tender_year'].item())

ET_income_tax_rate = df_cost_data.loc['income_tax_rate'].item()
ET_inflation = df_cost_data.loc['inflation'].item()                 
ET_general_WACC = df_cost_data.loc['wacc'].item()
ET_loan_interest_rate = df_cost_data.loc['loan_interest_rate'].item()
ET_length_of_loan = int(df_cost_data.loc['length_of_loan'].item())
ET_depreciation = int(df_cost_data.loc['depreciation'].item())

ET_contingency = df_cost_data.loc['contingency'].item()
ET_loan_percentage = df_cost_data.loc['loan_percentage'].item()
ET_decomissioning_percentage = df_cost_data.loc['decommissioning_percentage'].item()

#ET_electricity_volume = df_cost_data.loc['electricity_volume'].item()
ET_electricity_transport_tariff = df_cost_data.loc['electricity_transport_tariff'].item()

########## Calculate cost data

if current == 'DC':
    platform_capex = (df_yearly_data.loc['capex_dc_platform_offshore', tender_year] * tot_transport_capacity)
    substation_capex = (df_yearly_data.loc['capex_dc_substation', tender_year] * tot_transport_capacity)*2 + df_yearly_data.loc['capex_dc_topside_adjustment_offshore', tender_year] * tot_transport_capacity
    cable_capex_km = df_yearly_data.loc['capex_dc_cables_submarine', tender_year] * tot_transport_capacity / 1000 # total capex per km of lenght, divided by 1000 to get to MEUR/km instead of kEUR
elif current == 'AC':
    platform_capex = df_yearly_data.loc['capex_ac_platform_offshore', tender_year] * tot_transport_capacity
    substation_capex = (df_yearly_data.loc['capex_ac_substation', tender_year] * tot_transport_capacity)*2 + df_yearly_data.loc['capex_ac_topside_adjustment_offshore', tender_year] * tot_transport_capacity
    cable_capex_km = df_yearly_data.loc['capex_ac_cables_submarine', tender_year] * tot_transport_capacity / 1000 # total capex per km of lenght, divided by 1000 to get to MEUR/km instead of kEUR
else:
    print("Error: please select a suitable current, choose between 'AC' or 'DC'.")
    raise SystemExit("Stopping the program") #stop program if no suitable location has been chosen

opex_platform_substation = (platform_capex + substation_capex) * df_yearly_data.loc['opex_perc']
opex_cables_km = cable_capex_km * df_yearly_data.loc['opex_perc']

#print(df_cost_data.loc['electricity_transport_tariff','most_likely'])
#print(df_yearly_data.loc['ET_electricity_volume'])

revenue_connections = df_yearly_data.loc['number_connections'] * df_yearly_data.loc['connection_tariff']

ET_electricity_volume = pd.DataFrame(columns=all_years)
ET_electricity_volume.loc['ET_electricity_volume'] = np.array(df_yearly_data.loc['ET_electricity_volume']) #in Mwh
df_ET_revenue_transport = pd.DataFrame(columns=all_years)
df_ET_revenue_transport.loc['revenue_transport'] = np.array(ET_electricity_volume.loc['ET_electricity_volume']) * ET_electricity_transport_tariff /1000000

# here we make a df with just the opex numbers, so we can use this for the sensitivity later on
df_ET_opex = pd.DataFrame(columns=all_years)
df_ET_opex.loc['opex_cables_km'] = np.array(opex_cables_km)
df_ET_opex.loc['opex_platform_substation'] = np.array(opex_platform_substation)
df_ET_opex

# here we make a df with just the revenue numbers, so we can use this for the sensitivity later on
df_ET_revenues_connections = pd.DataFrame(columns=all_years)
df_ET_revenues_connections.loc['revenue_connections'] = np.array(revenue_connections)
df_ET_revenues_connections

# calcualte cost data

# ET_loan = (platform_capex + substation_capex) * ET_loan_percentage  #This excludes loan for cables

# # numpy financial calculates the annuity payment for the loan. Same as the PMT function in Excel (but slightly different arguments). See 'Cost data ET' cell C9.
# ET_annuity_loan = -npf.pmt(ET_loan_interest_rate, ET_length_of_loan, (platform_capex + substation_capex)*ET_loan_percentage, fv=0, when='end')


# construction years
year_construction_start = tender_year + 1
construction_years_list = list(range(year_construction_start, year_construction_start + duration_construction))


########## Input variables used for business case ET
# This is a list of all the input variables used in the business case. 
# Make sure to always use the same order in functions
# These are all the factors that we do sensitivity analysis on

input_variables_list = ['ET_total_capex',
                        'platform_capex_variable',
                        'substation_capex_variable',
                        'cable_capex_km_variable',
                        'df_opex_variable',
                        'inflation_variable',
                        'revenues_transport_tariffs',
                        'df_revenues_connection_tariffs',
                        'decomissioning_variable',
                        'loan_percentage_variable',
                        'loan_interest_rate_variable',
                        'income_tax_rate_variable',
                        'wacc_variable',
                        #'duration_operation_variable',
                        'lifetime_investment_variable',
                        'cable_length']
