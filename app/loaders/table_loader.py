import sqlite3
from contextlib import closing
from dataclasses import asdict, fields
from typing import Any


class TableLoader:
    def __init__(self, conn: sqlite3.Connection, table: str, klass: type, exclusions: list[str]) -> None:
        self.conn = conn
        self.table = table
        self.klass = klass
        self.exclusions = exclusions

    def load(self, rows: list[Any]) -> None:
        self.insert_data((rows))

    def insert_data(self, rows: list[Any]) -> None:
        sql = self.insert_sql()
        print(sql)
        with closing(self.conn.cursor()) as csr:
            csr.executemany(sql, [asdict(row) for row in rows])

    def insert_sql(self) -> str:
        field_list = [f.name for f in fields(self.klass) if f.name not in self.exclusions and f.name != "id"]
        cols = ", ".join(field_list)
        vals = ", ".join(f":{field_name}" for field_name in field_list)
        return f"INSERT INTO {self.table} ({cols}) VALUES ({vals})"

    def update_player_ids(self, player_id_cols: dict) -> None:
        for id_col, map_from in player_id_cols.items():
            sql = f"""
                UPDATE {self.table}
                    SET {id_col} = (
                        SELECT id
                        FROM players
                        WHERE players.code={self.table}.{map_from}
                    )
                """
            self.conn.execute(sql)
