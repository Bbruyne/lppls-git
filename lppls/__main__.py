from .data import fetch_data
from .signal import LPPL_confidence_signal
import datetime
import pandas as pd
if __name__ == '__main__':

    # import price data (take a sufficiently long history)
    start_date = datetime.datetime(2016, 1, 1)
    end_date = datetime.datetime(2020, 8, 30)
    ticker = 'sp500'
    source = 'fred'

    data = fetch_data(start_date=start_date, end_date=end_date, ticker=ticker, source=source)
    log_price = data['log_price']
    dates = data['dates']

    # define the time range for when to compute the lppls signal
    time_range = range(900,1200,2)
    # define the number of time windows to fit for every day in the time range
    time_windows=range(300,700,5)
    # compute the signal
    sig=LPPL_confidence_signal(log_price=log_price, time=time_range, time_windows=time_windows)

    # save the signal in csv
    sig.to_csv('sig.csv')
