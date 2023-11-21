import sqlite3
from typing import Any

from dataclass_csv import DataclassReader

from app.loaders.load_defs import LoadDefinition
from app.loaders.table_loader import TableLoader


class CsvLoader:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def load(self, load_def: LoadDefinition) -> None:
        csv_rows = self.read_csv(load_def)
        loader = TableLoader(self.conn, load_def.table, load_def.klass)
        loader.load(csv_rows)
        loader.update_player_ids(load_def.player_id_cols)

    def read_csv(self, load_def: LoadDefinition) -> list[Any]:
        with open(f"data/csvdata/{load_def.table}.csv", "r") as f:
            reader = DataclassReader(f, load_def.klass)
            for hdr_in, hdr_out in load_def.header_map:
                reader.map(hdr_in).to(hdr_out)
            return list(reader)

    def load_schema(self) -> None:
        with open("db_schema.sql") as f:
            self.conn.executescript(f.read())

    def set_match_ids(self) -> None:
        for tbl in ["match_batting", "match_bowling"]:
            sql = f"""
                UPDATE {tbl}
                SET match_id =
                (
                    SELECT id FROM matches WHERE date = match_date AND oppo = opp
                )
            """
            self.conn.execute(sql)

    def set_player_ids(self) -> None:
        for tbl in ["match_batting", "match_bowling"]:
            sql = f"""
                UPDATE {tbl} t
                SET player_id =
                (
                    SELECT id FROM players p WHERE p.name = t.name
                )
            """
            self.conn.execute(sql)
