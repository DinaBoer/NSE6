# imports
from esdl import esdl
from esdl.esdl_handler import EnergySystemHandler
import pandas as pd
import numpy as np
import numpy_financial as npf
from decimal import Decimal, ROUND_HALF_UP
import pickle

########## Set up energy system handler

# Setup Energy System Handler
esh = EnergySystemHandler()

# CHOOSE FILE CORRESPONDING TO SCENARIO!
file_name = "TNVDW_cost_single_units_v1_most_likely_scenario.esdl"
esh.load_file(file_name) #load here the file created in the mapeditor

energy_system = esh.get_energy_system()
instance_list = energy_system.instance
my_instance = instance_list[0]

# CHOOSE SCENARIO HERE

# the scenario is automatically chosen based on the file name!
if "most_likely" in file_name:
    drop_scenarios = ['optimistic','pessimistic']
    current_scenario = ['most_likely']
elif "optimistic" in file_name:
    drop_scenarios = ['most_likely','pessimistic']
    current_scenario = ['optimistic']
elif "pessimistic" in file_name:
    drop_scenarios = ['optimistic','most_likely']
    current_scenario = ['pessimistic']
else:
    raise ValueError("Unknown scenario or typo in file name!")     


########## Get input data from ESDL

#https://pyesdl.readthedocs.io/en/latest/Tutorials/tutorial4.html

asset_types_list = []
asset_names_list = []
asset_ids_list = []
asset_powers_list = []
asset_efficiencies_list = []
asset_investment_costs_list = [] #Capex, fixed_om and var_om are a singlevalue, not a range!
asset_fixed_opex_list = []
asset_var_opex_list = []
asset_wacc_list = []


#iterate through all ESDL elements: get all instances of type
for esdl_element in energy_system.eAllContents():

    #check if the element is an EnergyAsset
    if isinstance(esdl_element, esdl.EnergyAsset):

        #if it is, write its type, ID and name to a corresponding list
        asset_types_list.append(esdl_element.eClass.name)
        asset_names_list.append(esdl_element.name)

        #if it has costinformation, then append
        if esdl_element.costInformation is not None:
            asset_investment_costs_list.append(esdl_element.costInformation.investmentCosts.value) #singlevalues, not a range!
            asset_fixed_opex_list.append(esdl_element.costInformation.fixedOperationalAndMaintenanceCosts.value)
            asset_var_opex_list.append(esdl_element.costInformation.variableOperationalAndMaintenanceCosts.value)
            asset_wacc_list.append(esdl_element.costInformation.discountRate.value)   
        else:
            asset_investment_costs_list.append("")
            asset_fixed_opex_list.append("")
            asset_var_opex_list.append("")
            asset_wacc_list.append("")


        #if an element is a producer, consumer or conversion, write its power
        if isinstance(esdl_element, esdl.Producer) or isinstance(esdl_element, esdl.Consumer) or isinstance(esdl_element, esdl.Conversion):
            asset_powers_list.append(esdl_element.power)
        else:
            asset_powers_list.append("")

        #if an element is an electrolyzer, write its efficiency
        if isinstance(esdl_element, esdl.Electrolyzer):
            asset_efficiencies_list.append(esdl_element.efficiency)
        else:
            asset_efficiencies_list.append("")


# maybe include some units!

#create empty dataframe
asset_parameters = pd.DataFrame(index=asset_names_list)
asset_parameters.columns.name = 'name'

# fill in the data in the dataframe
asset_parameters["type"] = asset_types_list                   # e.g., Windpark, Electrolyser, GasDemand, ElectricityCable, Pipe
asset_parameters["power"] = asset_powers_list
asset_parameters["efficiency"] = asset_efficiencies_list
asset_parameters["investment_costs"] = asset_investment_costs_list
asset_parameters["fixed_opex"] = asset_fixed_opex_list
asset_parameters["variable_opex"] = asset_var_opex_list
asset_parameters["wacc"] = asset_wacc_list

#decided to remove these from dataframe
asset_parameters = asset_parameters.drop("type", axis=1)
asset_parameters = asset_parameters.drop("ElectricityCable", axis=0)
asset_parameters = asset_parameters.drop("H2-pipe", axis=0)

#display dataframe 
# print(asset_parameters)



def save_to_pickle(drop_scenarios, asset_parameters):
    
    filename = 'NSE_get_data_from_ESDL.pkl'

    variables_to_save = {
        'drop_scenarios' : drop_scenarios,
        'asset_parameters': asset_parameters,
    }

    with open(filename, 'wb') as f:
        pickle.dump(variables_to_save, f)

    print(f"All variables saved to {filename}")

save_to_pickle(drop_scenarios, asset_parameters)
