"""
Fetches required data sources for the hackathon.
Inserts the data into MariaDB.
"""
# Global imports
import json
import sys
from pathlib import Path

import mariadb
import pandas as pd

from src.db.db_utility import establish_connection_mariadb

# Local imports
from src.db.io_mariadb import MARIADB

# Global scope
PROJECT_ROOT = Path.cwd().parent.parent


def main() -> None:
    """
    Main function.
    :return: None.
    """
    integrationevents_path = PROJECT_ROOT / "source" / "source=lw-go-events"
    database_path = integrationevents_path.__str__().split('=')[1]
    mdb_connector = setup_connection(database_path)
    load_data_from_parquet(integrationevents_path, db_connector=mdb_connector)
    return None


def setup_connection(db: str) -> MARIADB:
    """
    Sets up the initial connection to the database.
    :param db: The database name.
    :return: None.
    """

    db_config = PROJECT_ROOT / "config" / "mariadb.yaml"
    mdb = establish_connection_mariadb(str(db_config), database=db)
    print(f"Connected to database: '{db}'") if mdb.test_connection() else print("error")
    return mdb


def load_data_from_parquet(path: Path, db_connector: MARIADB) -> None:
    """

    :param path:
    :param db_connector:
    :return:
    """
    for folder in [f for f in path.iterdir() if f.is_dir()]:
        table = folder.__str__().split('=')[-1]
        for day in [f for f in folder.iterdir() if f.is_dir()]:
            for source_path in [f for f in day.iterdir() if f.is_file() and ".snappy.parquet" in f.__str__()]:
                event = pd.read_parquet(source_path, engine="pyarrow")
                json_struct = json.loads(event.to_json(orient="records"))
                event = pd.json_normalize(json_struct)
                while any(len(i) > 63 for i in event.columns):
                    event.columns = list(map(lambda x: ".".join(x.split('.')[1:]) if "." in x else x, event.columns))
                try:
                    event.drop(columns=event.columns[event.applymap(type).eq(list).any()], inplace=True)
                    db_connector.pd_insert_data(table_name=table, data=event)
                except Exception as e:
                    print(f"Encountered {e}")
                    pass

    return None


if __name__ == '__main__':
    main()
