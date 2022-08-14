from pytrends.request import TrendReq
import plotly.express as px
import pandas as pd
import json
import requests


class GoogleSearchBrandSts:

    def __init__(self, brand, other_keys=None):
        self.brand_name = brand
        self.py_trends = TrendReq(hl='en-US', tz=320)  #### hl : language, tz : time zone based on minute
        self.kw_combinations = [other_keys]

    def rate_of_interest(self, timeframe='today 5-y', geo=''):
        self.py_trends.build_payload(self.brand_name, cat=0, timeframe=timeframe, geo=geo, gprop='')
        df = self.py_trends.interest_over_time().reset_index()
        return df

    def auto_complete(self, string=None):
        if string is not None:
            string = [string]
        else:
            string = self.kw_combinations

        # client param could be replaced with firefox or other browser
        for s in string:
            response = requests.get(f'http://google.com/complete/search?client=chrome&q={s}')
            for result in json.loads(response.text)[1]:
                print(result)

sample = GoogleSearchBrandSts("عالیس")
sample.auto_complete('دوغ سنتی')