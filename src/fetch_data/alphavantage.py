"""
Fetches required data sources for the hackathon.
Inserts the data into MariaDB.
"""
# Global imports
from pathlib import Path
from src.db.db_utility import establish_connection_mariadb

# Local imports
from src.db.io_mariadb import MARIADB


def setup_connection(db: str) -> MARIADB:
    """
    Sets up the initial connection to the database.
    :param db: The database name.
    :return: None.
    """
    project_root = Path.cwd().parent.parent
    db_config = project_root / "config" / "mariadb.yaml"
    mdb = establish_connection_mariadb(str(db_config), database=db)
    print("connected") if mdb.test_connection() else print("error")
    return mdb


if __name__ == '__main__':
    database = "crypto"
    setup_connection(database)
