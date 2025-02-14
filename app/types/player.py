from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import date

YEAR_PERFS_SQL = """
WITH batting_plus_year AS (
	SELECT
		*
	,	CAST(STRFTIME('%Y', DATETIME(match_date)) AS INTEGER) AS year
	FROM match_batting
)
SELECT
	ba.match_date
,	ba.opp
,	ba.captain
,	ba.kept_wicket AS keeper
,	ba.position AS bat_pos
,	ba.how_out
,	ba.runs AS runs_scored
,	ba.fours
,	ba.sixes
,	bo.overs
,	bo.balls
,	bo.maidens
,	bo.runs_conceded
,	bo.wickets
,	ba.caught
,	ba.caught_wkt
,	ba.stumped
FROM batting_plus_year ba
	LEFT JOIN match_bowling bo
	ON ba.player_id = bo.player_id
	AND ba.match_id = bo.match_id
WHERE ba.player_id = :player_id
AND ba.year = :year
ORDER BY ba.match_date
"""


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
        print(res)
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

    @classmethod
    def table_cols(cls) -> list[dict]:
        return [
            {"name": "date", "label": "Date", "field": "match_date", "align": "center"},
            {"name": "opp", "label": "Opp", "field": "opp", "align": "left"},
            {"name": "pos", "label": "Pos", "field": "position", "align": "center"},
            {"name": "how_out", "label": "How Out", "field": "how_out"},
            {"name": "run", "label": "Runs", "field": "runs_scored"},
            {"name": "fours", "label": "4s", "field": "fours"},
            {"name": "sixes", "label": "6s", "field": "sixes"},
            {"name": "overs_balls", "label": "Overs", "field": "overs_balls"},
            {"name": "maidens", "label": "Maidens", "field": "maidens"},
            {"name": "runs_conceded", "label": "Runs", "field": "runs_conceded"},
            {"name": "wickets", "label": "Wickets", "field": "wickets"},
            {"name": "caught", "label": "", "field": ""},
            {"name": "fielding", "label": "Fielding", "field": "fielding", "align": "center"},
        ]


@dataclass(kw_only=True)
class Player:
    id: int = -1
    code: str = ""
    surname: str = ""
    initial: str = ""
    firstname: str = ""
    active: bool = False

    @property
    def name(self) -> str:
        if forename := self.firstname or self.initial:
            return f"{self.surname}, {forename}"
        return self.surname

    @classmethod
    def get(cls, db: sqlite3.Connection, player_id: int) -> Player:
        with closing(db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM players WHERE id = :player_id",
                {
                    "player_id": player_id,
                },
            )
            row: dict = csr.fetchone()
            return Player(**row)

    @classmethod
    def all(cls, db: sqlite3.Connection, surname_like: str = "%") -> dict[int, Player]:
        with closing(db.cursor()) as csr:
            csr.execute(
                """SELECT *
                FROM players WHERE surname LIKE :surname_like ORDER BY surname, initial
                """,
                {
                    "surname_like": surname_like,
                },
            )
            rows: list[dict] = csr.fetchall()
            return {row["id"]: Player(**row) for row in rows}

    def match_perf_years(self, db: sqlite3.Connection) -> list[int]:
        with closing(db.cursor()) as csr:
            csr.execute(
                """
                SELECT DISTINCT strftime('%Y', datetime(match_date)) AS yr
                FROM match_batting
                WHERE player_id = :player_id
                ORDER BY 1""",
                {
                    "player_id": self.id,
                },
            )
            rows = csr.fetchall()
            return [int(row["yr"]) for row in rows]

    def match_perfs(self, db: sqlite3.Connection, year: int) -> list[PlayerMatchPerf]:
        with closing(db.cursor()) as csr:
            csr.execute(
                YEAR_PERFS_SQL,
                {
                    "player_id": self.id,
                    "year": year,
                },
            )
            rows = csr.fetchall()
            return [PlayerMatchPerf(**row) for row in rows]
