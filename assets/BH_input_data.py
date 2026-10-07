# This business case represents an industrial user of hydrogen
# Thats wants to either invest in blue hydrogen with their own ATR + CCS plant
# Or to buy green hydrogen from the hydrogen grid


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
# Load prices input data
# =============================================================================

from profiles.Prices_input_data import (hydrogen_price_profiles_2030, hydrogen_price_profiles_2040, hydrogen_price_profiles_2050,
                                        naturalgas_price_profiles_2030, naturalgas_price_profiles_2040, naturalgas_price_profiles_2050,
                                        electricity_price_profiles_2030, electricity_price_profiles_2040, electricity_price_profiles_2050)

# Calculate the annual average prices 
h2_price_profiles_2030 = (np.array(
    [hydrogen_price_profiles_2030['Pessimistic'].sum(), 
     hydrogen_price_profiles_2030["Most likely"].sum(), 
     hydrogen_price_profiles_2030['Optimistic'].sum()]) 
     / 8760).tolist()

h2_price_profiles_2040 = (np.array(
    [hydrogen_price_profiles_2040['Pessimistic'].sum(), 
     hydrogen_price_profiles_2040["Most likely"].sum(), 
     hydrogen_price_profiles_2040['Optimistic'].sum()]) 
     / 8760).tolist()

h2_price_profiles_2050 = (np.array(
    [hydrogen_price_profiles_2050['Pessimistic'].sum(), 
     hydrogen_price_profiles_2050["Most likely"].sum(), 
     hydrogen_price_profiles_2050['Optimistic'].sum()]) 
     / 8760).tolist()

ng_price_profiles_2030 = (np.array(
    [naturalgas_price_profiles_2030['Pessimistic'].sum(), 
     naturalgas_price_profiles_2030["Most likely"].sum(), 
     naturalgas_price_profiles_2030['Optimistic'].sum()]) 
     / 8760).tolist()

ng_price_profiles_2040 = (np.array(
    [naturalgas_price_profiles_2040['Pessimistic'].sum(), 
     naturalgas_price_profiles_2040["Most likely"].sum(), 
     naturalgas_price_profiles_2040['Optimistic'].sum()]) 
     / 8760).tolist()

ng_price_profiles_2050 = (np.array(
    [naturalgas_price_profiles_2050['Pessimistic'].sum(), 
     naturalgas_price_profiles_2050["Most likely"].sum(), 
     naturalgas_price_profiles_2050['Optimistic'].sum()]) 
     / 8760).tolist()

e_price_profiles_2030 = (np.array(
    [electricity_price_profiles_2030['Pessimistic'].sum(), 
     electricity_price_profiles_2030["Most likely"].sum(), 
     electricity_price_profiles_2030['Optimistic'].sum()]) 
     / 8760).tolist()

e_price_profiles_2040 = (np.array(
    [electricity_price_profiles_2040['Pessimistic'].sum(), 
     electricity_price_profiles_2040["Most likely"].sum(), 
     electricity_price_profiles_2040['Optimistic'].sum()]) 
     / 8760).tolist()

e_price_profiles_2050 = (np.array(
    [electricity_price_profiles_2050['Pessimistic'].sum(), 
     electricity_price_profiles_2050["Most likely"].sum(), 
     electricity_price_profiles_2050['Optimistic'].sum()]) 
     / 8760).tolist()


# =============================================================================
# Input data - from Mapeditor
# =============================================================================

# can also add investment_costs, opex
bh_general_WACC = asset_parameters['wacc']['Offtaker']/100         # from % to decimal


# =============================================================================
# Cost data from factsheet
# =============================================================================

lhv_h2_mj_kg = 119.96         # MJ/kg
hhv_h2_mj_kg = 141.8          # MJ/kg

atr_plant_capacity = 1350 / 3 / hhv_h2_mj_kg * lhv_h2_mj_kg     # MW
atr_annual_utilisation = 0.92                                   # %

# Used factsheet: Hydelta2 D3.4, P4 ATR+CCS
# Date: 29-08-2024

# format: [2030[pes-ml-opt], 2040[pes-ml-opt], 2050[pes-ml-opt]]
# note: the plant capacity in the factsheet was 1350 MW, which is unreasonably large. 
# Divided by 3 to achieve plant capacity of 450 MW! Also for associated values, we divide everything by 4!

capex_atr_per_kw = [[1201,1300,1400],[1201,1300,1400],[1201,1300,1400]]       # EUR/kW  
atr_fixed_opex = np.array([[3,3,5],[3,3,5],[3,3,5]]) / 100                              # % of CAPEX

# CAPEX and OPEX in MEUR
bh_atr_capex = np.array(capex_atr_per_kw) * 1000 * np.array(atr_plant_capacity) / 1E6   # MEUR
bh_atr_opex = np.array(bh_atr_capex) * np.array(atr_fixed_opex)                         # MEUR

specific_ng_consumption = [[1.18,1.202,1.202],[1.18,1.202,1.202],[1.18,1.202,1.202]]    # MJ-NG/MJ-H2
specific_e_consumption = [[0.011,0.014,0.014],[0.011,0.014,0.014],[0.011,0.014,0.014]]  # kWh/MJ-H2

# NG and H2 prices 
# NG and E prices are inverted, because high NG prices means more avoided cost so is positive for the business case
bh_h2_price = [h2_price_profiles_2030, h2_price_profiles_2040, h2_price_profiles_2050]                        # EUR/MWh
bh_ng_price = [ng_price_profiles_2030[::-1], ng_price_profiles_2040[::-1], ng_price_profiles_2050[::-1]]      # EUR/MWh
bh_e_price = [e_price_profiles_2030[::-1], e_price_profiles_2040[::-1], e_price_profiles_2050[::-1]]          # EUR/MWh

electricity_tax = [[1.88, 1.88, 1.88],[1.88, 1.88, 1.88],[1.88, 1.88, 1.88]]            #EUR/MWh from belastingdienst, 2024 data

# HWI price - from CE Delft report 'Toetsing beleidsontwikkelingen waterstof' 2024
hwi_price = [[5.20, 5.16, 5.12],[5.20,5.16,5.12],[5.20,5.16,5.12]]                      # EUR/kgH2
carbon_permits = [[87, 87, 87],[130, 130, 130],[500, 500, 500]]                         # EUR/ton, Source: Enerdata


# =============================================================================
# Select active scenario and interpolate to get yearly data
# =============================================================================

# Define all factsheet data in a dictionary
# If new parameters are added with format: [2030[pes-ml-opt], 2040[pes-ml-opt], 2050[pes-ml-opt]], they should be added in this dictionary
raw_factsheet_data = {
    'capex_atr_per_kw': capex_atr_per_kw,
    'atr_fixed_opex': atr_fixed_opex,
    'bh_atr_capex': bh_atr_capex,
    'bh_atr_opex': bh_atr_opex,
    'specific_ng_consumption': specific_ng_consumption,
    'specific_e_consumption': specific_e_consumption,
    'bh_h2_price': bh_h2_price,
    'bh_ng_price': bh_ng_price,
    'bh_e_price': bh_e_price,
    'electricity_tax': electricity_tax,
    'hwi_price': hwi_price,
    'carbon_permits': carbon_permits
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
# Input data from Excel
# =============================================================================

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
bh_h2_pipeline_depreciation_list = bh_investment_lifetime_list             # assumption, pipeline is deprecated over length of bc, because unlikely to re-sell the pipeline. Could be changed to deprecation over lifetime, and to add resale value to bc.
bh_h2_station_depreciation_list = bh_investment_lifetime_list              # assumption, station is deprecated over length of bc, because unlikely to re-sell the station. Could be changed to deprecation over lifetime, and to add resale value to bc.


# Cost data from 'cost data offtaker' sheet
bh_contingency_list = [0.1, 0.1, 0.1]                       # in %
bh_loan_percentage_list = [0.75, 0.75, 0.75]                # in %
bh_decommissioning_percentage_list = [0.02, 0.02, 0.02]      # in %
bh_capex_h2_receiving_station_list = [5.38, 4.15, 3.37]     # MEUR      Assumption - Rob #Note: the order here is the other way around than most pes-ml-opt because this is an expense and not an avoided expense!
bh_capex_h2_pipeline_list = [38.75, 38.75, 38.75]           # MEUR      CHECK! calculation in Excel not clear!
bh_network_costs_ng_per_m3_list = [0.035, 0.035, 0.035]            # EUR/m3
bh_network_costs_h2_per_m3_list = [0.070, 0.0525, 0.035]           # EUR/m3    Assumption: 2x current NG costs for most likely/pessimistic, equal to NG for optimistic  

# Cost data from 'PPA offtaker' sheet
# bh_hpa_price_h2_list = h2_price_hpa_list[::-1]              # EUR/MWh prices from electrolyser, but inverted because optimistic for electrolyser is pessimistic for offtaker etc.
# bh_ng_price_list = [26.25, 35.00, 43.75]                    # EUR/MWh
bh_ng_tax_cost_list = [0.0489, 0.0489, 0.0611]              # EUR/m3


# =============================================================================
# Get active scenario for Excel data
# =============================================================================

# Get the active scenario (i.e., pes/ml,opt) for each parameter
# If new inputs are added in format: [pessimistic, most_likely, optimistic], they should be added here

bh_lifetime = bh_investment_lifetime_list[active_index]
duration_construction = duration_construction_list[active_index]
duration_operation = duration_operation_list[active_index]
duration_decommissioning = duration_decommissioning_list[active_index]
tender_year = tender_year_list[active_index]
co2_emissions_annual = co2_emissions_annual_list[active_index]

bh_income_tax_rate = bh_income_tax_rate_list[active_index]
bh_inflation = bh_inflation_list[active_index]
bh_loan_interest_rate = bh_loan_interest_rate_list[active_index]
bh_length_of_loan = bh_length_of_loan_list[active_index]
bh_atr_depreciation = bh_atr_depreciation_list[active_index]
bh_h2_pipeline_depreciation = bh_h2_pipeline_depreciation_list[active_index]
bh_h2_station_depreciation = bh_h2_station_depreciation_list[active_index]

bh_contingency = bh_contingency_list[active_index]
bh_loan_percentage = bh_loan_percentage_list[active_index]
bh_decommissioning_percentage = bh_decommissioning_percentage_list[active_index]
bh_capex_h2_receiving_station = bh_capex_h2_receiving_station_list[active_index]
bh_capex_h2_pipeline = bh_capex_h2_pipeline_list[active_index]
bh_network_costs_ng_per_m3 = bh_network_costs_ng_per_m3_list[active_index]
bh_network_costs_h2_per_m3 = bh_network_costs_h2_per_m3_list[active_index]
bh_ng_tax_cost = bh_ng_tax_cost_list[active_index]


# =============================================================================
# Demands and commodity volumes
# =============================================================================

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


# =============================================================================
# Cashflow dataframes
# =============================================================================

df_bh_atr_opex = pd.DataFrame(df_yearly_data.loc[['bh_atr_opex']], columns=all_years)
df_bh_h2_price = pd.DataFrame(df_yearly_data.loc[['bh_h2_price']], columns=all_years)
df_bh_ng_price = pd.DataFrame(df_yearly_data.loc[['bh_ng_price']], columns=all_years)
df_bh_e_price = pd.DataFrame(df_yearly_data.loc[['bh_e_price']], columns=all_years)
df_bh_electricity_tax = pd.DataFrame(df_yearly_data.loc[['electricity_tax']], columns=all_years)
df_bh_carbon_permits = pd.DataFrame(df_yearly_data.loc[['carbon_permits']], columns=all_years)

# =============================================================================
# Calculate cost data
# =============================================================================

# Network costs
bh_network_costs_h2 = bh_network_costs_h2_per_m3 * h2_demand_m3 / 1E6   # MEUR
bh_network_costs_ng = bh_network_costs_ng_per_m3 * ng_demand_m3 / 1E6   # MEUR

bh_atr_capex = df_yearly_data.loc['bh_atr_capex', tender_year]

bh_hwi_percentage = pd.DataFrame(0.0, index=["hwi_percentage"], columns=all_years)
bh_hwi_percentage.loc["hwi_percentage", 2030:2034] = 0.42
bh_hwi_percentage.loc["hwi_percentage", 2035::] = 0.6

# HWI costs
bh_hwi_costs = pd.DataFrame(columns=all_years)
bh_hwi_costs.loc['bh_hwi_costs'] = np.array(df_yearly_data.loc['hwi_price']) * h2_demand_kg / 1E6       # MEUR


# Financing
bh_avoided_loan = bh_loan_percentage * bh_atr_capex
bh_loan = bh_loan_percentage * (bh_capex_h2_receiving_station + bh_capex_h2_pipeline)

# numpy financial calculates the annuity payment for the loan. Same as the PMT function in Excel (but slightly different arguments). See 'Cost data OWF' cell C9.
bh_avoided_annuity_loan = -npf.pmt(bh_loan_interest_rate, bh_length_of_loan, bh_avoided_loan, fv=0, when='end')
bh_annuity_loan = -npf.pmt(bh_loan_interest_rate, bh_length_of_loan, bh_loan, fv=0, when='end')

# construction years
year_construction_start = tender_year + 1
year_construction_end = year_construction_start + duration_construction
construction_years_list = list(range(year_construction_start, year_construction_start + duration_construction))

# =============================================================================
# Calculate net capex and net loan, and depreciation - necessary for tax and profits calculations
# =============================================================================

# Total depreciation per year for H2 CAPEX investments
yearly_depreciation_h2 = (
    bh_capex_h2_receiving_station / bh_h2_station_depreciation 
    + bh_capex_h2_pipeline / bh_h2_pipeline_depreciation)  

# Total depreciation per year for CAPEX ATR
yearly_depreciation_atr = df_yearly_data.loc['bh_atr_capex',tender_year] / bh_atr_depreciation

# Net yearly depreciation rate (MEUR/year)
bh_net_yearly_depreciation = yearly_depreciation_h2 - yearly_depreciation_atr


# Net CAPEX investments
bh_net_capex = bh_capex_h2_receiving_station + bh_capex_h2_pipeline - df_yearly_data.loc['bh_atr_capex',tender_year]

bh_net_annuity_loan = bh_annuity_loan - bh_avoided_annuity_loan


# =============================================================================
# PARAMETER DICTIONARY
# =============================================================================

bh_parameters = {
    # General Business Case Data
    'lifetime_investment': bh_lifetime,
    'duration_construction': duration_construction,
    'duration_operation': duration_operation,
    'duration_decommissioning': duration_decommissioning,
    'tender_year': tender_year,

    # Financial Parameters
    'wacc': bh_general_WACC,
    'income_tax_rate': bh_income_tax_rate,
    'inflation': bh_inflation,
    'loan_interest_rate': bh_loan_interest_rate,
    'loan_percentage': bh_loan_percentage,
    'length_of_loan': bh_length_of_loan,

    # CAPEX & OPEX
    'capex_h2_receiving_station': bh_capex_h2_receiving_station,
    'capex_h2_pipeline': bh_capex_h2_pipeline,
    'capex_atr': bh_atr_capex,
    'opex_atr': df_bh_atr_opex,

    # Prices, Tariffs & Commodity Costs DataFrames
    "h2_price": df_bh_h2_price,
    "ng_price": df_bh_ng_price,
    "e_price": df_bh_e_price,
    "carbon_permits": df_bh_carbon_permits,
    "hwi_price": bh_hwi_costs,
    "network_costs_ng": bh_network_costs_ng,
    "network_costs_h2": bh_network_costs_h2,
    "ng_tax_costs": bh_ng_tax_cost,
    "e_tax_costs": df_bh_electricity_tax,

    # Additional parameters required to generalize functions
    # But not required for the sensitivity analysis
    "capex": bh_net_capex,
    "yearly_depreciation": bh_net_yearly_depreciation,
    "annuity_loan": bh_net_annuity_loan,
    "construction_years_list": construction_years_list,
    "contingency_percentage": bh_contingency,
    "allow_tax_savings": True,
}


# =============================================================================
# Dictionary to update parameters for sensitivity analysis
# =============================================================================

bh_parameter_update = {
    "cost_keys": ["capex_h2_receiving_station",
                  "capex_h2_pipeline"],

    "avoided_cost_keys": ["capex_atr"],

    "depreciation_years": {
        "capex_h2_receiving_station": bh_lifetime,
        "capex_h2_pipeline": bh_lifetime},

    "avoided_depreciation_years": {
        "capex_atr": bh_lifetime},
}
