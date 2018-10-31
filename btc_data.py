from datetime import datetime, date, timedelta
from time import sleep
import pandas as pd
from tqdm import tqdm
import os
from config import BlockchainInfoConfig, BtcDataConfig
from sklearn.externals import joblib

class WebData():
    def __int__(self):
        self.current_time = datetime.now()
        self.starting_date = '1/3/2009'
        self.ending_date = self.current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.time_series = pd.Series(pd.date_range(start=self.starting_date, end=self.ending_date).date)
        self.data = self._get_data()

    def _get_data(self):
        raise NotImplementedError

    def _adapt_time_seire(self, ts: pd.DataFrame) -> pd.Series:
        # aggregate daily data to its mean
        ts = ts.groupby('time').mean()
        # merge to standard time series
        ts = pd.merge(pd.DataFrame(self.time_series, columns=['time']), ts.reset_index(), how='left',
                      on='time').set_index('time')
        # interpolate missing values, missing past data will be filled with 0,
        # missing future data filled with last nonna
        ts = ts.interpolate().fillna(0)
        return ts

    def _datetime_str_to_date(self, datetime_str: str) -> datetime.date:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').date()

class BlockchaininfoData(WebData):
    def __init__(self):
        super().__init__(self)
        self.data_identifier = 'BI'
        self.charts = BlockchainInfoConfig["ts_charts"]
        self.time_span = BlockchainInfoConfig["time_span"]
        self.chart_format = BlockchainInfoConfig["format"]

        self.url_header = BlockchainInfoConfig["url_header"]
        self.data = self._create_btc_dataframe()

    def _create_btc_dataframe(self, charts=None):
        if charts is None:
            charts = self.charts
        else:
            charts = [c.replace('_', '-') for c in charts]
        data = pd.DataFrame(index=self.time_series)
        for chart in tqdm(charts):
            sleep(0.5)
            chart_name = chart.replace('-', '_') + '_' + self.data_identifier
            chart_url = self.url_header + chart + "?timespan={0}&format={1}".format(self.time_span, self.chart_format)
            ts = pd.read_csv(chart_url, header=None, names=['time', '{}'.format(chart_name)])
            ts.time = ts.time.apply(self._datetime_str_to_date)
            ts = self._adapt_time_seire(ts)
            data[chart_name] = ts[chart_name]
        return data



class BitinfochartData(WebData):
    def __init__(self):
        super().__init__()

class BtcData():
    def __init__(self, update_interval=3):
        self.ts_data_file = BtcDataConfig['blockchaininfo_ts_data_file']
        self.blockchaininfo_data = BlockchaininfoData()
        self.btc_data = self.blockchaininfo_data.data
        self.current_time = self.blockchaininfo_data.current_time
        self.update_interval = update_interval

    def _get_data(self):
        if not os.path.isfile(self.ts_data_file) \
                or self.current_time.date() - self._get_file_last_modified_date(
                self.ts_data_file) > timedelta(self.update_interval):
            data = self._create_date_file()

        else:
            data = joblib.load(self.ts_data_file)

        return data

    def _get_file_last_modified_date(self, file: str) -> datetime.date:
        return date.fromtimestamp(os.stat(file).st_mtime)

    def _create_date_file(self):
        joblib.dump(self.btc_data, self.ts_data_file)
        return self.btc_data



