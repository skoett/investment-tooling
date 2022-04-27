#!/usr/bin/env python3
import string

import pandas as pd
import mariadb
import sqlalchemy

from src.utils.utils import reformat_str_to_dt_format as reformat


class MARIADB(object):
    """
    Database connector class for handling data in a MariaDB.
    The MariaDB module handles the connection between Python and the database. This class wraps
    necessary functionality to interact with the database.
    The config file in form of .yaml is not released to git for safety reasons.
    """

    def __init__(self, db_info: dict, initial_database: str) -> None:
        self.db_info = db_info.get('dbinfo')
        self._user = self.db_info.get("dbUID")
        self._host = self.db_info.get("dbaddr")
        self._port = self.db_info.get("port")
        self._pwd = self.db_info.get("dbpwd")
        self._db = initial_database
        self.engine = None
        self.connector = None
        self.cursor = None
        assert self.test_connection(), "Connection to local database could not be established"

    def update_database(self, database: str) -> None:
        """
        Updates the database that is connected to.
        :param database: THe database name.
        :return: None.
        """
        try:
            self._db = database
            self.test_connection()
        except mariadb.Error as e:
            raise ConnectionError(f"Could not connect to stated database {database}. Got error: {e}")

    def test_connection(self) -> bool:
        """
        Tests the database connection to the Microsoft SQL Server
        :param self: Database information is contained in self.
        :return: True if connection is established
        """
        try:
            mariadb.connect(port=self._port,
                            host=self._host,
                            user=self._user,
                            password=self._pwd,
                            database=self._db,
                            autocommit=True)
            return True
        except ConnectionError:
            return False

    def _set_connector(self) -> None:
        """
        Sets the database connection
        :return: None
        """

        self.connector = mariadb.connect(port=self._port,
                                         host=self._host,
                                         user=self._user,
                                         password=self._pwd,
                                         database=self._db,
                                         autocommit=True)
        self.cursor = self.connector.cursor()

    def run_simple_query(self, sql: str) -> bool:
        """
        Runs a sql query in MariaDB using the set connector.
        :param sql: The query.
        :return: A boolean to determine whether the query was successful.
        """
        if self.connector is None:
            self._set_connector()
        try:
            self.cursor.execute(sql)
            return True
        except mariadb.Error as e:
            print(f"Error with query: {sql}\n\n error was: {e}")
            return False

    def get_data(self, query: str) -> pd.DataFrame:
        """
        Gets data from the corresponding query in the database connector
        :param self: Contains database connection information
        :param query: The query to get the data
        :return: The data in form of a Pandas DataFrame
        """
        if self.connector is None:
            self._set_connector()
        return pd.read_sql(query, self.connector)

    def get_bt_data(self, start: str, end: str, pair: str) -> pd.DataFrame:
        """
        Gets a view from the database based on a query with
        parameters. Start and end date are converted to fit the requirements from
        the WHERE-clause.
        :param start: The start date
        :param end: The end date
        :param pair: The corresponding currency pair
        :return: A Pandas DataFrame that contains the data
        """
        if self.connector is None:
            self._set_connector()
        assert len(str(start)) == 8 and start.isdigit(), "Start date is not well-formed!"
        assert len(str(end)) == 8 and end.isdigit(), "End date is not well-formed!"
        assert end > start, "End date is prior or equals to start date!"
        q = f'SELECT DT, BUY, SELL, OPEN, CLOSE, HIGH, LOW, VOL FROM {pair} ' + \
            f'WHERE DT BETWEEN {reformat(start)} AND {reformat(end)}'
        try:
            df = pd.read_sql_query(q, self.connector)
            df['DT'] = pd.to_datetime(df['DT'], dayfirst=True)
            return df
        except ConnectionError:
            return pd.empty

    def get_entire_table(self, table_name: str) -> pd.DataFrame:
        """
        Gets a view from the database based on a query with
        parameters. Start and end date are converted to fit the requirements from
        the WHERE-clause.
        :param table_name: The table name to extract data from
        :return: A Pandas DataFrame that contains the data
        """
        if self.connector is None:
            self._set_connector()
        assert self.check_if_table_exists(table_name), "table name does not exist"
        try:
            df = pd.read_sql_query(f'SELECT * FROM {table_name}', self.connector)
            return df
        except ConnectionError:
            return pd.empty

    def insert_row(self, query: str) -> None:
        """
        Inserts a row in the database from a complete query
        :param query: The query to execute
        :return: None
        """
        if self.connector is None:
            self._set_connector()
        cursor = self.connector.cursor()
        cursor.execute(query)

    def insert_data(self, query: str, data: pd.DataFrame, schema: list) -> None:
        """
        Inserts data in the database in correspondence with the given query
        :param self: Contains database connection information
        :param query: The query to insert the corresponding data
        :param data: The data in form of a Pandas DataFrame
        :param schema: The column names as list
        :return: None
        """
        if self.connector is None:
            self._set_connector()
        cursor = self.connector.cursor()
        for _, row in data.iterrows():
            tuple([str(row[col]) for col in schema])
            cursor.execute(query, tuple([str(row[col]) for col in schema]))

    def pd_insert_data(self, data: pd.DataFrame, table_name: str, schema: list = None,
                       chunks: int = 200000, mode: str = 'append') -> None:
        """
        Inserts data in the database in correspondence with the
        given Pandas DataFrame
        :param self: Contains database connection information
        :param data: The data in form of a Pandas DataFrame
        :param table_name: The table name to insert into
        :param schema: The table schema
        :param chunks: Defined chunk size to write at a time
        :param mode: Corresponding parameter for if_exists
        :return: None
        """
        if self.engine is None:
            self._set_engine()
        print(f"Inserting data into: {table_name}")
        data.to_sql(name=table_name, con=self.engine, schema=schema, if_exists=mode, chunksize=chunks, index=False)

    def create_table(self, query: str, table_name: str) -> None:
        """
        Creates a table in the database
        :param self: Contains database information
        :param query: The corresponding query with schema
        :param table_name: Table name for the new table
        :return: None
        """
        print(f"Creating table: {table_name}")
        if self.connector is None:
            self._set_connector()
        try:
            cursor = self.connector.cursor()
            cursor.execute(query)
        except ConnectionError as error:
            print(f"Could not create table {table_name}.. {error}")

    def check_if_table_exists(self, table_name: str) -> bool:
        """
        Checks if a table exists in the database.
        Returns a boolean
        :param table_name: Name of the table we want to check
        :return: True if found, False otherwise
        """
        if self.connector is None:
            self._set_connector()
        cursor = self.connector.cursor()
        cursor.execute(f" SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'")
        if cursor.fetchone()[0] == 1:
            return True
        return False

    def _set_engine(self) -> None:
        """
        Creates and sets the sqlAlchemy engine to establish connection to MariaDB for inserting
        entire Pandas DataFrames.
        :return: None.
        """
        self.engine = sqlalchemy.create_engine(
            f"mariadb+mariadbconnector://{self._user}:{self._pwd}@{self._host}:{self._port}/{self._db}"
        )
