# %%
import os
while(os.getcwd().endswith('Optimisation') == False ):
    os.chdir('..')

# %%
import pandas as pd
import numpy as np
import sys
from sklearn.metrics import make_scorer
from loss_function.loss_function import *
from damage_models.johnson_cook import *
from modules.helper import *
from opt_algorithm.bayesian_opt import *


# %%
display_intro()

# %%
display_global_config_data()

# %%
print("Starting the Optimisation process...")

# %%
# Read the Excel file and split it into separate DataFrames
data = pd.read_excel("experimental_data/pm_superalloy/stress_strain.xlsx", sheet_name=None)

temperature_list = []

# Save the individual sheets as CSV files
for sheet_name, df in data.items():
    df.rename(columns={'Unnamed: 0': 'strain'}, inplace=True)
    df.to_csv(f"experimental_data/pm_superalloy/{sheet_name}.csv", index=False)
    temperature_list.append(int(sheet_name))

strain_rate_list = df.columns.to_list()
strain_rate_list.remove('strain')

# %%
best_parameters, best_loss = bayesian_optimisation(temperature_list, strain_rate_list)

print("Optimisation process completed.")
# Print or use the best parameters and their loss

display_best_params(best_parameters)
print("Best Value:", best_loss)

# %%



