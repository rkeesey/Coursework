import torch
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def tens_func(x, a, b, c):
    return a * torch.exp(-b * x) + c

def np_func(x, a, b, c):
    return a * np.exp(-b * x) + c

# generate raw dataset
def exp_data(a_i, b_i, c_i):
    xdata = torch.linspace(0, 4, 50)
    y = tens_func(xdata, a_i, b_i, c_i)
    torch.manual_seed(42)
    y_noise = 0.2 * torch.rand(len(xdata))
    ydata = y + y_noise
    return xdata, ydata

def scipy_cf(a_i, b_i, c_i):
    xdata, ydata = exp_data(a_i, b_i, c_i)
    xdata = xdata.detach().numpy()
    ydata = ydata.detach().numpy()
    fit_params, pcov = curve_fit(np_func, xdata, ydata)
    perr = np.sqrt(np.diag(pcov))
    return fit_params, pcov, perr

def torch_cf(a_i, b_i, c_i):
    xdata, ydata = exp_data(a_i, b_i, c_i)
    xdata_np = xdata.detach().numpy()
    ydata_np = ydata.detach().numpy()
    
    # Now compute Hessian at the SciPy-optimized parameters
    params_optimized = torch.tensor(fit_params, dtype=torch.float32, requires_grad=True)
    
    def loss_fn(params):
        a, b, c = params
        ysim = tens_func(xdata, a, b, c)
        return torch.sum((ysim - ydata) ** 2)
    
    # Compute Hessian at the optimized parameters
    hessian = torch.autograd.functional.hessian(loss_fn, params_optimized)
    
    # Scale by residual variance (same as SciPy)
    n = len(ydata)
    p = len(params_optimized)
    
    with torch.no_grad():
        ysim_opt = tens_func(xdata, *params_optimized)
        residual_variance = torch.sum((ysim_opt - ydata) ** 2) / (n - p)
    
    covariance = torch.linalg.inv(hessian) * (2 * residual_variance)
    
    return covariance.detach().numpy()
    

if __name__=='__main__':
    
    a_i = torch.tensor(2.5, requires_grad=True)
    b_i = torch.tensor(1.3, requires_grad=True)
    c_i = torch.tensor(0.5, requires_grad=True)

    fit_params, pcov, perr = scipy_cf(a_i, b_i, c_i)
    print(fit_params, '\n')
    print(pcov, '\n')
    
    cov = torch_cf(a_i, b_i, c_i)
    print(cov)
    