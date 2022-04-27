#!/usr/bin/env python3

from src.patterns.point import Point
from src.patterns.pattern import Pattern
from src.patterns.utils import (get_total_body_lengths,
                                has_small_body,
                                shooting_star_hammer_hanging_helper)


class SinglePatterns(Pattern):

    def __init__(self):
        super(SinglePatterns, self).__init__()

    def all_single_patterns(self, point: Point) -> bool:
        """
        Wrapper around all single candle pattern functions.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: True if either spinning top is identified.
        """
        return True \
            if any([self.spinning_tops(point),
                    self.hammer_hanging_shooting_star_patterns(point),
                    self.marabozu_patterns(point),
                    self.doji_patterns(point)]) \
            else self.eval_single_condition(True, point, '')

    def spinning_tops(self, point: Point) -> bool:
        """
        Wrapper function for spinning tops.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: True if either spinning top is identified.
        """
        return any([self.white_spinning_top(point), self.black_spinning_top(point)])

    def black_spinning_top(self, point: Point) -> bool:
        """
        Black spinning tops indicates indecision between buyers and sellers, where neither part could influence a
        significant trend. If a black spinning top appears, it indicates that there are not many sellers left, thus
        a reversal could be near.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp.
        :return: True if a white spinning top is found in the given point.
        """
        body_len, total_len = get_total_body_lengths(point=point, inverted=False)
        if body_len < 0 or body_len == total_len:
            return False
        midpoint = (point.low + point.high) / 2
        small_body = has_small_body(body_len=body_len, total_len=total_len)
        # It must have a small body and the midpoint must be between open and close
        condition = small_body is True and point.close < midpoint < point.open
        return self.eval_single_condition(condition, point, 'Black Spinning Top')

    def white_spinning_top(self, point: Point) -> bool:
        """
        White spinning tops indicates indecision between buyers and sellers, where neither part could influence a
        significant trend. If a black spinning top appears, it indicates that there are not many buyers left, thus
        a reversal could be near.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp.
        :return: True if a white spinning top is found in the given point.
        """
        body_len, total_len = get_total_body_lengths(point=point, inverted=True)
        if body_len < 0 or body_len == total_len:
            return False
        midpoint = (point.low + point.high) / 2
        small_body = has_small_body(body_len=body_len, total_len=total_len)
        # It must have a small body and the midpoint must be between open and close
        condition = small_body is True and point.open < midpoint < point.close
        return self.eval_single_condition(condition, point, 'White Spinning Top')

    def marabozu_patterns(self, point: Point) -> bool:
        """
        Wrapper function around white_marabozu and black_marabozu. Returns true if point is either marabozu.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: True if either marabozu is identified.
        """
        return any([self.white_marabozu(point), self.black_marabozu(point)])

    def white_marabozu(self, point: Point) -> bool:
        """
        A white marabozu indicates that buyers are in control. The candle opened at its lowest price and closed
        at its highest price. It normally starts a bullish continuation or a bullish reversal pattern. Thus:
        If a white marabozu forms at the end of an uptrend, a continuation is likely.
        If a white marabozu forms at the end of a downtrend, a reversal is likely.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: A boolean that indicates whether the pattern is present in the given point
        """
        condition = point.high == point.close and point.low == point.open and point.low != point.high
        return self.eval_single_condition(condition, point, 'White Marabozu')

    def black_marabozu(self, point: Point) -> bool:
        """
        A black marabozu indicates that the candle opened at its highest price and closed at its lowest price.
        I.e. sellers are in control which indicates a bearish continuation. Thus:
        If a black marabozu forms at the end of a downtrend, a continuation is likely.
        If a black marabozu forms at the end of an uptrend, a reversal is likely.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: A boolean that indicates whether the pattern is present in the given point
        """
        condition = point.high == point.open and point.low == point.close and point.low != point.high
        return self.eval_single_condition(condition, point, 'Black Marabozu')

    def doji_patterns(self, point: Point) -> bool:
        """
        Wrapper function around all doji functions. Returns true if point is recognized as doji.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: True if either marabozu is identified.
        """
        return any([self.long_legged_doji(point),
                    self.dragonfly_doji(point),
                    self.gravestone_doji(point),
                    self.four_price_doji(point)])

    def long_legged_doji(self, point: Point) -> bool:
        """
        Dojis are indicating that open and close are equivalent. High and Low differs, which gives four distinct
        variants of dojis. Long-legged dojis have both distance from open/close to both high and low.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: A boolean that indicates whether the pattern is present in the given point
        """
        condition = point.low < point.close == point.open < point.high or \
            point.high < point.close == point.open < point.low
        return self.eval_single_condition(condition, point, 'Long Legged Doji')

    def dragonfly_doji(self, point: Point) -> bool:
        """
        Dojis are indicating that open and close are equivalent. High and Low differs, which gives four distinct
        variants of dojis. Dragonfly dojis indicates that high, open and close are equal.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: A boolean that indicates whether the pattern is present in the given point
        """
        condition = point.open == point.close == point.high != point.low
        return self.eval_single_condition(condition, point, 'Dragonfly Doji')

    def gravestone_doji(self, point: Point) -> bool:
        """
        Dojis are indicating that open and close are equivalent. High and Low differs, which gives four distinct
        variants of dojis. Gravestone dojis signals that open, close and low are equal.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: A boolean that indicates whether the pattern is present in the given point
        """
        condition = point.open == point.close == point.low != point.high
        return self.eval_single_condition(condition, point, 'Gravestone Doji')

    def four_price_doji(self, point: Point) -> bool:
        """
        Dojis are indicating that open and close are equivalent. High and Low differs, which gives four distinct
        variants of dojis. Four price dojis are special as high, low, open and close are equal.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: A boolean that indicates whether the pattern is present in the given point
        """
        condition = point.open == point.close == point.high == point.low
        return self.eval_single_condition(condition, point, 'Four Price Doji')

    def hammer_hanging_shooting_star_patterns(self, point: Point) -> bool:
        """
        Wrapper function around all single pattern functions. Returns true if point is recognized as any.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: True if either marabozu is identified.
        """
        return any([self.hanging_man(point),
                    self.hammer(point),
                    self.inverted_hammer(point),
                    self.shooting_star(point)])

    def hanging_man(self, point: Point) -> bool:
        """
        Hanging man indicates a bearish reversal pattern and can mark a top or strong resistance level.
        It can signal that sellers are beginning to outnumber buyers as the low shadow is much longer than high shadow.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: A boolean that indicates whether the pattern is present in the given point
        """
        small_body, high_len, low_len = shooting_star_hammer_hanging_helper(point=point, inverted=False)
        condition = small_body and high_len * 4 < low_len and point.close != point.open
        return self.eval_single_condition(condition, point, 'Hanging Man')

    def hammer(self, point: Point) -> bool:
        """
        The hammer indicates a bullish reversal pattern and forms during downtrends.
        It can then indicate that prices are starting to rise again. It can signal that buyers are beginning
        to outnumber sellers as the low shadow is much longer than high shadow.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: A boolean that indicates whether the pattern is present in the given point
        """
        small_body, high_len, low_len = shooting_star_hammer_hanging_helper(point=point, inverted=True)
        condition = small_body and high_len * 4 < low_len and point.close != point.open
        return self.eval_single_condition(condition, point, 'Hammer')

    def inverted_hammer(self, point: Point) -> bool:
        """
        The inverted hammer indicates a bullish reversal pattern and forms during downtrends.
        It can then indicate that prices are starting to rise again. It can signal that buyers are trying to bid the
        price higher, where sellers are pushing the price down. It might indicate that everyone that wants to sell
        have already sold, thus only buyers are left and hence pushing the price upwards.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: A boolean that indicates whether the pattern is present in the given point
        """
        small_body, high_len, low_len = shooting_star_hammer_hanging_helper(point=point, inverted=True)
        condition = small_body and low_len * 4 < high_len and point.close != point.open
        return self.eval_single_condition(condition, point, 'Inverted Hammer')

    def shooting_star(self, point: Point) -> bool:
        """ REWRITE
        A shooting star indicates a bearish reversal pattern and forms during uptrends.
        It can then indicate that prices are starting to fall again as there are no buyers left. It can be seen
        by the long shadow, testing the candle, but ended near the opening price, as sellers are outnumbering buyers.
        :param point: A point is a data type consisting of high, low, close, open and the corresponding timestamp
        :return: A boolean that indicates whether the pattern is present in the given point
        """
        small_body, high_len, low_len = shooting_star_hammer_hanging_helper(point=point, inverted=False)
        condition = small_body and low_len * 4 < high_len and point.close != point.open
        return self.eval_single_condition(condition, point, 'Shooting Star')
