import logging
from network_security_package.entity.artifact_entity import DataIngestionArtifact
from network_security_package.exception.exception import NetworkSecurityException
from network_security_package.logging.logger import logger
from network_security_package.entity.config_entity import DataIngestionConfig

import os
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        try:
            self.config = config
        except Exception as e:
            raise NetworkSecurityException(e)

    def export_collection_as_dataframe(self):
        try:
            mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            database = mongo_client[self.config.database_name]
            collection = database[self.config.collection_name]
            data = pd.DataFrame(list(collection.find()))
            if "_id" in data.columns:
                data = data.drop(columns=["_id"], axis=1)
            data.replace({"na":np.nan},inplace=True)
            logger.info(f"Dataframe shape: {data.shape}")
            return data
        except Exception as e:
            raise NetworkSecurityException(e)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            dir_path = os.path.dirname(self.config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(self.config.training_file_path, index=False, header=True)
            test_set.to_csv(self.config.testing_file_path, index=False, header=True)
            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise NetworkSecurityException(e)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            dataingestionartifact = DataIngestionArtifact(
                trained_file_path=self.config.training_file_path,
                test_file_path=self.config.testing_file_path,
            )
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e)
