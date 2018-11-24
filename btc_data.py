import os
from datetime import datetime, date, timedelta
from time import sleep
import urllib.request as ur

import pandas as pd
import numpy as np
from config import BlockchainInfoConfig, BtcDataConfig, BitinfochartConfig
from sklearn.externals import joblib
from tqdm import tqdm


class WebData():
    def __init__(self):
        self.current_time = datetime.now()
        self.starting_date = '1/3/2009'
        self.ending_date = self.current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.time_series = pd.Series(pd.date_range(start=self.starting_date, end=self.ending_date).date)

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
        try:
            date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').date()
        except:
            date = datetime.strptime(datetime_str, '%Y-%m-%d').date()

        return date

    def _create_btc_dataframe(self):
        raise NotImplementedError


class BlockchaininfoData(WebData):
    def __init__(self):
        super().__init__()
        self.data_identifier = 'BI'
        self.charts = BlockchainInfoConfig["ts_charts"]
        self.time_span = BlockchainInfoConfig["time_span"]
        self.chart_format = BlockchainInfoConfig["format"]

        self.url_header = BlockchainInfoConfig["url_header"]
        self.url_tail = BlockchainInfoConfig["url_tail"]

        self.data = self._create_btc_dataframe(self.charts)

    def _create_btc_dataframe(self, charts=None):
        if charts is None:
            charts = self.charts
        else:
            charts = [c.replace('_', '-') for c in charts]
        data = pd.DataFrame(index=self.time_series)
        for chart in tqdm(charts):
            sleep(1)
            chart_name = chart.replace('-', '_') + '_' + self.data_identifier
            chart_url = self.url_header + chart + "?timespan={0}&format={1}".format(self.time_span,
                                                                                    self.chart_format) + self.url_tail
            ts = pd.read_csv(chart_url, header=None, names=['time', chart_name])
            ts.time = ts.time.apply(self._datetime_str_to_date)
            ts = self._adapt_time_seire(ts)
            data[chart_name] = ts[chart_name]
        return data


class BitinfochartData(WebData):
    def __init__(self):
        super().__init__()
        self.data_identifier = 'BIC'
        self.charts = BitinfochartConfig["ts_charts"]

        self.url_header = BitinfochartConfig["url_header"]
        self.url_tail = BitinfochartConfig["url_tail"]

        self.data = self._create_btc_dataframe(self.charts)

    def _create_btc_dataframe(self, charts=None):
        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'

        if charts is None:
            charts = self.charts

        data = pd.DataFrame(index=self.time_series)
        for chart in tqdm(charts):
            sleep(1)
            chart_name = chart + '_' + self.data_identifier
            chart_url = self.url_header + chart + self.url_tail
            request = ur.urlopen(ur.Request(chart_url, data=None, headers={'User-Agent': user_agent}))

            webContent = request.read()
            source = webContent.decode('utf-8')

            data_str = source.split('Dygraph(document.getElementById("container"),')[1].split(', {labels: ["Date"')[0]
            data_str = data_str.replace('new Date(', '').replace(')', '').replace('null', 'np.nan').replace('/', '-')

            data_array = np.array(eval(data_str))
            ts = pd.DataFrame({'time': data_array[:, 0], chart_name: data_array[:, 1]})
            ts.replace('nan', np.nan, inplace=True)
            ts[chart_name] = ts[chart_name].map(lambda x: eval(x) if isinstance(x, str) else x)
            ts.time = ts.time.apply(self._datetime_str_to_date)
            ts = self._adapt_time_seire(ts)
            data[chart_name] = ts[chart_name]
        return data




class BtcData():
    def __init__(self, update_interval=3):
        self.current_time = datetime.now()
        self.ts_data_file = BtcDataConfig['blockchaininfo_ts_data_file']

        self.update_interval = update_interval
        self.data = self._get_data()

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
        self.blockchaininfo_data = BlockchaininfoData()
        self.bitinfochart_data = BitinfochartData()

        data = self.bitinfochart_data.data.join(self.blockchaininfo_data.data)
        joblib.dump(data, self.ts_data_file)
        return data
