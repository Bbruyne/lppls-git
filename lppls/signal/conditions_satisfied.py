import numpy as np

def conditions_satisfied(beta, omega, tc, A, B, C1, C2, dt):
    c1 = 0.01 < beta < 1.2
    c2 = 2 < np.abs(omega) < 25
    #c3 = 0.95*dt < tc < 1.11*dt
    #print('tc in interval: ' + str(c3))
    C = np.sqrt(C1**2+C2**2) 
    #c3 = abs(C) < 1
    # print('Amplitude of log-oscillations: ' + str(c3))
    c4 = 2.5 < np.abs(omega)/2*np.log(abs(tc/(tc-dt)))
    #print('number oscillation: ' + str(c4))
    c5 = 0 < beta * abs(B) / (omega * abs(C))
    print('damping: ' + str(c5) )
    # return c1 and c2 and c3 and c4 and c5 
    return c1 and c2 and c4 and c5 