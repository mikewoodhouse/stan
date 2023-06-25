import sqlite3
from contextlib import closing
from dataclasses import asdict, fields
from typing import Any

from dataclass_csv import DataclassReader

from app.loaders.load_defs import LoadDefinition, load_defs


class CsvLoader:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def load(self, filename: str) -> None:
        load_def = load_defs[filename]
        csv_rows = self.read_csv(filename, load_def)
        self.insert_data(load_def, csv_rows)
        self.update_player_ids(load_def)

    def read_csv(self, filename: str, load_def: LoadDefinition) -> list[Any]:
        with open(f"csvdata/{filename}.csv") as f:
            reader = DataclassReader(f, load_def.klass)
            for hdr_in, hdr_out in load_def.header_map:
                reader.map(hdr_in).to(hdr_out)
            return list(reader)

    def insert_sql(self, klass: type, tablename: str) -> str:
        cols = ", ".join(field.name for field in fields(klass) if field.name != "id")
        vals = ", ".join(
            f":{field.name}" for field in fields(klass) if field.name != "id"
        )
        return f"INSERT INTO {tablename} ({cols}) VALUES ({vals})"

    def load_schema(self) -> None:
        with open("db_schema.sql") as f:
            self.conn.executescript(f.read())

    def insert_data(self, load_def: LoadDefinition, rows: list[Any]) -> None:
        sql = self.insert_sql(load_def.klass, load_def.table)
        with closing(self.conn.cursor()) as csr:
            csr.executemany(sql, [asdict(row) for row in rows])

    def update_player_ids(self, load_def: LoadDefinition) -> None:
        for id_col, map_from in load_def.player_id_cols.items():
            sql = f"""
                UPDATE {load_def.table}
                    SET {id_col} = (
                        SELECT id
                        FROM players
                        WHERE players.code={load_def.table}.{map_from}
                    )
                """
            self.conn.execute(sql)
