import numpy as np
from .wrapper_scaling import wrapper_scaling

def func7(x, A, B, C1, C2, log_price):
    '''
    finds the least square difference
    '''
    tc, beta, omega = wrapper_scaling(x,log_price)
    t = np.arange(len(log_price))

    return np.sum((LPPL(t=t, A=A, B=B, C1=C1, C2=C2, beta=beta, omega=omega, tc=tc)-log_price)**2)


def LPPL(t, A, B, C1, C2, beta, omega, tc):
    return A + B*_f(tc, t, beta) + C1*_g(tc, t, beta, omega) + C2*_h(tc, t, beta, omega)
def _f(tc, t, beta):
    return (abs(tc-t))**beta
def _g(tc, t, beta, omega):
    return _f(tc, t, beta)*np.cos(omega*np.log(abs(tc-t)+0.001))
def _h(tc, t, beta, omega):
    return _f(tc, t, beta)*np.sin(omega*np.log(abs(tc-t)+0.001))
