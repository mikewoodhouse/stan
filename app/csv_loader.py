import sqlite3
from dataclasses import dataclass, field, fields, asdict
from dataclass_csv import DataclassReader
from contextlib import closing
from app.types.classes import Player, Season, HundredPlus, Partnership
from typing import Type


@dataclass
class LoadDefinition:
    klass: Type
    table: str
    headers: str
    player_id_cols: dict = field(default_factory=dict)

    @property
    def header_map(self) -> list[tuple]:
        return [(h, h.lower()) for h in self.headers.split("|")]


load_defs = {
    "players": LoadDefinition(
        klass=Player,
        table="players",
        headers="Code|Surname|Initial|Active|FirstName",
    ),
    "seasons": LoadDefinition(
        klass=Season,
        table="seasons",
        headers="Year|Played|Won|Lost|Drawn|Tied|NoResult|MaxPossibleGames",
    ),
    "hundred_plus": LoadDefinition(
        klass=HundredPlus,
        table="hundred_plus",
        headers="Year|Code|Date|Score|NotOut|Opponents|Minutes",
        player_id_cols={
            "player_id": "code",
        },
    ),
    "partnerships": LoadDefinition(
        klass=Partnership,
        table="partnerships",
        headers="Year|Wicket|Date|Total|Undefeated|Bat1|Bat1Score|Bat1NotOut|Bat2|Bat2Score|Bat2NotOut|Opp",
        player_id_cols={
            "bat1_id": "bat1",
            "bat2_id": "bat2",
        },
    ),
}


class CsvLoader:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def load(self, filename: str) -> None:
        load_def = load_defs[filename]
        csv_rows = self.read_csv(filename, load_def)
        self.insert_data(load_def, csv_rows)
        self.update_player_ids(load_def)

    def read_csv(self, filename: str, load_def: LoadDefinition) -> None:
        with open(f"csvdata/{filename}.csv") as f:
            reader = DataclassReader(f, load_def.klass)
            for hdr_in, hdr_out in load_def.header_map:
                reader.map(hdr_in).to(hdr_out)
            return list(reader)

    def insert_sql(self, klass: type, tablename: str) -> str:
        cols = ", ".join(field.name for field in fields(klass))
        vals = ", ".join(f":{field.name}" for field in fields(klass))
        return f"INSERT INTO {tablename} ({cols}) VALUES ({vals})"

    def load_schema(self) -> None:
        with open("db_schema.sql") as f:
            self.conn.executescript(f.read())

    def insert_data(self, load_def: LoadDefinition, rows: list[dict]) -> None:
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
