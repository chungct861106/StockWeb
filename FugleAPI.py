from fugle_realtime import intraday
import time
import pygsheets
import pandas as pd
import datetime
import numpy as np

datafile = "TrackStocks.json"
GoogleSheet_key = "1PHPjJnbAPPlEU9byk3eOQtpXlHuIwNQMxDbh9iG7K-o"

GoogleClient = 'MyProfile\\GoogleProfile.json'

# chart.index = range(datetime.str


class DayStocks():
    def __init__(self):
        self.APIKey = "ef3d39a8b35665be0706cf4aec3c18e7"
        self.stocks_new = list()
        self.stock_df = dict()
        self.GoogleClient = GoogleClient
        self.sheet_key = GoogleSheet_key
        self.gc = pygsheets.authorize(service_file=self.GoogleClient)
        self.workbook = self.gc.open_by_key(GoogleSheet_key)
        self.sheets = self.workbook.worksheets()
        self.stocks = [sheet.title for sheet in self.sheets]
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
        
    def update(self, NewStock=list()):
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        for stock in [s for s in self.stock_df] + NewStock:
            # try:
            if stock in self.stock_df and len(self.stock_df[stock].index) == 266:
                if self.stock_df[stock].columns[-1] == today and int(datetime.datetime.now().strftime("%H%M")) > 1330:
                    print(stock + " is already updated to latest version.")
                    continue
                elif self.stock_df[stock].columns[-1] == today and int(datetime.datetime.now().strftime("%H%M")) <= 1330:
                    self.stock_df[stock].drop(self.stock_df[stock].columns[-1], axis=1)
                chart = intraday.chart(apiToken=self.APIKey, output="dataframe", symbolId=stock)
                self.stock_df[stock][today] = np.array(chart["open"]).tolist() + [None]*(len(self.stock_df[stock].index) - len(chart.index))
                
            else:
                chart = intraday.chart(apiToken=self.APIKey, output="dataframe", symbolId=stock)
                delta = datetime.timedelta(hours = 8)
                times = [t + delta for t in np.array(chart['at']).tolist()]
                chart.index = [t.strftime("%H:%M") for t in times]
                self.stock_df[stock] = chart['open'].to_frame()
                self.stock_df[stock].columns = [datetime.datetime.today().strftime("%Y-%m-%d")]
            print("Update " + stock + " success.")
            # except :
            #     print("Fail update " + stock +".")
    def Delete_stock(self, name):
        if name in self.stock_df:
            del self.stock_df[name]
        else:
            print(name + " does not exist.")
            return None
        if name in [sheet.title for sheet in self.sheets]:
            index = [sheet.title for sheet in self.sheets].index(name)
            self.workbook.del_worksheet(self.sheets[index])
        else:
            print(name + " does not exist.")
            return None
        print(name + " has been removed.")
            
    def Save_stock(self):
        for stock in self.stock_df:
            if stock in [sheet.title for sheet in self.workbook.worksheets()]:
                sheet = self.workbook.worksheet_by_title(stock)
            else:
                sheet = self.workbook.add_worksheet(stock)
            sheet.set_dataframe(
                self.stock_df[stock], "A1", copy_index=True, fit=True)
            sheet.frozen_rows = 1
            sheet.frozen_cols = 1
        print("Google sheets {} saved success.".format(self.workbook.title))
