from pollution_forecasting.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

from scipy.stats import ks_2samp
 
from pollution_forecasting.entity.config_entity import DataValidationConfig
from pollution_forecasting.exception.exception import PollutionException 
from pollution_forecasting.logging.logger import logging 
from pollution_forecasting.constant.training_pipeline import SCHEMA_FILE_PATH
import pandas as pd
import os,sys
from pollution_forecasting.utils.main.utils import read_yaml_file, write_yaml_file

class DataValidation:
    """
    Class responsible for validating data quality and detecting data drift between training and testing datasets.
    """

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        """
        Initialize the DataValidation with artifacts and configuration.
        
        Args:
            data_ingestion_artifact (DataIngestionArtifact): Contains paths to ingested data files
            data_validation_config (DataValidationConfig): Configuration for validation process
            
        Raises:
            PollutionException: If initialization fails
        """   
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        
        except Exception as e:
            raise PollutionException(e, sys)

            
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        """
        Read CSV data from the given file path.
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            pd.DataFrame: DataFrame containing the file data
            
        Raises:
            PollutionException: If reading the file fails
        """
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise PollutionException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        """
        Validate that the DataFrame has the expected number of columns based on schema.
        
        Args:
            dataframe (pd.DataFrame): DataFrame to validate
            
        Returns:
            bool: True if the number of columns matches the schema, False otherwise
            
        Raises:
            PollutionException: If validation process fails
        """
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Dataframe has columns:{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        
        except Exception as e:
            raise PollutionException(e,sys)
        
    def detect_dataset_drift(self,base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        """
        Detect data drift between base DataFrame and current DataFrame using
        Kolmogorov-Smirnov test.
        
        Args:
            base_df (pd.DataFrame): Base DataFrame (typically training data)
            current_df (pd.DataFrame): Current DataFrame to check for drift (typically test data)
            threshold (float, optional): p-value threshold for determining drift. Defaults to 0.05.
            
        Returns:
            bool: False if drift is detected in any column, True otherwise
            
        Raises:
            PollutionException: If drift detection fails
        """
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise PollutionException(e,sys)
        
    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            ## read the data from train and test
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            
            ## validate number of columns

            status=self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"Test dataframe does not contain all columns.\n"   

            ## lets check datadrift
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        
        except Exception as e:
            raise PollutionException(e, sys)



