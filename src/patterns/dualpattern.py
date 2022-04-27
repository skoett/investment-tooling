#!/usr/bin/env python3

from src.patterns.pattern import Pattern


class DualPatterns(Pattern):

    def __init__(self):
        super(DualPatterns, self).__init__()

    def all_dual_patterns(self) -> bool:
        """
        Wrapper around all single candle pattern functions.
        :return: True if either spinning top is identified.
        """
        return any([self.marabozu_doji_wrapper(),
                    self.engulfing_wrapper()])

    def marabozu_doji_wrapper(self) -> bool:
        """
        A wrapper function for both dual marabozu-doji patterns. Returns true if any is found in the last two
        candles.
        :return: True if either spinning top is identified.
        """
        if len(self.single_patterns) < 2:
            return False
        return any([self.black_marabozu_doji(), self.white_marabozu_doji()])

    def white_marabozu_doji(self) -> bool:
        """
        A white marabozu (or long, white candle) followed by a doji indicates that buyers are becoming exhausted.
        Prices cannot continue to rise unless more buyers arrive, which are unlikely. sellers are then trying to
        get in cheap and push the price down.
        :return: True if either spinning top is identified.
        """
        condition = 'White Marabozu' in self.single_patterns[-2].single_pattern and (
                'Long Legged Doji' == self.single_patterns[-1].single_pattern or
                'Gravestone Doji' == self.single_patterns[-1].single_pattern or
                'Four Price Doji' == self.single_patterns[-1].single_pattern or
                'Dragonfly Doji' == self.single_patterns[-1].single_pattern
        )
        return self.eval_dual_condition(condition, self.single_patterns[-2:], "White Marabozu Doji")

    def black_marabozu_doji(self) -> bool:
        """
        A Black marabozu (or long, black candle) followed by a doji indicates that sellers are becoming exhausted.
        More sellers are needed to continue the downtrend, but no more are likely to exist. Thus, buyers might try
        to get in and get a favourable trade where prices are likely to go up.
        :return: True if either spinning top is identified.
        """
        condition = 'Black Marabozu' == self.single_patterns[-2].single_pattern and (
                'Long Legged Doji' == self.single_patterns[-1].single_pattern or
                'Gravestone Doji' == self.single_patterns[-1].single_pattern or
                'Four Price Doji' == self.single_patterns[-1].single_pattern or
                'Dragonfly Doji' == self.single_patterns[-1].single_pattern
        )
        return self.eval_dual_condition(condition, self.single_patterns[-2:], "Black Marabozu Doji")

    def tweezer_wrapper(self) -> bool:
        """
        Tweezers are candlestick reversal patterns.
        :return: True if either spinning top is identified.
        """
        if len(self.single_patterns) < 2:
            return False
        return any([self.tweezer_bottom(), self.tweezer_top()])

    def tweezer_bottom(self) -> bool:
        """
        https://www.babypips.com/forexpedia/tweezer-bottom
        A Tweezer Bottom is a bullish reversal pattern seen at the bottom of downtrends and consists of two Japanese
        candlesticks with matching bottoms. The matching bottoms are usually composed of shadows (or wicks) but can be
        the candle’s bodies as well. A Tweezer Bottom occurs during a downtrend when sellers push prices lower, often
        ending the session near the lows, but were not able to push the bottom any further.
        Tweezer Bottoms are considered to be short-term bullish reversal patterns that signal a market bottom.
        Recognition criteria:
        1. There must be two or more consecutive candles of either color.
        2. A clear downtrend should be present.
        3. Both candles must reach the same low point.
        :return: True if either spinning top is identified.
        """
        condition = (self.single_patterns[-2].low == self.single_patterns[-1].low
                     and self._def_tweezer_xor()
                     and self._any_two_is_minima())
        return self.eval_dual_condition(condition, self.single_patterns[-2:], "Tweezer Bottom")

    def tweezer_top(self) -> bool:
        """
        A Tweezer Top is a bearish reversal pattern seen at the top of uptrends and consists of two Japanese
        candlesticks with matching tops. The matching tops are usually composed of shadows (or wicks) but can be the
        candle’s bodies as well. A Tweezer Top occurs during an uptrend when buyers push prices higher, often ending
        the session near the highs, but were not able to push the top any further.
        Recognition criteria:
        1. There must be two or more consecutive candles of either color.
        2. A clear uptrend should be present.
        3. Both candles must reach the same high point.
        :return: True if either spinning top is identified.
        """
        condition = (self.single_patterns[-2].high == self.single_patterns[-1].high
                     and self._def_tweezer_xor()
                     and self._any_two_is_maxima())
        return self.eval_dual_condition(condition, self.single_patterns[-2:], "Tweezer Top")

    def engulfing_wrapper(self) -> bool:
        """

        :return: True if either spinning top is identified.
        """
        if len(self.single_patterns) < 2:
            return False
        return any([self.bullish_engulfing(), self.bearish_engulfing()])

    def bullish_engulfing(self) -> bool:
        """
        The Bullish Engulfing pattern is a two candlestick reversal pattern that signals a strong up move may occur.
        It happens when a bearish candle is immediately followed by a larger bullish candle. This second candle
        “engulfs” the bearish candle. This means buyers are flexing their muscles and that there could be a strong
        up move after a recent downtrend or a period of consolidation.
        :return: True if either spinning top is identified.
        """
        condition = (self.single_patterns[-2].bearish and
                     abs(self.single_patterns[-2].open - self.single_patterns[-2].close) <
                     abs(self.single_patterns[-1].high - self.single_patterns[-1].low) and self._any_two_is_minima)
        return self.eval_dual_condition(condition, self.single_patterns[-2:], "Bullish Engulfing")

    def bearish_engulfing(self) -> bool:
        """
        The Bearish Engulfing pattern is a two candlestick reversal pattern that signals a strong down move may occur.
        It happens when a bullish candle is immediately followed by a larger bearish candle. This second candle
        “engulfs” the bullish candle. This means buyers are flexing their muscles and that there could be a strong
        up move after a recent downtrend or a period of consolidation.
        :return: True if either spinning top is identified.
        """
        condition = (self.single_patterns[-2].bullish and
                     abs(self.single_patterns[-2].open - self.single_patterns[-2].close) <
                     abs(self.single_patterns[-1].open - self.single_patterns[-1].close) and self._any_two_is_maxima)
        return self.eval_dual_condition(condition, self.single_patterns[-2:], "Bearish Engulfing")

    def _def_tweezer_xor(self) -> bool:
        """
        Returns the xor of the color between the two points used in a tweezer top or bottom
        :return: a boolean according to the xor result
        """
        return (self.single_patterns[-2].bearish != self.single_patterns[-1].bearish and
                self.single_patterns[-2].bullish != self.single_patterns[-1].bullish)

    def _any_two_is_minima(self) -> bool:
        """
        Returns true if either points are a local minima.
        :return: A boolean if the condition is satisfied.
        """
        return self.single_patterns[-2].minima or self.single_patterns[-1].minima

    def _any_two_is_maxima(self) -> bool:
        """
        Returns true if either points are a local maxima.
        :return: A boolean if the condition is satisfied.
        """
        return True if any([self.single_patterns[-2].maxima, self.single_patterns[-1].maxima]) else False
