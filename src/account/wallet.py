#!/usr/bin/env/ python3

import uuid


class Wallet(object):

    def __init__(self, starting_balance: float, currency: str, commission: float) -> None:
        """

        :param starting_balance: Starting balance for the simulation
        :param currency: The currency the starting balance is stated in
        :param commission: The commission per trade stated as a float
        """
        self.balance = starting_balance
        self.currency = currency
        self.commission = commission

    def buy_market_position(self, amount) -> uuid.UUID:
        """

        :param amount:
        :return: Should return an order object when implemented.
        """
        return NotImplemented

    def sell_market_position(self, order: uuid.UUID):
        """

        :param order:
        :return: should return some kind of boolean when implemented.
        """
        return NotImplemented

    def open_pending_order(self, pair: str, amount) -> uuid.UUID:
        """

        :param pair:
        :param amount:
        :return:
        """
        return NotImplemented

    def close_pending_order(self, order: uuid.UUID):
        """

        :param order:
        :return:
        """
        return NotImplemented
