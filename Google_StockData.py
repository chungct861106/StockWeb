import pygsheets
import pandas as pd
import requests
import datetime
import time
from pytz import timezone
tz = timezone('Asia/Taipei')
GoogleClient = 'MyProfile\\GoogleProfile.json'


class GoogleStockData:
    def __init__(self, GoogleSheet_key):
        self.stocks_new = list()
        self.stock_df = dict()
        self.GoogleClient = GoogleClient
        self.sheet_key = GoogleSheet_key
        self.gc = pygsheets.authorize(service_file=self.GoogleClient)
        self.workbook = self.gc.open_by_key(GoogleSheet_key)
        self.sheets = self.workbook.worksheets()
        self.stocks = [sheet.title for sheet in self.sheets]
        self.ProfileSheet = None
        if "Profile" in self.stocks:
            index = self.stocks.index("Profile")
            self.stocks.pop(index)
            self.ProfileSheet = self.sheets.pop(index)
    
        for sheet in self.sheets:
            data = sheet.get_all_values(
                include_tailing_empty=False, include_tailing_empty_rows=False)
            head = data.pop(0)
            df = pd.DataFrame(data, columns=head)
            datelist = []
            for i in range(len(df)):
                datelist.append(df.iloc[:, 0][i])
            df.index = datelist
            df = df.drop([df.columns[0]], axis=1)
            self.stock_df[sheet.title] = df
        print("Google sheet {} loaded success.".format(self.workbook.title))

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
        params={
                'resolution':'D',
                'symbol':'TWS:{}:STOCK'.format(stock),
                'from': int(time.mktime(to.timetuple())),
                'to':int(time.mktime(start.timetuple())),
                'quote':1
        }
        
        res = requests.get(url=stock_url, params=params).json()['data']
        data = {
                'open':res['o'],
                'close':res['c'],
                'high':res['h'],
                'low':res['l'],
                'value':res['v']
        }
        return pd.DataFrame(data, index=[datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d") for t in res['t']])

    def update_stock(self, today=datetime.datetime.today().strftime("%Y-%m-%d"), from_date=str(), NewStocks=list()):
        self.stocks_new = NewStocks
        for stock in self.stocks_new:
            if stock not in self.stocks:
                self.stocks.append(stock)

        for stock in self.stocks:
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
            # except:
            #     print("Update", stk_id, "failed.")
                
    def DeleteStock(self, name):
        if name in self.stock:
            self.workbook.del_worksheet(self.sheet[self.stock.index(name)])
            self.stock.remove(name)
        else:
            print("Name not found")

    def Save_stock(self):
        for stock in self.stock_df:
            if stock in [sheet.title for sheet in self.workbook.worksheets()]:
                sheet = self.workbook.worksheet_by_title(stock)
            else:
                sheet = self.workbook.add_worksheet(stock)
            sheet.set_dataframe(
                self.stock_df[stock].sort_index(), "A1", copy_index=True, fit=True)
            sheet.frozen_rows = 1
            sheet.frozen_cols = 1
        print("Google sheets {} saved success.".format(self.workbook.title))
        today = datetime.datetime.today().replace(tzinfo=tz)  
        self.ProfileSheet.update_value('B5', today.strftime("%Y-%m-%d %H:%M:%S"))
        self.ProfileSheet.update_value("B4", str(len(self.stock_df)))


def NewGoogleSheet(name):
    client = pygsheets.authorize(service_file=GoogleClient)
    sheet = client.create(
        title=name, folder="1bw8FvNvjUdtAGb1ViiceRfwtTULr2zkZ")
    ProfileSheet = sheet.worksheet_by_title("Sheet1")
    ProfileSheet.title = "Profile"
    indexs = ["Name", "Create Date", "Stocks Number", "last Update Time"]
    profile = dict()
    profile["Data"] = [name, datetime.datetime.today(), 0, datetime.datetime.today()]
    df = pd.DataFrame(profile)
    df.index = indexs
    ProfileSheet.set_dataframe(df, "A1", copy_index=True, fit=True)
    ProfileSheet.frozen_rows = 1
    ProfileSheet.frozen_cols = 1
    ProfileSheet.adjust_column_width(start=1, end=2)
    return sheet.id

def DeleteGoogleSheet(SheetID):
    client = pygsheets.authorize(service_file=GoogleClient)
    client.drive.delete(SheetID)
