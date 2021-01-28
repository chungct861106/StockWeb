import json
import pandas as pd
import requests
import datetime
import time
from pytz import timezone
from bs4 import BeautifulSoup

tz = timezone('Asia/Taipei')
StockDataProfile = 'StockDataBase.json'
  
def GetStockInfo(string, Single=False, No=False):
    url = 'https://isin.twse.com.tw/isin/single_main.jsp'
    try:
        int(string)
        params = {'owncode':string}
    except:
        params = {'stockname':string}
    res = requests.get(url=url, params=params).text
    soup = BeautifulSoup(res, features="lxml")
    d = [str(tag.string) for tag in soup.findAll('td')]
    d = d[0:min(200, len(d))]
    if No is not True:
        names = ["{} ({})".format(d[10*n + 3], d[10*n + 2]) for n in range(1,int(len(d)/10))]
    else:
        names = [d[10*n + 2] for n in range(1,int(len(d)/10))]
    if Single:
        return names[0]
    else:
        return names
checking = []
class JsonStockData:
    def __init__(self):
        self.stock_df = dict()
        self.stocks = list()
        self.sets = dict()
        with open("StockDataBase.json", encoding="utf-8") as f:
            Info = json.load(f)
            self.stocks = Info['stocks']
            if len(Info['sets']) > 0:
                self.sets = Info['sets']
        for stock in self.stocks:
            self.stock_df[stock] = pd.DataFrame(self.stocks[stock])

    def __getStock(self, stock=str(), start=None, to=None):
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
                'Open':res1['o'][0:length],
                'Close':res1['c'][0:length],
                'High':res1['h'][0:length],
                'Low':res1['l'][0:length],
                'Margin buy':[line['marginBuy'] for line in res2[0:length]],
                'Margin sell':[line['marginSell'] for line in res2[0:length]],
                'Margin used ratio':[line['marginUsedPercent'] for line in res2[0:length]],
                'Short buy':[line['shortBuy'] for line in res2[0:length]],
                'Short sell':[line['shortSell'] for line in res2[0:length]],
                'Margin short ratio':[line['shortMarginPercent'] for line in res2[0:length]],
                'Dealer net add':[line['dealerNetBuySellVolume'] for line in res3[0:length]],
                'Domestic net add':[line['domesticNetBuySellVolume'] for line in res3[0:length]],
                'Foreign net add':[line['foreignNetBuySellVolume'] for line in res3[0:length]],
                'Total net add':[line['totalNetBuySellVolume'] for line in res3[0:length]]
        }
        
        df = pd.DataFrame(data)
        dates = [datetime.datetime.fromtimestamp(t) for t in res1['t'][0:length]]
        df.index = [date.strftime("%Y-%m-%d") for date in dates]
        df['year'] = [date.year for date in dates]
        df['month'] = [date.month for date in dates]
        df['date'] = [date.day for date in dates]
        df['weekday'] = [weekday[date.weekday()] for date in dates]
        df = df.sort_index(ascending=True)
        df['Rate']= df['Open'].pct_change()
        df = df.dropna()
        return df

    def GetStock_test(self, stock=str(), start=None, to=None):
        return self.__getStock(stock=stock, start=start, to=to)
    
    def update_stock(self, today=datetime.datetime.today().strftime("%Y-%m-%d"), from_date=str(), NewStocks=list()):
        total_stocks = list(self.stocks.keys())
        for stock in NewStocks:
            if stock not in total_stocks:
                total_stocks.append(stock)

        for stock in total_stocks:
            # try:
            if stock in self.stock_df:
                first_date = min(self.stock_df[stock].index)
                last_date = max(self.stock_df[stock].index)
                data = [self.stock_df[stock]]
                if last_date < today:
                    data = [self.__getStock(stock=stock, start=last_date, to=today)] + data
                
                if first_date > from_date:
                    data.append(self.__getStock(stock=stock, start=from_date, to=first_date))
                df = pd.concat(data)
                df = df.reset_index().drop_duplicates(
                    subset='index', keep='last').set_index('index').sort_index()
                self.stock_df[stock] = df
                print("Update", stock, "success.")
            else:
                datas = self.__getStock(stock=stock, start=from_date, to=today)
                if len(datas) == 0:
                    print("Update", stock, "failed.")
                else:
                    self.stock_df[stock] = datas
                    print("Update", stock, "success.")
        self.Save()
            # except:
            #     print("Update", stk_id, "failed.")
    def NewStock(self, stock, today=datetime.datetime.today().strftime("%Y-%m-%d"), from_date=str()):
        if stock not in self.stock_df:
            datas = self.__getStock(stock=stock, start=from_date, to=today)
            if len(datas) == 0:
                print("Update", stock, "failed.")
            else:
                self.stock_df[stock] = datas
                print("Update", stock, "success.")
        else:
            if max(self.stock_df[stock].index) < today:
                datas = self.__getStock(stock=stock, start=from_date, to=today)
                if len(datas) == 0:
                    print("Update", stock, "failed.")
                else:
                    self.stock_df[stock] = datas
                    print("Update", stock, "success.")
            else:
                print("Already existed and updated.")
        self.Save()
                
                
    def DeleteStock(self, name):
        if name.find(" ")!=-1:
            name = name.split(" ")[1][1:-1]
        if name in self.stock_df:
            del self.stock_df[name]
        else:
            print("Name not found")
        self.Save()

    def Save(self):
        save_dict = dict()
        for stock in self.stock_df:
            save_dict[stock] = self.stock_df[stock].to_dict()
        now = datetime.datetime.now().strftime("%Y-%m-%d %I:%M")
        output = {'sets':self.sets, 'stocks':save_dict, 'LastUpdate':now}
        with open('StockDataBase.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
    
    def NewSets(self, name):
        if name not in self.sets:
            self.sets[name] = list()
        else:
            print(name + " already exist.")
        self.Save()
    
    def DeletSets(self, name):
        if name in self.sets:
            del self.sets[name]
        else:
            print(name + " not found.")
        self.Save()
    
    def Set_add_Stock(self, sets, stock):
        if stock not in self.sets[sets]:
            if stock.find(" ") == -1:
                stock = GetStockInfo(string=stock, Single=True)
                print("Add stock: " + stock)
            stockNo = stock.split(" ")[1][1:-1]
            if stockNo not in self.stock_df:
                print("in")
                self.NewStock(stockNo, from_date='2000-01-01')
            self.sets[sets].append(stock)
            self.Save()
        else:
            print('Already exist.')
    
    def Set_del_Stock(self, sets, stock):
        if stock in self.sets[sets]:
            self.sets[sets].remove(stock)
        self.Save()
