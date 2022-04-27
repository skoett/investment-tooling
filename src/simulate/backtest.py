#!/usr/bin/env/ python3

import os
import yaml
import logging.config
import logging.handlers
import logging
from string import digits
import pandas as pd

from src.patterns.point import Point
from src.patterns.pattern import Pattern
from src.patterns.singlepattern import SinglePatterns
from src.patterns.dualpattern import DualPatterns
from src.patterns.triplepattern import TriplePatterns
from src.utils.log_utils import shutdown_and_move_logfiles


class BTConfig(object):
    """
    Holds the configuration and manipulating functionality for back testing
    various algorithms.
    """
    def __init__(self, bt_params: str) -> None:
        self.__dict__.update(bt_params)
        self.logger = logging.getLogger(__name__)
        self.time_frames = ['M', 'H', 'D']
        self.currency = ['USD', 'DKK']
        self.currency_pairs = ['EURUSD',
                               'EURCAD',
                               'EURCHF',
                               'EURGBP',
                               'NZDUSD',
                               'USDCHF',
                               'USDJPY',
                               'XAGUSD',
                               'XAUUSD']
        self.setup_logging()
        assert self.well_formed(), "back test config is ill-formed!"

    def setup_logging(self) -> None:
        log_path = self.__dict__.get("log_config_path", None)
        if os.path.exists(log_path):
            with open(log_path, 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        else:
            print("Warning. Logging is not set up correctly as log_config_path is missing in configuration.")
            logging.basicConfig(level="default_level")

    def return_dict(self) -> dict:
        """ Returns the dictionary"""
        return self.__dict__

    def return_value(self, key: str) -> any:
        """
        Returns a value from dict, given by key.
        :param key: The name of the corresponding key.
        :return: The corresponding value
        """
        dictionary = self.return_dict()
        return dictionary.get(key, None)

    def add_key_value(self, key: str, value: str) -> None:
        """ Can add key value pairs to the dictionary if needed"""
        self.__dict__[key] = value

    def well_formed(self) -> bool:
        """
        Asserts whether the config is valid by checking multiple conditions.
        :return: boolean in correspondence to whether the config is valid
        """
        bt = self.__dict__.get('backtest')
        try:
            if all(c in set(digits).union('/') for c in bt['start_date']) and \
               all(c in set(digits).union('/') for c in bt['end_date']) and \
               all(i in self.currency_pairs for i in bt['pairs']) and \
               bt['currency'] in self.currency and \
               float(bt['start_capital']) and \
               bt['time_frame'] in self.time_frames:
                return True
            return False
        except ValueError:
            return False


class StartBT(BTConfig):

    def __init__(self, bt_params: str, df: pd.DataFrame) -> None:
        # TODO: Here, we want to start optimize data structures wrt. AL-19
        super().__init__(bt_params)
        self.single_patterns = SinglePatterns()
        self.dual_patterns = DualPatterns()
        self.triple_patterns = TriplePatterns()
        self.patterns = Pattern()
        self.data = df
        self.metadata = {
            'start_day': self.data.DT.min().strftime('%m/%d/%Y'),
            'end_day': self.data.DT.max().strftime('%m/%d/%Y'),
            'days': self.data.DT.dt.normalize().nunique()
            }

    def execute(self) -> None:
        """
        Executes the backtest
        :return: None
        """
        print(f"Running simulation over {self.metadata.get('days')} "
              f"days between {self.metadata.get('start_day')}"
              f" and {self.metadata.get('end_day')}")

        for index, (_, row) in enumerate(self.data.iterrows()):
            point = Point(row.OPEN, row.CLOSE, row.HIGH, row.LOW, row.DT)

            # Find local extrema for the last n points
            if index > 5 and index % 10 == 0:
                self.patterns.mark_local_extrema(10)

            # Find all single candle patterns
            self.single_patterns.all_single_patterns(point)

            # Find dual patterns
            if index != 0:
                self.dual_patterns.all_dual_patterns()

            # Find triple patterns
            if index > 2:
                self.triple_patterns.all_triple_patterns()

            # Find trendlines

        # Clean up
        shutdown_and_move_logfiles(self.return_value("log_path"))
