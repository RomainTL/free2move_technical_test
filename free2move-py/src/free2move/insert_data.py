"""Module containing methods used to insert data"""

from pandas import DataFrame, read_csv
from psycopg2.errors import DatetimeFieldOverflow, ForeignKeyViolation, NotNullViolation, UniqueViolation  # pylint: disable=E0611
from tqdm import tqdm

from free2move.utils import get_conn


def get_dtype(table):
    """Get dtype depending of the table"""

    dtype = {}

    if table == "CUSTOMERS":
        dtype["customer_zip_code_prefix"] = object

    return dtype


def insert_data(conn_args, table, csv_filepath):
    """Insert data in a table from a csv_filepath according to the conn_args"""

    print(f"\t{table}..")

    conn = get_conn(conn_args=conn_args)
    cursor = conn.cursor()

    data = read_csv(csv_filepath, dtype=get_dtype(table=table))
    cols = ",".join(data.columns)

    data_dict_errors = []
    for i in tqdm(data.index):
        vals = [
            data.at[i, col] if not isinstance(data.at[i, col], str) else data.at[i, col].replace("'", "''")
            for col in data.columns
        ]
        vals = tuple(vals) if len(vals) > 1 else f"('{vals[0]}')"
        query = f"INSERT INTO {table} ({cols}) VALUES {vals}"
        query_without_nan = query.replace("nan", "NULL").replace('"', "'")
        try:
            cursor.execute(query_without_nan)
            conn.commit()
        except (DatetimeFieldOverflow, ForeignKeyViolation, NotNullViolation, UniqueViolation) as error:
            data_dict_error = data.loc[i].to_dict()
            data_dict_error["error_msg"] = str(error)
            data_dict_errors.append(data_dict_error)
            conn.close()
            conn = get_conn(conn_args=conn_args)
            cursor = conn.cursor()

    conn.close()

    return DataFrame(data_dict_errors)
