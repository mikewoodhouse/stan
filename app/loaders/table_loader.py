from contextlib import closing
from dataclasses import asdict, fields
from typing import Any

from app.config import config
from app.utils import count


class TableLoader:
    def __init__(self, table: str, klass: type, exclusions: list[str]) -> None:
        self.conn = config.db
        self.table = table
        self.klass = klass
        self.exclusions = exclusions

    def load(self, rows: list[Any]) -> None:
        self.insert_data(rows)

    def insert_data(self, rows: list[Any]) -> None:
        sql = self.insert_sql()
        print(len(rows), "rows to load...")
        with closing(self.conn.cursor()) as csr:
            rows_as_dicts = [asdict(row) for row in rows]
            print(len(rows_as_dicts), "rows as dicts to load...")
            csr.executemany(sql, rows_as_dicts)
            self.conn.commit()
        print(count(self.table), ": rows inserted")

    def insert_sql(self) -> str:
        field_list = [f.name for f in fields(self.klass) if f.name not in self.exclusions and f.name != "id"]
        cols = ", ".join(field_list)
        vals = ", ".join(f":{field_name}" for field_name in field_list)
        return f"INSERT INTO {self.table} ({cols}) VALUES ({vals})"

    def update_player_ids(self, player_id_cols: dict) -> None:
        """
        maps code to player id where defined in LoadDefinition
        """
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
            self.conn.commit()
