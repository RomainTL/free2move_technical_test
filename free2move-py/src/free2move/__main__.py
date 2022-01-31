"""Main module"""

import argparse
from pathlib import Path

from free2move.entrypoints import entrypoint_question1, entrypoint_question2, entrypoint_question3, entrypoint_question4
from free2move.utils import get_conn_args


def main():
    """
    Main entrypoint

        q1 example: docker exec free2move_container free2move -q 1
        q2 example: docker exec free2move_container free2move -q 2 -d 2017-01-23
        q3 example: docker exec free2move_container free2move -q 3 -s 2017-01-23 -e 2017-01-26
        q4 example: docker exec free2move_container free2move -q 4

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", dest="question", type=int, required=True, help="Number of question")
    parser.add_argument("-d", dest="datetime_str", type=str, required=False, default='2017-01-23',
                              help="q2 arg datetime_str format: '2017-01-23'")
    parser.add_argument("-s", dest="start_datetime_str", type=str, required=False, default='2017-01-23',
                              help="q3 arg start_datetime_str (format: '2017-01-23')")
    parser.add_argument("-e", dest="end_datetime_str", type=str, required=False, default='2017-01-26',
                              help="q3 arg end_datetime_str (format: '2017-01-26')")

    args = parser.parse_args()

    print(f"Question selected: {args.question}")

    answer_path = Path(f"/tmp/answer{args.question}")

    if args.question == 1:
        entrypoint_question1(conn_args=get_conn_args())

    elif args.question == 2:
        print(f"\tdatetime_str selected: {args.datetime_str}")
        answer = entrypoint_question2(
            conn_args=get_conn_args(),
            datetime_str=args.datetime_str
        )
        answer_path = answer_path.with_suffix(".csv")
        print(f"\nAnswer path: {answer_path.as_posix()}")
        answer.to_csv(answer_path, index=False)
        print(f"Answer:\n{answer}")

    elif args.question == 3:
        print(f"\tstart_datetime_str selected: {args.datetime_str}")
        print(f"\tend_datetime_str selected: {args.datetime_str}")
        answer = entrypoint_question3(
            conn_args=get_conn_args(),
            start_datetime_str=args.start_datetime_str,
            end_datetime_str=args.end_datetime_str
        )
        answer_path = answer_path.with_suffix(".csv")
        print(f"\nAnswer path: {answer_path.as_posix()}")
        answer.to_csv(answer_path, index=False)
        print(f"\nAnswer:\n{answer}")

    elif args.question == 4:
        answer = entrypoint_question4(
            conn_args=get_conn_args()
        )
        answer_path = answer_path.with_suffix(".txt")
        print(f"\nAnswer path: {answer_path.as_posix()}")
        with open(answer_path, "w") as outfile:
            outfile.write(str(answer))
        print(f"\nAnswer:\n{answer} repeaters")

    else:
        print("Error: question allowed are 1, 2, 3 or 4!")


if __name__ == '__main__':
    main()
