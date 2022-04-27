#!/usr/bin/env python3
"""

"""
import pandas
import plotly.graph_objects as go
from typing import List

from src.patterns.pattern import Pattern
from src.frontend.hover_content import hover_content_by_object_list_comprehension


def create_plot(df: pandas.DataFrame, hover_text: List) -> go.Figure:
    """

    :param df:
    :param hover_text:
    :return:
    """
    return go.Figure(data=go.Candlestick(x=df.DT,
                                         open=df.OPEN,
                                         high=df.HIGH,
                                         low=df.LOW,
                                         close=df.CLOSE,
                                         text=hover_text,
                                         hoverinfo='text'))


def create_hover_text(df: pandas.DataFrame, pattern: Pattern) -> List:
    """

    :param df:
    :param pattern:
    :return:
    """
    return df.apply(lambda x: hover_content_by_object_list_comprehension(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7],
                                                                         pattern), axis=1)


def build_and_create_plot(df: pandas.DataFrame, pattern: Pattern) -> go.Figure:
    """
    Wrapper function to construct the candlestick plot with comprehensive hover text
    :param df: The dataframe that contains the data
    :param pattern: The pattern class
    :return: A Plotly Figure
    """
    hover_text = create_hover_text(df=df, pattern=pattern)
    fig = create_plot(df=df, hover_text=hover_text)
    return fig
