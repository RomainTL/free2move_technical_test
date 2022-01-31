import sys
from pathlib import Path

from psycopg2 import connect


def get_conn_args(database="mydb", user="user", password="password", host="mydb", port="5432"):
    """
    Get arguments for the connection to the PostgreSQL database server

    Parameters
    ----------
    database: str
        String of the database (default: "mydb")
    user: str
        String of the user (default: "user")
    password: str
        String of the password (default: "password")
    host: str
        String of the host (default: "mydb"), "mydb" in docker and "localhost" in local
    port: str
        String of the port (default: 5432)

    Returns
    -------
    conn_args: dict
        Dictionnary for the connection to the PostgreSQL database server

    """
    conn_args = {
        "database": database,
        "user": user,
        "password": password,
        "host": host,
        "port": port
    }

    return conn_args


def get_conn(conn_args):
    """
    Get connection to the PostgreSQL database server
    """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = connect(**conn_args)
    except Exception as error:
        print(error)
        sys.exit(1)

    return conn


def get_csv_folder_path():
    """Folder path of input data"""
    return Path("/tmp/data/")
