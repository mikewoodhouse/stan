from __future__ import annotations

from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import date

from dataclass_csv import dateformat

from app.config import config
from app.utils import sql_query


@dateformat("%Y-%m-%d %H:%M:%S")
@dataclass
class MatchBowling:
    id: int = -1
    match_id: int = -1
    match_date: date = date(1900, 1, 1)
    opp: str = ""
    name: str = ""
    player_id: int = 0
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
        try:
            ob, m, r, w, wd, nb = parts + ([""] * (6 - len(parts)))
        except Exception:
            print(name, match_date, input)
            exit()
        o, b = ob.split(".") if "." in ob else (int(ob) if ob else 0, 0)
        return MatchBowling(
            match_date=match_date,
            opp=opp,
            name=name,
            overs=int(o),
            balls=int(b) if b else 0,
            maidens=int(m) if m else 0,
            runs_conceded=int(r) if r else 0,
            wickets=int(w) if w else 0,
            wides=int(wd) if wd else 0,
            noballs=int(nb) if nb else 0,
        )

    def row_dict(self) -> dict:
        return asdict(self) | {
            "overs_and_balls": f"{self.overs}.{self.balls}",
            "econ": f"{self.economy:0.2f}",
            "strike_rate": "" if self.wickets == 0 else f"{self.strike_rate:0.2f}",
        }

    @property
    def economy(self) -> float:
        return self.runs_conceded * 6.0 / (self.overs * 6 + self.balls)

    @property
    def strike_rate(self) -> float:
        return (self.overs * 6 + self.balls) / self.wickets

    @staticmethod
    def for_match_id(match_id: int) -> list[MatchBowling]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                sql_query("match_bowling"),
                {"match_id": match_id},
            )
            rows = csr.fetchall()
        return [MatchBowling(**row) for row in rows]
