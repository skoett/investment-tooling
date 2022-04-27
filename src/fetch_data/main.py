from alpha_vantage.foreignexchange import ForeignExchange
from google.cloud import bigquery
from pprint import pprint
import json, os


class BQHandler:
    def __init__(self, api_key, from_curr, to_curr):
        self.key = api_key
        self.exchange = ForeignExchange(key=self.key)
        self.interval = "1min"
        self.outputsize = 'full'
        self.from_curr = from_curr
        self.to_curr = to_curr
        self.client = bigquery.Client()
        self.dataset_id = "Forex2020"
        self.table_id = "major_intraday_1min"
        self.table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        self.table = self.client.get_table(self.table_ref)

    # def write_to_BQ():
    def get_intraday_data(self):
        response = self.exchange.get_currency_exchange_intraday(from_symbol=self.from_curr
                                                                , to_symbol=self.to_curr
                                                                , interval=self.interval
                                                                , outputsize=self.outputsize)
        return response[0]


def invoke(msg, _):

    api_key = msg['attributes'].get("Key")
    from_curr = msg['attributes'].get("from_curr")
    to_curr = msg['attributes'].get("to_curr")

    api_handler = BQHandler(api_key, from_curr, to_curr)
    return api_handler.get_intraday_data()


with open("example.json") as f:
    data = json.load(f)
    meta_key = list(data.keys())[0]
    timestamps = list(data[meta_key].keys())
    keys = list(data[meta_key][timestamps[0]].keys())
    vals = list(data[meta_key][timestamps[0]].values())
    print(list(zip(keys,vals)))
    #print(list(data[meta_key][timestamps[0]].values()))
