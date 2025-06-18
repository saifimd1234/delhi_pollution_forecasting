import os
import sys
import numpy as np
import pandas as pd

'''
Define the common constant variable for training pipeline.
'''
TARGET_COLUMN = "PM2.5"
PIPELINE_NAME: str = "PollutionForecastingPipeline"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "delhi_pollution_data.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"


'''
Data Ingestion related constants start with DATA_INGESTION VAR NAME
'''

DATA_INGESTION_COLLECTION_NAME: str = "air_quality"
DATA_INGESTION_DATABASE_NAME: str = "delhi_pollution"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2