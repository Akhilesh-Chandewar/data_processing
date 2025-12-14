import yaml
from network_security_package.exception.exception import NetworkSecurityException
from network_security_package.logging.logger import logging
import os
import numpy as np
from numpy import ndarray
import pickle

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e)


def save_numpy_array_data(file_path: str, array: ndarray):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e) from e


def load_numpy_array_data(file_path: str) -> ndarray:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e) from e


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered save_object")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited save_object")
    except Exception as e:
        raise NetworkSecurityException(e) from e


def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")

        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e) from e


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for name, model in models.items():
            params = param[name]

            gs = GridSearchCV(model, params, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            report[name] = r2_score(y_test, y_test_pred)

        return report

    except Exception as e:
        raise NetworkSecurityException(e)
