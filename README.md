## Configurations
The project is designed in a way that requires several initial configurations. First, we need to define the search space (parameter bounds) by inputting this information into an Excel file named "param_config.xlsx." Additionally, we need to set the number of iterations, reference temperature, reference strain rate, and other parameters by editing the "global_config.xlsx" file. Once all configurations are in place, the optimization process can begin.

## Optimization Process
The project utilizes Bayesian optimization and is developed modularly, making it easy to integrate different damage models, materials, and data ranges.

## Project Structure
The project is structured as follows:
```
.
├── experimental_data──{material}
│                     └── stress_strain.xslx
├── damage_models
│   ├── johnson_cook
│   └── more models can be added..
│  
├── opt_algorithm
│   └── bayesian_opt
│   
├── modules
│   └── helper_functions
│   
├── global_config.xlsx
├── param_config.xlsx
│  
├── optimise.py
│  
├── results
│   └── {material} ── params.npy
│
└── README.md
```

## Run the code
To run the code, simply clone the repository and run the command below in the terminal: 
```bash
python main.py
```
The code will automatically read the configurations and start the optimization process. The results will be saved in the "results" folder.

## Results
The results are saved in the "results" folder. The results include the optimized parameters and the corresponding error. The results are saved in a numpy array format. The first column is the error, and the rest of the columns are the optimized parameters. The order of the parameters is the same as the order in the "param_config.xlsx" file.
