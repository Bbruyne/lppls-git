from .data import fetch_data
from .signal import LPPL_confidence_signal
import datetime
import time
import pandas as pd
if __name__ == '__main__':

    start_date = datetime.datetime(2016, 1, 1)
    end_date = datetime.datetime(2020, 8, 30)
    ticker = 'sp500'
    source = 'fred'

    data = fetch_data(start_date=start_date, end_date=end_date, ticker=ticker, source=source)
    log_price = data['log_price']
    dates = data['dates']

    time_range = range(900,1200,2)
    time_windows=range(300,700,5)
    t0 = time.time()
    sig=LPPL_confidence_signal(log_price=log_price, time=time_range, time_windows=time_windows)
    t1 = time.time()
    sig.to_csv('sig.csv')
    a=pd.DataFrame([t1-t0])
    a.to_csv('time.csv')
