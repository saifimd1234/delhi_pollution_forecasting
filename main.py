from pollution_forecasting.components.data_ingestion import DataIngestion
from pollution_forecasting.components.data_validation import DataValidation
from pollution_forecasting.exception.exception import PollutionException
from pollution_forecasting.logging.logger import logging
from pollution_forecasting.entity.config_entity import DataIngestionConfig, DataValidationConfig
from pollution_forecasting.entity.artifact_entity import DataIngestionArtifact
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
        print(dataingestionartifact)
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Initiate the data validation.")
        data_validation_artifact = data_validation.initiate_data_validation()
        
        logging.info("Data Validation process completed successfully.")
        print(dataingestionartifact)
        print(data_validation_artifact)

    except Exception as e:
        raise PollutionException(e, sys)
