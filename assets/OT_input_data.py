# This business case represents an offtaker (OT) that replaces their natural gas demand with hydrogen 
# Used to be named NG_input_data

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
ot_general_wacc = asset_parameters['wacc']['Offtaker']/100         # from % to decimal


# =============================================================================
# Input data from Excel
# =============================================================================

# Energy densities of natural gas in MJ/m3 and MJ/kg
lhv_ng_mj_m3 = 31.65          # MJ/m3 
lhv_ng_mj_kg = 47.13          # MJ/kg (derived from essential hydrogen and natural gas conversions excel) 

#Energy densities of hydrogen
lhv_h2_mj_m3 = 10.8           # MJ/m3
lhv_h2_mj_kg = 119.96         # MJ/kg
lhv_h2_kwh_kg = 33.33         # kWh/kg
h2_density = 0.08988          # kg/m3 (@STP)

# Boiler efficiencies
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

# =============================================================================
# Input data from Excel and other sources
# =============================================================================

# format: [2030[pes-ml-opt], 2040[pes-ml-opt], 2050[pes-ml-opt]]

capex_ng_boiler_per_mw = [[0.069,0.069,0.069],[0.069,0.069,0.069],[0.069,0.069,0.069]]          # M€/MW(th) - data from data alignment WP3 system analysis + corrected for inflation 2019-2030
opex_ng_boiler_per_mw = [[0.0021,0.0028,0.0035],[0.0021,0.0028,0.0035],[0.0021,0.0028,0.0035]]  # M€/MW(th)/yr - data from data alignment WP3 system analysis + corrected for inflation 2019-2030 
capex_ng_boiler = np.array(capex_ng_boiler_per_mw)*ot_ng_boiler_capacity                        # MEUR
opex_ng_boiler = np.array(opex_ng_boiler_per_mw)*ot_ng_boiler_capacity                          # MEUR

capex_h2_boiler_per_mw = [[0.152,0.152,0.152],[0.152,0.152,0.152],[0.152,0.152,0.152]]          # M€/MW(th) - data from data alignment WP3 system analysis + corrected for inflation 2019-2030
opex_h2_boiler_per_mw = [[0.0048,0.0048,0.0048],[0.0048,0.0048,0.0048],[0.0048,0.0048,0.0048]]  # M€/MW(th)/yr - data from data alignment WP3 system analysis + corrected for inflation 2019-2030 
capex_h2_boiler = np.array(capex_h2_boiler_per_mw)*ot_h2_boiler_capacity                        # MEUR
opex_h2_boiler = np.array(opex_h2_boiler_per_mw)*ot_h2_boiler_capacity                          # MEUR

# Price projections (NG and E inverted: pes for producer = opt for consumer)
ot_h2_price = [h2_price_profiles_2030,h2_price_profiles_2040,h2_price_profiles_2050]                        # EUR/MWh
ot_ng_price = [ng_price_profiles_2030[::-1],ng_price_profiles_2040[::-1],ng_price_profiles_2050[::-1]]      # EUR/MWh
ot_e_price = [e_price_profiles_2030[::-1],e_price_profiles_2040[::-1],e_price_profiles_2050[::-1]]          # EUR/MWh

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
    "capex_ng_boiler_per_mw": capex_ng_boiler_per_mw,
    "opex_ng_boiler_per_mw": opex_ng_boiler_per_mw,
    "capex_ng_boiler": capex_ng_boiler,
    "opex_ng_boiler": opex_ng_boiler,
    "capex_h2_boiler_per_mw": capex_h2_boiler_per_mw,
    "opex_h2_boiler_per_mw": opex_h2_boiler_per_mw,
    "capex_h2_boiler": capex_h2_boiler,
    "opex_h2_boiler": opex_h2_boiler,
    "ot_h2_price": ot_h2_price,
    "ot_ng_price": ot_ng_price,
    "ot_e_price": ot_e_price,
    "electricity_tax": electricity_tax,
    "hwi_price": hwi_price,
    "carbon_permits": carbon_permits,
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
# Cashflow dataframes
# =============================================================================

# here we make a df with just the ng_capex numbers, so we can use this for the sensitivity later on
# double brackets [['name']] returns a df 

df_ng_boiler_opex = df_yearly_data.loc[['opex_ng_boiler']]
df_h2_boiler_opex = df_yearly_data.loc[['opex_h2_boiler']]
ot_h2_price = df_yearly_data.loc[['ot_h2_price']]
ot_ng_price = df_yearly_data.loc[['ot_ng_price']]
# ot_e_price = df_yearly_data.loc[['ot_e_price']]
# ot_electricity_tax = df_yearly_data.loc[['electricity_tax']]
ot_carbon_permits = df_yearly_data.loc[['carbon_permits']]


# construct HWI percentages, expected to increase over the years
ot_hwi_percentage = pd.DataFrame(0.0, index=["hwi_percentage"], columns=all_years)
ot_hwi_percentage.loc["hwi_percentage", 2030:2034] = 0.42
ot_hwi_percentage.loc["hwi_percentage", 2035::] = 0.6


# =============================================================================
# Input data from Excel
# =============================================================================

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
ot_h2_boiler_decommissioning_percentage_list = [0.02, 0.02, 0.02]    # in %
ot_ng_boiler_decommissioning_percentage_list = [0.02, 0.02, 0.02]    # in %
ot_capex_h2_receiving_station_list = [1, 1, 1]                      # MEUR      Assumption - Rob
ot_capex_h2_pipeline_list = [13.28, 10.81, 8.33]                    # MEUR      CHECK! calculation in Excel not clear! NUmbers corrected for inflation 2022-2030
ot_network_costs_ng_per_m3_list = [0.071, 0.071, 0.071]                    # EUR/m3 for ng demand up to 28.4 Mm3, for >28.4 costs are 0.035
ot_network_costs_h2_per_m3_list = [0.142, 0.107, 0.071]                    # EUR/m3    Assumption: 2x current NG costs for pessimistic, 1.5x NG for most likely, equal to NG for optimistic  


# Cost data from 'PPA offtaker' sheet
#bh_hpa_price_h2_list = h2_price_hpa_list[::-1]              # EUR/MWh prices from electrolyser, but inverted because optimistic for electrolyser is pessimistic for offtaker etc.
# ng_price_list = [26.25, 35.00, 43.75]                    # EUR/MWh
ng_tax_cost_list = [0.0489, 0.0489, 0.0611]              # EUR/m3


# =============================================================================
# Get active scenario for Excel data
# =============================================================================

# Get the active scenario (i.e., pes/ml,opt) for each parameter
# If new inputs are added in format: [pessimistic, most_likely, optimistic], they should be added here


ot_h2_boiler_lifetime = ot_h2_boiler_lifetime_list[active_index]
ot_ng_boiler_lifetime = ot_ng_boiler_lifetime_list[active_index]
duration_construction = duration_construction_list[active_index]
duration_operation = duration_operation_list[active_index]
duration_decommissioning = duration_decommissioning_list[active_index]
tender_year = tender_year_list[active_index]
# carbon_permits = carbon_permits[active_index]
co2_per_mwh_ng = co2_per_mwh_ng_list[active_index]

ot_income_tax_rate = ot_income_tax_rate_list[active_index]
ot_inflation = ot_inflation_list[active_index]
ot_loan_interest_rate = ot_loan_interest_rate_list[active_index]
ot_length_of_loan = ot_length_of_loan_list[active_index]

ot_h2_boiler_depreciation = ot_h2_boiler_depreciation_list[active_index]
ot_ng_boiler_depreciation = ot_ng_boiler_depreciation_list[active_index]
ot_h2_pipeline_depreciation = ot_h2_pipeline_depreciation_list[active_index]
ot_h2_station_depreciation = ot_h2_station_depreciation_list[active_index]

ot_contingency = ot_contingency_list[active_index]
ot_loan_percentage = ot_loan_percentage_list[active_index]
ot_h2_boiler_decommissioning_percentage = ot_h2_boiler_decommissioning_percentage_list[active_index]
ot_ng_boiler_decommissioning_percentage = ot_ng_boiler_decommissioning_percentage_list[active_index]

ot_capex_h2_receiving_station = ot_capex_h2_receiving_station_list[active_index]
ot_capex_h2_pipeline = ot_capex_h2_pipeline_list[active_index]
ot_network_costs_ng_per_m3 = ot_network_costs_ng_per_m3_list[active_index]
ot_network_costs_h2_per_m3 = ot_network_costs_h2_per_m3_list[active_index]
ot_ng_tax_cost = ng_tax_cost_list[active_index]


# =============================================================================
# Calculate cost data
# =============================================================================

# Network costs H2 & NG
ot_network_costs_h2 = ot_network_costs_h2_per_m3 * ot_h2_demand_m3 / 1E6    #MEUR
ot_network_costs_ng = ot_network_costs_ng_per_m3 * ot_ng_demand_m3 / 1E6    #MEUR

# HWI costs
ot_hwi_costs = pd.DataFrame(columns=all_years)
ot_hwi_costs.loc['ot_hwi_costs'] = np.array(df_yearly_data.loc['hwi_price']) * ot_h2_demand_kg / 1E6       # MEUR

# CAPEX
ot_capex_ng_boiler = df_yearly_data.loc['capex_ng_boiler', tender_year]
ot_capex_h2_boiler = df_yearly_data.loc['capex_h2_boiler', tender_year]

# calcualte loan costs
ot_avoided_loan = ot_loan_percentage * df_yearly_data.loc['capex_ng_boiler',tender_year]
ot_loan = ot_loan_percentage * (df_yearly_data.loc['capex_h2_boiler',tender_year] + ot_capex_h2_receiving_station + ot_capex_h2_pipeline)

# numpy financial calculates the annuity payment for the loan. Same as the PMT function in Excel (but slightly different arguments). See 'Cost data OWF' cell C9.
ot_avoided_annuity_loan = -npf.pmt(ot_loan_interest_rate, ot_length_of_loan, ot_avoided_loan, fv=0, when='end')
ot_annuity_loan = -npf.pmt(ot_loan_interest_rate, ot_length_of_loan, ot_loan, fv=0, when='end')

# construction years
year_construction_start = tender_year + 1
year_construction_end = year_construction_start + duration_construction
construction_years_list = list(range(year_construction_start, year_construction_start + duration_construction))

# =============================================================================
# Calculate total depreciation, necessary for tax and profits calculations
# =============================================================================

# Because the lifetime of the H2 boiler and the NG boiler are not the same, 
# and we still want to use the general taxes_and_profits_part1 formula, 
# we need to calculate the net yearly depreciation here

# Total depreciation per year for H2 CAPEX investments (18 years)
yearly_depreciation_h2 = (
    ot_capex_h2_boiler / ot_h2_boiler_depreciation
    + ot_capex_h2_receiving_station / ot_h2_station_depreciation
    + ot_capex_h2_pipeline / ot_h2_pipeline_depreciation
)

# Avoided depreciation per year for NG CAPEX investments (25 years)
yearly_depreciation_ng = ot_capex_ng_boiler / ot_ng_boiler_depreciation

# Net yearly depreciation rate (MEUR/year)
ot_net_yearly_depreciation = yearly_depreciation_h2 - yearly_depreciation_ng

# Calculate net CAPEX investments
ot_net_capex = (
    ot_capex_h2_boiler + ot_capex_h2_receiving_station + ot_capex_h2_pipeline - ot_capex_ng_boiler
)

ot_net_annuity_loan = ot_annuity_loan - ot_avoided_annuity_loan


# =============================================================================
# PARAMETER DICTIONARY
# =============================================================================

ot_parameters = {
    # General Business Case Data
    "lifetime_investment": ot_h2_boiler_lifetime,
    "ng_boiler_lifetime": ot_ng_boiler_lifetime,
    "duration_construction": duration_construction,
    "duration_operation": duration_operation,
    "duration_decommissioning": duration_decommissioning,
    "tender_year": tender_year,

    # Financial Parameters
    "wacc": ot_general_wacc,
    "income_tax_rate": ot_income_tax_rate,
    "inflation": ot_inflation,
    "loan_interest_rate": ot_loan_interest_rate,
    "loan_percentage": ot_loan_percentage,
    "length_of_loan": ot_length_of_loan,
    "h2_boiler_decommissioning_percentage": ot_h2_boiler_decommissioning_percentage,
    "ng_boiler_decommissioning_percentage": ot_ng_boiler_decommissioning_percentage,
    
    # CAPEX & OPEX
    "capex_h2_receiving_station": ot_capex_h2_receiving_station,
    "capex_h2_pipeline": ot_capex_h2_pipeline,
    "capex_ng_boiler": ot_capex_ng_boiler,
    "capex_h2_boiler": ot_capex_h2_boiler,
    "ng_boiler_opex": df_ng_boiler_opex,
    "h2_boiler_opex": df_h2_boiler_opex,

    # Prices, Tariffs & Commodity Costs DataFrames
    "h2_price": ot_h2_price,
    "ng_price": ot_ng_price,
    "carbon_permits": ot_carbon_permits,
    "hwi_price": ot_hwi_costs,
    "network_costs_ng": ot_network_costs_ng,
    "network_costs_h2": ot_network_costs_h2,
    "ng_tax_costs": ot_ng_tax_cost,

    # Additional parameters required to generalize functions
    # But not required for the sensitivity analysis
    "capex": ot_net_capex,
    "yearly_depreciation": ot_net_yearly_depreciation,
    "annuity_loan": ot_net_annuity_loan,
    "construction_years_list": construction_years_list,
    "contingency_percentage": ot_contingency,
    "allow_tax_savings": True,
}






