from ..optimization import fit_cma7, get_dt_max
from .conditions_satisfied import conditions_satisfied
import numpy as np

def LPPL_confidence(log_price, time_windows):
    
    sols = []
    for dt in time_windows:
        sols.append(fit_cma7(log_price[-dt:]))

    dt_max = get_dt_max(sols, time_windows)
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
                tcs.append(dt - sol['tc'])
                omegas.append(sol['omega'])
                betas.append(sol['beta'])
                As.append(sol['A'])
                Bs.append(sol['B'])
                C1s.append(sol['C1'])
                C2s.append(sol['C2'])
            else:
                LPPL_confidences.append(0)
    if total_returns:
        conf = np.mean(LPPL_confidences)*np.sign(np.median(total_returns))
        res = {'conf':conf,'tc_avg':np.mean(tcs), 'tc_std':np.std(tcs),  'tc_min':np.min(tcs), 'tc_max':np.max(tcs), 'tc_median':np.median(tcs), 'tc_q1':np.percentile(tcs,25), 'tc_q3':np.percentile(tcs,75),
        'omega_avg':np.mean(omegas), 'omega_std':np.std(omegas), 'omega_min':np.min(omegas), 'omega_max':np.max(omegas), 'omega_median':np.median(omegas), 'omega_q1':np.percentile(omegas,25), 'omega_q3':np.percentile(omegas,75)}
  #      res = {'conf': conf,
  #      'tc_avg':np.mean(tcs), 'tc_std':np.std(tcs), 'tc_min':np.min(tcs), 'tc_max':np.max(tcs), 'tc_median':np.median(tcs), 'tc_q1':np.percentile(tcs,25), 'tc_q3':np.percentile(tcs,75),
  #      'omega_avg':np.mean(omegas), 'omega_std':np.std(omegas), 'omega_min':np.min(omegas), 'omega_max':np.max(omegas), 'omega_median':np.median(omegas), 'omega_q1':np.percentile(omegas,25), 'omega_q3':np.percentile(omegas,75),
  #      'beta_avg':np.mean(betas), 'beta_std':np.std(betas),'beta_min':np.min(betas), 'beta_max':np.max(betas), 'beta_median':np.median(betas), 'beta_q1':np.percentile(betas,25), 'beta_q3':np.percentile(betas,75),
  #      'A_avg':np.mean(As), 'A_std':np.std(As), 'A_min':np.min(As), 'A_max':np.max(As), 'A_median':np.median(As), 'A_q1':np.percentile(As,25), 'A_q3':np.percentile(As,75),
  #      'B_avg':np.mean(Bs), 'B_std':np.std(Bs), 'B_min':np.min(Bs), 'B_max':np.max(Bs), 'B_median':np.median(Bs), 'B_q1':np.percentile(Bs,25), 'B_q3':np.percentile(Bs,75),
  #      'C1_avg':np.mean(C1s), 'C1_std':np.std(C1s),'C1_min':np.min(C1s), 'C1_max':np.max(C1s), 'C1_median':np.median(C1s), 'C1_q1':np.percentile(C1s,25), 'C1_q3':np.percentile(C1s,75),
  #      'C2_avg':np.mean(C2s), 'C2_std':np.std(C2s),'C2_min':np.min(C2s), 'C2_max':np.max(C2s), 'C2_median':np.median(C2s), 'C2_q1':np.percentile(C2s,25), 'C2_q3':np.percentile(C2s,75)
  #      }
    else:
        res = {'conf':0,'tc_avg': 0, 'tc_std':0,  'tc_min':0, 'tc_max':0, 'tc_median':0, 'tc_q1':0, 'tc_q3':0,
        'omega_avg':0, 'omega_std':0, 'omega_min':0, 'omega_max':0, 'omega_median':0, 'omega_q1':0, 'omega_q3':0}
  #      res = {'conf': 0,
  #      'tc_avg': 0, 'tc_std': 0, 'tc_min': 0, 'tc_max':0, 'tc_median':0, 'tc_q1':0, 'tc_q3':0,
  #      'omega_avg':0, 'omega_std':0, 'omega_min':0, 'omega_max':0, 'omega_median':0, 'omega_q1':0, 'omega_q3':0,
  #      'beta_avg':0, 'beta_std':0,'beta_min':0, 'beta_max':0, 'beta_median':0, 'beta_q1':0, 'beta_q3':0,
  #      'A_avg':0, 'A_std':0, 'A_min':0, 'A_max':0, 'A_median':0, 'A_q1':0, 'A_q3':0,
  #      'B_avg':0, 'B_std':0, 'B_min':0, 'B_max':0, 'B_median':0, 'B_q1':0, 'B_q3':0,
  #      'C1_avg':0, 'C1_std':0,'C1_min':0, 'C1_max':0, 'C1_median':0, 'C1_q1':0, 'C1_q3':0,
  #      'C2_avg':0, 'C2_std':0,'C2_min':0, 'C2_max':0, 'C2_median':0, 'C2_q1':0, 'C2_q3':0
  #      }
    return res

def _total_return(log_price):
    price = np.array(np.exp(log_price))
    return (price[-1]-price[0])/price[0]