import requests
import datetime
import time
import pandas as pd

start = '2000-01-01'
to = '2021-01-25'
stock = '00881'
if start:
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
else:
    start = datetime.datetime.today()
if to:
    to = datetime.datetime.strptime(to, "%Y-%m-%d")
else:
    to = start - datetime.timedelta(day=1)

stock_url = "https://ws.api.cnyes.com/ws/api/v1/charting/history"
market_url = 'https://marketinfo.api.cnyes.com/mi/api/v1/TWS:{}:STOCK/marginTrading'.format(stock)
invest_url = "https://marketinfo.api.cnyes.com/mi/api/v1/investors/buysell/TWS:{}:STOCK".format(stock)
params={
        'resolution':'D',
        'symbol':'TWS:{}:STOCK'.format(stock),
        'from': int(time.mktime(to.timetuple())),
        'to':int(time.mktime(start.timetuple())),
        'quote':1
}

res1 = requests.get(url=stock_url, params=params).json()['data']

params = {'from':params['from'], 'to':params['to']}
res2 = requests.get(url=market_url, params=params).json()['data']
res3 = requests.get(url=invest_url, params=params).json()['data']
length = min(len(res1['t']), len(res2), len(res3))
res2.reverse()
res3.reverse()
weekday = {0:"Monday", 1:"Tuesday", 2:"Wensday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
data = {
        'open':res1['o'][0:length],
        'close':res1['c'][0:length],
        'high':res1['h'][0:length],
        'low':res1['l'][0:length],
        'margin buy':[line['marginBuy'] for line in res2[0:length]],
        'margin sell':[line['marginSell'] for line in res2[0:length]],
        'margin used ratio':[line['marginUsedPercent'] for line in res2[0:length]],
        'short buy':[line['shortBuy'] for line in res2[0:length]],
        'short sell':[line['shortSell'] for line in res2[0:length]],
        'margin short ratio':[line['shortMarginPercent'] for line in res2[0:length]],
        'dealer net add':[line['dealerNetBuySellVolume'] for line in res3[0:length]],
        'domestic net add':[line['domesticNetBuySellVolume'] for line in res3[0:length]],
        'foreign net add':[line['foreignNetBuySellVolume'] for line in res3[0:length]],
        'total net add':[line['totalNetBuySellVolume'] for line in res3[0:length]]
}

df = pd.DataFrame(data)
dates = [datetime.datetime.fromtimestamp(t) for t in res1['t'][0:length]]
df.index = [date.strftime("%Y-%m-%d") for date in dates]
df['year'] = [date.year for date in dates]
df['month'] = [date.month for date in dates]
df['date'] = [date.day for date in dates]
df['weekday'] = [weekday[date.weekday()] for date in dates]
df = df.sort_index(ascending=True)
df['rate']= df['open'].pct_change()
df = df.dropna()


