from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import date

from dataclass_csv import dateformat


@dateformat("%Y-%m-%d %H:%M:%S")
@dataclass(kw_only=True)
class Match:
    id: int = -1
    date: date
    oppo: str
    venue: str = "?"
    result: str = "?"
    bat_first: str = "?"
    first_runs: int = 0
    first_wkts: int = 0
    first_all_out: bool = False
    first_notes: str = ""
    second_runs: int = 0
    second_wkts: int = 0
    second_all_out: bool = False
    second_notes: str = ""
    overs_opp: float = 0
    overs_tocc: float = 0
    tocc_w: int = 0
    tocc_nb: int = 0
    tocc_b: int = 0
    tocc_lb: int = 0
    opp_w: int = 0
    opp_nb: int = 0
    opp_b: int = 0
    opp_lb: int = 0

    @classmethod
    def for_year(cls, db: sqlite3.Connection, year: int) -> list[Match]:
        with closing(db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM matches WHERE date between :soy AND :eoy ORDER BY date",
                {"soy": f"{year}-01-01", "eoy": f"{year}-12-31"},
            )
            rows = csr.fetchall()
        matches = [Match(**row) for row in rows]
        return matches
