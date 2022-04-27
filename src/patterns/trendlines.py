#!/bin/usr/env python3

from src.patterns.pattern import Pattern
from src.patterns.utils import (calculate_slope_by_points,
                                find_maxima_in_list_by_index,
                                find_minima_in_list_by_index)


class Trendlines(Pattern):

    def __init__(self):
        super(Trendlines, self).__init__()

    def downtrend(self, history: list, slope_threshold: float) -> None:
        """
        A downtrend is defined by a negative slope between two or more high points.
        The second (or last) high must be lower than the first high, thus yielding a negative slope.
        :param history: A list of the n previous points that can determine whether the current point
        is part of a downtrend
        :param slope_threshold: The required, absolute slope level to define a downtrend
        :return None
        """
        maxima_indices = find_maxima_in_list_by_index(history[:-1])
        if not maxima_indices:
            for point in maxima_indices:
                slope = calculate_slope_by_points(point,
                                                  history[-1],
                                                  'downtrend',
                                                  (history.index(history[-1]) - history.index(point)))
                if abs(slope) > slope_threshold:
                    self.trendlines.append(('downtrend', point, history[-1], slope))

    def uptrend(self, history: list, slope_threshold: float) -> None:
        """
        An uptrend is defined by a positive slope formed by two or more low points.
        The second (or last) low must be higher than the first low, thus yielding a positive slope.
        :param history: A list of the n previous points that can determine whether the current point
        is part of an uptrend.
        :param slope_threshold: The required, absolute slope level to define an uptrend.
        :return None.
        """
        minima_indices = find_minima_in_list_by_index(history[:-1])
        if not minima_indices:
            for point in minima_indices:
                slope = calculate_slope_by_points(point,
                                                  history[-1],
                                                  'uptrend',
                                                  (history.index(history[-1]) - history.index(point)))
                if abs(slope) > slope_threshold:
                    self.trendlines.append(('uptrend', point, history[-1], slope))
