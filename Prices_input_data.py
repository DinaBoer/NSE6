# imports --> EDSL data might not be needed (yet)
#from esdl import esdl
#from esdl.esdl_handler import EnergySystemHandler
import pandas as pd
import numpy as np
import numpy_financial as npf
from decimal import Decimal, ROUND_HALF_UP
import h5py

#Loading Excel files takes quite some time. In order to save time the needed dataframes are stored in H5 format.
#If you want to load new Excel input data, please change the 'no' into 'yes'.

#Do you want do enter new Excel input data?
answer = 'no'

if answer == 'yes':

    #Scenario input data
    #Pessimistic, optimistic and most likely price scenarios are seen from Windfarm and hydrogen offtaker perspective.
    #Note that prices can differ along the scenarios (e.g. scenario x has 'optimistic' prices for electricity and 'pessimistic' prices for natural gas). Therefore a check will be performed in the specific business case sheet
    #For the wind profile ideally pessimistic means lowest output and optimistic highest output.
    #However, make sure that wind profile and price outcomes match with each other

    #Scenario NSWPH_GA_II3050_NAT
    df_pessimistic_windprofile_file = pd.read_excel('IELGAS_Windprofiles.xlsx')
    df_pessimistic_solarprofile_file = pd.read_excel('IELGAS_Windprofiles.xlsx')
    #pessimistic_price_profile_file_2030 = 'NSWPH-GA II3050-KA 2030 20240611 + Hub Design - no congestion.xlsx'
    #pessimistic_price_profile_file_2040 = 'NSWPH-GA II3050-NAT 2040 20240612 + Hub Design - no congestion.xlsx'
    #pessimistic_price_profile_file_2050 = 'NSWPH-GA II3050-NAT 2050 20240612 + Hub Design - no congestion.xlsx'
    
    #uncomment for IO/explorative scenarios
    pessimistic_price_profile_file_2030 = 'TYNDP2024-NT II3050-NAT 2030 + Hubs 90onshoreandsolar.xlsx'
    pessimistic_price_profile_file_2040 = 'TYNDP2024-NT II3050-NAT 2040 + Hubs 90onshoreandsolar.xlsx'
    pessimistic_price_profile_file_2050 = 'TYNDP2024-GA II3050-NAT 2050 + Hubs 80onshoreandsolar.xlsx'
    
    #uncomment for Trend-Reflective scenarios
    #pessimistic_price_profile_file_2030 = 'I-ELGAS V2.2 NSE 2030 TYNDP2024-NT OPERA-ADAPT.xlsx'
    #pessimistic_price_profile_file_2040 = 'I-ELGAS V2.2 NSE 2040 TYNDP2024-NT OPERA-TRANSFORM.xlsx'
    #pessimistic_price_profile_file_2050 = 'I-ELGAS V2.2 NSE 2050 TYNDP2024-GA OPERA-TRANSFORM.xlsx'


    #Scenario NSWPH_GA_II3050_NAT
    df_mostlikely_windprofile_file = pd.read_excel('IELGAS_Windprofiles.xlsx')
    df_mostlikely_solarprofile_file = pd.read_excel('IELGAS_Windprofiles.xlsx')
    #mostlikely_price_profile_file_2030 = 'NSWPH-GA II3050-KA 2030 20240611 + Hub Design - no congestion.xlsx'
    #mostlikely_price_profile_file_2040 = 'NSWPH-GA II3050-NAT 2040 20240612 + Hub Design - no congestion.xlsx'
    #mostlikely_price_profile_file_2050 = 'NSWPH-GA II3050-NAT 2050 20240612 + Hub Design - no congestion.xlsx'

    #uncomment for IO/explorative scenarios
    mostlikely_price_profile_file_2030 = 'TYNDP2024-NT IP2024-KA 2030 + Hubs - no congestion v2.2 20241017.xlsx'
    mostlikely_price_profile_file_2040 = 'TYNDP2024 NT II3050 NAT 2040 + Hubs - no congestion v2.2 20241004.xlsx'
    mostlikely_price_profile_file_2050 = 'TYNDP2024-GA II3050-NAT 2050 + Hubs 90onshoreandsolar.xlsx'

    #uncomment for Trend-Reflective scenarios
    #mostlikely_price_profile_file_2030 = 'I-ELGAS V2.2 NSE 2030 TYNDP2024-NT OPERA-ADAPT.xlsx'
    #mostlikely_price_profile_file_2040 = 'I-ELGAS V2.2 NSE 2040 TYNDP2024-NT OPERA-LCI.xlsx'
    #mostlikely_price_profile_file_2050 = 'I-ELGAS V2.2 NSE 2050 TYNDP2024-NT OPERA-LCI.xlsx'


    #Scenario TYNDP2020_GA_II3050_NAT
    df_optimistic_windprofile_file = pd.read_excel('IELGAS_Windprofiles.xlsx')
    df_optimistic_solarprofile_file = pd.read_excel('IELGAS_Windprofiles.xlsx')
    #optimistic_price_profile_file_2030 = 'I-ELGAS Database V2.0 TYNDP2020-GA IP2024 KA 2030 + Hubs - no congestion.xlsx'
    #optimistic_price_profile_file_2040 = 'TYNDP2020_GA_II3050_NAT_2040_Hubs_no_congestion.xlsx'
    #optimistic_price_profile_file_2050 = 'I-ELGAS Database V2.0 TYNDP2020-GA II3050 NAT 2050 + Hubs - no congestion.xlsx'

    #uncomment for IO/explorative scenarios
    optimistic_price_profile_file_2030 = 'TYNDP2024-NT II3050-NAT 2030 + Hubs 110onshoreandsolar.xlsx'
    optimistic_price_profile_file_2040 = 'TYNDP2024-NT II3050-NAT 2040 + Hubs 110onshoreandsolar.xlsx'
    optimistic_price_profile_file_2050 = 'TYNDP2024 GA II3050 NAT 2050 + Hubs - no congestion v2.2 20241003.xlsx'

    #uncomment for Trend-Reflective scenarios
    #optimistic_price_profile_file_2030 = 'I-ELGAS V2.2 NSE 2030 TYNDP2024-NT OPERA-ADAPT.xlsx'
    #optimistic_price_profile_file_2040 = 'I-ELGAS V2.2 NSE 2040 TYNDP2024-NT OPERA-ADAPT.xlsx'
    #optimistic_price_profile_file_2050 = 'I-ELGAS V2.2 NSE 2050 TYNDP2024-GA OPERA-ADAPT.xlsx'

    #column names
    case_titles = ['Pessimistic', 'Most likely', 'Optimistic']
    #windprofile_files = (pessimistic_windprofile_file, mostlikely_windprofile_file, optimistic_windprofile_file)

    #create wind profile dataframes for pessimistic, most likely and optimistic scenarios for every location
    df_wind_profiles_HUBN = pd.concat([df_pessimistic_windprofile_file['CF_Wind_HUBN'],df_mostlikely_windprofile_file['CF_Wind_HUBN'],df_optimistic_windprofile_file['CF_Wind_HUBN']],axis=1)
    df_wind_profiles_HUBN.columns = case_titles
    df_wind_profiles_HUBE = pd.concat([df_pessimistic_windprofile_file['CF_Wind_HUBN'],df_mostlikely_windprofile_file['CF_Wind_HUBN'],df_optimistic_windprofile_file['CF_Wind_HUBN']],axis=1)
    df_wind_profiles_HUBE.columns = case_titles
    df_wind_profiles_HUBW = pd.concat([df_pessimistic_windprofile_file['CF_Wind_HUBW'],df_mostlikely_windprofile_file['CF_Wind_HUBW'],df_optimistic_windprofile_file['CF_Wind_HUBW']],axis=1)
    df_wind_profiles_HUBW.columns = case_titles
    df_solar_profiles_NED = pd.concat([df_pessimistic_solarprofile_file['CF_Solar'],df_mostlikely_solarprofile_file['CF_Solar'],df_optimistic_solarprofile_file['CF_Solar']],axis=1)
    df_solar_profiles_NED.columns = case_titles

    #function create dataframes with pessimistic, expected and optimistic hourly values from the Excel input files
    def create_PesExpOpt_dataframe_hourlydata(pessimistic_file, expected_file, optimistic_file, sheetname, columnname):
        df_pessimistic_sheet = pd.read_excel(pessimistic_file, sheet_name=sheetname)
        df_expected_sheet = pd.read_excel(expected_file, sheet_name=sheetname)
        df_optimistic_sheet = pd.read_excel(optimistic_file, sheet_name=sheetname)
        if sheetname == 'Hourly H2 Balance NED':
            df_pessimistic_column = df_pessimistic_sheet[columnname]
            maxproduction_pessimistic = max(df_pessimistic_column)
            df_CF_pessimistic = df_pessimistic_column / maxproduction_pessimistic
            df_expected_column = df_expected_sheet[columnname]
            maxproduction_expected = max(df_expected_column)
            df_CF_expected = df_expected_column / maxproduction_expected
            df_optimistic_column = df_optimistic_sheet[columnname]
            maxproduction_optimistic = max(df_optimistic_column)
            df_CF_optimistic = df_optimistic_column / maxproduction_optimistic
            df_output = pd.concat([df_CF_pessimistic,df_CF_expected,df_CF_optimistic],axis=1)
        else:
            df_output = pd.concat([df_pessimistic_sheet[columnname],df_expected_sheet[columnname],df_optimistic_sheet[columnname]],axis=1)
        df_output.columns = ['Pessimistic', 'Most likely', 'Optimistic']
        return df_output

    #create dataframes for electricity price data
    electricity_price_profiles_2030 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2030, mostlikely_price_profile_file_2030, optimistic_price_profile_file_2030, 'Hourly Electricity Prices','HUBN')
    electricity_price_profiles_2040 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2040, mostlikely_price_profile_file_2040, optimistic_price_profile_file_2040, 'Hourly Electricity Prices','HUBN')
    electricity_price_profiles_2050 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2050, mostlikely_price_profile_file_2050, optimistic_price_profile_file_2050, 'Hourly Electricity Prices','HUBN')
    #create dataframes for hydrogen price data
    hydrogen_price_profiles_2030 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2030, mostlikely_price_profile_file_2030, optimistic_price_profile_file_2030, 'Hourly H2 Prices','HUBN')
    hydrogen_price_profiles_2040 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2040, mostlikely_price_profile_file_2040, optimistic_price_profile_file_2040, 'Hourly H2 Prices','HUBN')
    hydrogen_price_profiles_2050 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2050, mostlikely_price_profile_file_2050, optimistic_price_profile_file_2050, 'Hourly H2 Prices','HUBN')
    #create dataframes for natural gas price data
    naturalgas_price_profiles_2030 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2030, mostlikely_price_profile_file_2030, optimistic_price_profile_file_2030, 'Hourly Gas Prices','G-ALK')
    naturalgas_price_profiles_2040 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2040, mostlikely_price_profile_file_2040, optimistic_price_profile_file_2040, 'Hourly Gas Prices','G-ALK')
    naturalgas_price_profiles_2050 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2050, mostlikely_price_profile_file_2050, optimistic_price_profile_file_2050, 'Hourly Gas Prices','G-ALK')
    #create dataframes for electrolyser capactity factors
    CF_electrolyser_profiles_2030 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2030, mostlikely_price_profile_file_2030, optimistic_price_profile_file_2030, 'Hourly H2 Balance NED','Hourly_Annual_H2production_electrolysis_NED')
    CF_electrolyser_profiles_2040 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2040, mostlikely_price_profile_file_2040, optimistic_price_profile_file_2040, 'Hourly H2 Balance NED','Hourly_Annual_H2production_electrolysis_NED')
    CF_electrolyser_profiles_2050 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2050, mostlikely_price_profile_file_2050, optimistic_price_profile_file_2050, 'Hourly H2 Balance NED','Hourly_Annual_H2production_electrolysis_NED')
    #create dataframes for electrolyser capactity factors
    CF_ATR_profiles_2030 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2030, mostlikely_price_profile_file_2030, optimistic_price_profile_file_2030, 'Hourly H2 Balance NED','Hourly_Annual_H2production_ATR_NED')
    CF_ATR_profiles_2040 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2040, mostlikely_price_profile_file_2040, optimistic_price_profile_file_2040, 'Hourly H2 Balance NED','Hourly_Annual_H2production_ATR_NED')
    CF_ATR_profiles_2050 = create_PesExpOpt_dataframe_hourlydata(pessimistic_price_profile_file_2050, mostlikely_price_profile_file_2050, optimistic_price_profile_file_2050, 'Hourly H2 Balance NED','Hourly_Annual_H2production_ATR_NED')

    #Overwrite data in HDFstore files
    with pd.HDFStore('profiles.h5') as store:
        store.put('electricity_price_profiles_2030', electricity_price_profiles_2030)
        store.put('electricity_price_profiles_2040', electricity_price_profiles_2040)
        store.put('electricity_price_profiles_2050', electricity_price_profiles_2050)
        store.put('hydrogen_price_profiles_2030', hydrogen_price_profiles_2030)
        store.put('hydrogen_price_profiles_2040', hydrogen_price_profiles_2040)
        store.put('hydrogen_price_profiles_2050', hydrogen_price_profiles_2050)
        store.put('naturalgas_price_profiles_2030', naturalgas_price_profiles_2030)
        store.put('naturalgas_price_profiles_2040', naturalgas_price_profiles_2040)
        store.put('naturalgas_price_profiles_2050', naturalgas_price_profiles_2050)
        store.put('CF_electrolyser_profiles_2030', CF_electrolyser_profiles_2030)
        store.put('CF_electrolyser_profiles_2040', CF_electrolyser_profiles_2040)
        store.put('CF_electrolyser_profiles_2050', CF_electrolyser_profiles_2050)
        store.put('CF_ATR_profiles_2030', CF_ATR_profiles_2030)
        store.put('CF_ATR_profiles_2040', CF_ATR_profiles_2040)
        store.put('CF_ATR_profiles_2050', CF_ATR_profiles_2050)
        store.put('df_wind_profiles_HUBN', df_wind_profiles_HUBN)
        store.put('df_wind_profiles_HUBE', df_wind_profiles_HUBE)
        store.put('df_wind_profiles_HUBW', df_wind_profiles_HUBW)
        store.put('df_solar_profiles_NED', df_solar_profiles_NED)
else:
    with pd.HDFStore('profiles.h5') as store:
        electricity_price_profiles_2030 = store['electricity_price_profiles_2030']
        electricity_price_profiles_2040 = store['electricity_price_profiles_2040']
        electricity_price_profiles_2050 = store['electricity_price_profiles_2050']
        hydrogen_price_profiles_2030 = store['hydrogen_price_profiles_2030']
        hydrogen_price_profiles_2040 = store['hydrogen_price_profiles_2040']
        hydrogen_price_profiles_2050 = store['hydrogen_price_profiles_2050']
        naturalgas_price_profiles_2030 = store['naturalgas_price_profiles_2030']
        naturalgas_price_profiles_2040 = store['naturalgas_price_profiles_2040']
        naturalgas_price_profiles_2050 = store['naturalgas_price_profiles_2050']
        CF_electrolyser_profiles_2030 = store['CF_electrolyser_profiles_2030']
        CF_electrolyser_profiles_2040 = store['CF_electrolyser_profiles_2040']
        CF_electrolyser_profiles_2050 = store['CF_electrolyser_profiles_2050']
        CF_ATR_profiles_2030 = store['CF_ATR_profiles_2030']
        CF_ATR_profiles_2040 = store['CF_ATR_profiles_2040']
        CF_ATR_profiles_2050 = store['CF_ATR_profiles_2050']
        df_wind_profiles_HUBN = store['df_wind_profiles_HUBN']
        df_wind_profiles_HUBE = store['df_wind_profiles_HUBE']
        df_wind_profiles_HUBW = store['df_wind_profiles_HUBW']
        df_solar_profiles_NED = store['df_solar_profiles_NED']

