#%%
from ast import Call
from dataclasses import dataclass
import math
from re import L
from typing import List, Callable  

import pandas


@dataclass
class Housemate(object):
    income: int
    savings: int
    fixed_costs: int
    name: str
    
    def __post_init__(self):
        self.disposable_income = self.get_disposable_income()

    def get_disposable_income(self):
            state_threshold = 12570
            if self.income < state_threshold:
                return state_threshold
            else:
                return state_threshold + 0.8 * (self.income - state_threshold)
        
H1 = Housemate(income= 32000, fixed_costs= 0, savings= 20000, name= 'Drew')
H2 = Housemate(income= 46000, fixed_costs= 0, savings= 30000, name= 'Sacha')
H3 = Housemate(income= 41000, fixed_costs= 0, savings= 20000, name= 'Yaqub')
H4 = Housemate(income= 14000, fixed_costs= 0, savings= 0, name= 'Kenneth')
H5 = Housemate(income= 14000, fixed_costs= 0, savings= 0, name= 'Moses')
H6 = Housemate(income= 14000, fixed_costs= 0, savings= 0, name= 'Freddie')
H7 = Housemate(income= 14000, fixed_costs= 0, savings= 0, name= 'Leblanc')
H8 = Housemate(income= 27000, fixed_costs= 0, savings= 10000, name= 'Andy')
H9 = Housemate(income= 30000, fixed_costs= 0, savings= 0, name= 'Blaine')
H10 = Housemate(income= 0, fixed_costs= 0, savings= 0, name= 'Tyla')

list_of_housies = [H10, H9, H8, H7, H6, H5, H4, H3, H2, H1,] 

# H_Bezos = Housemate(income= 100000, fixed_costs= 0, savings= 0)
# H_Asisi = Housemate(income= 0, fixed_costs= 0, savings= 0)

@dataclass
class Scenario(object):
    base_rent: int
    bills: int
    cap_ratio: float
    income_threshold: int
    savings_threshold: int
    a: float
    b: float
    c: float
    
    def total_rent(self, list_of_housemates: List[Housemate], rent_formula: Callable):
        rent = 0
        for h in list_of_housemates:
            rent += rent_formula(scenario=self, housemate=h) 
        return rent

    def total_bills(self, list_of_housemates: List[Housemate], bills_formula: Callable):
        bills = 0
        for h in list_of_housemates:
            bills += bills_formula(scenario=self, housemate=h) 
        return bills
    
    def total_income(self, list_of_housemates: List[Housemate], bills_formula: Callable, rent_formula: Callable):
        rent = self.total_rent(list_of_housemates=list_of_housemates, rent_formula=rent_formula)
        bills = self.total_bills(list_of_housemates=list_of_housemates, bills_formula=bills_formula)
        return rent + bills
    
    
def rent_current(scenario: Scenario, housemate: Housemate):
    rent = scenario.base_rent
    if housemate.disposable_income > scenario.income_threshold:
        rent +=  math.ceil((housemate.disposable_income - scenario.income_threshold) / 3000)
        
    if housemate.savings > scenario.savings_threshold:
        rent += (housemate.savings - scenario.savings_threshold) / 3000
    
    if rent > scenario.cap_ratio:
        rent = scenario.cap_ratio * scenario.base_rent
    return rent * 52.2 / 12

def bills_current(scenario: Scenario, housemate: Housemate):
    return scenario.base_rent

def rent_nonlinear(scenario: Scenario, housemate: Housemate):
    if housemate.disposable_income < scenario.income_threshold:
        prop = scenario.base_rent
    else:
        diff = housemate.disposable_income - scenario.base_rent
        prop = (
            scenario.base_rent + 
            scenario.a * (scenario.b * (diff / 10) ** scenario.c) 
        )
    if prop > scenario.base_rent * scenario.cap_ratio:
        prop = scenario.base_rent * scenario.cap_ratio
    return prop * 52.2 / 12
    

def combined_nonlinear(scenario: Scenario, housemate: Housemate):
    diff = housemate.disposable_income - scenario.income_threshold
    outgoing = (
        (scenario.base_rent + scenario.bills) * (
            1 + 
            diff *  scenario.a + 
            scenario.b * (diff**scenario.c)
        )
    )
    return outgoing

def rent_from_combined(scenario: Scenario, housemate: Housemate):
    combined = combined_nonlinear(scenario=scenario, housemate=housemate)
    return combined - scenario.bills

def bills_from_combined(scenario: Scenario, housemate: Housemate):
    return scenario.bills


def make_df(scenario: Scenario, housemate_list: List[Housemate]):
    data =[]
    for h in housemate_list:
        data += [{
            'name': h.name,
            'current rent': rent_current(scenario=scenario, housemate=h),
            'current bills': bills_current(scenario=scenario, housemate=h),
            'non-linear rent': rent_nonlinear(scenario=scenario, housemate=h),
            'combined nonlinear rent': rent_from_combined(scenario=scenario, housemate=h),
            'bills from combined': bills_from_combined(scenario=scenario, housemate=h),
        }]
    return pandas.DataFrame(data)

    
    
    
    
    
    
    
    
    
    
    
    