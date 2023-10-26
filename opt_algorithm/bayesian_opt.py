import numpy as np
import os
import sys
from bayes_opt import UtilityFunction
from bayes_opt import BayesianOptimization

while(os.getcwd().endswith('Optimisation') == False ):
    os.chdir('..')

sys.path.append(os.getcwd())
from modules.helper import *

def bayesian_optimisation(temperature_list, strain_rate_list):

    bounds = get_bounds()
    num_iterations = get_iterations()

    loss_calculator = LossCalculator(temperature_list, strain_rate_list)

    def objective_function(param1, param2, param3, param4, param5):
        parameters = [param1, param2, param3, param4, param5]
        loss = loss_calculator.total_loss(parameters)
        return -loss  # Minimize, so negate the loss

    # Create an instance of BayesianOptimization
    optimizer = BayesianOptimization(
        f=objective_function,
        pbounds=bounds,
        random_state=1
    )

    # Perform Bayesian optimization

    for _ in range(num_iterations):

        utility = UtilityFunction(kind="ucb", kappa=2.5, xi=0.0)
        # Suggest parameters
        suggested_params = optimizer.suggest(utility_function=utility)  # Use EI as the utility function
        suggested_params = scale_parameters(suggested_params)
        print(_)

        # Calculate the loss for the suggested parameters
        loss = loss_calculator.total_loss(suggested_params)

        # Tell the loss to the BayesianOptimization library
        optimizer.register(params=suggested_params, target=loss)

    # Get the best set of parameters and the corresponding maximum value
    best_params = optimizer.max['params']
    best_value = optimizer.max['target']
    return best_params, best_value


