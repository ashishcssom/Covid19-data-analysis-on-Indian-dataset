import pandas as pd # Library to read and write the data in structure format
import numpy as np # Library to deal with vector, array and matrices
import requests # Library to read APIs
import re # Library for regular expression
import json # Library to read and write JSON file
from bs4 import BeautifulSoup # Library for web scraping
####################################### APIs to be scrapped to getting real time Corna data ############################
moh_link = "https://www.mohfw.gov.in/"
url_state = "https://api.covid19india.org/state_district_wise.json"
data_data = "https://api.covid19india.org/data.json"
travel_history="https://api.covid19india.org/travel_history.json"
raw_data="https://api.covid19india.org/raw_data.json"


class COVID19India(object):    
    def __init__(self):
        self.moh_url = moh_link  # Ministry of Health and Family welfare website
        self.url_state = url_state  # districtwise data
        self.data_url = data_data  # All India data ==> Statewise data, test data, timeseries data etc
        self.travel_history_url=travel_history # Travel history of Patient
        self.raw_data_url=raw_data
    def __request(self, url):
        content=requests.get(url).json()
        return content
    def moh_data(self):
        url = self.moh_url
        df = pd.read_html(url)[-1].iloc[:-1]
        del df['S. No.']
        cols = df.columns.values.tolist()
        return df
    def statewise(self):
        data=self.__request(self.data_url)
        delta=pd.DataFrame(data.get('key_values'))
        statewise=pd.concat([pd.DataFrame(data.get('statewise')),pd.DataFrame([i.get('delta') for i in data.get('statewise')])],axis=1)
        del statewise["delta"]
        cases_time_series=pd.DataFrame(data.get('cases_time_series'))
        tested=pd.DataFrame(data.get('tested'))
        return(delta,statewise,cases_time_series,tested)
    def state_district_data(self):
        state_data = self.__request(self.url_state)
        key1 = state_data.keys()
        Values = []
        for k in key1:
            key2 = state_data[k]['districtData'].keys()
            for k2 in key2:
                c = list(state_data[k]['districtData'][k2].values())
                v = [k, k2, c[0]]
                Values.append(v)
        state_data = pd.DataFrame(Values,columns=['State_UT', 'District', 'Confirmed'])
        return state_data
    def travel_history(self):
        history_data = self.__request(self.travel_history_url)
        travel=pd.DataFrame(history_data.get("travel_history"))
        return(travel)
    def raw_data_info(self):
        raw = self.__request(self.raw_data_url)
        data=pd.DataFrame(raw.get("raw_data"))
        return(data)
