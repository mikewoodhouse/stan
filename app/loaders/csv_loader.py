from collections import defaultdict
from typing import Any

from dataclass_csv import DataclassReader

from app.config import config
from app.loaders.load_defs import LoadDefinition
from app.loaders.table_loader import TableLoader
from app.types import Player


class CsvLoader:
    def __init__(self) -> None:
        self.conn = config.db

    def load(self, load_def: LoadDefinition) -> None:
        csv_rows = self.read_csv(load_def)
        loader = TableLoader(load_def.table, load_def.klass, load_def.exclude_from_insert)
        loader.load(csv_rows)
        loader.update_player_ids(load_def.player_id_cols)

    def read_csv(self, load_def: LoadDefinition) -> list[Any]:
        with open(f"data/csvdata/{load_def.table}.csv", "r") as f:
            reader = DataclassReader(f, load_def.klass)
            for hdr_in, hdr_out in load_def.header_map:
                reader.map(hdr_in).to(hdr_out)
            records = list(reader)
            print(load_def.table, len(records), "records read")
            return records

    def load_schema(self) -> None:
        with open("db_schema.sql") as f:
            self.conn.executescript(f.read())

    def set_match_ids(self) -> None:
        for tbl in ["match_batting", "match_bowling"]:
            print(f"setting match ids for {tbl}")
            sql = f"""
                UPDATE {tbl}
                SET match_id =
                (
                    SELECT id FROM matches WHERE date = match_date AND oppo = opp
                )
            """
            self.conn.execute(sql)
            self.conn.commit()

    def set_player_ids(self) -> None:
        for tbl in ["match_batting", "match_bowling"]:
            rows = self.conn.execute("SELECT * FROM player_lookup")
            players = [Player(**row) for row in rows]
            lookup: dict[str, list] = defaultdict(list[Player])
            for player in players:
                lookup[player.surname].append(player)
            print(f"setting player ids for {tbl} from {len(players)} players")
            name_rows = list(
                self.conn.execute(
                    f"""
                    WITH players_by_season
                    AS (
                        SELECT DISTINCT
                          name
                        , strftime('%Y', match_date) AS season
                        FROM {tbl}
                    )
                    SELECT
                          name
                        , min(season) AS from_year
                        , max(season) AS to_year
                        , count(*) AS seasons
                        from players_by_season
                        GROUP BY name
                    """
                )
            )
            print("got", len(name_rows), "name rows")
            for row in name_rows:
                name = row["name"]
                surname = name[: name.rindex(" ")] if " " in name else name
                possibles = lookup[surname]
                if len(possibles) == 1:
                    self.update_player_id(tbl, name, possibles[0].player_id)
                elif not possibles:
                    print(f"{tbl}: no name match for {row}")
                elif " " not in name:  # no initial
                    print(f"{tbl}: multiple possibles for {row} and no initial")
                else:
                    initial = name.split(" ")[-1]
                    for possible in possibles:
                        if possible.initial == initial:
                            self.update_player_id(tbl, name, possible.player_id)
            print(f"{tbl} has {self.null_player_id_count(tbl)} NULL player_ids")
            self.conn.commit()

    def null_player_id_count(self, tbl: str) -> int:
        csr = self.conn.execute(f"SELECT name, count(*) AS row_count FROM {tbl} WHERE player_id IS NULL GROUP BY name")
        nulls = 0
        for row in csr.fetchall():
            print(row)
            nulls += 1
        return nulls

    def update_player_id(self, tbl: str, name: str, player_id: int) -> None:
        escaped_name = name.replace("'", "''")
        sql = f"UPDATE {tbl} SET player_id={player_id} WHERE name = '{escaped_name}'"
        self.conn.execute(sql)
