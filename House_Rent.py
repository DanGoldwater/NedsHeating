
import math
from matplotlib.pyplot import get_current_fig_manager
from numpy import arange
import numpy as np
import seaborn
import matplotlib.pyplot as plt
np.set_printoptions(precision=2)

rent_income_2020 = 26480
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
        
H1 = house_mate(**{
    'income' : 32000,
    'fixed_costs' : 0,
    'savings' : 20000})
H2 = house_mate(**{
    'income' : 46000,
    'fixed_costs' : 0,
    'savings' : 30000})
H3 = house_mate(**{
    'income' : 41000,
    'fixed_costs' : 0,
    'savings' : 20000})
H4 = house_mate(**{
    'income' : 14000,
    'fixed_costs' : 0,
    'savings' : 0})
H5 = house_mate(**{
    'income' : 14000,
    'fixed_costs' : 0,
    'savings' : 0})
H6 = house_mate(**{
    'income' : 14000,
    'fixed_costs' : 0,
    'savings' : 0})
H7 = house_mate(**{
    'income' : 14000,
    'fixed_costs' : 0,
    'savings' : 0})
H8 = house_mate(**{
    'income' : 27000,
    'fixed_costs' : 0,
    'savings' : 10000})
H9 = house_mate(**{
    'income' : 30000,
    'fixed_costs' : 0,
    'savings' : 0})
H10 = house_mate(**{
    'income' : 0,
    'fixed_costs' : 0,
    'savings' : 0})
H_Bezos = house_mate(**{
    'income' : 100000,
    'fixed_costs' : 0,
    'savings' : 0})
H_Asisi = house_mate(**{
    'income' : 0,
    'fixed_costs' : 0,
    'savings' : 0})

HouseMateList = [H1, H2, H3, H4, H5, H6, H7, H8, H9
                #  , H10
                ]
HouseMateListWithBryony = HouseMateList + [H10]

class scenario(object):
    def __init__(self, base_rent, income_threshold, savings_threshold, bills, cap_ratio, rent_rule, bills_rule):
        self.base_rent = base_rent
        self.income_threshold = income_threshold
        self.savings_threshold = savings_threshold
        self.bills = bills
        self.cap_ratio = cap_ratio
        self.rent_rule = rent_rule
        self.bills_rule = bills_rule
    
    def get_rent(self, housemate):
        return self.rent_rule(self, housemate)
    
    def get_bills(self, housemate):
        return self.bills_rule(self, housemate)
    
    def get_total(self, housemate):
        return self.get_bills(housemate) + self.get_rent(housemate)
        
def rent_formula_current(scenario, house_mate):
    rent = scenario.base_rent
    if (house_mate.disposable_income ) > scenario.income_threshold:
        rent += (house_mate.disposable_income - scenario.income_threshold) / 3000
    if (house_mate.savings ) > scenario.savings_threshold:
        rent += (house_mate.savings - scenario.income_threshold) / 3000
    if rent > scenario_current.cap_ratio * scenario_current.base_rent:
        rent = scenario_current.cap_ratio * scenario_current.base_rent
    rent = math.ceil(rent)
    
    rent =  rent * 52.2 / 12
    return rent

def bills_formula_current(scenario, house_mate):
    return scenario.bills

def bills_formula_new(scenatio, house_mate):
    return 0
scaling = 23

exponent = 11000
base = 15000


def rent_formula_new(scenario, house_mate):
    if house_mate.disposable_income < scenario.income_threshold:
        rent = scenario.base_rent
    else:
        diff = house_mate.disposable_income - scenario.income_threshold
        prop = scaling * (1+ 1/(1+np.exp(-(diff-base) / exponent)))
        rent = scenario.base_rent +  prop
    return rent


scenario_current = scenario(**{
    'base_rent' : 46,
    'income_threshold' : 14200,
    'savings_threshold' : 14200,
    'bills' : 70,
    'cap_ratio' : 1.5,
    'rent_rule': rent_formula_current,
    'bills_rule': bills_formula_current
})

scenario_proposed = scenario(**{
    'base_rent' :  60,
    'income_threshold': 14200,
    'savings_threshold': 14200,
    'bills' : 0,
    'cap_ratio' : 1.5,
    'rent_rule': rent_formula_new,
    'bills_rule': bills_formula_new
    })

        




def get_house_income(housemate_list, scenario):
    income = 0
    for h in housemate_list:
        income += scenario.get_rent(h)
    return income * 12

def plot_scenario_rents(scenario, housemate_list):
     rent_list = [scenario.get_rent(h) for h in housemate_list]
     plt.bar(arange(len(housemate_list)), rent_list)
     plt.ylim(bottom=(min(rent_list) - 20))
     plt.xlabel('Housemate')
     plt.ylabel('rent per month')

house_income_current = get_house_income(HouseMateList, scenario_current)
rent_list_current = [scenario_current.get_rent(h) for h in HouseMateList]







    
    
    