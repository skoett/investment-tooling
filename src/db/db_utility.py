#!/usr/bin/env python3
"""

"""
import yaml
from src.db.io_mariadb import MARIADB
from src.db.io_bigquery import BQ


def establish_connection_mariadb(config: str, database: str) -> MARIADB:
    """
    Establishes the connection to the MariaDB
    along necessary functions to communicate with the instance.
    :param config: The relative path to the config file.
    :param database: The initial database to connect to.
    :return: a Maria DB object that holds the connection.
    """
    with open(config) as stream:
        return MARIADB(yaml.safe_load(stream), initial_database=database)


def establish_connection_bigquery(config: str) -> BQ:
    """
    Sets up the bigquery client.
    :param config: The relative path to the config file
    :return: A bigquery client object.
    """
    with open(config) as stream:
        return BQ(yaml.safe_load(stream))
