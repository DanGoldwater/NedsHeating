#%%
from house_rent_functions import *


Arguments_Current_9 = {
    "base_rent": 47,
    "income_threshold": 14200,
    "savings_threshold": 14200,
    "bills_to_pay": 80 * 9,
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


Arguments_Current_10 = Arguments_Current_9.copy()
Arguments_Current_10['list_of_housemates'] = Housemate_List_Current_10
Arguments_Proposed_9 = Arguments_Current_9.copy()
Arguments_Proposed_9.update(
  {'cap_ratio':
    1.75,
    "rent_params":
    {'alpha':.8,
     'gamma':.5,
     'beta':.12      
    },
    "bills_params":{
    "alpha": .6,
    "beta": .11}})
# Arguments_Proposed_9['base_rent'] = 47
Arguments_Proposed_10 = Arguments_Proposed_9.copy()
Arguments_Current_10['list_of_housemates'] = Housemate_List_Current_10
Scenario_Current_9 = Scenario(**Arguments_Current_9)
Scenario_Current_10 = Scenario(**Arguments_Current_10)
Scenario_Proposed_9 = Scenario(**Arguments_Proposed_9)
Scenario_Proposed_10 = Scenario(**Arguments_Proposed_10)
