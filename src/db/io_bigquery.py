#!/usr/bin/env python3

import json
from typing import List, Dict, Any, Literal, Optional

import pandas as pd
from google.cloud import bigquery as bq
from google.oauth2 import service_account as sa


class BQ(object):
    """
    Database connector class for handling data in a MariaDB.
    The MariaDB module handles the connection between Python and the database. This class wraps
    necessary functionality to interact with the database.
    The config file in form of .yaml is not released to git for safety reasons.
    """

    def __init__(self, connector_info: dict) -> None:
        self.connector_info = connector_info.get('dbinfo')
        self.project = self.connector_info.get("project")
        self.dataset = self.connector_info.get("dataset")
        self.quest_table = self.connector_info.get("quest_table")
        self.season_table = self.connector_info.get("season_table")
        self.credentials = self.connector_info.get("sa_key")
        self.client = self._initiate_client()
        assert self.test_connection(), "Cloud not find any datasets with BigQuery client."

    def test_connection(self) -> bool:
        """
        Asserts that at least 1 dataset is found in the project.
        :return: A boolean corresponding to the query.
        """
        return bool(len(list(self.client.list_datasets())))

    def _initiate_client(self) -> bq.Client:
        """
        Initiates the bigquery client.
        :return: The bigquery client.
        """
        credentials = sa.Credentials.from_service_account_info(json.loads(self.credentials))
        return bq.Client(project=self.project, credentials=credentials)

    def _initiate_table(self, table: str) -> None:
        """
        Sets the active table.
        :param table: The table to initiate.
        :return: None, as the table is set directly.
        """
        self.table = self.client.get_table(f"{self.project}.{self.dataset}.{table}")

    def insert_row(self, row: List[Dict[str, Any]], table) -> bool:
        """
        Inserts a row into a bigquery table.
        :param row: The corresponding row to insert.
        :param table, The designated table to insert data into.
        :return: A boolean that determines whether any errors were intercepted.
        """
        bq_uri = '.'.join((self.project, self.dataset, table))
        errors = self.client.insert_rows_json(bq_uri, row)
        print(f"Insertion errors into {table}: {errors}")
        return bool(len(errors))

    def construct_row(self, data: List[Any]) -> Dict[str, Any]:
        """
        Constructs a dict with columns as keys pandas data objects as values.
        :param data: The corresponding data to merge with the columns from the table schema.
        :return: A dictionary with columns as keys and data as values.
        """
        try:
            return {column.name: value for column, value in zip(self.table.schema, data)}
        except AttributeError:
            print("Row is malformed!")
            return {}
