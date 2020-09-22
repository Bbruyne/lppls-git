import numpy as np
from .wrapper_scaling import wrapper_scaling

def func(x, log_price):
    '''
    finds the least square difference
    '''
    tc, beta, omega = wrapper_scaling(x,log_price)
    fit = fit_ABC(beta, omega, tc, log_price)

    t = np.arange(len(log_price))
    return np.sum((LPPL(t=t, A=fit['A'], B=fit['B'], C1=fit['C1'], C2=fit['C2'], beta=beta, omega=omega, tc=tc)-log_price)**2)

def LPPL(t, A, B, C1, C2, beta, omega, tc):
    return A + B*_f(tc, t, beta) + C1*_g(tc, t, beta, omega) + C2*_h(tc, t, beta, omega)
def _f(tc, t, beta):
    return (abs(tc-t))**beta
def _g(tc, t, beta, omega):
    return _f(tc, t, beta)*np.cos(omega*np.log(abs(tc-t)))
def _h(tc, t, beta, omega):
    return _f(tc, t, beta)*np.sin(omega*np.log(abs(tc-t)))

def fit_ABC(beta, omega, tc, log_price):
    
    one_col = np.ones(len(log_price))

    t = np.arange(1,len(log_price)+1)
    f_col = _f(tc=tc, t=t, beta=beta)
    g_col = _g(tc=tc, t=t, beta=beta, omega=omega)
    h_col = _h(tc=tc, t=t, beta=beta, omega=omega)

    X = np.array([one_col,f_col,g_col,h_col]).T
    
    A, B, C1, C2 = np.linalg.lstsq(X, log_price,rcond=None)[0]
    return {"A":A, "B":B, "C1":C1, "C2":C2}