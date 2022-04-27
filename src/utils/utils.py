"""
Utility and helper functions are located here.
"""
import time
import logging
import logging.config
import logging.handlers

import yaml
import json

from types import SimpleNamespace
from pathlib import Path
from typing import Callable, Any, Dict


def get_project_root() -> str:
    return str(Path(__file__).parent.parent.parent)


def time_execution(func: Callable) -> Callable:
    """
    A decorator function at enables us to measure time in function calls.
    :param func: The function that we want to call
    :return: The wrapper function
    """
    def wrapper(*args, **kwargs) -> Any:
        """The wrapper function"""
        start = time.time()
        val = func(*args, **kwargs)
        print(f"Execution of '{func.__name__}' took: {round(time.time() - start, 2)} seconds")
        return val
    return wrapper


def setup_config(config_path) -> SimpleNamespace:
    """
    Loads in the config file into a SimpleNamespace object.
    :param config_path: The path to the config file for users.
    :return: A SimpleNamespace object that contains the configuration.
    """
    with open(config_path) as stream:
        config_file = yaml.safe_load(stream)
    return SimpleNamespace(**config_file)


def load_yaml_config_to_dict(config_path) -> Dict:
    """
    Loads in the config file into a dictionary object.
    :param config_path: The path to the config file.
    :return: A dictionary that contains the configuration.
    """
    with open(config_path) as stream:
        return yaml.safe_load(stream)


def setup_users(users_path) -> SimpleNamespace:
    """
    Loads in the users config file into a SimpleNamespace object.
    :param users_path: The path to the config file for users.
    :return: A SimpleNamespace object that contains the users configuration.
    """
    with open(users_path) as infile:
        users = json.load(infile)
        return users


def reformat_str_to_dt_format(dt: str) -> str:
    """
    Assumes the input string is in yyyymmdd
    returns the string as yyyy-mm-dd
    :param dt: the datetime string
    :return: the reformed datetime string
    """
    return '"' + dt[:4] + '-' + dt[4:6] + '-' + dt[6:] + '"'


def setup_logging(self) -> None:
    log_path = self.__dict__.get("log_config_path", None)
    if Path.exists(log_path):
        with open(log_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        print("Warning. Logging is not set up correctly as log_config_path is missing in configuration.")
        logging.basicConfig(level="default_level")
