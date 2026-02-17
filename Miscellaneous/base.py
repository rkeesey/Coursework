#!/usr/bin/env python3
import torch
from evotorch import Problem
from typing import Iterable
import multiprocessing
import pandas as pd
import json
from evotorch.algorithms import GeneticAlgorithm
from evotorch.operators import TwoPointCrossOver
from evotorch.operators import GaussianMutation
from evotorch.logging import StdOutLogger, Logger
from scipy.interpolate import interp1d
import sys
import random
import numpy as np
import secrets

class init_Problem(Problem):
    def __init__(self, param_num, bounds, init_params, fitness_func, num_actors):
        
        self.fitness_func = fitness_func
        self.init_params = torch.tensor(init_params, dtype=torch.float32)
        self._already_initialized = False
        
        super().__init__(
            objective_sense="min",
            solution_length=param_num,
            bounds=bounds,
            objective_func=fitness_func,
            dtype=torch.float32,
            num_actors=num_actors,
            num_gpus_per_actor=0
        )  
    """ only uncomment if initial values need to be initialized!!!!!
    def _fill(self, values: Iterable):

        if not self._already_initialized:
            values[0] = self.init_params

            low = self.initial_lower_bounds
            high = self.initial_upper_bounds
            values[1:] = low + (high - low) * torch.rand(values.shape[0]-1, values.shape[1], dtype=values.dtype)
            self._already_initialized = True
            return values

        else:
            return self.make_uniform(
                out=values,
                lb=self.initial_lower_bounds,
                ub=self.initial_upper_bounds,
            )
    """

class GA_fit:

    def __init__(self, x, y, rate_eqn, chain_l, init_ch, bounds, iterations=1000, popsize=40, num_actors=12):
        self.x = x
        self.y = y # reference data
        self.chain_l = chain_l
        self.init_ch = init_ch
        self.rate_eqn = rate_eqn
        self.iterations = iterations
        self.bounds = bounds
        self.popsize = popsize
        self.num_actors = num_actors

    def run_GA(self, init_params):

        num_cores = multiprocessing.cpu_count() # all available cores

        problem = init_Problem(
                               param_num=len(init_params), 
                               bounds=self.bounds,
                               init_params=init_params,
                               fitness_func=self.fitness_func,
                               num_actors=self.num_actors
                               )

        ga = GeneticAlgorithm(
            problem, 
            popsize=self.popsize,
            operators=[TwoPointCrossOver(problem, tournament_size=4),
                       GaussianMutation(problem, stdev=0.01)]
        )
        
        logger = PopulationLogger(ga)

        ga.run(num_generations=self.iterations)

        values = ga.status['best'].values.tolist()
        fitness = ga.status['best'].evals.item()
        
        return values, fitness

    def fitness_func(self, params):
        #"""
        for param in range(len(params)):
            evaluate = params[param]
            lwr = self.bounds[0][param]
            upr = self.bounds[1][param]
            if evaluate <= lwr or evaluate >= upr:
                return torch.tensor(1e12, dtype=torch.float32)
        #"""
        ODE_local = ODE_sim_t2(
            self.chain_l,
            self.init_ch,
            self.rate_eqn,
            self.x, 
            self.y
        )
        norm_pops, sim_time = ODE_local.ODE_sim(params)

        total_mse = 0.0
        num_pops = len(norm_pops)

        comp_data = self.y

        for chain in range(num_pops):
            # Create interpolation function for this chain's simulation data
            interp_func = interp1d(
                                   sim_time, 
                                   norm_pops[chain], 
                                   bounds_error=False, 
                                   fill_value='extrapolate'
                                   )
            
            # Get simulated values at experimental time points
            sim_values = torch.tensor(
                                      interp_func(self.x),
                                      dtype=torch.float32
                                      )
            experimental = comp_data[chain].detach().clone()

            mse = torch.mean((sim_values - experimental) ** 2)

            total_mse += mse

        avg_mse = total_mse / num_pops
        return avg_mse
    
class PopulationLogger(Logger):
    def __call__(self, ga):
        
        print(f"Iteration {ga['iter']}")

        values = (ga['best'].values).tolist()
        print("Parameters:\n", values)

        fitness = (ga['best'].evals).item()
        print("Fitness:\n", fitness)
        print("\n")

def write_csv(random_seed, MSE, fit_params, trajectory=0):
    row = {"trajectory": trajectory, 
           "random seed": random_seed,
           "fitness": MSE,
           "parameters": fit_params}
    
    df = pd.DataFrame([row])
    df.to_csv(f"GA_traj_{trajectory}.csv", index=False)

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
