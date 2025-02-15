from __future__ import annotations

from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import date

from dataclass_csv import dateformat

from app.config import config


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
                "SELECT * FROM match_bowling WHERE match_id = :match_id ORDER BY id",
                {"match_id": match_id},
            )
            rows = csr.fetchall()
        return [MatchBowling(**row) for row in rows]

    @staticmethod
    def table_cols() -> list[dict]:
        return [
            {
                "name": "name",
                "label": "Name",
                "field": "name",
                "sortable": True,
            },
            {
                "name": "overs",
                "label": "Overs",
                "field": "overs_and_balls",
                "sortable": False,
            },
            {
                "name": "maidens",
                "label": "Maidens",
                "field": "maidens",
                "sortable": False,
            },
            {
                "name": "runs",
                "label": "Runs",
                "field": "runs_conceded",
                "sortable": False,
            },
            {
                "name": "wickets",
                "label": "Wickets",
                "field": "wickets",
                "sortable": True,
            },
            {
                "name": "econ",
                "label": "Econ",
                "field": "econ",
                "sortable": True,
            },
            {
                "name": "strike_rate",
                "label": "Strike rate",
                "field": "strike_rate",
                "sortable": True,
            },
        ]
