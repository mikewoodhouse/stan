from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date

from dataclass_csv import dateformat


@dateformat("%Y-%m-%d %H:%M:%S")
@dataclass
class MatchBowling:
    id: int = -1
    match_id: int = -1
    match_date: date = date(1900, 1, 1)
    opp: str = ""
    name: str = ""
    overs: int = 0
    balls: int = 0
    maidens: int = 0
    runs_conceded: int = 0
    wickets: int = 0
    wides: int = 0
    noballs: int = 0

    @staticmethod
    def from_string(name: str, input: str, match_date: date, opp: str) -> MatchBowling:
        parts = input.split("/")
        ob, m, r, w, wd, nb = parts + ([""] * (6 - len(parts)))
        o, b = ob.split(".") if "." in ob else (int(ob), 0)
        return MatchBowling(
            match_date=match_date,
            opp=opp,
            name=name,
            overs=int(o),
            balls=int(b) if b else 0,
            maidens=int(m),
            runs_conceded=int(r),
            wickets=int(w),
            wides=int(wd) if wd else 0,
            noballs=int(nb) if nb else 0,
        )

    @staticmethod
    def for_match_id(db: sqlite3.Connection, match_id: int) -> list[MatchBowling]:
        return []

    @staticmethod
    def table_cols() -> list[dict]:
        return []
