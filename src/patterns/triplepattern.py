#!/usr/bin/env python3

from src.patterns.pattern import Pattern
from src.patterns.utils import (has_large_body_point,
                                has_small_body_point,
                                get_midpoint,
                                small_wick_up,
                                small_wick_low)


class TriplePatterns(Pattern):

    def __init__(self):
        super(TriplePatterns, self).__init__()

    def all_triple_patterns(self) -> bool:
        """
        Wrapper around all triple candle pattern functions.
        :return: True if either spinning top is identified.
        """
        return any([self.stars_wrapper(),
                    self.three_solid_wrapper(),
                    self.three_inside_wrapper()])

    def stars_wrapper(self) -> bool:
        """
        A wrapper function for both morning and evening star patterns.
        Returns true if any is found in the last three candles.
        :return: True if either pattern is identified.
        """
        if len(self.single_patterns) < 3:
            return False
        return any([self.morning_star(), self.evening_star()])

    def morning_star(self) -> bool:
        """
        The morning star is a bullish reversal pattern usually found at the end of a trend.
        It signifies a potential bottom of the weakness in a downtrend which might lead to a trend reversal.
        It's characteristics are:
        1. A long-bodied black candle extending the current downtrend
        2. A short middle candle that gapped down on the open
        3. A long-bodied white candle that gapped up on the open and closed above the midpoint of
        the body of the first candle.
        :return: True if the pattern is found, otherwise false.
        """
        # TODO add downtrend from trendlines
        candle_1, candle_2, candle_3 = tuple(self.single_patterns[-3:])
        condition_1 = candle_1.bearish and has_large_body_point(candle_1, threshold=50)
        condition_2 = has_small_body_point(candle_2, threshold=50)
        condition_3 = candle_3.bullish and has_large_body_point(candle_3, threshold=50) and \
            (candle_3.high > candle_3.close) and (candle_3.close > get_midpoint(candle_1))
        condition = condition_1 and condition_2 and condition_3
        return self.eval_triple_condition(condition, self.single_patterns[-3:], "Morning star")

    def evening_star(self) -> bool:
        """
        The evening star is a bearish reversal pattern usually found at the end of a trend.
        It consists of a large bullish candle, a small-bodied candle and a bearish candle.
        Evening star appears at the top of a price uptrend.
        THe characteristics are the following:
        1. The first candlestick is a bullish candle, which is part of a recent uptrend.
        2. The second candle has a small body, indicating that there could be some indecision in the market.
           This candle can be either bullish or bearish.
        3. The third candlestick acts as a confirmation that a reversal is in place, as the candle closes beyond the
        midpoint of the first candle.
        :return: True if the pattern is found, otherwise false.
        """
        # TODO add uptrend from trendlines
        # TODO assert that the conditions match the requirements above
        candle_1, candle_2, candle_3 = tuple(self.single_patterns[-3:])
        condition_1 = candle_1.bullish and has_large_body_point(candle_1, threshold=50)
        condition_2 = has_small_body_point(candle_2, threshold=50)
        condition_3 = candle_3.bearish and has_large_body_point(candle_3, threshold=50) and \
            (candle_3.low > candle_3.open) and (candle_3.open > get_midpoint(candle_1))
        condition = condition_1 and condition_2 and condition_3
        return self.eval_triple_condition(condition, self.single_patterns[-3:], "Evening star")

    def three_solid_wrapper(self) -> bool:
        """
        A wrapper function for both the black crows, and three white soldier patterns.
        Returns true if any is found in the last three candles.
        :return: True if either pattern is identified.
        """
        if len(self.single_patterns) < 3:
            return False
        return any([self.three_white_soldiers(), self.black_crows()])

    def three_white_soldiers(self) -> bool:
        """
        The Three White Soldiers is a bullish Japanese candlestick reversal pattern consisting of three consecutive
        white bodies, each with a higher close. The Three White Soldiers candlestick pattern marches upward, creating a
        staircase-like structure as the price climbs higher and higher. The pattern usually indicates a weakness in an
        established downtrend and the potential emergence of an uptrend. Each candle should open within the previous
        body and the close should be near the high of the candle.
        The characteristics are the following:
        1. There must be three long and bullish (i.e., white or green) candlesticks in a row.
        2. Each of those candles must open above the previous day’s open. Ideally, it will open in the middle price
           range of the previous day.
        3. Each candle must open progressively upward, establishing a new short-term high.
        4. The candles should have very small (or nonexistent) upper shadows/wicks.
        :return: True if either pattern is identified.
        """
        # TODO Add uptrend in condition 3
        candle_1, candle_2, candle_3 = tuple(self.single_patterns[-3:])
        condition_1 = candle_1.bullish and candle_2.bullish and candle_3.bullish and has_large_body_point(candle_1) \
            and has_large_body_point(candle_2) and has_large_body_point(candle_3)
        condition_2 = (candle_2.open > get_midpoint(candle_1)) and (candle_3.open > get_midpoint(candle_2))
        condition_3 = candle_1.high < candle_2.high < candle_3.high
        condition_4 = small_wick_up(candle_1) and small_wick_up(candle_2) and small_wick_up(candle_3)
        condition = condition_1 and condition_2 and condition_3 and condition_4
        return self.eval_triple_condition(condition, self.single_patterns[-3:], "Three white soldiers")

    def black_crows(self) -> bool:
        """
        The Three Black Crows candlestick pattern is just the opposite of the Three White Soldiers. It is formed when
        three bearish candles follow a strong UPTREND, indicating that a reversal is in the works. The second candle’s
        body should be bigger than the first candle and should close at or very near it's low. Finally, the third candle
        should be the same size or larger than the second candle’s body with a very short or no lower shadow.
        The characteristics are the following:
        1. There should be a prevailing uptrend in progress.
        2. There must be three long and bearish candlesticks in a row.
        3. Each of those candles must open below the previous day’s open.
        4. Ideally, it will open in the middle price range of the previous day
        5. Each candle must close progressively downward, establishing a new short-term low.
        6. The candles have very small (or nonexistent) lower wicks.
        :return: True if either pattern is identified.
        """
        # TODO Add uptrend in condition 3
        candle_1, candle_2, candle_3 = tuple(self.single_patterns[-3:])
        condition_1 = candle_1.bearish and candle_2.bearish and candle_3.bearish and has_large_body_point(candle_1) \
            and has_large_body_point(candle_2) and has_large_body_point(candle_3)
        condition_2 = (candle_2.open < get_midpoint(candle_1)) and (candle_3.open < get_midpoint(candle_2))
        condition_3 = candle_1.low > candle_2.low > candle_3.low
        condition_4 = small_wick_low(candle_1) and small_wick_low(candle_2) and small_wick_low(candle_3)
        condition = condition_1 and condition_2 and condition_3 and condition_4
        return self.eval_triple_condition(condition, self.single_patterns[-3:], "Black crows")

    def three_inside_wrapper(self) -> bool:
        """
        A wrapper function for both three inside up and down patterns.
        Returns true if any is found in the last three candles.
        :return: True if either pattern is identified.
        """
        if len(self.single_patterns) < 3:
            return False
        return any([self.three_inside_down(), self.three_inside_up()])

    def three_inside_up(self) -> bool:
        """
        The Three Inside Up candlestick formation is a trend-reversal pattern that is found at the bottom of a
        DOWNTREND. This triple candlestick pattern indicates that the downtrend is possibly over and that a new uptrend
        has started.
        It has the following traits:
        1. The first candle should be found at the bottom of a downtrend and is characterized by a long bearish
           candlestick.
        2. The second candle should at least make it up all the way up to the midpoint of the first candle.
        3. The third candlestick needs to close above the first candle’s high to confirm that buyers have overpowered
           the strength of the downtrend.
        :return: True if either pattern is identified.
        """
        condition = False
        return self.eval_triple_condition(condition, self.single_patterns[-3:], "Three inside up")

    def three_inside_down(self) -> bool:
        """
        The Three Inside Down candlestick formation is found at the top of an UPTREND. It means that the uptrend is
        possibly over and that a new downtrend has started.
        It has the following traits:
        1. The first candle should be found at the top of an uptrend and is characterized by a long bullish candlestick.
        2. The second candle should make it up all the way down the midpoint of the first candle.
        3. The third candlestick needs to close below the first candle’s low to confirm that sellers have overpowered
           the strength of the uptrend.
        :return: True if either pattern is identified.
        """
        condition = False
        return self.eval_triple_condition(condition, self.single_patterns[-3:], "Three inside down")
