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
    tcs = []
    omegas = []
    betas = []
    As = []
    Bs = []
    C1s = []
    C2s = []
    for dt in time_windows:
        sol = sols.pop(0)
        if dt <= dt_max: 
            if conditions_satisfied(beta=sol['beta'], omega=sol['omega'], tc=sol['tc'], A=sol['A'], B=sol['B'], C1=sol['C1'], C2=sol['C2'], dt=dt):
                LPPL_confidences.append(1)
                total_returns.append(_total_return(log_price[-dt:]))
                tcs.append(sol['tc'])
                omegas.append(sol['omega'])
                betas.append(sol['beta'])
                As.append(sol['A'])
                Bs.append(sol['B'])
                C1s.append(sol['C1'])
                C2s.append(sol['C2'])
            else:
                LPPL_confidences.append(0)
    conf = np.mean(LPPL_confidences)*np.sign(np.median(total_returns))
    res = {'conf': conf,
     'tc_avg':np.mean(tcs), 'tc_std':np.std(tcs),
     'omega_avg':np.mean(omegas), 'omega_std':np.std(omegas),
     'beta_avg':np.mean(betas), 'beta_std':np.std(betas),
     'A_avg':np.mean(As), 'A_std':np.std(As),
     'B_avg':np.mean(Bs), 'B_std':np.std(Bs),
     'C1_avg':np.mean(C1s), 'C1_std':np.std(C1s),
     'C2_avg':np.mean(C2s), 'C2_std':np.std(C2s),
    }
    return res

def _total_return(log_price):
    price = np.array(np.exp(log_price))
    return (price[-1]-price[0])/price[0]