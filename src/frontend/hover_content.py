#!/usr/bin/env python3
from datetime import datetime

import pandas as pd
from src.patterns.pattern import Pattern


def st_hover(dt: datetime, open_price: float, close_price: float, high_price: float, low_price: float,
             signal: str, single_pattern: str, dual_pattern: str, extrema: str = '') -> str:
    """
    Wrapper for generating most general data-part of the hover content.
    :param dt: The datetime.
    :param open_price: The open price.
    :param close_price: The closing price.
    :param high_price: The high price.
    :param low_price: The low price.
    :param signal: The signal.
    :param single_pattern: The single pattern.
    :param dual_pattern: The dual pattern.
    :param extrema: The extrema value.
    :return: A string corresponding to the standard hover content.
    """
    standard = str(dt) + '<br>Open: ' + str(open_price) + '<br>Close: ' + str(close_price) + \
                         '<br>High: ' + str(high_price) + '<br>Low: ' + str(low_price)

    if signal != 'None':
        standard += '<br>Signal: ' + signal
    if single_pattern != 'None':
        standard += '<br>Single Pattern: ' + single_pattern
    if dual_pattern != 'None':
        standard += '<br>Dual Pattern: ' + dual_pattern
    if extrema:
        standard += '<br>Extrema: ' + extrema
    return standard


def hover_content(row: pd.Series, signal: str, single_pattern: str, dual_pattern: str) -> str:
    """
    Reforms the content of the hover text in correspondence with the content.
    I.e. remove blank lines etc.
    :param row: A Pandas Series as a row
    :param signal: A signal as string
    :param single_pattern: A single pattern as string
    :param dual_pattern: A dual pattern as string
    :return: Returns a string that is a hover text line
    """
    standard = st_hover(dt=row.DT, open_price=row.OPEN, close_price=row.CLOSE, high_price=row.HIGH, low_price=row.LOW,
                        signal=signal, single_pattern=single_pattern, dual_pattern=dual_pattern)
    return standard


def hover_content_by_object(row: pd.Series, pattern: Pattern) -> str:
    """
    Reforms the content of the hover text in correspondence with the content.
    I.e. remove blank lines etc.
    :param row: A Pandas Series as a row
    :param pattern: The Pattern object
    :return: Returns a string that is a hover text line
    """
    signal = Pattern.return_signals_by_row(row)
    single_pattern, dual_pattern = Pattern.return_conditions_by_row(row)
    extrema = pattern.return_extrema_by_row(row)
    standard = st_hover(dt=row.DT, open_price=row.OPEN, close_price=row.CLOSE, high_price=row.HIGH, low_price=row.LOW,
                        signal=signal, single_pattern=single_pattern, dual_pattern=dual_pattern, extrema=extrema)
    return standard


def hover_content_by_object_list_comprehension(dt: datetime,
                                               _buy: float,
                                               _sell: float,
                                               open_price: float,
                                               close_price: float,
                                               high_price: float,
                                               low_price: float,
                                               _volume: float,
                                               pattern: Pattern) -> str:
    """
    Reforms the content of the hover text in correspondence with the content.
    I.e. remove blank lines etc.
    :param dt: Datetime value as float
    :param _buy: Buy-value as float
    :param _sell: Sell-value as float
    :param open_price: Open value as float
    :param close_price: Close value as float
    :param high_price: High value as float
    :param low_price: Low value as float
    :param _volume: Volume value as float
    :param pattern: The Pattern object
    :return: Returns a string that is a hover text line
    """
    signal = pattern.return_signals_by_row_optimised(dt)
    single_pattern, dual_pattern = pattern.return_conditions_by_row_optimised(dt)
    extrema = pattern.return_extrema_by_row_optimised(dt)
    standard = st_hover(dt=dt, open_price=open_price, close_price=close_price, high_price=high_price,
                        low_price=low_price, signal=signal, single_pattern=single_pattern, dual_pattern=dual_pattern,
                        extrema=extrema)
    return standard
