import pandas as pd
import numpy as np
import os
import sys
from prettytable import PrettyTable

while(os.getcwd().endswith('Optimisation') == False ):
    os.chdir('..')

sys.path.append(os.getcwd())
from damage_models.johnson_cook import *


def get_iterations():
    iterations, _, _, _, _ = get_global_config_data()
    return iterations

def get_bounds():
    # Read the Excel file into a DataFrame
    file_path = "param_config.xlsx"
    df = pd.read_excel(file_path)

    # Create a dictionary to store the parameter bounds
    bounds = {}

    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        parameter = row['Parameter']
        lower_bound = row['lower_bound']
        upper_bound = row['upper_bound']
        bounds[parameter] = (lower_bound, upper_bound)
    return bounds

def  get_exponent(name):
    # Read the Excel file into a DataFrame
    file_path = "param_config.xlsx"
    df = pd.read_excel(file_path)

    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        parameter = row['Parameter']
        if parameter == name:
            exponent = row['exponent']
    return exponent

def load_data(temperature, strain_rate):
    file_name = f"experimental_data/pm_superalloy/{temperature}.csv"
    data = pd.read_csv(file_name)
    # Extract strain and stress data for the given strain rate
    strain = data["strain"]
    stress = data[f"{strain_rate}"]
    return strain, stress

def experimental_fracture_strain(stress, strain):
    max_stress_index = stress.idxmax()  # Find the index of the maximum stress
    fracture_strain = strain[max_stress_index]  # Get the corresponding strain
    return fracture_strain

def scale_parameters(params):
    D_1, D_2, D_3, D_4, D_5 = params.values()
    D_1 = D_1 * get_exponent("D_1")
    D_2 = D_2 * get_exponent("D_2")
    D_3 = D_3 * get_exponent("D_3")
    D_4 = D_4 * get_exponent("D_4")
    D_5 = D_5 * get_exponent("D_5")

    return D_1, D_2, D_3, D_4, D_5


def display_intro():
    # Read data from an Excel file
    param_info_file_path = "param_config.xlsx"
    data = pd.read_excel(param_info_file_path)

    # Apply the exponent to lower_bound and upper_bound
    data['lower_bound'] = data['lower_bound'] * data['exponent']
    data['upper_bound'] = data['upper_bound'] * data['exponent']

    # Remove the 'exponent' column
    data.drop('exponent', axis=1, inplace=True)

    # Create a PrettyTable
    table = PrettyTable(data.columns.to_list())
    table.title = "Parameter Optimization of Johnson-Cook Damage Model using Bayesian Optimisation"
    # Populate the table with data
    for _, row in data.iterrows():
        table.add_row(row)

    # Display the table
    print(table)


def display_global_config_data():
    iterations, stress_triaxility, reference_temperature, melting_temperature, reference_strain_rate = get_global_config_data()
    table = PrettyTable(["Parameter", "Value"])
    # Populate the table with data
    table.add_row(["Number of iterations", iterations])
    table.add_row(["Stress triaxility", stress_triaxility])
    table.add_row(["Reference temperature", reference_temperature])
    table.add_row(["Melting temperature", melting_temperature])
    table.add_row(["Reference strain rate", reference_strain_rate])
    # Display the table
    print(table)

def display_best_params(best_params):
    table = PrettyTable(["Parameter", "Value"])
    # Populate the table with data
    for key, value in best_params.items():
        table.add_row([key, value])
    # Display the table
    print(table)


class LossCalculator:
    def __init__(self, temperature_list, strain_rate_list):
        self.temperature_list = temperature_list
        self.strain_rate_list = strain_rate_list

    def calculate_loss(self, parameters, temperature, strain_rate, strain, stress):
        D_1, D_2, D_3, D_4, D_5 = parameters

        _, sigma_star, T_ref, T_m, eps_ref = get_global_config_data()

        eps_dot_star = get_eps_dot_star(strain_rate, eps_ref)
        T_star = get_T_star(temperature, T_m, T_ref)

        eps_f = johnson_cook(D_1, D_2, D_3, D_4, D_5, sigma_star, eps_dot_star, T_star)
        experimental_eps_f = experimental_fracture_strain(stress, strain)
        loss = eps_f - experimental_eps_f
        return loss

    def total_loss(self, parameters):
        D_1, D_2, D_3, D_4, D_5 = parameters
        total_loss = 0.0
        for temperature in self.temperature_list:
            for strain_rate in self.strain_rate_list:
                strain, stress = load_data(temperature, strain_rate)
                loss = self.calculate_loss(parameters, temperature, strain_rate, strain, stress)
                total_loss += np.sqrt(loss ** 2)
        return -total_loss