import numpy as np
from .wrapper_scaling import wrapper_scaling
import random
from .func import func, fit_ABC

def fit_genetic(log_price):
    init_limits = [
    (0, 10), 
    (0, 10),                
    (0, 10),                     
]
    pop_num = 1000
    elite_num = int(pop_num*0.15)
    cross_num = int(pop_num*0.20)
    mut_num = int(pop_num*0.20)
    new_num = pop_num - elite_num - mut_num
    gen_num = 100
    avg_elite_value = np.inf
    for gen in range(gen_num):
        if gen == 0:
            pop = _new(new_num=pop_num,init_limits=init_limits)
        else:
            pop = elite.copy()
            pop.extend(_crossover(elite=elite,elite_value=elite_value,cross_num=cross_num))
            pop.extend(_mutation(elite=elite,elite_value=elite_value,mut_num=mut_num,init_limits=init_limits))
            pop.extend(_new(new_num=new_num,init_limits=init_limits))

        pop_eval = {func(x=chro, log_price=log_price):chro for chro in pop}

        elite_value = sorted(pop_eval)[:elite_num]
        elite = [pop_eval[value] for value in elite_value]
        print('Residual :' + str(elite_value[0]))
        if (avg_elite_value - np.mean(elite_value)) < 0.0001:
            break
        else:
            avg_elite_value = np.mean(elite_value)

    tc, beta, omega = wrapper_scaling(pop_eval[elite_value[0]],log_price)
    normed_residual = func(pop_eval[elite_value[0]],log_price)/len(log_price)

    fit = fit_ABC(beta, omega, tc, log_price)
    sol = {'tc':tc, 'beta':beta, 'omega':omega, 'A':fit['A'], 'B':fit['B'], 'C1':fit['C1'], 'C2':fit['C2'], 'Res':normed_residual}
    return sol


def _crossover(elite,elite_value,cross_num):
    pop_temp = []
    for _ in range(cross_num):
        chro = random.choices(elite,weights=1/np.array(elite_value))[0]
        chro_mate = random.choices(elite,weights=1/np.array(elite_value))[0]
        pop_temp.append([chro[0], chro[1], chro_mate[2]])
    return pop_temp

def _mutation(elite,elite_value,mut_num,init_limits):
    pop_temp = []
    for _ in range(mut_num):
        chro = random.choices(elite,weights=1/np.array(elite_value))[0]
        gene = random.randrange(len(chro))
        chro_mutated = chro.copy()
        chro_mutated[gene] = random.uniform(init_limits[gene][0], init_limits[gene][1]) 
        pop_temp.append(chro_mutated)
    return pop_temp

def _new(new_num,init_limits):
    pop_temp = []
    for _ in range(new_num):
        pop_temp.append([random.uniform(a[0], a[1]) for a in init_limits])
    return pop_temp
