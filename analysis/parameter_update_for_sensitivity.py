import numpy_financial as npf

def update_derived_parameters(
        params,
        cost_keys,
        avoided_cost_keys,
        depreciation_years,
        avoided_depreciation_years,
):
    """
    Updates the parameters of business cases that use cost/avoided cost structure
    like the offtaker and blue hydrogen business cases
    """

    # step 1: total costs and avoided costs
    total_costs = sum(params[key] for key in cost_keys)
    total_avoided_costs = sum(params[key] for key in avoided_cost_keys)

    # net CAPEX
    params["capex"] = total_costs - total_avoided_costs


    # step 2: net yearly depreciation
    yearly_depreciation = sum(
        params[key] / depreciation_years[key] for key in cost_keys)

    avoided_yearly_depreciation = sum(
        params[key] / avoided_depreciation_years[key] for key in avoided_cost_keys)


    params["yearly_depreciation"] = (yearly_depreciation - avoided_yearly_depreciation)

    # step 3: loan amounts
    loan = params["loan_percentage"] * total_costs
    avoided_loan = params["loan_percentage"]  * total_avoided_costs

    # step 4: net annuity loan
    annuity_loan = -npf.pmt(
        params["loan_interest_rate"],
        params["length_of_loan"],
        loan,
        fv=0,
        when="end"
    )

    avoided_annuity_loan = -npf.pmt(
        params["loan_interest_rate"],
        params["length_of_loan"],
        avoided_loan,
        fv=0,
        when="end"
    )

    params["annuity_loan"] = annuity_loan - avoided_annuity_loan

    return params

