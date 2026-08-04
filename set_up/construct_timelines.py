from decimal import Decimal, ROUND_HALF_UP
import numpy as np


def construct_calendar_year_list(**kwargs):
    
    # 1. Get the parameters we need
    tender_year = kwargs['tender_year']
    duration_construction = kwargs['duration_construction']
    lifetime_investment = kwargs['lifetime_investment']
    duration_decommissioning = kwargs['duration_decommissioning']

    # 2. Calculate calendar years  
    year_construction_start = tender_year + 1
    year_start_operation = year_construction_start + duration_construction
    year_decommissioning_start = (year_start_operation + int(Decimal(lifetime_investment).to_integral_value(rounding=ROUND_HALF_UP)))
    # use Decimal.to_integral_value to prevent python to round to nearest even integral
    # this method uses the same rounding method as Excel (i.e., x.5 is rounded up)

    calendar_year_list = list(range(tender_year, year_decommissioning_start + duration_decommissioning))  

    return calendar_year_list



def construct_business_case_year_list(**kwargs):

    business_case_year_list = np.array(range(len(construct_calendar_year_list(**kwargs))))
    
    return business_case_year_list



def construct_operations_years_list(**kwargs):

    # 1. Get the parameters we need
    tender_year = kwargs['tender_year']
    duration_construction = kwargs['duration_construction']
    lifetime_investment = kwargs['lifetime_investment']

    # 2. Calculate the operational years
    year_construction_start = tender_year + 1
    year_start_operation = year_construction_start + duration_construction

    operations_years_list = list(range(year_start_operation, year_start_operation + int(Decimal(lifetime_investment).to_integral_value(rounding=ROUND_HALF_UP))))
    
    return operations_years_list



def construct_decommissioning_years_list(**kwargs):
    
    # 1. Get the parameters we need
    tender_year = kwargs['tender_year']
    duration_construction = kwargs['duration_construction']
    lifetime_investment = kwargs['lifetime_investment']
    duration_decommissioning = kwargs['duration_decommissioning']

    # 2. Calculate the decommissioning years
    year_construction_start = tender_year + 1
    year_start_operation = year_construction_start + duration_construction
    year_decommissioning_start = year_start_operation + int(Decimal(lifetime_investment).to_integral_value(rounding=ROUND_HALF_UP))

    decomissioning_years_list = list(range(year_decommissioning_start, year_decommissioning_start + duration_decommissioning))

    return decomissioning_years_list