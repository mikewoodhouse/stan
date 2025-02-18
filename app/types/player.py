from __future__ import annotations

from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import date

from app.config import config
from app.utils import sql_query


@dataclass
class PlayerMatchPerf:
    match_date: date
    opp: str

    captain: bool
    keeper: bool
    bat_pos: int

    how_out: str
    runs_scored: int
    fours: int
    sixes: int

    overs: int
    balls: int
    maidens: int
    runs_conceded: int
    wickets: int

    caught: int
    caught_wkt: int
    stumped: int

    def row_dict(self) -> dict:
        res = asdict(self) | {
            "position": self.position,
            "overs_balls": self.overs_balls,
            "fielding": self.fielding,
        }
        return res

    @property
    def position(self) -> str:
        return "".join(["*" * self.captain, "+" * self.keeper, str(self.bat_pos)])

    @property
    def overs_balls(self) -> str:
        o = self.overs or 0
        b = self.balls or 0
        return f"{o + b/10:4.1f}" if o + b > 0 else ""

    @property
    def fielding(self) -> str:
        if self.keeper:
            ct = f"ct: {self.caught_wkt}" if self.caught_wkt else ""
            st = f"st: {self.stumped}" if self.stumped else ""
            res = ct + (", " if ct and st else "") + st
            return res
        else:
            return f"ct: {self.caught}" if self.caught else ""


@dataclass(kw_only=True)
class Player:
    id: int = -1
    code: str = ""
    surname: str = ""
    initial: str = ""
    firstname: str = ""
    active: bool = False

    @classmethod
    def get(cls, player_id: int) -> Player:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                sql_query(("player_by_id")),
                {
                    "player_id": player_id,
                },
            )
            row: dict = csr.fetchone()
            return Player(**row)

    @classmethod
    def all(cls, surname_like: str = "%") -> dict[int, Player]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                sql_query("player_surname_like"),
                {
                    "surname_like": surname_like,
                },
            )
            rows: list[dict] = csr.fetchall()
            return {row["id"]: Player(**row) for row in rows}

    def match_perf_years(self) -> list[int]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                sql_query("player_years_batted_in"),
                {
                    "player_id": self.id,
                },
            )
            rows = csr.fetchall()
            return [int(row["yr"]) for row in rows]

    def match_perfs(self, year: int) -> list[PlayerMatchPerf]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                sql_query("player_match_perfs_for_year"),
                {
                    "player_id": self.id,
                    "year": year,
                },
            )
            rows = csr.fetchall()
            return [PlayerMatchPerf(**row) for row in rows]
