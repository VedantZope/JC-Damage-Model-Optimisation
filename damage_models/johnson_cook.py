import pandas as pd
import numpy as np

def get_global_config_data():
    data = pd.read_excel("global_config.xlsx")
    iterations = data["iterations"][0]
    stress_triaxility = data["stress triaxility"][0]
    reference_temperature = data["reference temperature"][0]
    melting_temperature = data["melting temperature"][0]
    reference_strain_rate = data["reference strain rate"][0]
    return iterations, stress_triaxility, reference_temperature, melting_temperature, reference_strain_rate


def get_eps_dot_star(eps_dot, eps_ref):
    eps_dot_star = eps_dot/eps_ref # dimensionless strain rate
    return eps_dot_star


def get_T_star(T, T_m, T_ref):
    T_star = (T - T_ref)/(T_m - T_ref) # homologous temperature
    return T_star

def johnson_cook(D_1, D_2, D_3, D_4, D_5, sigma_star, eps_dot_star, T_star):
    
    eps_f = (D_1 + D_2 * np.exp(D_3 * sigma_star)) * (1 + D_4 * np.log(eps_dot_star)) * (1 + D_5 * T_star)

    return eps_f #fracture strain


get_global_config_data()