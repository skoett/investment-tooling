#!/usr/bin/env python3


class Point(object):

    def __init__(self, open_price, close_price, high_price, low_price, timestamp):
        self.open = open_price
        self.close = close_price
        self.high = high_price
        self.low = low_price
        self.ts = timestamp
        self._bullish = False
        self._bearish = False
        self._minima = False
        self._maxima = False
        self.single_pattern = None
        self.dual_pattern = None
        self.triple_pattern = None

    @property
    def bearish(self) -> bool:
        return self._bearish

    @bearish.setter
    def bearish(self, value: bool) -> None:
        """
        Sets the bearish value
        :param value: The boolean value wrt. bearish
        :return:
        """
        self._bearish = value

    @property
    def bullish(self) -> bool:
        return self._bullish

    @bullish.setter
    def bullish(self, value: bool) -> None:
        """
        Sets the bullish value
        :param value: The boolean value wrt. bullish
        :return:
        """
        self._bullish = value

    @property
    def minima(self) -> bool:
        return self._minima

    @minima.setter
    def minima(self, value: bool) -> None:
        """
        Sets the minima value
        :param value: The boolean value wrt. minima
        :return: None.
        """
        self._minima = value

    @property
    def maxima(self) -> bool:
        return self._maxima

    @maxima.setter
    def maxima(self, value: bool) -> None:
        """
        Sets the maxima value
        :param value: The boolean value wrt. maxima
        :return:
        """
        self._maxima = value
