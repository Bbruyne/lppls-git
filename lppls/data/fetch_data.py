from pandas_datareader import data
import numpy as np
import pandas as pd

def fetch_data(start_date, end_date, ticker, source):
    price = data.DataReader([ticker], source, start_date, end_date).ffill().bfill()
    log_price = np.log(price).values.flatten()
    dates = price.index
    return {'dates':dates, 'log_price':log_price}