#%%
from dataclasses import dataclass
import math
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
    
    def describe(self):
        print(f'{self.name} earns {self.income}, has {self.savings} in savings, and fixed costs of {self.fixed_costs}')
        
H1 = Housemate(income= 49000, fixed_costs= 0, savings= 20000, name= 'Drew')
H2 = Housemate(income= 46000, fixed_costs= 0, savings= 30000, name= 'Sacha')
H3 = Housemate(income= 41000, fixed_costs= 0, savings= 20000, name= 'Yaqub')
H4 = Housemate(income= 14000, fixed_costs= 0, savings= 0, name= 'Kenneth')
H5 = Housemate(income= 14000, fixed_costs= 0, savings= 0, name= 'Moses')
H6 = Housemate(income= 14000, fixed_costs= 0, savings= 0, name= 'Freddie')
H7 = Housemate(income= 14000, fixed_costs= 0, savings= 0, name= 'Leblanc')
H8 = Housemate(income= 27000, fixed_costs= 0, savings= 10000, name= 'Andy')
H9 = Housemate(income= 30000, fixed_costs= 0, savings= 0, name= 'Blaine')
H10 = Housemate(income= 0, fixed_costs= 0, savings= 0, name= 'Tyla')

Housemate_List_Current_9 = [H9, H8, H7, H6, H5, H4, H3, H2, H1,] 
Housemate_List_Current_10 = Housemate_List_Current_9 + [H10]

H_Bezos = Housemate(income= 100000, fixed_costs= 0, savings= 0, name='Bezos')
H_Asisi = Housemate(income= 0, fixed_costs= 0, savings= 0, name='Asisi')

@dataclass
class Scenario(object):
    base_rent: int
    bills_to_pay: int
    cap_ratio: float
    income_threshold: int
    savings_threshold: int
    a: float
    b: float
    c: float
    rent_params: dict
    bills_params: dict
    list_of_housemates: List[Housemate]
    rent_formula: Callable
    bills_formula: Callable

    def __post_init__(self) -> None:
        for h in self.list_of_housemates:
            h.excess = self.get_excess_for_housemate(h)
        self.b0 = self.calculate_b0()

    def get_excess_for_housemate(self, housemate: Housemate):
        savings_excess = max(housemate.savings - self.savings_threshold, 0)
        earning_excess = max(housemate.disposable_income  - housemate.fixed_costs - self.income_threshold, 0)
        excess = earning_excess + savings_excess
        return max(excess/1000, 0)

    def get_rent_linear_for_housemate(self, housemate: Housemate):
        prop =  (self.base_rent + housemate.excess / 3) 
        if prop > self.base_rent * 1.5:
            prop  = self.base_rent * 1.5
        return round(prop * 52.2 / 12)

    def get_rent_nonlinear_for_housemate(self, housemate: Housemate):
        extra = self.rent_params['alpha'] *  math.exp(self.rent_params['beta'] * housemate.excess) + self.rent_params['gamma'] * housemate.excess
        if extra > self.base_rent / 2:
            extra = self.base_rent / 2
        rent =  (self.base_rent +  extra) * 52.2 / 12
        return round(rent)
        
   
        
    def get_bills_for_housemate_linear(self):
        return round(self.bills_to_pay / len(self.list_of_housemates))


    def get_housemate_outgoings(self, housemate:Housemate):
        return round(self.get_bills_for_housemate_nonlinear(housemate) + self.get_rent_for_housemate(housemate))

    def print_housemate_by_housemate_linear(self):
        for h in self.list_of_housemates:
            print(f'{h.name} would pay {self.get_bills_for_housemate_linear()} on bills, and {self.get_rent_linear_for_housemate(h)} on rent')

    def print_housemate_by_housemate_nonlinear(self):
        for h in self.list_of_housemates:
            print(f'{h.name} would pay {self.get_bills_for_housemate_nonlinear(h)} on bills, and {self.get_rent_nonlinear_for_housemate(h)} on rent')

    def describe_all_housemates(self):
        for h in self.list_of_housemates:
            h.describe()
        

    def get_total_outgoings_for_housemate_linear(self, h):
        return self.get_bills_for_housemate_linear() + self.get_rent_linear_for_housemate(h)
        
    def get_total_outgoings_for_housemate_nonlinear(self, h):
        return self.get_bills_for_housemate_nonlinear(h) + self.get_rent_nonlinear_for_housemate(h)
    
    def get_total_rent_linear(self):
        return sum([self.get_rent_linear_for_housemate(h) for h in self.list_of_housemates])

    def get_total_rent_nonlinear(self):
        return sum([self.get_rent_nonlinear_for_housemate(h) for h in self.list_of_housemates])
    

    
    def calculate_b0(self):
        extra_bills = 0
        for h in self.list_of_housemates:
            extra_bills += self.bills_params['alpha'] * math.exp(self.bills_params['beta'] * h.excess)
        return (self.bills_to_pay - extra_bills) / len(self.list_of_housemates)
        
    def get_bills_for_housemate_nonlinear(self, housemate: Housemate):
        extra_bills = self.bills_params['alpha'] * math.exp(self.bills_params['beta'] * housemate.excess)
        return round(self.b0 + extra_bills)

    def get_total_bills_paid(self):
        return sum([self.get_bills_for_housemate_nonlinear(h) for h in self.list_of_housemates])


    def print_scenario_summary(self):
        print(f'In this scenario, the total monthly income would be {self.total_income()}')
        print(f'Total yearly income would be {self.total_income()}')
        print(f'The minimal rent would be {self.rent_formula(scenario=self, housemate=H_Asisi)}, and mimimum bills {self.rent_formula(scenario=self, housemate=H_Asisi)}')
        print(f'The maximum rent would be {self.rent_formula(scenario=self, housemate=H_Bezos)}, and mimimum bills {self.rent_formula(scenario=self, housemate=H_Bezos)}')
    
    
def rent_current(scenario: Scenario, housemate: Housemate):
    rent = scenario.base_rent
    if housemate.disposable_income > scenario.income_threshold:
        rent +=  math.ceil((housemate.disposable_income - scenario.income_threshold) / 3000)
        
    if housemate.savings > scenario.savings_threshold:
        rent += (housemate.savings - scenario.savings_threshold) / 3000
    
    if rent > (scenario.cap_ratio * scenario.base_rent):
        rent = scenario.cap_ratio * scenario.base_rent
    return int(math.ceil( rent * 52.2 / 12))

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

    
    
    
    
    
    
    
    
    
    
    