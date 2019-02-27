import pandas_datareader as web
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

start = dt.datetime(2018,1,1)
end = dt.datetime.now()

fb = web.DataReader('FB','yahoo',start,end)
amzn =  web.DataReader('AMZN','yahoo',start,end)
nvda =  web.DataReader('NVDA','yahoo',start,end)
nflx =  web.DataReader('NFLX','yahoo',start,end)
googl =  web.DataReader('GOOGL','yahoo',start,end)

fb = fb['Adj Close']
amzn = amzn['Adj Close']
nvda = nvda['Adj Close']
nflx = nflx['Adj Close']
googl = googl['Adj Close']

fb = fb/fb[0]
amzn = amzn/amzn[0]
nvda = nvda/nvda[0]
nflx = nflx/nflx[0]
googl = googl/googl[0]

print("Facebook : " ,fb[fb.__len__()-1])
print("AMAZON   : " ,amzn[amzn.__len__()-1])
print("NVDIA    : " ,nvda[nvda.__len__()-1])
print("NetFLIX  : " ,nflx[nflx.__len__()-1])
print("Google   : " ,googl[googl.__len__()-1])

fig, ax1 = plt.subplots()
ax1.plot(fb,color="black", label="Facebook")
ax1.plot(amzn, label = "Amazon")
ax1.plot(nvda,":", label = "NVDA")
ax1.plot(nflx, label = "NetFlix")
ax1.plot(googl, '--', label = "Google")

plt.legend()
plt.show()

