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

# from EL_input_data import h2_price_hpa_list  # probably remove this

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
ot_general_WACC = asset_parameters['wacc']['Offtaker']/100         # from % to decimal


########## Cost data from factsheet - None for NG



########## Values below are derived from "General data offtaker" - Used input data

# Energy densities of natural gas in MJ/m3 and MJ/kg
lhv_ng_mj_m3 = 31.65          # MJ/m3 
lhv_ng_mj_kg = 47.13          # MJ/kg (derived from essential hydrogen and natural gas conversions excel) 


#Energy densities of hydrogen
lhv_h2_mj_m3 = 10.8           # MJ/m3
lhv_h2_mj_kg = 119.96         # MJ/kg
lhv_h2_kwh_kg = 33.33         # kWh/kg
h2_density = 0.08988          # kg/m3 (@STP)

# Natural gas boiler efficieny
ot_ng_boiler_eff = 0.885            # 88.5%
ot_h2_boiler_eff = 1                # 100%

#Plant capacity and demand levels
ot_ng_demand_m3 = 28000000                                          # m3/a
ot_ng_demand_mwh = ot_ng_demand_m3 * lhv_ng_mj_m3 / 3600            # MWh/a


ot_ng_boiler_capacity = (ot_ng_demand_m3*lhv_ng_mj_m3/8760/3600)*ot_ng_boiler_eff   # the result of this is 24.9MW which is also directly an output from the Mapeditor # equal for H2 and NG, heat demand
ot_h2_boiler_capacity = ot_ng_boiler_capacity / ot_h2_boiler_eff                    # MW

ot_h2_demand_mwh = ot_h2_boiler_capacity * 8760                     # MWh / a
ot_h2_demand_m3 = ot_h2_demand_mwh * 3600 / lhv_h2_mj_m3            # m3 / a
ot_h2_demand_kg = ot_h2_demand_mwh * 1000 / lhv_h2_kwh_kg           # kg / a

########## Input data from Excel: Cost Data Offtaker

# format: [2030[pes-ml-opt], 2040[pes-ml-opt], 2050[pes-ml-opt]]

capex_ng_boiler_per_mw = [[0.069,0.069,0.069],[0.069,0.069,0.069],[0.069,0.069,0.069]]          # M€/MW(th) - data from data alignment WP3 system analysis + corrected for inflation 2019-2030
opex_ng_boiler_per_mw = [[0.0021,0.0028,0.0035],[0.0021,0.0028,0.0035],[0.0021,0.0028,0.0035]]  # M€/MW(th)/yr - data from data alignment WP3 system analysis + corrected for inflation 2019-2030 
capex_ng_boiler = np.array(capex_ng_boiler_per_mw)*ot_ng_boiler_capacity                        # MEUR
opex_ng_boiler = np.array(opex_ng_boiler_per_mw)*ot_ng_boiler_capacity                          # MEUR

capex_h2_boiler_per_mw = [[0.152,0.152,0.152],[0.152,0.152,0.152],[0.152,0.152,0.152]]          # M€/MW(th) - data from data alignment WP3 system analysis + corrected for inflation 2019-2030
opex_h2_boiler_per_mw = [[0.0048,0.0048,0.0048],[0.0048,0.0048,0.0048],[0.0048,0.0048,0.0048]]  # M€/MW(th)/yr - data from data alignment WP3 system analysis + corrected for inflation 2019-2030 
capex_h2_boiler = np.array(capex_h2_boiler_per_mw)*ot_h2_boiler_capacity                        # MEUR
opex_h2_boiler = np.array(opex_h2_boiler_per_mw)*ot_h2_boiler_capacity                          # MEUR

# NG and H2 prices 
ot_h2_price = [h2_price_profiles_2030,h2_price_profiles_2040,h2_price_profiles_2050]                        # EUR/MWh
ot_ng_price = [ng_price_profiles_2030[::-1],ng_price_profiles_2040[::-1],ng_price_profiles_2050[::-1]]      # EUR/MWh
ot_e_price = [e_price_profiles_2030[::-1],e_price_profiles_2040[::-1],e_price_profiles_2050[::-1]]          # EUR/MWh

electricity_tax = [[1.88, 1.88, 1.88],[1.88, 1.88, 1.88],[1.88, 1.88, 1.88]]            #EUR/MWh from belastingdienst, 2024 data

# HWI price - from CE Delft report 'Toetsing beleidsontwikkelingen waterstof' 2024
hwi_price = [[5.20, 5.16, 5.12],[5.20,5.16,5.12],[5.20,5.16,5.12]]                      # EUR/kgH2
carbon_permits = [[87, 87, 87],[130, 130, 130],[500, 500, 500]]                         # EUR/ton, Source: Enerdata

factsheet_parameters = [capex_ng_boiler_per_mw, opex_ng_boiler_per_mw, capex_ng_boiler, opex_ng_boiler, capex_h2_boiler_per_mw, opex_h2_boiler_per_mw, capex_h2_boiler, opex_h2_boiler ,ot_h2_price, ot_ng_price, ot_e_price,electricity_tax,hwi_price, carbon_permits]
index_names = ['capex_ng_boiler_per_mw', 'opex_ng_boiler_per_mw', 'capex_ng_boiler', 'opex_ng_boiler', 'capex_h2_boiler_per_mw', 'opex_h2_boiler_per_mw', 'capex_h2_boiler', 'opex_h2_boiler','ot_h2_price','ot_ng_price','ot_e_price','electricity_tax','hwi_price','carbon_permits']

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

df_factsheet_2030.style.format(precision=2)


########## Transform 2030, 2040, 2050 data from factsheet into yearly data

all_years = range(2029,2100,1)
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

# here we make a df with just the ng_capex numbers, so we can use this for the sensitivity later on
df_ng_boiler_capex = pd.DataFrame(columns=all_years)
df_ng_boiler_opex = pd.DataFrame(columns=all_years)
df_h2_boiler_capex = pd.DataFrame(columns=all_years)
df_h2_boiler_opex = pd.DataFrame(columns=all_years)
ot_h2_price = pd.DataFrame(columns=all_years)
ot_ng_price = pd.DataFrame(columns=all_years)
# ot_e_price = pd.DataFrame(columns=all_years)
# ot_electricity_tax = pd.DataFrame(columns=all_years)
ot_hwi_costs = pd.DataFrame(columns=all_years)
ot_carbon_permits = pd.DataFrame(columns=all_years)

df_ng_boiler_capex.loc['ng_boiler_capex'] = np.array(df_yearly_data.loc['capex_ng_boiler'])
df_ng_boiler_opex.loc['ng_boiler_opex'] = np.array(df_yearly_data.loc['opex_ng_boiler'])
df_h2_boiler_capex.loc['h2_boiler_capex'] = np.array(df_yearly_data.loc['capex_h2_boiler'])
df_h2_boiler_opex.loc['h2_boiler_opex'] = np.array(df_yearly_data.loc['opex_h2_boiler'])
ot_h2_price.loc['ot_h2_price'] = np.array(df_yearly_data.loc['ot_h2_price'])
ot_ng_price.loc['ot_ng_price'] = np.array(df_yearly_data.loc['ot_ng_price'])
# ot_e_price.loc['ot_e_price'] = np.array(df_yearly_data.loc['ot_e_price'])
# ot_electricity_tax.loc['bh_electricity_tax'] = np.array(df_yearly_data.loc['electricity_tax']) 
ot_carbon_permits.loc['ot_carbon_permits'] = np.array(df_yearly_data.loc['carbon_permits'])


ot_hwi_percentage = pd.DataFrame(columns=all_years)
ot_hwi_percentage.loc[0, 2028:2029] = 0
ot_hwi_percentage.loc[0, 2030:2034] = 0.42
ot_hwi_percentage.loc[0, 2035::] = 0.6
ot_hwi_percentage.index=['hwi_percentage']


########## Input data from Excel

# Data format: [pessimistic, most_likely, optimistic]

# General data: business case length
ot_h2_boiler_lifetime_list = [15, 18, 25]                  
ot_ng_boiler_lifetime_list = [25, 25, 25]
ot_h2_pipeline_lifetime_list = [50, 50, 50]                 # assumption
ot_h2_receiving_station_lifetime_list = [30, 30, 30]        # assumption
duration_construction_list = [1, 1, 1]
duration_operation_list = ot_h2_boiler_lifetime_list           # amount of operational years is equal to lifetime of h-boiler                   
duration_decommissioning_list = [1, 1, 1]
tender_year_list = [2029, 2029, 2029]                       # year at which business case is 0, 
                                                            # i.e. year before start construction
# carbon_permits_list = [87, 130, 500]                        # EUR/ton, Source: Enerdata
co2_per_mwh_ng_list = [201.96, 201.96, 201.96]              # kg/MWh
                                                    
# Cost data from 'inflation-WACC' sheet
ot_income_tax_rate_list = [0.258, 0.258, 0.258]             # in %
ot_inflation_list = [0.02, 0.02, 0.02]                      # in %
ot_loan_interest_rate_list = [0.091, 0.07, 0.049]           # in %
ot_length_of_loan_list = [15, 15, 15]                       # years
ot_loan_type = 'annuity'
ot_h2_boiler_depreciation_list = ot_h2_boiler_lifetime_list       # years  
ot_ng_boiler_depreciation_list = ot_ng_boiler_lifetime_list       # assumption
ot_h2_pipeline_depreciation_list = ot_h2_boiler_lifetime_list     # assumption, pipeline is deprecated over length of bc, because unlikely to re-sell the pipeline. Could be changed to deprecation over lifetime, and to add resale value to bc.
ot_h2_station_depreciation_list = ot_h2_boiler_lifetime_list      # assumption, station is deprecated over length of bc, because unlikely to re-sell the station. Could be changed to deprecation over lifetime, and to add resale value to bc.


# Cost data from 'cost data offtaker' sheet
ot_contingency_list = [0.1, 0.1, 0.1]                               # in %
ot_loan_percentage_list = [0.75, 0.75, 0.75]                        # in %
ot_h2_boiler_decomissioning_percentage_list = [0.02, 0.02, 0.02]    # in %
ot_ng_boiler_decomissioning_percentage_list = [0.02, 0.02, 0.02]    # in %
ot_capex_h2_receiving_station_list = [1, 1, 1]                      # MEUR      Assumption - Rob
ot_capex_h2_pipeline_list = [13.28, 10.81, 8.33]                    # MEUR      CHECK! calculation in Excel not clear! NUmbers corrected for inflation 2022-2030
ot_network_costs_ng_list = [0.071, 0.071, 0.071]                    # EUR/m3 for ng demand up to 28.4 Mm3, for >28.4 costs are 0.035
ot_network_costs_h2_list = [0.142, 0.107, 0.071]                    # EUR/m3    Assumption: 2x current NG costs for pessimistic, 1.5x NG for most likely, equal to NG for optimistic  



# Cost data from 'PPA offtaker' sheet
#bh_hpa_price_h2_list = h2_price_hpa_list[::-1]              # EUR/MWh prices from electrolyser, but inverted because optimistic for electrolyser is pessimistic for offtaker etc.
# ng_price_list = [26.25, 35.00, 43.75]                    # EUR/MWh
ng_tax_cost_list = [0.0489, 0.0489, 0.0611]              # EUR/m3

'''Update dataframe below with numbers as filled in directly above. 
Also change ng to ot to make the names more intuitive'''

# Construct a dataframe with the input from above
df_cost_data = pd.DataFrame(columns=['pessimistic','most_likely','optimistic'])

df_cost_data.loc['h2_boiler_lifetime'] = ot_h2_boiler_lifetime_list
df_cost_data.loc['ng_boiler_lifetime'] = ot_ng_boiler_lifetime_list
df_cost_data.loc['duration_construction'] = duration_construction_list
df_cost_data.loc['duration_operation'] = duration_operation_list
df_cost_data.loc['duration_decommissioning'] = duration_decommissioning_list
df_cost_data.loc['tender_year'] = tender_year_list
# df_cost_data.loc['carbon_permits'] = carbon_permits_list
df_cost_data.loc['co2_per_mwh_ng'] = co2_per_mwh_ng_list

df_cost_data.loc['income_tax_rate'] = ot_income_tax_rate_list
df_cost_data.loc['inflation'] = ot_inflation_list
df_cost_data.loc['loan_interest_rate'] = ot_loan_interest_rate_list
df_cost_data.loc['length_of_loan'] = ot_length_of_loan_list
df_cost_data.loc['h2_boiler_depreciation'] = ot_h2_boiler_depreciation_list
df_cost_data.loc['ng_boiler_depreciation'] = ot_ng_boiler_depreciation_list
df_cost_data.loc['h2_pipeline_depreciation'] = ot_h2_boiler_lifetime_list
df_cost_data.loc['h2_station_depreciation'] = ot_h2_station_depreciation_list

df_cost_data.loc['contingency'] = ot_contingency_list
df_cost_data.loc['loan_percentage'] = ot_loan_percentage_list
df_cost_data.loc['h2_boiler_decommissioning_percentage'] = ot_h2_boiler_decomissioning_percentage_list
df_cost_data.loc['ng_boiler_decommissioning_percentage'] = ot_ng_boiler_decomissioning_percentage_list
df_cost_data.loc['capex_h2_receiving_station'] = ot_capex_h2_receiving_station_list
df_cost_data.loc['capex_h2_pipeline'] = ot_capex_h2_pipeline_list
df_cost_data.loc['network_costs_ng'] = ot_network_costs_ng_list
df_cost_data.loc['network_costs_h2'] = ot_network_costs_h2_list

#df_cost_data.loc['hpa_price_h2'] = bh_hpa_price_h2_list
# df_cost_data.loc['ng_price'] = ng_price_list
df_cost_data.loc['ng_tax_cost'] = ng_tax_cost_list

df_cost_data

# the scenario is chosen, by dropping the other two scenario's from the dataframe

df_cost_data.drop(columns=drop_scenarios,axis=1,inplace=True)
df_cost_data.style.format(precision=3)


# get cost data for the correct scenario
# in the df we can see that we have the most_likely scenario
# we can get the parameters from the df by using the row index
# using df_cost_data.loc['parameter'] not only gives the value, but also column name, dtype etc.
# therefore, we use .item() to get the desired value

ot_h2_boiler_lifetime = int(df_cost_data.loc['h2_boiler_lifetime'].item())
ot_ng_boiler_lifetime = int(df_cost_data.loc['ng_boiler_lifetime'].item())
duration_construction = int(df_cost_data.loc['duration_construction'].item())
duration_operation = int(df_cost_data.loc['duration_operation'].item())
duration_decommissioning = int(df_cost_data.loc['duration_decommissioning'].item())
tender_year = int(df_cost_data.loc['tender_year'].item())
# carbon_permits  = df_cost_data.loc['carbon_permits'].item()
co2_per_mwh_ng = df_cost_data.loc['co2_per_mwh_ng'].item()

ot_income_tax_rate = df_cost_data.loc['income_tax_rate'].item()
ot_inflation = df_cost_data.loc['inflation'].item()                 
ot_loan_interest_rate = df_cost_data.loc['loan_interest_rate'].item()
ot_length_of_loan = int(df_cost_data.loc['length_of_loan'].item())
ot_h2_boiler_depreciation = int(df_cost_data.loc['h2_boiler_depreciation'].item())
ot_ng_boiler_depreciation = int(df_cost_data.loc['ng_boiler_depreciation'].item())
ot_h2_pipeline_depreciation = int(df_cost_data.loc['h2_pipeline_depreciation'].item())
ot_h2_station_depreciation = int(df_cost_data.loc['h2_station_depreciation'].item())

ot_contingency = df_cost_data.loc['contingency'].item()
ot_loan_percentage = df_cost_data.loc['loan_percentage'].item()
ot_h2_boiler_decomissioning_percentage = df_cost_data.loc['h2_boiler_decommissioning_percentage'].item()
ot_ng_boiler_decomissioning_percentage = df_cost_data.loc['ng_boiler_decommissioning_percentage'].item()
ot_capex_h2_receiving_station = df_cost_data.loc['capex_h2_receiving_station'].item()
ot_capex_h2_pipeline = df_cost_data.loc['capex_h2_pipeline'].item()
ot_network_costs_ng = df_cost_data.loc['network_costs_ng'].item()
ot_network_costs_h2 = df_cost_data.loc['network_costs_h2'].item()

#bh_hpa_price_h2 = df_cost_data.loc['hpa_price_h2'].item()
# ng_price = df_cost_data.loc['ng_price'].item()
ot_ng_tax_cost = df_cost_data.loc['ng_tax_cost'].item()


# HWI costs
ot_hwi_costs.loc['ot_hwi_costs'] = np.array(df_yearly_data.loc['hwi_price']) * ot_h2_demand_kg / 1E6       # MEUR




# calcualte cost data
ot_avoided_loan = ot_loan_percentage * df_yearly_data.loc['capex_ng_boiler',tender_year]
ot_loan = ot_loan_percentage * (df_yearly_data.loc['capex_h2_boiler',tender_year] + ot_capex_h2_receiving_station + ot_capex_h2_pipeline)

# numpy financial calculates the annuity payment for the loan. Same as the PMT function in Excel (but slightly different arguments). See 'Cost data OWF' cell C9.
ot_avoided_annuity_loan = -npf.pmt(ot_loan_interest_rate, ot_length_of_loan, ot_avoided_loan, fv=0, when='end')
ot_annuity_loan = -npf.pmt(ot_loan_interest_rate, ot_length_of_loan, ot_loan, fv=0, when='end')

# construction years
year_construction_start = tender_year + 1
year_construction_end = year_construction_start + duration_construction
construction_years_list = list(range(year_construction_start, year_construction_start + duration_construction))






########## Input variables used for business case offtaker
# This is a list of all the input variables used in the business case. 
# Make sure to always use the same order in functions
# These are all the factors that we did a sensitivity analysis on in Excel


input_variables_list = ['capex_h2_station_variable',
                        'capex_h2_pipeline_variable',
                        'capex_h2_boiler_variable',
                        'capex_ng_boiler_variable',
                        'opex_h2_boiler_variable',
                        'network_costs_h2_variable',
                        'h2_price_variable',
                        'hwi_price_variable',  
                        'opex_ng_boiler_variable',
                        'network_costs_ng_variable',
                        'carbon_permits_variable',
                        'ng_price_variable',
                        'ng_tax_variable',
                        'inflation_variable',
                        'loan_percentage_variable',
                        'loan_interest_rate_variable',
                        'income_tax_rate_variable',
                        'wacc_variable',
                        #'duration_operation_variable',
                        'lifetime_investment_variable']


