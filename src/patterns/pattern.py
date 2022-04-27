#!/usr/bin/env python3
import logging
from datetime import datetime

import pandas as pd

from src.patterns.utils import eval_bullish_bearish, eval_extrema
from src.patterns.point import Point


class Pattern(object):
    logger = logging.getLogger("backtest_logger")
    single_patterns = []
    dual_patterns = []
    triple_patterns = []
    trendlines = []

    @classmethod
    def eval_single_condition(cls, condition: bool, point: Point, pattern: str) -> bool:
        if condition:
            if point.open < point.close:
                point.bullish = True
            elif point.open > point.close:
                point.bearish = True
            if pattern:
                point.single_pattern = pattern
            else:
                point.single_pattern = "None"
            cls.logger.info(f"Single pattern: {pattern} - detected at ts: {point.ts}")
            cls.single_patterns.append(point)
            return True
        return False

    @classmethod
    def eval_dual_condition(cls, condition: bool, points: [Point], pattern: str) -> bool:
        if condition:
            for point in points:
                point.dual_pattern = pattern
                cls.logger.info(f"Dual pattern: {pattern} - detected at ts: {point.ts}")
                cls.dual_patterns.append(point)
            return True
        return False

    @classmethod
    def eval_triple_condition(cls, condition: bool, points: [Point], pattern: str) -> bool:
        if condition:
            for point in points:
                point.triple_pattern = pattern
                cls.logger.info(f"Triple pattern: {pattern} - detected at ts: {point.ts}")
                cls.triple_patterns.append(point)
            return True
        return False

    @classmethod
    def ensure_valid_prior(cls) -> list:
        """
        Helper function that determines whether the prior candle was a single candle pattern
        :return: None if prior candle was not a pattern, otherwise return the candle point object.
        """
        return [] if not cls.single_patterns[:-2] else cls.single_patterns[:-2]

    @classmethod
    def return_conditions_by_row(cls, row: pd.Series) -> (str, str):
        """
        Returns all conditions by row as a list of strings
        :param row: A pandas Series that defines a row.
        :return: A list of strings in correspondence with number of conditions.
        """
        single_cond = [p.single_pattern for p in cls.single_patterns if p.ts == row.DT]
        dual_cond = [p.dual_pattern for p in cls.dual_patterns if p.ts == row.DT]
        single_pattern = 'None' if len(single_cond) == 0 else single_cond[0]
        dual_pattern = 'None' if len(dual_cond) == 0 else dual_cond[0]
        return single_pattern, dual_pattern

    @classmethod
    def return_signals_by_row(cls, row: pd.Series) -> str:
        """
        Returns all signals by row as a single string.
        :param row: A Pandas Series that defines a row.
        :return: A single string in correspondence with the signal.
        """
        signal = [eval_bullish_bearish(p) for p in cls.single_patterns if p.ts == row.DT]
        if signal:
            cls.logger.info(f"Signal: {signal[0]} - detected at ts: {row.DT}")
        return "Could not be determined" if not signal else signal[0]

    @classmethod
    def return_conditions_by_row_optimised(cls, dt: datetime) -> (str, str):
        """
        Returns all conditions by row as a list of strings
        :param dt: The datetime value.
        :return: A list of strings in correspondence with number of conditions.
        """
        single_cond = [p.single_pattern for p in cls.single_patterns if p.ts == dt]
        dual_cond = [p.dual_pattern for p in cls.dual_patterns if p.ts == dt]
        single_pattern = 'None' if len(single_cond) == 0 else single_cond[0]
        dual_pattern = 'None' if len(dual_cond) == 0 else dual_cond[0]
        return single_pattern, dual_pattern

    @classmethod
    def return_signals_by_row_optimised(cls, dt: datetime) -> str:
        """
        Returns all signals by row as a single string.
        :param dt: Datetime value.
        :return: A single string in correspondence with the signal.
        """
        signal = [eval_bullish_bearish(p) for p in cls.single_patterns if p.ts == dt]
        if signal:
            cls.logger.info(f"Signal: {signal[0]} - detected at ts: {dt}")
        return "Could not be determined" if not signal else signal[0]

    @classmethod
    def return_extrema_by_row_optimised(cls, dt: datetime) -> (bool, bool):
        """
        Returns all extrema by row as a single string.
        :param dt: The datetime value.
        :return: A tuple in correspondence with a potential minimum and maximum.
        """
        signal = [eval_extrema(p) for p in cls.single_patterns if p.ts == dt]
        if signal != ['']:
            cls.logger.info(f"Extrema found: {signal[0]}: detected at ts: {dt}")
            return signal[0]
        return ''

    @classmethod
    def return_extrema_by_row(cls, row: pd.Series) -> (bool, bool):
        """
        Returns all extrema by row as a single string.
        :param row: A Pandas Series that defines a row.
        :return: A tuple in correspondence with a potential minimum and maximum.
        """
        signal = [eval_extrema(p) for p in cls.single_patterns if p.ts == row.DT]
        if signal != ['']:
            cls.logger.info(f"Extrema found: {signal[0]} - detected at ts: {row.DT}")
            return signal[0]
        return ''

    @classmethod
    def mark_local_extrema(cls, n: int) -> None:
        """
        Marks a local minima and maxima in the list of historical points.
        The minimum is defined as the Point in the list which has the lowest low.
        The attribute <Point.minima> (and <Point.maxima>, respectively) is marked as True for the given point.
        :param n: last n number of points for finding extrema
        :return: None
        """
        minima = min(cls.single_patterns[-n:], key=lambda p: p.low)
        maxima = max(cls.single_patterns[-n:], key=lambda p: p.high)

        # If extrema is first or last in list, we are in the middle of a trend. Thus, the
        # point cannot be determined as an extrema.
        if minima not in [cls.single_patterns[-(n+2):][0], cls.single_patterns[-(n+2):][-1]]:
            minima.minima = True
        if maxima not in [cls.single_patterns[-(n+2):][0], cls.single_patterns[-(n+2):][-1]]:
            maxima.maxima = True
