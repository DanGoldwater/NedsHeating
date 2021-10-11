#%%

import math
from matplotlib.pyplot import get_current_fig_manager
from numpy import arange
import numpy as np
import seaborn
import matplotlib.pyplot as plt

np.set_printoptions(precision=2)

rent_income_2020 = 26480

base = 500


class house_mate(object):
    def __init__(self, income, fixed_costs, savings):
        self.income = income
        self.fixed_costs = fixed_costs
        self.disposable_income = self.get_disposable_income()
        self.savings = savings

    def get_disposable_income(self):
        state_threshold = 12570
        if self.income < state_threshold:
            return state_threshold
        else:
            return state_threshold + 0.8 * (self.income - state_threshold)


H1 = house_mate(**{"income": 32000, "fixed_costs": 0, "savings": 20000})
H2 = house_mate(**{"income": 46000, "fixed_costs": 0, "savings": 30000})
H3 = house_mate(**{"income": 41000, "fixed_costs": 0, "savings": 20000})
H4 = house_mate(**{"income": 14000, "fixed_costs": 0, "savings": 0})
H5 = house_mate(**{"income": 14000, "fixed_costs": 0, "savings": 0})
H6 = house_mate(**{"income": 14000, "fixed_costs": 0, "savings": 0})
H7 = house_mate(**{"income": 14000, "fixed_costs": 0, "savings": 0})
H8 = house_mate(**{"income": 27000, "fixed_costs": 0, "savings": 10000})
H9 = house_mate(**{"income": 30000, "fixed_costs": 0, "savings": 0})
H10 = house_mate(**{"income": 0, "fixed_costs": 0, "savings": 0})
H_Bezos = house_mate(**{"income": 100000, "fixed_costs": 0, "savings": 0})
H_Asisi = house_mate(**{"income": 0, "fixed_costs": 0, "savings": 0})

HouseMateList = [
    H1,
    H2,
    H3,
    H4,
    H5,
    H6,
    H7,
    H8,
    H9
    #  , H10
]
HouseMateListWithBryony = HouseMateList + [H10]


class scenario(object):
    def __init__(
        self,
        base_rent,
        income_threshold,
        savings_threshold,
        bills,
        cap_ratio,
        rent_rule,
        bills_rule,
        a,
        b,
        c
    ):
        self.base_rent = base_rent
        self.income_threshold = income_threshold
        self.savings_threshold = savings_threshold
        self.bills = bills
        self.cap_ratio = cap_ratio
        self.rent_rule = rent_rule
        self.bills_rule = bills_rule
        self.a = a
        self.b = b
        self.c = c

    def get_rent(self, housemate):
        return self.rent_rule(self, housemate)

    def get_bills(self, housemate):
        return self.bills_rule(self, housemate)

    def get_total(self, housemate):
        return self.get_bills(housemate) + self.get_rent(housemate)


def rent_formula_current(scenario, house_mate):
    return rent_formula_current_form(scenario.cap_ratio, scenario.income_threshold, scenario.base_rent, house_mate.savings, house_mate.disposable_income, scenario.savings_threshold)

    # rent = scenario.base_rent
    # if (house_mate.disposable_income) > scenario.income_threshold:
    #     rent += (house_mate.disposable_income - scenario.income_threshold) / 3000
    # if (house_mate.savings) > scenario.savings_threshold:
    #     rent += (house_mate.savings - scenario.income_threshold) / 3000
    # if rent > scenario_current.cap_ratio * scenario_current.base_rent:
    #     rent = scenario_current.cap_ratio * scenario_current.base_rent
    # rent = math.ceil(rent)

    # rent = rent * 52.2 / 12
    # return rent

def rent_formula_current_form(cap_ratio, income_threshold, base_rent, savings, disposable_income, savings_threshold):
    rent = base_rent
    if (disposable_income) > income_threshold:
        rent += math.ceil((disposable_income - income_threshold) / 3000)
    if (savings) > savings_threshold:
        rent += (savings - income_threshold) / 3000
    if rent > cap_ratio * base_rent:
        rent = cap_ratio * base_rent
    # rent = math.ceil(rent)

    rent = rent * 52.2 / 12
    return rent


def bills_formula_current(scenario, house_mate):
    return scenario.bills


def bills_formula_new(scenatio, house_mate):
    return 0





def rent_formula_new(scenario, house_mate):
    # if house_mate.disposable_income < scenario.income_threshold:
    #     rent = scenario.base_rent
    # else:
    a = scenario.a
    b = scenario.b
    c = scenario.c
    rent = rent_formula_form(house_mate.disposable_income, scenario.income_threshold, scenario.base_rent, a, b, c, scenario.cap_ratio)
    return rent

# def rent_formula_form(disposable_income, base, slope, income_threshold):
#     if disposable_income < income_threshold:
#         return base
#     diff = disposable_income - income_threshold
#     prop = base
#     prop *= 1 + 1/(1+np.exp(-(diff-base) / slope))
#     return prop

def rent_formula_form(disposable_income, income_threshold, base,  a, b, c, cap):
    if disposable_income < income_threshold:
        prop = base
    else:
        diff = disposable_income - income_threshold
        prop = base + ( a * diff + b * ((diff / 10)  ** c) ) /5000
    if prop > base * cap:
        prop = base * cap
    return prop * 52 / 12


scenario_current = scenario(
    **{
        "base_rent": 46,
        "income_threshold": 14200,
        "savings_threshold": 14200,
        "bills": 70,
        "cap_ratio": 1.5,
        "rent_rule": rent_formula_current,
        "bills_rule": bills_formula_current,
        "a": 0,
        "b": 0,
        "c": 0
    }
)

scenario_proposed = scenario(
    **{
        "base_rent": 63,
        "income_threshold": 14200,
        "savings_threshold": 14200,
        "bills": 0,
        "cap_ratio": 1.8,
        "rent_rule": rent_formula_new,
        "bills_rule": bills_formula_new,
        "a": .8,
        "b": 1.3,
        "c": 1.56
    }
)

scenario_proposed_2 = scenario(
    **{
        "base_rent": 65,
        "income_threshold": 14200,
        "savings_threshold": 14200,
        "bills": 0,
        "cap_ratio": 1.8,
        "rent_rule": rent_formula_new,
        "bills_rule": bills_formula_new,
        "a": 1,
        "b": .8,
        "c": 1.3
    }
)


def get_house_income(housemate_list, scenario):
    income = 0
    for h in housemate_list:
        income += scenario.get_rent(h)
    return income * 12


def plot_scenario_rents(scenario, housemate_list):
    rent_list = [scenario.get_rent(h) for h in housemate_list]
    plt.bar(arange(len(housemate_list)), rent_list)
    plt.ylim(bottom=(min(rent_list) - 20))
    plt.xlabel("Housemate")
    plt.ylabel("rent per month")

income_range = arange(10000, 50000, 10)

def make_scenario_plot_data(scenario):
    return [rent_formula_form(xi,scenario.income_threshold,  scenario.base_rent, scenario.a, scenario.b, scenario.c, scenario.cap_ratio) for xi in income_range]

house_income_current = get_house_income(HouseMateList, scenario_current)
rent_list_current = [scenario_current.get_rent(h) for h in HouseMateList]



