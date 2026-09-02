# imports --> EDSL data might not be needed (yet)
#from esdl import esdl
#from esdl.esdl_handler import EnergySystemHandler
import pandas as pd
import pickle
from pathlib import Path


# =============================================================================
# File locations
# =============================================================================

# Make sure all the input files are referenced relative to the python script
base_dir = Path(__file__).resolve().parent

# Create pickle file to store the loaded data
cache_file = base_dir / "profiles.pkl"

# Set to True when new Excel input data should be loaded
# Otherwise the data is saved in pickle format and can be directly used
load_new_data = False


# =============================================================================
# Scenario input files - IO/explorative scenarios
# =============================================================================

pessimistic_price_profile_file_2030 = ("TYNDP2024-NT II3050-NAT 2030 + Hubs 90onshoreandsolar.xlsx")
pessimistic_price_profile_file_2040 = ("TYNDP2024-NT II3050-NAT 2040 + Hubs 90onshoreandsolar.xlsx")
pessimistic_price_profile_file_2050 = ("TYNDP2024-GA II3050-NAT 2050 + Hubs 80onshoreandsolar.xlsx")

mostlikely_price_profile_file_2030 = ("TYNDP2024-NT IP2024-KA 2030 + Hubs - no congestion v2.2 20241017.xlsx")
mostlikely_price_profile_file_2040 = ("TYNDP2024 NT II3050 NAT 2040 + Hubs - no congestion v2.2 20241004.xlsx")
mostlikely_price_profile_file_2050 = ("TYNDP2024-GA II3050-NAT 2050 + Hubs 90onshoreandsolar.xlsx")

optimistic_price_profile_file_2030 = ("TYNDP2024-NT II3050-NAT 2030 + Hubs 110onshoreandsolar.xlsx")
optimistic_price_profile_file_2040 = ("TYNDP2024-NT II3050-NAT 2040 + Hubs 110onshoreandsolar.xlsx")
optimistic_price_profile_file_2050 = ("TYNDP2024 GA II3050 NAT 2050 + Hubs - no congestion v2.2 20241003.xlsx")


# Define the sheets that you want to load, instead of loading the full Excels
sheets_to_load = [
    "Hourly Electricity Prices",
    "Hourly H2 Prices",
    "Hourly Gas Prices",
    "Hourly H2 Balance NED",
]


# =============================================================================
# Load the Excel files
# =============================================================================

if load_new_data or not cache_file.exists():
    print("Loading Excel files...")

    # Load 2030
    pessimistic_2030 = pd.read_excel(base_dir / pessimistic_price_profile_file_2030, sheet_name=sheets_to_load)
    mostlikely_2030 = pd.read_excel(base_dir / mostlikely_price_profile_file_2030, sheet_name=sheets_to_load)
    optimistic_2030 = pd.read_excel(base_dir / optimistic_price_profile_file_2030, sheet_name=sheets_to_load)


    # Load 2040
    pessimistic_2040 = pd.read_excel(base_dir / pessimistic_price_profile_file_2040, sheet_name=sheets_to_load)
    mostlikely_2040 = pd.read_excel(base_dir / mostlikely_price_profile_file_2040, sheet_name=sheets_to_load)
    optimistic_2040 = pd.read_excel(base_dir / optimistic_price_profile_file_2040, sheet_name=sheets_to_load)


    # Load 2050
    pessimistic_2050 = pd.read_excel(base_dir / pessimistic_price_profile_file_2050, sheet_name=sheets_to_load)
    mostlikely_2050 = pd.read_excel(base_dir / mostlikely_price_profile_file_2050, sheet_name=sheets_to_load)
    optimistic_2050 = pd.read_excel(base_dir / optimistic_price_profile_file_2050, sheet_name=sheets_to_load)

    # Load wind and solar data
    wind_solar_data = pd.read_excel(base_dir / "IELGAS_Windprofiles.xlsx")

    # =============================================================================
    # Helper function to create dataframe for pes-ml-opt with hourly data
    # =============================================================================

    def create_PesMlOpt_dataframe_hourlydata(
        pessimistic_data,
        mostlikely_data,
        optimistic_data,
        sheetname,
        columnname,
        normalize=False,
    ):

        df_pessimistic_column = pessimistic_data[sheetname][columnname]
        df_mostlikely_column = mostlikely_data[sheetname][columnname]
        df_optimistic_column = optimistic_data[sheetname][columnname]

        if normalize:
            df_pessimistic_column = df_pessimistic_column / df_pessimistic_column.max()
            df_mostlikely_column = df_mostlikely_column / df_mostlikely_column.max()
            df_optimistic_column = df_optimistic_column / df_optimistic_column.max()
        
        df_output = pd.concat(
            [df_pessimistic_column, df_mostlikely_column, df_optimistic_column], axis=1)

        df_output.columns = ["Pessimistic", "Most likely", "Optimistic"]

        return df_output

    # =============================================================================
    # Create the dfs with the price profiles and capacity factors
    # =============================================================================

    # -------------------------------------------------------------------------
    # Create electricity price profile
    # -------------------------------------------------------------------------

    electricity_price_profiles_2030 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2030,
            mostlikely_2030,
            optimistic_2030,
            "Hourly Electricity Prices",
            "HUBN",
        )
    )

    electricity_price_profiles_2040 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2040,
            mostlikely_2040,
            optimistic_2040,
            "Hourly Electricity Prices",
            "HUBN",
        )
    )

    electricity_price_profiles_2050 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2050,
            mostlikely_2050,
            optimistic_2050,
            "Hourly Electricity Prices",
            "HUBN",
        )
    )

    # -------------------------------------------------------------------------
    # Create hydrogen price profile
    # -------------------------------------------------------------------------

    hydrogen_price_profiles_2030 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2030,
            mostlikely_2030,
            optimistic_2030,
            "Hourly H2 Prices",
            "HUBN",
        )
    )

    hydrogen_price_profiles_2040 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2040,
            mostlikely_2040,
            optimistic_2040,
            "Hourly H2 Prices",
            "HUBN",
        )
    )

    hydrogen_price_profiles_2050 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2050,
            mostlikely_2050,
            optimistic_2050,
            "Hourly H2 Prices",
            "HUBN",
        )
    )

    # -------------------------------------------------------------------------
    # Create natural gas price profile
    # -------------------------------------------------------------------------

    naturalgas_price_profiles_2030 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2030,
            mostlikely_2030,
            optimistic_2030,
            "Hourly Gas Prices",
            "G-ALK",
        )
    )

    naturalgas_price_profiles_2040 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2040,
            mostlikely_2040,
            optimistic_2040,
            "Hourly Gas Prices",
            "G-ALK",
        )
    )

    naturalgas_price_profiles_2050 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2050,
            mostlikely_2050,
            optimistic_2050,
            "Hourly Gas Prices",
            "G-ALK",
        )
    )

    # -------------------------------------------------------------------------
    # Create electrolyser capacity factors
    # -------------------------------------------------------------------------

    CF_electrolyser_profiles_2030 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2030,
            mostlikely_2030,
            optimistic_2030,
            "Hourly H2 Balance NED",
            "Hourly_Annual_H2production_electrolysis_NED",
            normalize=True,
        )
    )

    CF_electrolyser_profiles_2040 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2040,
            mostlikely_2040,
            optimistic_2040,
            "Hourly H2 Balance NED",
            "Hourly_Annual_H2production_electrolysis_NED",
            normalize=True,
        )
    )

    CF_electrolyser_profiles_2050 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2050,
            mostlikely_2050,
            optimistic_2050,
            "Hourly H2 Balance NED",
            "Hourly_Annual_H2production_electrolysis_NED",
            normalize=True,
        )
    )

    # -------------------------------------------------------------------------
    # Create ATR capacity factors 
    # -------------------------------------------------------------------------

    CF_ATR_profiles_2030 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2030,
            mostlikely_2030,
            optimistic_2030,
            "Hourly H2 Balance NED",
            "Hourly_Annual_H2production_ATR_NED",
            normalize=True,
        )
    )

    CF_ATR_profiles_2040 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2040,
            mostlikely_2040,
            optimistic_2040,
            "Hourly H2 Balance NED",
            "Hourly_Annual_H2production_ATR_NED",
            normalize=True,
        )
    )

    CF_ATR_profiles_2050 = (
        create_PesMlOpt_dataframe_hourlydata(
            pessimistic_2050,
            mostlikely_2050,
            optimistic_2050,
            "Hourly H2 Balance NED",
            "Hourly_Annual_H2production_ATR_NED",
            normalize=True,
        )
    )

    # =============================================================================
    # Wind and Solar
    # =============================================================================

    scenario_names = [
        "Pessimistic",
        "Most likely",
        "Optimistic",
    ]

    # For all hubs and the solar profiles, there is no difference between the scenarios
    # Therefore, we use * 3 to fill each scenario column with the same values

    # HUB North
    df_wind_profiles_HUBN = pd.concat(
        [wind_solar_data["CF_Wind_HUBN"]] * 3,
        axis=1,
    )

    df_wind_profiles_HUBN.columns = scenario_names

    # HUB East
    df_wind_profiles_HUBE = pd.concat(
        [wind_solar_data["CF_Wind_HUBE"]] * 3,
        axis=1,
    )

    df_wind_profiles_HUBE.columns = scenario_names

    # HUB West
    df_wind_profiles_HUBW = pd.concat(
        [wind_solar_data["CF_Wind_HUBW"]] * 3,
        axis=1,
    )

    df_wind_profiles_HUBW.columns = scenario_names

    # Solar
    df_solar_profiles_NED = pd.concat(
        [wind_solar_data["CF_Solar"]] * 3,
        axis=1,
    )

    df_solar_profiles_NED.columns = scenario_names

    # =============================================================================
    # Create a dictionary with all profiles
    # =============================================================================

    profiles = {
        # Electricity prices
        "electricity_price_profiles_2030": electricity_price_profiles_2030,
        "electricity_price_profiles_2040": electricity_price_profiles_2040,
        "electricity_price_profiles_2050": electricity_price_profiles_2050,

        # Hydrogen prices
        "hydrogen_price_profiles_2030": hydrogen_price_profiles_2030,
        "hydrogen_price_profiles_2040": hydrogen_price_profiles_2040,
        "hydrogen_price_profiles_2050": hydrogen_price_profiles_2050,

        # Natural gas prices
        "naturalgas_price_profiles_2030": naturalgas_price_profiles_2030,
        "naturalgas_price_profiles_2040": naturalgas_price_profiles_2040,
        "naturalgas_price_profiles_2050": naturalgas_price_profiles_2050,

        # Electrolyser capacity factors
        "CF_electrolyser_profiles_2030": CF_electrolyser_profiles_2030,
        "CF_electrolyser_profiles_2040": CF_electrolyser_profiles_2040,
        "CF_electrolyser_profiles_2050": CF_electrolyser_profiles_2050,

        # ATR capacity factors
        "CF_ATR_profiles_2030": CF_ATR_profiles_2030,
        "CF_ATR_profiles_2040": CF_ATR_profiles_2040,
        "CF_ATR_profiles_2050": CF_ATR_profiles_2050,

        # Wind profiles
        "df_wind_profiles_HUBN": df_wind_profiles_HUBN,
        "df_wind_profiles_HUBE": df_wind_profiles_HUBE,
        "df_wind_profiles_HUBW": df_wind_profiles_HUBW,

        # Solar profiles
        "df_solar_profiles_NED": df_solar_profiles_NED,
    }

    # =============================================================================
    # Save the dictionary in a pickle file
    # =============================================================================

    with open(cache_file, "wb") as f:
        pickle.dump(profiles, f, protocol=pickle.HIGHEST_PROTOCOL)



else: 

    print(f"loading cached data from {cache_file.name}...")

    with open(cache_file, "rb") as f:
        profiles = pickle.load(f)

        # Electricity prices
        electricity_price_profiles_2030 = profiles["electricity_price_profiles_2030"]
        electricity_price_profiles_2040 = profiles["electricity_price_profiles_2040"]
        electricity_price_profiles_2050 = profiles["electricity_price_profiles_2050"]

        # Hydrogen prices
        hydrogen_price_profiles_2030 = profiles["hydrogen_price_profiles_2030"]
        hydrogen_price_profiles_2040 = profiles["hydrogen_price_profiles_2040"]
        hydrogen_price_profiles_2050 = profiles["hydrogen_price_profiles_2050"]

        # Natural gas prices
        naturalgas_price_profiles_2030 = profiles["naturalgas_price_profiles_2030"]
        naturalgas_price_profiles_2040 = profiles["naturalgas_price_profiles_2040"]
        naturalgas_price_profiles_2050 = profiles["naturalgas_price_profiles_2050"]

        # Electrolyser capacity factors
        CF_electrolyser_profiles_2030 = profiles["CF_electrolyser_profiles_2030"]
        CF_electrolyser_profiles_2040 = profiles["CF_electrolyser_profiles_2040"]
        CF_electrolyser_profiles_2050 = profiles["CF_electrolyser_profiles_2050"]

        # ATR capacity factors
        CF_ATR_profiles_2030 = profiles["CF_ATR_profiles_2030"]
        CF_ATR_profiles_2040 = profiles["CF_ATR_profiles_2040"]
        CF_ATR_profiles_2050 = profiles["CF_ATR_profiles_2050"]

        # Wind profiles
        df_wind_profiles_HUBN = profiles["df_wind_profiles_HUBN"]
        df_wind_profiles_HUBE = profiles["df_wind_profiles_HUBE"]
        df_wind_profiles_HUBW = profiles["df_wind_profiles_HUBW"]

        # Solar profiles
        df_solar_profiles_NED = profiles["df_solar_profiles_NED"]

