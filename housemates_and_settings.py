#%%
Housemates_2022 = [
  {'name': 'Pat', 'adjusted_income': 756, 'savings': 0},
  {'name': 'Jen', 'adjusted_income': 1415, 'savings': 21_000},
  {'name': 'SG', 'adjusted_income': 2533, 'savings': 165_000},
  {'name': 'DG', 'adjusted_income': 2167, 'savings': 18_000},
  ]


Bills = 1593
Rent = 2000
income_threshold = 14200 / 12
savings_threshold = 14200

import pandas as pd

df = pd.DataFrame(Housemates_2022)
df.head()