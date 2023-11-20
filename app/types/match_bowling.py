from __future__ import annotations

from dataclasses import dataclass
from datetime import date


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
    def from_string(input: str) -> MatchBowling:
        parts = input.split("/")
        ob, m, r, w, wd, nb = parts + ([""] * (6 - len(parts)))
        o, b = ob.split(".")
        return MatchBowling(
            overs=int(o),
            balls=int(b) if b else 0,
            maidens=int(m),
            runs_conceded=int(r),
            wickets=int(w),
            wides=int(wd) if wd else 0,
            noballs=int(nb) if nb else 0,
        )
