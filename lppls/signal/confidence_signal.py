from multiprocessing import Process, Queue
from .workers import Worker 
import pandas as pd
import time as timeSL

def LPPL_confidence_signal(log_price, time, time_windows):
    # init queues
    q_in = Queue()
    q_out = Queue()

    # parameters
    n_jobs = 32

    # create and start jobs
    jobs = []
    for i in range(n_jobs):
        p = Worker(i, q_in, q_out)
        jobs.append(p)
        p.start()

    # pass jobs
    for t2 in time:
        q_in.put({'log_price':log_price[:t2],'time_windows':time_windows})

    # send termination signal
    for i in range(n_jobs):
        q_in.put(None)

    # wait for answers
    #for j in jobs:
    #    j.join()

    d = {}
    count = 0
    while count < n_jobs:
        if not q_out.empty():
            item = q_out.get()
            if item is None:
                count += 1
                print('Number of workers done: ' + str(count))
            else:
                d.update(item)
        else:
            timeSL.sleep(2)

    lists = sorted(d.items()) # sorted by key, return a list of tuples
    time, LPPL_confidence_ts = zip(*lists) # unpack a list of pairs into two tuples
    
    return pd.DataFrame(LPPL_confidence_ts,index=time).fillna(0)
