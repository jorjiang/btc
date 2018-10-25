import pandas as pd
from database.config import BlockchainInfoConfig
import datetime
class BtcDatabase():
    def __init__(self, update_interval=3):
        self.current_time = datetime.datetime.now()
        self.update_interval = update_interval

        self.charts = ['my-wallet-n-users']
        # self.charts = BlockchainInfoConfig["ts_charts"]
        self.time_span = BlockchainInfoConfig["time_span"]
        self.chart_format = BlockchainInfoConfig["format"]

        self.url_header = BlockchainInfoConfig["url_header"]

    def create_btc_database(self):
        data = pd.DataFrame()
        for chart in self.charts:
            chart_url = self.url_header + chart + "?timespan={0}&format={1}".format(self.time_span, self.chart_format)
            ts = pd.read_csv(chart_url, header=None, names = ['time', '{}'.format(chart).replace('-', '_')])
            data = pd.concat([data, ts])
        self.data = data

    def update_databasa(self):
        pass


def test_btc_database():
    btc_database = BtcDatabase()
    btc_database.create_btc_database()
    print(btc_database.data)
