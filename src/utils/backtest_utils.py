#!/usr/bin/env python3
"""

"""
import yaml
from pandas import DataFrame
from src.simulate.backtest import BTConfig, StartBT


def setup_parameters(config: str) -> BTConfig:
    """
    setups the corresponding class that holds variables for the back testing
    configuration
    :param config: The YAML configuration file
    :return: a BTC object that supervises the backtest
    """
    with open(config) as stream:
        return BTConfig(yaml.safe_load(stream))


def setup_parameters_inheritance(config: str, df: DataFrame) -> StartBT:
    """
    setups the corresponding class that holds variables for the back testing
    configuration
    :param config: The YAML configuration file
    :param df: The data from the pandas DataFrame
    :return: a BTC object that supervises the backtest
    """
    with open(config) as stream:
        return StartBT(yaml.safe_load(stream), df)
