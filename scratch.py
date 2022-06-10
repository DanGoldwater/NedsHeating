#%%
from house_rent_functions import *


Scenario_Current_9 = Scenario(**{
        "base_rent": 46,
        "income_threshold": 14200,
        "savings_threshold": 14200,
        "bills": 70,
        "cap_ratio": 1.5,
        "rent_formula": rent_current,
        "bills_formula": bills_current,
        "list_of_housemates": Housies_Current_Ten,
        "a": 0,
        "b": 0,
        "c": 0
    }
)

print(Scenario_Current_9.total_rent())
