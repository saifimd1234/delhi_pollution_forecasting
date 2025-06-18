from pollution_forecasting.components.data_ingestion import DataIngestion
from pollution_forecasting.exception.exception import PollutionException
from pollution_forecasting.logging.logger import logging
from pollution_forecasting.entity.config_entity import DataIngestionConfig
from pollution_forecasting.entity.config_entity import TrainingPipelineConfig

import sys

if __name__ == '__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Data Ingestion object created successfully.")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion process completed successfully.")

        print(dataingestionartifact)

    except Exception as e:
        raise PollutionException(e, sys)
