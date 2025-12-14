from network_security_package.components.data_ingestion import DataIngestion
from network_security_package.components.data_validation import DataValidation
from network_security_package.exception.exception import NetworkSecurityException
from network_security_package.logging.logger import logging
from network_security_package.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
)
from network_security_package.entity.config_entity import TrainingPipelineConfig
from network_security_package.entity.config_entity import ModelTrainerConfig

if __name__ == "__main__":
    try:
        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=TrainingPipelineConfig()
        )
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.initiate_data_ingestion()
        logging.info("Initiated Data Ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        data_validation_config = DataValidationConfig(
            training_pipeline_config=TrainingPipelineConfig()
        )
        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config,
        )
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Initiated Data Validation")
    except Exception as e:
        raise NetworkSecurityException(e)
