import pandas_datareader as web
import pandas as pd
import datetime as dt
from data_modifier import *
import matplotlib.pyplot as plt
import hub as hub
from us_econ import *
import os

def get_spx(start,end):
    df = web.DataReader('^GSPC','yahoo',start,end)

    df.to_csv("chart_stock_to_bond_data/spx.csv")
    return(df)

def get_ust10y(start,end):
    df = web.DataReader('DGS10','fred',start,end)

    df.to_csv("chart_stock_to_bond_data/ust10y.csv")
    return(df)

start = dt.datetime(1990,1,1)
end = dt.datetime(2019,2,25)

if not os.path.exists('chart_stock_to_bond_data'):
    os.makedirs('chart_stock_to_bond_data')
    print('have made dirs')

if not os.path.isfile('chart_stock_to_bond_data/spx.csv'):
    get_spx(start, end)
    print('spx.csv file created')

if not os.path.isfile('chart_stock_to_bond_data/ust10y.csv'):
    get_ust10y(start,end)
    print('ust10y file created')


### 기존 CSV 파일에서 Data 받기
spx = pd.read_csv('chart_stock_to_bond_data/spx.csv',parse_dates=True, index_col=0)
spx.drop(['High','Low','Volume','Open','Close'],axis=1,inplace=True)
ust10 = pd.read_csv('chart_stock_to_bond_data/ust10y.csv',parse_dates=True,index_col=0)


### 파일 업데이트 여부 체크
first_date = ust10.index[0]
length = ust10.index.__len__()
last_date = ust10.index[length-1]

if(start < first_date):
    df = web.DataReader('DGS10','fred',start,first_date)



ust10.index.names=['Date']


merged = pd.merge(spx,ust10,how='outer', on='Date')
merged.dropna(inplace=True)


merged  = merged.iloc[merged.reset_index().groupby(merged.index.to_period('M'))['Date'].idxmax()]
merged = merged.rename(columns={'Adj Close':'Spx','DGS10':'UST10'})


spx_index = pd.DataFrame((merged['Spx']/merged['Spx'][0]).values,index = merged.index,columns=['spx index']) ## spx indexation
ust_index_return = ((merged['UST10']-merged['UST10'].shift(1))*8/100+merged['UST10']/12/100)



a = 1
k = []

for i in ust_index_return[1:]:
    a = a*(1+i)
    k.append(a)


ism = ism_pmi(start,end)



ust_index_return.dropna(inplace= True)

k = pd.DataFrame(k,index=ust_index_return.index,columns=['ust10y'])
stock_to_bond = (spx_index['spx index']/k['ust10y'])
# stock_to_bond = yoy(stock_to_bond,freq='m') ## YoY
print(stock_to_bond.head())
stock_to_bond = (stock_to_bond/stock_to_bond.shift(6))-1
stock_to_bond = stock_to_bond.rolling(9).mean()



fig, ax1 = plt.subplots()
lns1 = ax1.plot(stock_to_bond, color= 'black',label = 'stock_to_bond 6m chg% (LHS)')
ax1.set_ylim([-0.35,0.3])
ax2 = ax1.twinx()
lns2 = ax2.plot(ism, '--',color= 'grey',label = 'ISM Manufacturing (RHS)')
ax2.set_ylim([30,70])
lns = lns1+lns2
labs = [l.get_label() for l in lns]
plt.legend(lns,labs,loc=0)
plt.title('Stock to bond ratio and ISM Manufacturing PMI')

start = start.date()
end = end.date()

recession_period = us_recession(start,end)
range_list =[]
for i,j in recession_period.iterrows():
    range_list.append((j['start'],j['end']))

for (start,end) in range_list:
    plt.axvspan(start,end,color='grey',alpha=0.3)

plt.show()
