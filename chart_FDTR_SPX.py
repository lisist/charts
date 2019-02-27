import pandas_datareader as web
import pandas as pd
from fed import *
import datetime as dt
import matplotlib.pyplot as plt
from us_econ import us_recession

start = dt.date(1990,1,1)
end = dt.date(2019,2,1)


fed_fund = fdtr(start,end)
spx = web.DataReader('^GSPC','yahoo',start,end)
spx_close = spx['Adj Close']
recession_period = us_recession(start,end)


fig, ax1 = plt.subplots()
ax1.plot(fed_fund,color="black")
ax2 = ax1.twinx()
ax2.plot(spx_close)

range_list =[]
for i,j in recession_period.iterrows():
    range_list.append((j['start'],j['end']))

for (start,end) in range_list:
    plt.axvspan(start,end,color='grey',alpha=0.3)

plt.show()
