"""Module containing all entrypoints"""

from pathlib import Path

from free2move.create_table import drop_table, create_table, get_tables
from free2move.insert_data import insert_data
from free2move.statistics import get_statistics_period, get_statistics_day, get_repeaters
from free2move.utils import get_conn, get_csv_folder_path


def entrypoint_drop_tables(conn_args):
    """Entrypoint to drop all tables"""

    print("\nDrop tables:")

    conn = get_conn(conn_args=conn_args)
    cursor = conn.cursor()

    for dict_table in get_tables():
        drop_table(
            cursor=cursor,
            table=dict_table["table"]
        )

    conn.commit()
    conn.close()


def entrypoint_create_tables(conn_args):
    """Entrypoint to create all tables"""

    print("\nCreate tables:")

    conn = get_conn(conn_args=conn_args)
    cursor = conn.cursor()

    for dict_table in get_tables():
        create_table(
            cursor=cursor,
            table=dict_table["table"],
            sql_statement=dict_table["sql_statement"]
        )

    conn.commit()
    conn.close()


def entrypoint_insert_data(conn_args, csv_folder_path=get_csv_folder_path(), error_folder_path="/tmp"):
    """Entrypoint to insert data"""

    print("\nInsert data:")

    for dict_table in get_tables():
        table = dict_table["table"]
        csv_filepath = Path(csv_folder_path, f"{table.lower()}.csv")
        data_error = insert_data(
            conn_args=conn_args,
            table=table,
            csv_filepath=csv_filepath
        )
        print(f"data not inserted:\n{data_error}")
        error_filepath = Path(error_folder_path, f"error_{table.lower()}.csv")
        data_error.to_csv(error_filepath)


def entrypoint_question1(conn_args, csv_folder_path=get_csv_folder_path(), error_folder_path="/tmp"):
    """Entrypoint for the question 1"""

    entrypoint_drop_tables(conn_args=conn_args)
    entrypoint_create_tables(conn_args=conn_args)
    entrypoint_insert_data(
        csv_folder_path=csv_folder_path,
        error_folder_path=error_folder_path,
        conn_args=conn_args
    )


def entrypoint_question2(conn_args, datetime_str):
    """Entrypoint for the question 2"""

    conn = get_conn(conn_args=conn_args)
    cursor = conn.cursor()

    data_results = get_statistics_day(
        cursor=cursor,
        datetime_str=datetime_str
    )

    conn.close()

    return data_results


def entrypoint_question3(conn_args, start_datetime_str, end_datetime_str):
    """Entrypoint for the question 3"""

    conn = get_conn(conn_args=conn_args)
    cursor = conn.cursor()

    data_results = get_statistics_period(
        cursor=cursor,
        start_datetime_str=start_datetime_str,
        end_datetime_str=end_datetime_str
    )

    conn.close()

    return data_results


def entrypoint_question4(conn_args):
    """Entrypoint for the question 4"""

    conn = get_conn(conn_args=conn_args)
    cursor = conn.cursor()

    nb_repeaters = get_repeaters(cursor=cursor)

    conn.close()

    return nb_repeaters
