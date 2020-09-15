import numpy as np
import cma
from .wrapper_scaling import wrapper_scaling
import random
from .func7 import func7

def fit_cma7(log_price):
    init_limits = [
        (4, 6), 
        (0, 5),                
        (1, 3),                     
    ]
    non_lin_vals = [random.uniform(a[0], a[1]) for a in init_limits]
    tc_0 = non_lin_vals[0]
    beta_0 = non_lin_vals[1]
    omega_0 = non_lin_vals[2]
    A = 1
    B = -1
    C1 = 1
    C2 = 1
    seed = np.array([tc_0, beta_0, omega_0, A, B, C1, C2])
    
        
    opti_sol = cma.fmin(lambda x: func7(x[:3],x[3],x[4],x[5],x[6],log_price),sigma0=2,x0=seed)
    tc, beta, omega = wrapper_scaling(opti_sol[0][:3],log_price)
    normed_residual = func7(opti_sol[0][:3],opti_sol[0][3],opti_sol[0][4],opti_sol[0][5],opti_sol[0][6],log_price)/len(log_price)
    sol = {'tc':tc, 'beta':beta, 'omega':omega, 'A':opti_sol[0][3], 'B':opti_sol[0][4], 'C1':opti_sol[0][5], 'C2':opti_sol[0][6], 'Res':normed_residual}
    return sol
