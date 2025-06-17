import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
if MONGO_DB_URL:
    print(MONGO_DB_URL)
else:
    print("MONGO_DB_URL is not set.")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from pollution_forecasting.exception.exception import PollutionException
from pollution_forecasting.logging import logger

class PollutionDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise PollutionException(e,sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            # return data.to_dict(orient='records'), same as the below code but much simpler
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise PollutionException(e,sys)
        
    def insert_data_mongodb(self, records, database, collection):

        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
        
            return (len(self.records), "records inserted successfully")
        
        except Exception as e:
            raise PollutionException(e,sys)

if __name__=='__main__':
    FILE_PATH = "Pollution_Data\delhi_pollution_data.csv"
    DATABASE = "delhi_pollution"
    Collection="air_quality"
    networkobj = PollutionDataExtract()
    records = networkobj.csv_to_json_convertor(FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(no_of_records)