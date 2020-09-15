import pandas as pd
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import numpy as np

def plot_lppls(log_price,sig,dates):

    df=pd.concat([pd.DataFrame(log_price), sig], axis=1, sort=False).set_index(dates)
    df.columns= ['log_price','sig']


    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)

    par2 = host.twinx()

    offset = 0
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))

    par2.axis["right"].toggle(all=True)


    host.set_xlabel("time")
    host.set_ylabel("price")
    par2.set_ylabel("lppls")

    p1, = host.plot(np.exp(df['log_price']), label="price")
    p3, = par2.plot(df['sig'].dropna(), label="lppls")


    host.legend()

    host.axis["left"].label.set_color(p1.get_color())
    par2.axis["right"].label.set_color(p3.get_color())
    plt.draw()
    plt.savefig('C:\\Users\\b.debruyne\\bubble\\lppls.eps')
    plt.show()
    return True