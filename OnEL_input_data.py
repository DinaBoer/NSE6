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


# additional data
#from OWF_input_data import owf_sold_to_electrolyser_list

#type 'yes' to update the variables retrieved from Operation_analysis_OWF_EL.ipynb. Else, the stored variables in the Pickle file will be used. This latter helps to run the program faster
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

########## Get cost data from Mapeditor

# el_capex?
# el_opex?
# el_general_wacc = asset_parameters.loc['Electrolyzer','wacc']/100     # from % to decimal
el_general_wacc_list = [0.095, 0.095, 0.07]                             # 9.5%
# el_efficiency = asset_parameters['Electrolyzer','efficiency']         # decimal, i.e., 60% # use factsheet info for now



# ########## Data from TNO Pathway Databook_v10 - Public Version
# ### Not being used right now, we will get 2040,2050 data later from TNO based on RHYCEET data (see below)
# # format: [2030,2040,2050]
# capex = [0.90, 0.67, 0.53]                              # MEUR/MW
# fixed_om = [22.5, 16.75, 13.33]                         # kEUR/MW
# var_om = []
# stack_replacement = []
# stack_lifetime = [60000, 60000, 60000]                  # hours
# efficiency = [0.7, 0.745, 0.79]                         # in %


########## Data from TNO paper: Evaluation of the levelised cost of hydrogen based on proposed electrolyser projects in the Netherlands (RHyCEET)
# The scenario numbers have been calculated based on the mean and Figure 3.3
# format: [mean*bottom line box, mean, mean*upper line box]  (with box referring to the box and whisker plot in figure 3.3)


electricity_tax = [[1.88, 1.88, 1.88],[1.88, 1.88, 1.88],[1.88, 1.88, 1.88]]                    # Eur/MWh, 2024 values from belastingdienst
# electricity tax is not included for offshore electrolysis bc -> maybe good to include it!
# minimum_load_operation = 0.225                                                                # 22.5%, % of rated capacity
capacity_tariff_h2_network = [[21.13,21.13,21.13],[21.13,21.13,21.13],[21.13,21.13,21.13]]      # Eur/KWe/yr  entry part; 50% of total tariff
entry_tariff_h2_network = np.array(capacity_tariff_h2_network) * 0.5                            # EUR/KWe/yr  only entry to the network is accounted in the bc of the electrolyser

#capex
total_capex_mean = [3050,2440,2440]                                             # Eur/KWe, 2030-2040-2050(Leonard) unit capital costs incl direct costs, indirect costs, owners costs and contingency
capex_mean = np.array(total_capex_mean) * (1-0.17)                              # Eur/KWe, total capex minus contingency of 17%
capex_100mw = [[1.103*capex_mean[0], capex_mean[0], 0.692*capex_mean[0]],
               [1.103*capex_mean[1], capex_mean[1], 0.692*capex_mean[1]],
               [1.103*capex_mean[2], capex_mean[2], 1600*(1-0.17)]]             # Eur/KWe, format: [mean*upper line box, mean, mean*bottm line box]  (with box referring to the box and whisker plot in figure 3.3)

stack_replacement_100mw = np.array(capex_100mw) * 0.15                          # Eur/KWe, 15% of unit capital cost (TNO paper said 10%, but for offshore EL 15% is used so this is kept the same for onshore)

#opex
opex_mean = [75.34, 75.34*0.8, 75.34*0.8]                                       # Eur/KWe/yr, decreased 2040 and 2050 by 20%, similar as for the CAPEX numbers
opex_100mw = [[1.242*opex_mean[0], opex_mean[0], 0.698*opex_mean[0]],
              [1.242*opex_mean[1], opex_mean[1], 0.698*opex_mean[1]],
              [1.242*opex_mean[2], opex_mean[2], 0.698*opex_mean[2]]]           # Eur/KWe/yr, format: [mean*upper line box, mean, mean*bottom line box]  (with box referring to the box and whisker plot in figure 3.3)


# for now we use the same prices as for the offshore electrolyser, see below
# we could consider to update the ppa price according to this new data
# el_ppa_mean = 75                                                                # Eur/MWhe
# el_ppa_price_list = [110.4*el_ppa_mean, el_ppa_mean, 88.2*el_ppa_mean]          # Eur/MWhe, format: [mean*upper line box, mean, mean*bottom line box]  (with box referring to the box and whisker plot in figure 3.3)

# #stack lifetime and degradation rate
# stack_life_mean = 55556                                                                      # hours, replacement at 10% degradation
# stack_lifetime_list = [1.195*stack_life_mean, stack_life_mean, 0.824*stack_life_mean]        # hours, replacement at 10% degradation, format: [mean*upper line box, mean, mean*bottom line box]  (with box referring to the box and whisker plot in figure 3.3)
# stack_deg_mean = 0.0018                                                                      # 0.18% per 1000 hrs
# stack_degradation_rate_list = [1.177*stack_deg_mean, stack_deg_mean, 0.776*stack_deg_mean]   # 0.18% eper 1000 hrs, format: [mean*upper line box, mean, mean*bottom line box]  (with box referring to the box and whisker plot in figure 3.3)

# HWI price - from CE Delft report 'Toetsing beleidsontwikkelingen waterstof' 2024
hwi_price = [[5.12, 5.16, 5.20],[5.12,5.16,5.20],[5.12,5.16,5.20]]                    # EUR/kgH2

# costs and revenues
el_electricity_costs_ppa = [costs_E_PPA_2030, costs_E_PPA_2040, costs_E_PPA_2050]               # EUR/year
el_electricity_costs_grid = [costs_E_market_2030, costs_E_market_2040, costs_E_market_2050]     # EUR/year
h2_revenues_hpa = [rev_H2_PPA_2030, rev_H2_PPA_2040, rev_H2_PPA_2050]                           # EUR/year
h2_storage_costs = [storage_costs_2030, storage_costs_2040, storage_costs_2050]                 # EUR/year
h2_sold_to_hpa = [H2_sold_2030, H2_sold_2040, H2_sold_2050]                                     # MWh/year
h2_sold_to_hpa_kg = np.array(h2_sold_to_hpa) * 1000 / lhv_h2_kwh_kg                             # kg/year 

E_purchased_by_EL_2030 = E_purchased_by_EL_2030.values.flatten().tolist()
E_purchased_by_EL_2040 = E_purchased_by_EL_2040.values.flatten().tolist()
E_purchased_by_EL_2050 = E_purchased_by_EL_2050.values.flatten().tolist()
E_purchased_by_EL = [E_purchased_by_EL_2030, E_purchased_by_EL_2040, E_purchased_by_EL_2050]    # GWh

E_purchased_by_EL_from_market_2030 = E_purchased_by_EL_from_market_2030.values.flatten().tolist()
E_purchased_by_EL_from_market_2040 = E_purchased_by_EL_from_market_2040.values.flatten().tolist()
E_purchased_by_EL_from_market_2050 = E_purchased_by_EL_from_market_2050.values.flatten().tolist()
E_purchased_by_EL_from_market = [E_purchased_by_EL_from_market_2030, E_purchased_by_EL_from_market_2040, E_purchased_by_EL_from_market_2050]

E_purchased_by_EL_from_PPA_2030 = E_purchased_by_EL_from_PPA_2030.values.flatten().tolist()
E_purchased_by_EL_from_PPA_2040 = E_purchased_by_EL_from_PPA_2040.values.flatten().tolist()
E_purchased_by_EL_from_PPA_2050 = E_purchased_by_EL_from_PPA_2050.values.flatten().tolist()
E_purchased_by_EL_from_PPA = [E_purchased_by_EL_from_PPA_2030, E_purchased_by_EL_from_PPA_2040, E_purchased_by_EL_from_PPA_2050]


factsheet_parameters = [electricity_tax, entry_tariff_h2_network, capex_100mw, stack_replacement_100mw, opex_100mw, hwi_price, el_electricity_costs_ppa, el_electricity_costs_grid, h2_revenues_hpa, h2_storage_costs, h2_sold_to_hpa, h2_sold_to_hpa_kg, E_purchased_by_EL, E_purchased_by_EL_from_market, E_purchased_by_EL_from_PPA]
index_names = ['electricity_tax', 'entry_tariff_h2_network','capex_100mw', 'stack_replacement_100mw', 'opex_100mw', 'hwi_price', 'el_electricity_costs_ppa', 'el_electricity_costs_grid', 'h2_revenues_hpa', 'h2_storage_costs', 'h2_sold_to_hpa', 'h2_sold_to_hpa_kg', 'E_purchased_by_EL', 'E_purchased_by_EL_from_market', 'E_purchased_by_EL_from_PPA']

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


# here we make a df with just the opex/stack_replacement numbers, so we can use this for the sensitivity later on
df_onel_opex_100mw = pd.DataFrame(columns=all_years)
df_stack_replacement_100mw = pd.DataFrame(columns=all_years)

df_onel_opex_100mw.loc['opex'] = np.array(df_yearly_data.loc['opex_100mw'] * 1000 * electrolyser_capacity / 1E6)                                          # MEUR
df_stack_replacement_100mw.loc['stack_replacement'] = np.array(df_yearly_data.loc['stack_replacement_100mw'] * 1000 * electrolyser_capacity / 1E6)      # MEUR

################ Comment this section if you want to run the BC without the operation analysis file
onel_annual_electricity_costs_ppa = pd.DataFrame(columns=all_years)
onel_annual_electricity_costs_grid = pd.DataFrame(columns=all_years)
onel_h2_storage_costs = pd.DataFrame(columns=all_years)
onel_h2_revenues = pd.DataFrame(columns=all_years)
onel_h2_sold_to_hpa = pd.DataFrame(columns=all_years)
onel_hwi_revenues = pd.DataFrame(columns=all_years)
onel_entry_tariff_h2_network = pd.DataFrame(columns=all_years)
onel_electricity_tax = pd.DataFrame(columns=all_years)
onel_electricity_tax = pd.DataFrame(columns=all_years)
onel_fraction_e_from_market = pd.DataFrame(columns=all_years)


onel_annual_electricity_costs_ppa.loc['onel_annual_electricity_costs_ppa'] = np.array(df_yearly_data.loc['el_electricity_costs_ppa']) / 1E6                         #in MEUR
onel_annual_electricity_costs_grid.loc['onel_annual_electricity_costs_grid'] = np.array(df_yearly_data.loc['el_electricity_costs_grid']) / 1E6                      #in MEUR
onel_h2_storage_costs.loc['onel_h2_storage_costs'] = np.array(df_yearly_data.loc['h2_storage_costs']) / 1E6                                                         #in MEUR
onel_h2_revenues.loc['onel_h2_revenues'] = np.array(df_yearly_data.loc['h2_revenues_hpa']) / 1E6                                                                    #in MEUR
onel_h2_sold_to_hpa.loc['onel_h2_sold_to_hpa'] = np.array(df_yearly_data.loc['h2_sold_to_hpa'])
onel_entry_tariff_h2_network.loc['onel_entry_tariff_h2_network'] = np.array(df_yearly_data.loc['entry_tariff_h2_network']) * electrolyser_capacity * 1000 / 1E6     # MEUR
onel_electricity_tax.loc['onel_electricity_tax'] = np.array(df_yearly_data.loc['electricity_tax']) * np.array(df_yearly_data.loc['E_purchased_by_EL']) * 1000 / 1E6 # MEUR
onel_fraction_e_from_market.loc['fraction_e_from_market'] = np.array(df_yearly_data.loc['E_purchased_by_EL_from_market']) / np.array(df_yearly_data.loc['E_purchased_by_EL_from_PPA'])    # so this fraction of the electricity input in the electrolyser is not green, and thus that amount of H2 will not be green so won't be able to sell HWI's for this!
onel_hwi_revenues.loc['onel_hwi_revenues'] = np.array(df_yearly_data.loc['h2_sold_to_hpa_kg']) * np.array(df_yearly_data.loc['hwi_price']) * np.array(1-onel_fraction_e_from_market.loc['fraction_e_from_market']) / 1E6                    # MEUR

########## Input data from Excel

# Data format: [pessimistic, most_likely, optimistic]

# General data: business case length
el_lifetime_list = [20, 25, 30]                             # years
duration_construction_list = [3, 3, 3]
duration_operation_list = el_lifetime_list                  # amount of operational years is equal to lifetime of the investment
duration_decommissioning_list = [2, 2, 2]
tender_year_list = [start_year-duration_construction_list[0], start_year-duration_construction_list[1], start_year-duration_construction_list[2]]                       # year at which business case is 0, 
                       # year at which business case is 0, 
                                                            # i.e. year before start construction


# Cost data from 'inflation-WACC' sheet
el_income_tax_rate_list = [0.258, 0.258, 0.258]             # in %
el_inflation_list = [0.02, 0.02, 0.02]                      # in %
el_loan_interest_rate_list = [0.065, 0.05, 0.035]           # in %
el_length_of_loan_list = [15, 15, 15]                       # years
el_loan_type = 'annuity'
el_depreciation_list = el_lifetime_list                     # years  Possibly change to el_depreciation list = el_lifetime_list
el_stacks_depreciation_list = [5, 5, 5]                     # years


# Cost data from 'cost data OWF' sheet
el_contingency_list = [0.1, 0.1, 0.1]                               # in %
el_loan_percentage_list = [0.50, 0.50, 0.50]                        # in %
el_decommissioning_percentage_list = [0.02, 0.02, 0.02]             # in %
el_electricity_grid_connection_tariff_list = [144.3, 144.3, 144.3]  # EUR/kW

########### commented because this information is retrieved from Operational analysis
# Cost data from 'PPA Electrolyser sheet
#ppa_price_electricity_list = [69.67, 55.74, 41.80]          # EUR/MWh
#grid_price_electricity_list = [102.32, 81.86, 61.39]        # EUR/MWh
#purchased_from_ppa_list = owf_sold_to_electrolyser_list     # MWh/yr
#purchased_from_grid_list = [157536, 157536, 157536]         # MWh/yr
#h2_storage_tariff_list = [3.24, 4.32, 5.40]                 # EUR/MWh
#h2_storage_need_list = [346530.12, 315027.38, 283524.64]    # MWh/yr
#h2_price_hpa_list = [61.50, 82.00, 102.50]                  # EUR/MWh

# Construct a dataframe with the input from above
df_cost_data = pd.DataFrame(columns=['pessimistic','most_likely','optimistic'])

# commented because it is now in the yearly data section
# df_cost_data.loc['capex_100mw'] = capex_100mw_list
# df_cost_data.loc['stack_replacement'] = stack_replacement_list
# df_cost_data.loc['o&m'] = operations_maintenance_list
# df_cost_data.loc['flh'] = full_load_hours_list
# df_cost_data.loc['el_ppa_price'] = el_ppa_price_list
# df_cost_data.loc['stack_lifetime'] = stack_lifetime_list
# df_cost_data.loc['stack_degradation'] = stack_degradation_rate_list

df_cost_data.loc['el_general_wacc'] = el_general_wacc_list
df_cost_data.loc['el_lifetime'] = el_lifetime_list
df_cost_data.loc['duration_construction'] = duration_construction_list
df_cost_data.loc['duration_operation'] = duration_operation_list
df_cost_data.loc['duration_decommissioning'] = duration_decommissioning_list
df_cost_data.loc['tender_year'] = tender_year_list

df_cost_data.loc['income_tax_rate'] = el_income_tax_rate_list
df_cost_data.loc['inflation'] = el_inflation_list
df_cost_data.loc['loan_interest_rate'] = el_loan_interest_rate_list
df_cost_data.loc['length_of_loan'] = el_length_of_loan_list
df_cost_data.loc['el_depreciation'] = el_depreciation_list
df_cost_data.loc['stack_depreciation'] = el_stacks_depreciation_list

df_cost_data.loc['contingency'] = el_contingency_list
df_cost_data.loc['loan_percentage'] = el_loan_percentage_list
df_cost_data.loc['decommissioning_percentage'] = el_decommissioning_percentage_list
df_cost_data.loc['electricity_grid_connection_tariff'] = el_electricity_grid_connection_tariff_list

######## Commented because this is retrieved from OPerational analysis
#df_cost_data.loc['ppa_price_electricity'] = ppa_price_electricity_list
#df_cost_data.loc['grid_price_electricity'] = grid_price_electricity_list
#df_cost_data.loc['purchased_from_ppa'] = purchased_from_ppa_list
#df_cost_data.loc['purchased_from_grid'] = purchased_from_grid_list
#df_cost_data.loc['h2_storage_tariff'] = h2_storage_tariff_list
#df_cost_data.loc['h2_storage_need'] = h2_storage_need_list
#df_cost_data.loc['h2_price_hpa'] = h2_price_hpa_list


df_cost_data


# the scenario is chosen, by dropping the other two scenario's from the dataframe

df_cost_data.drop(columns=drop_scenarios,axis=1,inplace=True)
df_cost_data.style.format(precision=3)

# get cost data for the correct scenario
# in the df we can see that we have the most_likely scenario
# we can get the parameters from the df by using the row index
# using df_cost_data.loc['parameter'] not only gives the value, but also column name, dtype etc.
# therefore, we use .item() to get the desired value

# commented because it is now in the yearly data sections
# capex_100mw = df_cost_data.loc['capex_100mw'].item()
# el_stack_replacement = df_cost_data.loc['stack_replacement'].item()
# o_and_m = df_cost_data.loc['o&m'].item()
# el_flh = df_cost_data.loc['flh'].item()
# el_ppa_price = df_cost_data.loc['el_ppa_price'].item()
# el_stack_lifetime = df_cost_data.loc['stack_lifetime'].item()
# el_stack_degradation = df_cost_data.loc['stack_degradation'].item()

onel_general_wacc = df_cost_data.loc['el_general_wacc'].item()
onel_lifetime = int(df_cost_data.loc['el_lifetime'].item())
duration_construction = int(df_cost_data.loc['duration_construction'].item())
duration_operation = int(df_cost_data.loc['duration_operation'].item())
duration_decommissioning = int(df_cost_data.loc['duration_decommissioning'].item())
tender_year = int(df_cost_data.loc['tender_year'].item())

onel_income_tax_rate = df_cost_data.loc['income_tax_rate'].item()
onel_inflation = df_cost_data.loc['inflation'].item()                 
onel_loan_interest_rate = df_cost_data.loc['loan_interest_rate'].item()
onel_length_of_loan = int(df_cost_data.loc['length_of_loan'].item())
onel_depreciation = int(df_cost_data.loc['el_depreciation'].item())
onel_stack_depreciation = int(df_cost_data.loc['stack_depreciation'].item())

onel_contingency = df_cost_data.loc['contingency'].item()
onel_loan_percentage = df_cost_data.loc['loan_percentage'].item()
onel_decommissioning_percentage = df_cost_data.loc['decommissioning_percentage'].item()
onel_electricity_grid_connection_tariff = df_cost_data.loc['electricity_grid_connection_tariff'].item()

########### Commented because this is retrieved from OPerational Analysis
#el_ppa_price_electricity = df_cost_data.loc['ppa_price_electricity'].item()
#el_grid_price_electricity= df_cost_data.loc['grid_price_electricity'].item()
#el_purchased_from_ppa = df_cost_data.loc['purchased_from_ppa'].item()
#el_purchased_from_grid = df_cost_data.loc['purchased_from_grid'].item()
#el_h2_storage_tariff = df_cost_data.loc['h2_storage_tariff'].item()
#el_h2_stoarge_need = df_cost_data.loc['h2_storage_need'].item()
#el_h2_price_hpa = df_cost_data.loc['h2_price_hpa'].item()


########## Calculate cost data
onel_capex_100mw = df_yearly_data.loc['capex_100mw',tender_year] * electrolyser_capacity * 1000 / 1E6     # MEUR

onel_loan_100mw = onel_capex_100mw * onel_loan_percentage                                                 # MEUR


# numpy financial calculates the annuity payment for the loan. Same as the PMT function in Excel (but slightly different arguments). See 'Cost data OWF' cell C9.
onel_annuity_loan_100mw = -npf.pmt(onel_loan_interest_rate, onel_length_of_loan, onel_loan_100mw, fv=0, when='end')

# calculate electricity grid costs
onel_electricity_grid_connection = onel_electricity_grid_connection_tariff * electrolyser_capacity * 1000 / 1E6

######### Commented because this is retrieved from Operational Analysiis
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

########## Input variables used for business case EL
# This is a list of all the input variables used in the business case. 
# Make sure to always use the same order in functions
# These are all the factors that we did a sensitivity analysis on in Excel

input_variables_list = ['capex_variable',
                        'df_opex_variable',
                        'inflation_variable',
                        'annual_electricity_costs_ppa_variable',
                        'annual_electricity_costs_grid_variable',
                        'electricity_grid_connection_variable',
                        'h2_storage_costs_variable',
                        'entry_tariff_h2_network_variable',
                        'electricity_tax_variable',
                        'df_stack_replacement_costs_variable',
                        'hydrogen_revenues_variable',                        
                        'hwi_revenues_variable',                        
                        'decommissioning_variable',
                        'loan_percentage_variable',
                        'loan_interest_rate_variable',
                        'income_tax_rate_variable',
                        'wacc_variable',
                        #'duration_operation_variable',
                        'lifetime_investment_variable']
