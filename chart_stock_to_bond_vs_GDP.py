import pandas_datareader as web
import pandas as pd
import datetime as dt
from data_modifier import *
import matplotlib.pyplot as plt
from us_econ import *
import os
import time

def get_spx(start,end):
    df = web.DataReader('^GSPC','yahoo',start,end)

    df.to_csv("data/spx.csv")
    return(df)

def get_ust10y(start,end):
    df = web.DataReader('DGS10','fred',start,end)

    df.to_csv("data/ust10.csv")
    return(df)

start = dt.datetime(1980,1,1)
end = dt.datetime(2019,2,9)

if not os.path.exists('data'):
    os.makedirs('data')
    print('have made dirs')

if not os.path.isfile('data/spx.csv'):
    get_spx(start, end)
    print('spx.csv file created')

if not os.path.isfile('data/ust10.csv'):
    get_ust10y(start,end)
    print('ust10y file created')

if not os.path.isfile('data/rgdp.csv'):
    df = web.DataReader('GDPC1', 'fred', start, end)
    df.to_csv('data/rgdp.csv')
    print('real gdp file created')


### 기존 CSV 파일에서 Data 받기
spx = pd.read_csv('data/spx.csv',parse_dates=True, index_col=0)
ust10 = pd.read_csv('data/ust10.csv',parse_dates=True,index_col=0)
rgdp = pd.read_csv('data/rgdp.csv',parse_dates=True,index_col=0)

# ### 파일 업데이트 여부 체크
first_date = ust10.index[0]
length = ust10.index.__len__()
last_date = ust10.index[length-1]

# first_date = first_date.to_pydatetime()
# last_date = last_date.to_pydatetime()

if(start < first_date-dt.timedelta(days=1)):
    df_ust = web.DataReader('DGS10','fred',start,first_date-dt.timedelta(days=1))
    ust10 = pd.concat([df_ust,ust10])
    df_spx = web.DataReader('^GSPC','yahoo',start,first_date-dt.timedelta(days=1))
    spx = pd.concat([df_spx,spx])
    df_rgdp = web.DataReader('GDPC1', 'fred', start,first_date-dt.timedelta(days=1))
    rgdp = pd.concat([df_rgdp, rgdp])
    ust10.to_csv('data/ust10.csv')
    spx.to_csv('data/spx.csv')
    rgdp.to_csv('data/rgdp.csv')
    print('prior dates updated')

# print(last_date+dt.timedelta(days=1))
if(end > (last_date+dt.timedelta(days=2))):
    df_ust = web.DataReader('DGS10','fred',last_date+dt.timedelta(days=1),end)
    ust10 = pd.concat([ust10,df_ust])
    df_spx = web.DataReader('^GSPC','yahoo',last_date+dt.timedelta(days=1),end)
    spx = pd.concat([spx,df_spx],sort=False)
    df_rgdp = web.DataReader('GDPC1', 'fred', last_date + dt.timedelta(days=1), end)
    rgdp = pd.concat([rgdp, df_rgdp], sort=False)
    ust10.to_csv('data/ust10.csv')
    spx.to_csv('data/spx.csv')
    rgdp = web.DataReader('^GSPC', 'yahoo', last_date + dt.timedelta(days=1), end)
    spx = pd.concat([spx, df_spx], sort=False)
    print('lates dates updated')

#### Data를 요구 date에 맞게 조작

spx.drop(['High','Low','Volume','Open','Close'],axis=1,inplace=True)
ust10.index.names=['Date']  ## merge를 위해서 ust의 index를 Date로 바꿈

spx = spx[(spx.index >= start) & (spx.index <= end)]
ust10 = ust10[(ust10.index >= start) & (ust10.index <= end)]



##### Data merge and convert it to monthly basis

merged = pd.merge(spx,ust10,how='outer', on='Date')
merged.dropna(inplace=True)

merged  = merged.iloc[merged.reset_index().groupby(merged.index.to_period('M'))['Date'].idxmax()]
merged = merged.rename(columns={'Adj Close':'Spx','DGS10':'UST10'})


###### calculate the return index

spx_index = pd.DataFrame((merged['Spx']/merged['Spx'][0]).values,index = merged.index,columns=['spx index']) ## spx indexation
ust_index_return = ((merged['UST10']-merged['UST10'].shift(1))*8/100+merged['UST10']/12/100)

a = 1
k = []

for i in ust_index_return[1:]:
    a = a*(1+i)
    k.append(a)


##### get GDP file

rgdp = yoy(rgdp,freq='q')
ust_index_return.dropna(inplace= True)

k = pd.DataFrame(k,index=ust_index_return.index,columns=['ust10y'])
stock_to_bond = (spx_index['spx index']/k['ust10y'])
stock_to_bond = yoy(stock_to_bond,freq='m')


#### plotting

fig, ax1 = plt.subplots()
lns1 = ax1.plot(stock_to_bond, color= 'black',label = 'stock_to_bond (LHS)')
ax2 = ax1.twinx()
lns2 = ax2.plot(rgdp, '--',color= 'grey',label = 'Real GDP YoY% (RHS)')
lns = lns1+lns2
labs = [l.get_label() for l in lns]
plt.legend(lns,labs,loc=0)
plt.title('Stock to bond ratio and US real GDP YoY%')


plt.show()
