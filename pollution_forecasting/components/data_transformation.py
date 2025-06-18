import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from pollution_forecasting.constant.training_pipeline import (
    TARGET_COLUMN,
    DATA_TRANSFORMATION_IMPUTER_PARAMS
)
from pollution_forecasting.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)
from pollution_forecasting.entity.config_entity import DataTransformationConfig
from pollution_forecasting.exception.exception import PollutionException
from pollution_forecasting.logging.logger import logging
from pollution_forecasting.utils.main.utils import (
    save_numpy_array_data,
    save_object
)


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise PollutionException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise PollutionException(e, sys)

    def get_data_transformer_object(self) -> Pipeline:
        logging.info("Entered the get_data_transformer_object method of Data Transformation class")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Data transformation object (KNNImputer) created successfully.")
            processor = Pipeline([
                ("imputer", imputer)
            ])
            logging.info("Data transformation pipeline created successfully.")
            return processor
        except Exception as e:
            raise PollutionException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation.")

            train_df = self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = self.read_data(self.data_validation_artifact.valid_test_file_path)

            def preprocess(df: pd.DataFrame) -> pd.DataFrame:
                df['From Date'] = pd.to_datetime(df['From Date'], format='%d-%m-%Y %H:%M')
                df.set_index('From Date', inplace=True)
                df.drop(columns=['To Date'], inplace=True)
                df.replace('None', np.nan, inplace=True)

                pollutant_cols = ['PM2.5', 'PM10', 'NO2', 'NOx', 'SO2', 'CO', 'Ozone', 'NH3']
                df[pollutant_cols] = df[pollutant_cols].apply(pd.to_numeric, errors='coerce')
                return df

            train_df = preprocess(train_df)
            test_df = preprocess(test_df)

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]

            preprocessor = self.get_data_transformer_object()

            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)

            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)
            save_object("final_model/preprocessor.pkl", preprocessor_object)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            logging.info("Data transformation completed and artifact created.")
            return data_transformation_artifact

        except Exception as e:
            raise PollutionException(e, sys)
