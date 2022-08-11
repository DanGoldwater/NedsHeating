#%%
Housemates_2022 = [
  {'name': 'PS', 'adjusted_income': 756, 'savings': 0},
  {'name': 'JB', 'adjusted_income': 1415, 'savings': 21_000},
  # {'name': 'SG', 'adjusted_income': 2533, 'savings': 165_000},
  {'name': 'SG', 'adjusted_income': 2533, 'savings': 50_000},
  {'name': 'DG', 'adjusted_income': 2167, 'savings': 18_000},
  {'name': 'SL', 'adjusted_income': 1000, 'savings': 17_000},
  {'name': 'MV', 'adjusted_income': 1840, 'savings': 17_000},
  {'name': 'SM', 'adjusted_income': 0, 'savings': 0},
  {'name': 'PP', 'adjusted_income': 875, 'savings': 0},
  {'name': 'TA', 'adjusted_income': 1100, 'savings': 30_000},
  ]


Bills = 1593
Rent = 2000
income_threshold = 14200 / 12
savings_threshold = 14200

import pandas as pd

df = pd.DataFrame(Housemates_2022)
df.head()