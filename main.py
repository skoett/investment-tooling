#!/usr/bin/env python3

import plotly.io as pio

from src.account.wallet import Wallet
from src.db.db_utility import establish_connection_mariadb
from src.utils.backtest_utils import setup_parameters, setup_parameters_inheritance
from src.frontend.visualization import build_and_create_plot
from src.utils.utils import time_execution

pio.renderers.default = "chromium"

# Insert config path here:
CONFIG_PATH = ''
DATABASE = ''


@time_execution
def main() -> None:
    """
    Main loop.
    :return: None.
    """
    # Setup configuration for back testing
    config = setup_parameters("../../config/backtest.yaml")

    # Setup database information and connect. Get sample data for a single pair from the database
    db_conn = establish_connection_mariadb(config.return_value('db_path'), database=DATABASE)
    conf = config.return_value('backtest')
    df = db_conn.get_bt_data(conf.get('start_date'), conf.get('end_date'), conf.get('pairs')[0])

    # Set up account for backtesting a strategy
    account = Wallet(conf.get('start_capital'), conf.get('currency'), conf.get('commission'))
    print(f"Current balance is: {account.balance} {account.currency} with a commission of {account.commission * 100}%")

    # Initialize strategy
    #
    #
    # Execute backtest
    backtest = setup_parameters_inheritance("../../config/backtest.yaml", df)
    backtest.execute()

    # Construct candlestick graph with comprehensive hover text
    fig = build_and_create_plot(df=df, pattern=backtest.patterns)

    # Show generated plot
    if config.return_value('show_output'):
        fig.show()


if __name__ == '__main__':
    main()
