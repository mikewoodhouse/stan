import sqlite3
from datetime import date

sqlite3.register_adapter(date, lambda d: d.isoformat())
sqlite3.register_converter("DATE", lambda s: date.fromisoformat(s.decode("utf-8")))


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


class Configurator:
    MIN_APPS: int = 30
    MIN_CAPTAINED: int = 10

    @property
    def db(self) -> sqlite3.Connection:
        conn = sqlite3.connect("stan.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = dict_factory
        return conn


config = Configurator()
