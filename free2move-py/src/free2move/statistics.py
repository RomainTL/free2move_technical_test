"""Module containing methods used to get statistics"""

from datetime import datetime

from pandas import DataFrame


def get_statistics_day(cursor, datetime_str):
    """Get statistics according a day (q2)"""

    try:
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d")
    except (TypeError, ValueError) as error:
        error_msg = f"Argument datetime_str invalid: '{datetime_str}'" \
        f"\nReason: {error}" \
        "\nExpected datetime_str format: '2017-01-23'"
        return error_msg

    sql_statement = f"""
        SELECT
            c.customer_unique_id,
            SUM(i.price) as total_spending,
            COUNT(i.price) as products_number,
            COUNT(DISTINCT c.customer_id) as customers_number
        FROM customers c
        INNER JOIN orders o
        ON c.customer_id = o.customer_id
        INNER JOIN items i
        ON o.order_id = i.order_id
        GROUP BY o.order_purchase_timestamp, c.customer_unique_id
        HAVING date(o.order_purchase_timestamp) = date('{datetime_obj}')
        ORDER BY total_spending DESC;
    """
    cursor.execute(sql_statement)
    results = cursor.fetchall()

    columns = ["customer_unique_id", "total_spending", "products_number", "customers_number"]
    data_results = DataFrame(results, columns=columns)

    return data_results


def get_statistics_period(cursor, start_datetime_str, end_datetime_str):
    """Get statistics according a period (q3)"""

    try:
        start_datetime_obj = datetime.strptime(start_datetime_str, "%Y-%m-%d")
    except (TypeError, ValueError) as error:
        error_msg = f"Argument start_datetime_obj invalid: '{start_datetime_str}'" \
        f"\nReason: {error}" \
        "\nExpected start_datetime_obj format: '2017-01-23'"
        return error_msg

    try:
        end_datetime_obj = datetime.strptime(end_datetime_str, "%Y-%m-%d")
    except (TypeError, ValueError) as error:
        error_msg = f"Argument end_datetime_obj invalid: '{end_datetime_str}'" \
        f"\nReason: {error}" \
        "\nExpected end_datetime_obj format: '2017-01-26'"
        return error_msg

    sql_statement = f"""
        SELECT
            c.customer_unique_id,
            SUM(i.price) as total_spending,
            COUNT(i.price) as products_number,
            COUNT(DISTINCT c.customer_id) as customers_number
        FROM customers c
        INNER JOIN orders o
        ON c.customer_id = o.customer_id
        INNER JOIN items i
        ON o.order_id = i.order_id
        GROUP BY o.order_purchase_timestamp, c.customer_unique_id
        HAVING date(o.order_purchase_timestamp) BETWEEN date('{start_datetime_obj}') AND date('{end_datetime_obj}')
        ORDER BY total_spending DESC;
    """
    cursor.execute(sql_statement)
    results = cursor.fetchall()

    columns = ["customer_unique_id", "total_spending", "products_number", "customers_number"]
    data_results = DataFrame(results, columns=columns)

    return data_results


def get_repeaters(cursor):
    """Get the number of repeaters (q4)"""

    sql_statement = """
    SELECT COUNT(*)
    FROM (
        SELECT c.customer_unique_id, COUNT(o.order_id)
        FROM customers c
        INNER JOIN orders o
        ON c.customer_id = o.customer_id
        GROUP BY c.customer_unique_id
        HAVING COUNT(o.order_id) > 1
    ) AS repeaters;
    """
    cursor.execute(sql_statement)
    nb_repeaters = cursor.fetchall()[0][0]

    return nb_repeaters
