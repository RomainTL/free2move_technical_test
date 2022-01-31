from free2move.utils import get_conn_args

from free2move.entrypoints import entrypoint_question2, entrypoint_question3, entrypoint_question4


def get_conn_args_local():
    """Get conn_args in local"""

    conn_args = get_conn_args()
    conn_args["host"] = "localhost"

    return conn_args


def test_entrypoint_question2():
    """Test the function entrypoint_question2"""

    entrypoint_question2(
        conn_args=get_conn_args_local(),
        datetime_str="2017-01-23"
    )


def test_entrypoint_question3():
    """Test the function entrypoint_question3"""

    entrypoint_question3(
        conn_args=get_conn_args_local(),
        start_datetime_str="2017-01-23",
        end_datetime_str="2017-01-26"
    )


def test_entrypoint_question4():
    """Test the function entrypoint_question4"""

    entrypoint_question4(
        conn_args=get_conn_args_local()
    )
