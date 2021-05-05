from collections import namedtuple
from contextlib import contextmanager
import sqlite3


def namedtuple_factory(cursor, row):
    """
    Usage:
    con.row_factory = namedtuple_factory
    """
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


@contextmanager
def db_connection(*args, **kwargs):
    connection = sqlite3.connect("tocc.sqlite")
    connection.row_factory = namedtuple_factory
    try:
        yield connection
    finally:
        connection.close()
