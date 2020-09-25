import numpy as np

def wrapper_scaling(x,log_price):
    tc_s = x[0]
    beta_s = x[1]
    omega_s = x[2]
    return [len(log_price) + len(log_price)*0.2*(np.cos(np.pi*tc_s/10)+1)/2, 1-np.cos(np.pi*beta_s/10), 1 + 49*(1-np.cos(np.pi*omega_s/10))/2]