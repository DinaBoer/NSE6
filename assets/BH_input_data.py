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

# from EL_input_data import h2_price_hpa_list

from Prices_input_data import (hydrogen_price_profiles_2030, hydrogen_price_profiles_2040, hydrogen_price_profiles_2050,
                               naturalgas_price_profiles_2030, naturalgas_price_profiles_2040, naturalgas_price_profiles_2050,
                               electricity_price_profiles_2030, electricity_price_profiles_2040, electricity_price_profiles_2050)

h2_price_profiles_2030 = (np.array([hydrogen_price_profiles_2030['Pessimistic'].sum(), hydrogen_price_profiles_2030["Most likely"].sum(), hydrogen_price_profiles_2030['Optimistic'].sum()]) / 8760).tolist()
h2_price_profiles_2040 = (np.array([hydrogen_price_profiles_2040['Pessimistic'].sum(), hydrogen_price_profiles_2040["Most likely"].sum(), hydrogen_price_profiles_2040['Optimistic'].sum()]) / 8760).tolist()
h2_price_profiles_2050 = (np.array([hydrogen_price_profiles_2050['Pessimistic'].sum(), hydrogen_price_profiles_2050["Most likely"].sum(), hydrogen_price_profiles_2050['Optimistic'].sum()]) / 8760).tolist()

ng_price_profiles_2030 = (np.array([naturalgas_price_profiles_2030['Pessimistic'].sum(), naturalgas_price_profiles_2030["Most likely"].sum(), naturalgas_price_profiles_2030['Optimistic'].sum()]) / 8760).tolist()
ng_price_profiles_2040 = (np.array([naturalgas_price_profiles_2040['Pessimistic'].sum(), naturalgas_price_profiles_2040["Most likely"].sum(), naturalgas_price_profiles_2040['Optimistic'].sum()]) / 8760).tolist()
ng_price_profiles_2050 = (np.array([naturalgas_price_profiles_2050['Pessimistic'].sum(), naturalgas_price_profiles_2050["Most likely"].sum(), naturalgas_price_profiles_2050['Optimistic'].sum()]) / 8760).tolist()

e_price_profiles_2030 = (np.array([electricity_price_profiles_2030['Pessimistic'].sum(), electricity_price_profiles_2030["Most likely"].sum(), electricity_price_profiles_2030['Optimistic'].sum()]) / 8760).tolist()
e_price_profiles_2040 = (np.array([electricity_price_profiles_2040['Pessimistic'].sum(), electricity_price_profiles_2040["Most likely"].sum(), electricity_price_profiles_2040['Optimistic'].sum()]) / 8760).tolist()
e_price_profiles_2050 = (np.array([electricity_price_profiles_2050['Pessimistic'].sum(), electricity_price_profiles_2050["Most likely"].sum(), electricity_price_profiles_2050['Optimistic'].sum()]) / 8760).tolist()



########## Get cost data from Mapeditor

# can also add investment_costs, opex
bh_general_WACC = asset_parameters.loc['Offtaker','wacc']/100          # from % to decimal


########## Cost data from factsheet

lhv_h2_mj_kg = 119.96         # MJ/kg
hhv_h2_mj_kg = 141.8          # MJ/kg

atr_plant_capacity = 1350 / 3 / hhv_h2_mj_kg * lhv_h2_mj_kg     # MW
atr_annual_utilisation = 0.92                                   # %

# Used factsheet: Hydelta2 D3.4, P4 ATR+CCS
# Date: 29-08-2024

# format: [2030[pes-ml-opt], 2040[pes-ml-opt], 2050[pes-ml-opt]]
# note: the plant capacity in the factsheet was 1350 MW, which is unreasonably large. 
# Divided by 3 to achieve plant capacity of 450 MW! Also for associated values, we divide everything by 4!

capex_atr_per_kw = np.array([[1201,1300,1400],[1201,1300,1400],[1201,1300,1400]])       # EUR/kW  
atr_fixed_opex = np.array([[3,3,5],[3,3,5],[3,3,5]]) / 100                              # % of CAPEX
bh_atr_capex = np.array(capex_atr_per_kw) * 1000 * np.array(atr_plant_capacity) / 1E6   # MEUR
bh_atr_opex = np.array(bh_atr_capex) * np.array(atr_fixed_opex)                         # MEUR
specific_ng_consumption = [[1.18,1.202,1.202],[1.18,1.202,1.202],[1.18,1.202,1.202]]    # MJ-NG/MJ-H2
specific_e_consumption = [[0.011,0.014,0.014],[0.011,0.014,0.014],[0.011,0.014,0.014]]  # kWh/MJ-H2

# NG and H2 prices 
bh_h2_price = [h2_price_profiles_2030,h2_price_profiles_2040,h2_price_profiles_2050]                        # EUR/MWh
bh_ng_price = [ng_price_profiles_2030[::-1],ng_price_profiles_2040[::-1],ng_price_profiles_2050[::-1]]      # EUR/MWh
bh_e_price = [e_price_profiles_2030[::-1],e_price_profiles_2040[::-1],e_price_profiles_2050[::-1]]          # EUR/MWh

electricity_tax = [[1.88, 1.88, 1.88],[1.88, 1.88, 1.88],[1.88, 1.88, 1.88]]            #EUR/MWh from belastingdienst, 2024 data

# HWI price - from CE Delft report 'Toetsing beleidsontwikkelingen waterstof' 2024
hwi_price = [[5.20, 5.16, 5.12],[5.20,5.16,5.12],[5.20,5.16,5.12]]                      # EUR/kgH2
carbon_permits = [[87, 87, 87],[130, 130, 130],[500, 500, 500]]                          # EUR/ton, Source: Enerdata

factsheet_parameters = [capex_atr_per_kw, atr_fixed_opex, bh_atr_capex, bh_atr_opex,specific_ng_consumption,specific_e_consumption, bh_h2_price, bh_ng_price, bh_e_price, electricity_tax, hwi_price, carbon_permits]
index_names = ['capex_atr_per_kw', 'atr_fixed_opex', 'bh_atr_capex', 'bh_atr_opex','specific_ng_consumption','specific_e_consumption', 'bh_h2_price', 'bh_ng_price', 'bh_e_price', 'electricity_tax', 'hwi_price', 'carbon_permits']

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

all_years = range(2028,2100,1)
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

df_yearly_data.style.format(precision=2)



# here we make a df with specific numbers, so we can use this for the sensitivity later on
df_bh_atr_capex = pd.DataFrame(columns=all_years)
df_bh_atr_opex = pd.DataFrame(columns=all_years)
bh_h2_price = pd.DataFrame(columns=all_years)
bh_ng_price = pd.DataFrame(columns=all_years)
bh_e_price = pd.DataFrame(columns=all_years)
bh_electricity_tax = pd.DataFrame(columns=all_years)
bh_hwi_costs = pd.DataFrame(columns=all_years)
bh_carbon_permits = pd.DataFrame(columns=all_years)

df_bh_atr_capex.loc['bh_atr_capex'] = np.array(df_yearly_data.loc['bh_atr_capex'])
df_bh_atr_opex.loc['bh_atr_opex'] = np.array(df_yearly_data.loc['bh_atr_opex'])
bh_h2_price.loc['bh_h2_price'] = np.array(df_yearly_data.loc['bh_h2_price'])
bh_ng_price.loc['bh_ng_price'] = np.array(df_yearly_data.loc['bh_ng_price'])
bh_e_price.loc['bh_e_price'] = np.array(df_yearly_data.loc['bh_e_price'])
bh_electricity_tax.loc['bh_electricity_tax'] = np.array(df_yearly_data.loc['electricity_tax']) 
bh_carbon_permits.loc['bh_carbon_permits'] = np.array(df_yearly_data.loc['carbon_permits'])


bh_hwi_percentage = pd.DataFrame(columns=all_years)
bh_hwi_percentage.loc[0, 2028:2029] = 0
bh_hwi_percentage.loc[0, 2030:2034] = 0.42
bh_hwi_percentage.loc[0, 2035::] = 0.6
bh_hwi_percentage.index=['hwi_percentage']

########## Input data from Excel

# Data format: [pessimistic, most_likely, optimistic]

# General data: business case length
bh_investment_lifetime_list = [25, 25, 25]                  # years set to 25 which is atr lifetime
bh_h2_pipeline_lifetime_list = [50, 50, 50]                 # assumption, but not used in bc.  
bh_h2_receiving_station_lifetime_list = [30, 30, 30]        # assumption, but not used in bc.
duration_construction_list = [2, 2, 2]
duration_operation_list = bh_investment_lifetime_list       # amount of operational years is equal to lifetime of investments                      
duration_decommissioning_list = [1, 1, 1]
tender_year_list = [2028, 2028, 2028]                           # year at which business case is 0, 
                                                                # i.e. year before start construction
# carbon_permits_list = [87, 130, 500]                          # EUR/ton, Source: Enerdata
co2_emissions_annual_list = np.array([86.02, 87.62, 175.24])/4  # kt/year
                                                    
# Cost data from 'inflation-WACC' sheet
bh_income_tax_rate_list = [0.258, 0.258, 0.258]             # in %
bh_inflation_list = [0.02, 0.02, 0.02]                      # in %
bh_loan_interest_rate_list = [0.091, 0.07, 0.049]           # in %
bh_length_of_loan_list = [15, 15, 15]                       # years
bh_loan_type = 'annuity'
bh_atr_depreciation_list = bh_investment_lifetime_list                     # years  
bh_h2_pipeline_depreciation_list = bh_investment_lifetime_list             # assumption, to match business case length.
bh_h2_station_depreciation_list = bh_investment_lifetime_list              # assumption, to match business case length.

# Cost data from 'cost data offtaker' sheet
bh_contingency_list = [0.1, 0.1, 0.1]                       # in %
bh_loan_percentage_list = [0.75, 0.75, 0.75]                # in %
bh_decomissioning_percentage_list = [0.02, 0.02, 0.02]      # in %
bh_capex_h2_receiving_station_list = [5.38, 4.15, 3.37]     # MEUR      Assumption - Rob #Note: the order here is the other way around than most pes-ml-opt because this is an expense and not an avoided expense!
bh_capex_h2_pipeline_list = [38.75, 38.75, 38.75]           # MEUR      CHECK! calculation in Excel not clear!
bh_network_costs_ng_list = [0.035, 0.035, 0.035]            # EUR/m3
bh_network_costs_h2_list = [0.070, 0.0525, 0.035]           # EUR/m3    Assumption: 2x current NG costs for most likely/pessimistic, equal to NG for optimistic  

# Cost data from 'PPA offtaker' sheet
# bh_hpa_price_h2_list = h2_price_hpa_list[::-1]              # EUR/MWh prices from electrolyser, but inverted because optimistic for electrolyser is pessimistic for offtaker etc.
# bh_ng_price_list = [26.25, 35.00, 43.75]                    # EUR/MWh
bh_ng_tax_cost_list = [0.0489, 0.0489, 0.0611]              # EUR/m3


# Construct a dataframe with the input from above
df_cost_data = pd.DataFrame(columns=['pessimistic','most_likely','optimistic'])

df_cost_data.loc['bh_investment_lifetime'] = bh_investment_lifetime_list
df_cost_data.loc['duration_construction'] = duration_construction_list
df_cost_data.loc['duration_operation'] = duration_operation_list
df_cost_data.loc['duration_decommissioning'] = duration_decommissioning_list
df_cost_data.loc['tender_year'] = tender_year_list
# df_cost_data.loc['carbon_permits'] = carbon_permits_list
df_cost_data.loc['co2_emissions_annual'] = co2_emissions_annual_list

df_cost_data.loc['income_tax_rate'] = bh_income_tax_rate_list
df_cost_data.loc['inflation'] = bh_inflation_list
df_cost_data.loc['loan_interest_rate'] = bh_loan_interest_rate_list
df_cost_data.loc['length_of_loan'] = bh_length_of_loan_list
df_cost_data.loc['atr_depreciation'] = bh_atr_depreciation_list
df_cost_data.loc['h2_pipeline_depreciation'] = bh_h2_pipeline_depreciation_list
df_cost_data.loc['h2_station_depreciation'] = bh_h2_station_depreciation_list

df_cost_data.loc['contingency'] = bh_contingency_list
df_cost_data.loc['loan_percentage'] = bh_loan_percentage_list
df_cost_data.loc['decommissioning_percentage'] = bh_decomissioning_percentage_list
df_cost_data.loc['capex_h2_receiving_station'] = bh_capex_h2_receiving_station_list
df_cost_data.loc['capex_h2_pipeline'] = bh_capex_h2_pipeline_list
df_cost_data.loc['network_costs_ng'] = bh_network_costs_ng_list
df_cost_data.loc['network_costs_h2'] = bh_network_costs_h2_list

# df_cost_data.loc['hpa_price_h2'] = bh_hpa_price_h2_list
# df_cost_data.loc['ng_price'] = bh_ng_price_list
df_cost_data.loc['ng_tax_cost'] = bh_ng_tax_cost_list

df_cost_data

# the scenario is chosen, by dropping the other two scenario's from the dataframe

df_cost_data.drop(columns=drop_scenarios,axis=1,inplace=True)
df_cost_data.style.format(precision=3)


# get cost data for the correct scenario
# in the df we can see that we have the most_likely scenario
# we can get the parameters from the df by using the row index
# using df_cost_data.loc['parameter'] not only gives the value, but also column name, dtype etc.
# therefore, we use .item() to get the desired value

bh_lifetime = int(df_cost_data.loc['bh_investment_lifetime'].item())
duration_construction = int(df_cost_data.loc['duration_construction'].item())
duration_operation = int(df_cost_data.loc['duration_operation'].item())
duration_decommissioning = int(df_cost_data.loc['duration_decommissioning'].item())
tender_year = int(df_cost_data.loc['tender_year'].item())
# carbon_permits  = df_cost_data.loc['carbon_permits'].item()
co2_emissions_annual = df_cost_data.loc['co2_emissions_annual'].item()

bh_income_tax_rate = df_cost_data.loc['income_tax_rate'].item()
bh_inflation = df_cost_data.loc['inflation'].item()                 
bh_loan_interest_rate = df_cost_data.loc['loan_interest_rate'].item()
bh_length_of_loan = int(df_cost_data.loc['length_of_loan'].item())
bh_atr_depreciation = int(df_cost_data.loc['atr_depreciation'].item())
bh_h2_pipeline_depreciation = int(df_cost_data.loc['h2_pipeline_depreciation'].item())
bh_h2_station_depreciation = int(df_cost_data.loc['h2_station_depreciation'].item())

bh_contingency = df_cost_data.loc['contingency'].item()
bh_loan_percentage = df_cost_data.loc['loan_percentage'].item()
bh_decomissioning_percentage = df_cost_data.loc['decommissioning_percentage'].item()
bh_capex_h2_receiving_station = df_cost_data.loc['capex_h2_receiving_station'].item()
bh_capex_h2_pipeline = df_cost_data.loc['capex_h2_pipeline'].item()
bh_network_costs_ng = df_cost_data.loc['network_costs_ng'].item()
bh_network_costs_h2 = df_cost_data.loc['network_costs_h2'].item()

# bh_hpa_price_h2 = df_cost_data.loc['hpa_price_h2'].item()
# bh_ng_price = df_cost_data.loc['ng_price'].item()
bh_ng_tax_cost = df_cost_data.loc['ng_tax_cost'].item()


# H2 and NG and E demand
lhv_h2_mj_m3 = 10.8     # MJ/m3
lhv_ng_mj_m3 = 31.65    # MJ/m3
lhv_h2_kwh_kg = 33.33   # KWh/kg

h2_demand_mwh = atr_plant_capacity * 8760 * atr_annual_utilisation      # MWh/year
h2_demand_m3 = h2_demand_mwh * 3600 / lhv_h2_mj_m3                      # m3/year     
h2_demand_mj = h2_demand_mwh * 3600                                     # MJ/year
h2_demand_kg = h2_demand_mwh * 1000 / lhv_h2_kwh_kg                     # kg/year

ng_demand_mwh = h2_demand_mwh * df_yearly_data.loc['specific_ng_consumption',tender_year]      # MWh/year
ng_demand_m3 = ng_demand_mwh * 3600 / lhv_ng_mj_m3

e_demand_mwh = h2_demand_mj * df_yearly_data.loc['specific_e_consumption',tender_year]/1000    # MWh/year


# HWI costs
bh_hwi_costs.loc['bh_hwi_costs'] = np.array(df_yearly_data.loc['hwi_price']) * h2_demand_kg / 1E6       # MEUR


# calcualte cost data

bh_atr_avoided_loan = bh_loan_percentage * df_yearly_data.loc['bh_atr_capex',tender_year]
bh_loan = bh_loan_percentage * (bh_capex_h2_receiving_station + bh_capex_h2_pipeline)

# numpy financial calculates the annuity payment for the loan. Same as the PMT function in Excel (but slightly different arguments). See 'Cost data OWF' cell C9.
bh_atr_annuity_loan = -npf.pmt(bh_loan_interest_rate, bh_length_of_loan, bh_atr_avoided_loan, fv=0, when='end')
bh_annuity_loan = -npf.pmt(bh_loan_interest_rate, bh_length_of_loan, bh_loan, fv=0, when='end')

# construction years
year_construction_start = tender_year + 1
year_construction_end = year_construction_start + duration_construction
construction_years_list = list(range(year_construction_start, year_construction_start + duration_construction))





########## Input variables used for business case BH offtaker
# This is a list of all the input variables used in the business case. 
# Make sure to always use the same order in functions
# These are all the factors that we did a sensitivity analysis on in Excel


input_variables_list = ['capex_h2_station_variable',
                        'capex_h2_pipeline_variable',
                        'df_capex_atr_variable',
                        'network_costs_h2_variable',
                        'h2_price_variable',
                        'hwi_costs_variable',
                        'df_atr_opex_variable',
                        'network_costs_ng_variable',
                        'carbon_permits_variable',
                        'ng_price_variable',
                        'ng_tax_variable',
                        'e_price_variable',
                        'electricity_tax_variable',
                        'inflation_variable',
                        'loan_percentage_variable',
                        'loan_interest_rate_variable',
                        'income_tax_rate_variable',
                        'wacc_variable',
                        #'duration_operation_variable',
                        'lifetime_investment_variable']