import torch
from evotorch import Problem, Solution, SolutionBatch
from evotorch.algorithms import GeneticAlgorithm
from evotorch.operators import TwoPointCrossOver
from evotorch.operators import GaussianMutation
import matplotlib.pyplot as plt
from scipy import stats

class init_Problem(Problem):
    def __init__(self, param_num, init_bnds, init_params, fitness_func):
        super().__init__(
            objective_sense="min",
            solution_length=param_num,
            initial_bounds=init_bnds,
            dtype=torch.float32
        )  

        self.fitness_func = fitness_func
        self.init_params = init_params
        self.initial_bounds = init_bnds

    def _evaluate_batch(self, solutions):
        for sol in solutions:
            mse = self.fitness_func(sol.values)
            sol.set_evals(mse)
        
    def _fill(self, values: torch.Tensor): # values: (no. of solns, soln length)
        """ initialize starting generation with initial parameter values"""
        values[0] = torch.tensor(self.init_params)
        values[1:] = torch.rand(values.shape[0]-1, values.shape[1]) * self.initial_bounds[1]
        self._initialized = True


class GA_fit:

    def __init__(self, x, y):
        self.x = x
        self.y = y # reference data

    def run_GA(self, init_params, bounds):

        pop_size = 10

        problem = init_Problem(len(init_params), bounds, init_params, fitness_func=self.fitness)

        ga = GeneticAlgorithm(
            problem, 
            popsize=pop_size,
            operators=[TwoPointCrossOver(problem, tournament_size=4),
                       GaussianMutation(problem, stdev=0.1)]
        )

        ga.run(10)
        print("best individual: ", float(ga.status["best"][0]), float(ga.status["best"][1])) # best fitness for an individual and the population
        print("best fitness: ", ga.status["pop_best_eval"])
        print("mean fitness: ", ga.status["mean_eval"]) # average fitness of the best population
        return ga.status["best"]

    def model(self, params):
        a = params[0]
        b = params[1]
        return a * torch.sin(b * self.x)
    
    def fitness(self, params):

        y_pred = self.model(params)
        
        mse = torch.mean((y_pred - self.y) ** 2)
        return mse
    
    def plt_result(self, params):

        a = params[0]
        b = params[1]

        fine_x = torch.linspace(0, 2 * torch.pi, 100)
        fit_y = a * torch.sin(b * fine_x)

        fig = plt.figure(figsize=(15, 15))
        fit = plt.plot(fine_x, fit_y, color='red')
        data = plt.scatter(self.x, self.y)
        plt.show()

def gen_ref(noise_std=0.1):

    # reference function: y = A*sin(bx)
    A = 2.0
    b = 3.0

    x_data = torch.linspace(0, 2 * torch.pi, 30)
    y_clean = A * torch.sin(b * x_data)

    noise = torch.randn_like(y_clean) * noise_std
    y_data = y_clean + noise


    return x_data, y_data

def bootstrap(params, bounds, B, c18_0=1, ci=0.95, GA_iter=10):

    a_fits = []
    b_fits = []

    for boot in range(B):
        x_ref, y_ref = gen_ref(noise_std=0.5)
        boot_init = GA_fit(x_ref, y_ref)
        fit_boot = boot_init.run_GA(params, bounds)
        a, b = fit_boot
        a_fits.append(torch.tensor(a))
        b_fits.append(torch.tensor(b))

    tensor_a = torch.stack(a_fits, dim=0)
    tensor_b = torch.stack(b_fits, dim=0)

    lwr, upr = calc_CI([tensor_a, tensor_b], ci)

    return lwr, upr

def calc_CI(param_lists, ci):
    print(param_lists)
    
    lwr_list = []
    upr_list = []
    for param in range(len(param_lists)):
        n = len(param_lists[param])
        mean = torch.mean(param_lists[param])
        std_dev = torch.std(param_lists[param], unbiased=True)
        std_err = std_dev / torch.sqrt(torch.tensor(n, dtype=torch.float32))
        
        degrees_freedom = n - 1
        alpha = 1 - ci
        t_crit = stats.t.ppf(1 - alpha / 2, degrees_freedom)

        margin_err = t_crit * std_err
        lwr = mean - margin_err
        lwr_list.append(lwr)
        upr = mean + margin_err
        upr_list.append(upr)
        
    return lwr_list, upr_list

def main():
    x_ref, y_ref = gen_ref(noise_std=0.5)
    
    test = GA_fit(x_ref, y_ref)
    
    init_params = [1.9810, 3.0174]
    bounds = (0, 5)

    test_fit = test.run_GA(init_params, bounds)
    test.plt_result(test_fit)

    params = [2.0899651050567627, 2.98742413520813]
    B = 10

    lwr, upr = bootstrap(params, bounds, B)
    for i in range(len(lwr)):
        print(f"lower: {lwr[i]:.2f}, upper: {upr[i]:.2f}")

if __name__=='__main__':
    main()