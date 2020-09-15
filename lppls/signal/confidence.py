from ..optimization import fit_cma7, get_dt_max
from .conditions_satisfied import conditions_satisfied
import numpy as np

def LPPL_confidence(log_price, time_windows):
    
    sols = []
    for dt in time_windows:
        print('dt: ' + str(dt) )
        sols.append(fit_cma7(log_price[-dt:]))

    dt_max = get_dt_max(sols, time_windows)
    print('dt_max:' + str(dt_max))
    LPPL_confidences = []
    total_returns = []
    for dt in time_windows:
        sol = sols.pop(0)
        if dt <= dt_max: 
            if conditions_satisfied(beta=sol['beta'], omega=sol['omega'], tc=sol['tc'], A=sol['A'], B=sol['B'], C1=sol['C1'], C2=sol['C2'], dt=dt):
                LPPL_confidences.append(1)
                total_returns.append(_total_return(log_price[-dt:]))
            else:
                LPPL_confidences.append(0)
    print(LPPL_confidences)
    return np.mean(LPPL_confidences)*np.sign(np.median(total_returns))

def _total_return(log_price):
    price = np.array(np.exp(log_price))
    return (price[-1]-price[0])/price[0]