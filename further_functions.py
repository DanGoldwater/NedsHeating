#%%
from house_rent_functions import *

Housemates_2022 = [
  {'name': 'Pat', 'adjusted_income': 756, 'savings': 0},
  {'name': 'Jen', 'adjusted_income': 1415, 'savings': 21_000},
  {'name': 'SG', 'adjusted_income': 2533, 'savings': 165_000},
  {'name': 'DG', 'adjusted_income': 2167, 'savings': 18_000},
  ]

Arguments_Current_9 = {
    "base_rent": 47,
    "income_threshold": 14200,
    "savings_threshold": 14200,
    "bills_to_pay": 110 * 9,
    "cap_ratio": 1.5,
    "rent_formula": rent_current,
    "bills_formula": bills_current,
    "list_of_housemates": Housemate_List_Current_9,
    'rent_params':{
      'alpha': .8,
      'gamma': .4,
      'beta': .1
    },
    "a": 0,
    "b": 0,
    "c": 0,
    'bills_params': {
        'alpha': .5,
        'beta': .1}
}


#%%
def get_projected_bills_to_pay():
  total = ( 
      1176.21 * 12 #Electricity and gas, house\
    + 163.44 * 12 # Electricity and gas, flat and factory\
    + 72.43 * 12 # Water, monthly
    + 44.73 * 12  # Internet for flat
    + 73 * 12   #  internet, house\
    + 150 * 4   #  Household cleaning to veggies\
    + 159  # TV license\
  ) #* 1.15 # Bills 'profit', so that we can build a buffer level
  return total / 12
    

print(get_projected_bills_to_pay())
#%%  
  


Arguments_Current_10 = Arguments_Current_9.copy()
Arguments_Current_10['list_of_housemates'] = Housemate_List_Current_10
Arguments_Proposed_9 = Arguments_Current_9.copy()
Arguments_Proposed_9.update(
  {'cap_ratio':
    1.75,
    'bills_to_pay': get_projected_bills_to_pay(),
    "rent_params":
    {'alpha':.8,
     'gamma':.5,
     'beta':.12      
    },
    "bills_params":{
    "alpha": .6,
    "beta": .1}})
# Arguments_Proposed_9['base_rent'] = 47
Arguments_Proposed_10 = Arguments_Proposed_9.copy()
Arguments_Current_10['list_of_housemates'] = Housemate_List_Current_10
Scenario_Current_9 = Scenario(**Arguments_Current_9)
Scenario_Current_10 = Scenario(**Arguments_Current_10)
Scenario_Proposed_9 = Scenario(**Arguments_Proposed_9)
Scenario_Proposed_10 = Scenario(**Arguments_Proposed_10)
