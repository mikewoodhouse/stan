from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import asdict, dataclass

from app.utils import balls_to_overs


@dataclass(kw_only=True)
class Performance:
    id: int = -1
    player_id: int = -1
    code: str
    year: int | str
    matches: int
    innings: int = 0
    notout: int = 0
    highest: int = 0
    highestnotout: bool = False
    runsscored: int = 0
    fours: int = 0
    sixes: int = 0
    overs: int = 0
    balls: int = 0
    maidens: int = 0
    wides: int = 0
    noballs: int = 0
    runs: int = 0
    wickets: int = 0
    fivewktinn: int = 0
    caught: int = 0
    stumped: int = 0
    fifties: int = 0
    hundreds: int = 0
    fives: int = 0
    caughtwkt: int = 0
    captain: int = 0
    keptwicket: int = 0

    @property
    def high_score(self) -> str:
        return f"{self.highest}{'*' if self.highestnotout else ''}"

    @property
    def overs_bowled(self) -> str:
        return balls_to_overs(self.balls_bowled)

    @property
    def batting_average(self) -> float:
        if (self.innings - self.notout) > 0:
            return round(self.runsscored / (self.innings - self.notout), 2)
        else:
            return 0

    @property
    def bowling_average(self) -> float:
        return round(self.runs / self.wickets, 2) if self.wickets > 0 else 0

    @property
    def strike_rate(self) -> float | None:
        return round(self.balls_bowled / self.wickets, 2) if self.wickets else None

    @property
    def balls_bowled(self) -> int:
        return self.overs * 6 + self.balls

    @property
    def economy(self) -> float:
        return round(self.runs * 6 / self.balls_bowled, 2)

    def row_dict(self) -> dict:
        return asdict(self) | {
            "high_score": self.high_score,
            "overs_bowled": self.overs_bowled,
            "batting_average": self.batting_average,
            "bowling_average": self.bowling_average,
        }

    @staticmethod
    def sumof(field_name: str, perfs: list[Performance]):
        return sum(getattr(p, field_name) for p in perfs)

    @classmethod
    def for_player(cls, db: sqlite3.Connection, player_id: int) -> list[Performance]:
        with closing(db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM performances WHERE player_id = :player_id ORDER BY year",
                {"player_id": player_id},
            )
            rows = csr.fetchall()
        perfs = [Performance(**row) for row in rows]

        totals = Performance(
            code="",
            year="Total",
            matches=Performance.sumof("matches", perfs),
            innings=Performance.sumof("innings", perfs),
            notout=Performance.sumof("notout", perfs),
            runsscored=Performance.sumof("runsscored", perfs),
            fours=Performance.sumof("fours", perfs),
            sixes=Performance.sumof("sixes", perfs),
            overs=Performance.sumof("overs", perfs),
            balls=Performance.sumof("balls", perfs),
            maidens=Performance.sumof("maidens", perfs),
            runs=Performance.sumof("runs", perfs),
            wickets=Performance.sumof("wickets", perfs),
            fivewktinn=Performance.sumof("fivewktinn", perfs),
            caught=Performance.sumof("caught", perfs),
            stumped=Performance.sumof("stumped", perfs),
            fifties=Performance.sumof("fifties", perfs),
            hundreds=Performance.sumof("hundreds", perfs),
            caughtwkt=Performance.sumof("caughtwkt", perfs),
            captain=Performance.sumof("captain", perfs),
            keptwicket=Performance.sumof("keptwicket", perfs),
        )

        totals.highest, totals.highestnotout = max((p.highest, p.highestnotout) for p in perfs)

        perfs.append(totals)
        return perfs

    @classmethod
    def for_year(cls, db: sqlite3.Connection, year: int) -> list[Performance]:
        with closing(db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM performances WHERE year = :year",
                {"year": year},
            )
            rows = csr.fetchall()
        return [Performance(**row) for row in rows]

    @staticmethod
    def table_cols() -> list[dict]:
        return [
            {
                "name": "year",
                "label": "year",
                "field": "year",
                "sortable": True,
                "align": "center",
            },
            {
                "name": "matches",
                "label": "matches",
                "field": "matches",
                "sortable": True,
            },
            {
                "name": "innings",
                "label": "innings",
                "field": "innings",
                "sortable": True,
            },
            {"name": "notout", "label": "not out", "field": "notout", "sortable": True},
            {
                "name": "high_score",
                "label": "highest",
                "field": "high_score",
                "sortable": True,
            },
            {
                "name": "runsscored",
                "label": "runs",
                "field": "runsscored",
                "sortable": True,
            },
            {
                "name": "batave",
                "label": "ave",
                "field": "batting_average",
                "sortable": True,
            },
            {"name": "fours", "label": "fours", "field": "fours", "sortable": True},
            {"name": "sixes", "label": "sixes", "field": "sixes", "sortable": True},
            {
                "name": "overs_bowled",
                "label": "overs",
                "field": "overs_bowled",
                "sortable": True,
            },
            {
                "name": "maidens",
                "label": "maidens",
                "field": "maidens",
                "sortable": True,
            },
            {"name": "runs", "label": "runs", "field": "runs", "sortable": True},
            {
                "name": "wickets",
                "label": "wickets",
                "field": "wickets",
                "sortable": True,
            },
            {
                "name": "bowlave",
                "label": "ave",
                "field": "bowling_average",
                "sortable": True,
            },
            {
                "name": "fivewktinn",
                "label": "five-for",
                "field": "fivewktinn",
                "sortable": True,
            },
            {"name": "caught", "label": "caught", "field": "caught", "sortable": True},
            {
                "name": "stumped",
                "label": "stumped",
                "field": "stumped",
                "sortable": True,
            },
            {
                "name": "fifties",
                "label": "fifties",
                "field": "fifties",
                "sortable": True,
            },
            {
                "name": "hundreds",
                "label": "hundreds",
                "field": "hundreds",
                "sortable": True,
            },
            {
                "name": "caughtwkt",
                "label": "caught wkt",
                "field": "caughtwkt",
                "sortable": True,
            },
            {
                "name": "captain",
                "label": "captain",
                "field": "captain",
                "sortable": True,
            },
            {
                "name": "keptwicket",
                "label": "kept wicket",
                "field": "keptwicket",
                "sortable": True,
            },
        ]
