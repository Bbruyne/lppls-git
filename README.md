# lppls-git
Log Periodic Power Law Singularity model for financial bubble predictions. 
We use the Log Periodic Power Law Singularity model to build a time signal that predicts the existence of a financial bubble in the stock market.

This work is based on the research done at the Financial Crisis Observatory at ETH Zurich.

To use this code, make sure you have installed: `pandas, datetime, numpy, multiprocessing, time, sklearn, random, cma, pandas_datareader`.

To execute the code, define the stock index, time range, and number of fitting windows for which you want the signal to be computed in the `__main__.py` and then run `python -m lppls`. If you wish to change the qualifying conditions for the fits, go to `signal/conditions_satisfied.csv` and modify accordingly.

The output of the code is stored in `sig.csv`. It can be visualised with the python notebook `visulalise.ipynb`.

