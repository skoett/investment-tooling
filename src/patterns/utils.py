#!/usr/bin/env python3

from typing import Tuple
from src.patterns.point import Point

import pandas as pd


def get_all_lengths(point: Point, inverted: bool) -> Tuple[float, float, float, float]:
    """
    Helper function to get all lengths from Point object
    :param point: The Point instance
    :param inverted: Whether open/close and high/low should be inverted
    :return: A tuple of floats with lengths
    """
    if inverted:
        body_len, total_len = point.close - point.open, point.high - point.low
        low_len, high_len = point.close - point.low, point.high - point.open
    else:
        body_len, total_len = point.open - point.close, point.high - point.low
        low_len, high_len = point.close - point.low, point.high - point.open
    return body_len, total_len, low_len, high_len


def get_total_body_lengths(point: Point, inverted: bool = False):
    """
    Helper function to get total length and body length from Point instance
    :param point: The Point instance
    :param inverted: Whether open/close should be inverted
    :return: A tuple of floats with corresponding lengths
    """
    if inverted:
        body_len, total_len = point.close - point.open, point.high - point.low
    else:
        body_len, total_len = point.open - point.close, point.high - point.low
    return body_len, total_len


def has_small_body(body_len: float, total_len: float, threshold: int = 25) -> bool:
    """
    Tests whether a candlestick has a small (defaults to <25%) body.
    A small body (between open and close) is 25% or less of the total size between high and low
    :param body_len: The body length
    :param total_len: The total length
    :param threshold: The threshold factor for indicating a small body. Defaults to 25
    :return: A boolean that indicates whether the body is small
    """
    return True if body_len == 0 or (body_len / total_len * 100) <= threshold else False


def has_large_body(body_len: float, total_len: float, threshold: int = 75) -> bool:
    """
    Tests whether a candlestick has a large (defaults to >75%) body.
    A large body (between open and close) is 75% or more of the total size between high and low
    :param body_len: The body length
    :param total_len: The total length
    :param threshold: The threshold factor for indicating a small body. Defaults to 25
    :return: A boolean that indicates whether the body is large
    """
    return True if body_len / total_len * 100 >= threshold else False


def has_small_body_point(point: Point, threshold: int = 25) -> bool:
    """
    Tests whether a candlestick has a small (defaults to <25%) body.
    A small body (between open and close) is 25% or less of the total size between high and low
    :param point: The point to evaluate
    :param threshold: The threshold factor for indicating a small body. Defaults to 25
    :return: A boolean that indicates whether the body is small
    """
    body_len, total_len = get_total_body_lengths(point)
    return True if body_len == 0 or (body_len / total_len * 100) <= threshold else False


def has_large_body_point(point: Point, threshold: int = 75) -> bool:
    """
    Tests whether a candlestick has a large (defaults to >75%) body.
    A large body (between open and close) is 75% or more of the total size between high and low
    :param point: The point to evaluate.
    :param threshold: The threshold factor for indicating a small body. Defaults to 25
    :return: A boolean that indicates whether the body is large
    """
    body_len, total_len = get_total_body_lengths(point)
    return True if body_len / total_len * 100 >= threshold else False


def get_midpoint(point: Point) -> float:
    """
    Gets the midpoint of a candlestick
    :param point: The point to get the midpoint from
    :return: The midpoint as float
    """
    return (point.low + point.high) / 2


def small_wick_up(point: Point, threshold: int = 25) -> bool:
    """
    Determines whether a point has a small wick.
    :param point:  THe point to assert the wick
    :param threshold: The threshold for determine whether the wick is small or not
    :return: A boolean in correspondence to the size of the wick
    """
    body_len = abs(point.open - point.close)
    upper_len = abs(point.open - point.high)
    try:
        difference = ((body_len - upper_len) / ((body_len - upper_len) / 2)) * 100
        return True if difference <= threshold else False
    except ZeroDivisionError:
        return False


def small_wick_low(point: Point, threshold: int = 25) -> bool:
    """
    Determines whether a point has a small wick.
    :param point:  THe point to assert the wick
    :param threshold: The threshold for determine whether the wick is small or not
    :return: A boolean in correspondence to the size of the wick
    """
    body_len = abs(point.open - point.close)
    lower_len = abs(point.open - point.low)
    try:
        difference = ((body_len - lower_len) / ((body_len - lower_len) / 2)) * 100
        return True if difference <= threshold else False
    except ZeroDivisionError:
        return False


def shooting_star_hammer_hanging_helper(point: Point, inverted: bool, threshold: int = 25) -> Tuple[bool, float, float]:
    """
    A wrapper to the logic in shooting star, hammer, inverted hammer and hanging man dojis.
    :param point: The Point instance
    :param inverted: Whether the length measurements should be inverted.
    :param threshold: The threshold for identifying a small body
    :return: A tuple with a bool and two floats
    """
    body_len, total_len, low_len, high_len = get_all_lengths(point, inverted=inverted)
    small_body = has_small_body(body_len=body_len, total_len=total_len, threshold=threshold)
    if body_len < 0 or body_len == total_len:
        small_body = False
    return small_body, high_len, low_len


def eval_extrema(p: Point) -> str:
    """
    Returns the extrema as string of a given point if any
    :param p: A point as described in the corresponding class
    :return: A String  that is dependent on the values inside Point
    """
    if p.minima and p.maxima:
        return 'Both local minima and maxima'
    if p.minima:
        return 'Local minima'
    if p.maxima:
        return 'Local maxima'
    return ''


def eval_bullish_bearish(p: Point) -> str:
    """
    Returns the signal of a given point if any
    :param p: A point as described in the corresponding class
    :return: A String that is dependent on the values inside Point
    """
    if p.bullish:
        return 'Bullish'
    elif p.bearish:
        return 'Bearish'
    return 'Neutral'


def find_minima_in_list_by_index(points: list) -> list:
    """
    Finds all minima in a list of points
    :param points: The list of points
    :return: A list of points that is minima
    """
    return [e for e, x in enumerate(points) if x.minima]


def find_maxima_in_list_by_index(points: list) -> list:
    """
    Finds all minima in a list of points
    :param points: The list of points
    :return: A list of points that is minima
    """
    return [e for e, x in enumerate(points) if x.maxima]


def get_history(df: pd.DataFrame, index: int, offset: int) -> pd.DataFrame:
    """
    Gets the correct (row) slice of Pandas DataFrame in order to have history.
    :param df: The Pandas DataFrame object needed to create history slice
    :param index: The index of current timestamp
    :param offset: The size of the offset wanted
    :return: A Pandas DataFrame in correspondence with the wanted slice
    """
    return df.loc[index-offset:index]


def calculate_slope(x: float, y1: float, y2: float) -> float:
    """
    Calculates the slope between two points. One tick equals 1.0.
                     delta_y   y_2 - y_1   y_2 - y_1   rise
    Formula: Slope = ------- = --------- = ---------   ----
                     delta_x   x_2 - x_1       x       run
    :param x:  The absolute difference between x coordinates
    :param y1: First points y value
    :param y2: Second points y value
    :return: The given slope as a float
    """
    return (y2 - y1) / x


def calculate_slope_by_points(point1: Point, point2: Point, trend: str, x_difference: int) -> float:
    """
        Calculates the slope between two points. One tick equals 1.0.
                     delta_y   y_2 - y_1   y_2 - y_1   rise
    Formula: Slope = ------- = --------- = ---------   ----
                     delta_x   x_2 - x_1       x       run
    :param point1: The first point
    :param point2: The second point
    :param trend: Whether the direction is upwards or downwards.
    :param x_difference: the absolute x value to calculate the slope
    :return: The absolute float value between the two given points
    """
    if trend == 'uptrend':
        y = point2.low - point1.low
    elif trend == 'downtrend':
        y = point2.high - point1.high
    else:
        return 0.0  # soft fail
    return abs((y/x_difference)*100)
