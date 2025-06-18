from pollution_forecasting.exception.exception import PollutionException
from pollution_forecasting.logging.logger import logging

# configuration of the Data Ingestion Config

from pollution_forecasting.entity.config_entity import DataIngestionConfig
from pollution_forecasting.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    """
    Class for handling data ingestion operations from MongoDB to a feature store and splitting into training and testing datasets.
    """
    
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """
        Initialize the DataIngestion object with configuration settings.
        
        Args:
            data_ingestion_config (DataIngestionConfig): Configuration object containing parameters for data ingestion such as database name, collection name, file paths, and split ratio.
                
        Raises:
            PollutionException: If initialization fails.
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise PollutionException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Fetch data from MongoDB collection and convert it to a pandas DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame containing the data from MongoDB collection.
            
        Raises:
            PollutionException: If data export fails.
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"], axis=1, inplace=True)

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise PollutionException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        """
        Save the DataFrame to a CSV file in the feature store location.
        
        Args:
            dataframe (pd.DataFrame): DataFrame to be saved to the feature store.
            
        Returns:
            pd.DataFrame: The input DataFrame (unchanged).
            
        Raises:
            PollutionException: If saving to feature store fails.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            
            return dataframe
            
        except Exception as e:
            raise PollutionException(e, sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Split the input DataFrame into training and testing sets and save them as CSV files.
        
        Args:
            dataframe (pd.DataFrame): DataFrame to be split into training and testing sets.
            
        Raises:
            PollutionException: If splitting or saving the data fails.
        """
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info("Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info("Exported train and test file path.")
            
        except Exception as e:
            raise PollutionException(e, sys)
        
    def initiate_data_ingestion(self):
        """
        Orchestrate the complete data ingestion process.
        
        This method coordinates the workflow of:
        1. Exporting data from MongoDB to a DataFrame
        2. Saving the data to the feature store
        3. Splitting the data into training and testing sets
        
        Returns:
            Tuple[str, str]: Paths to the training and testing files.
            
        Raises:
            PollutionException: If any part of the data ingestion process fails.
        """
        try:
            dataframe = self.export_collection_as_dataframe()
            # Complete this method with feature store export and train/test split
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            
            dataingestionartifact = DataIngestionArtifact(training_file_path=self.data_ingestion_config.training_file_path, testing_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info("Data ingestion process completed successfully.")

            return dataingestionartifact
            
        except Exception as e:
            logging.error(f"Data ingestion process failed: {e}")
            raise PollutionException(e, sys)