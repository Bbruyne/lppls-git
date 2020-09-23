from multiprocessing import Process, Queue
import numpy as np
from .confidence import LPPL_confidence

class Worker(Process):

    def __init__(self, idx, queue_in, queue_out):
        super(Process, self).__init__()
        self.idx = idx
        self.queue_in = queue_in
        self.queue_out = queue_out

    def run(self):
        # initialize seed
        np.random.seed(self.idx)
        
        while True:
            # get job from queue
            job_params = self.queue_in.get()
            
            if job_params is None:
                break
            
            log_price = job_params['log_price']
            time_windows = job_params['time_windows']
            print('Worker [' + str(self.idx) + '] has taken day #' + str(len(log_price)) + ' from queue')
            sig = LPPL_confidence(log_price=log_price, time_windows=time_windows,worker_id=self.idx)
            self.queue_out.put({len(log_price): sig})
            print('Worker [' + str(self.idx) + '] has put day #' + str(len(log_price)) + ' on queue')
        
        return