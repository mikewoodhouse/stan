from __future__ import annotations

import re
import sqlite3
from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import date

from dataclass_csv import dateformat

batre = re.compile(
    r"""(?P<position>\d+)/"""
    r"""(?P<runs>\d+)/"""
    r"""(?P<how_out>[a-z]+)(?P<capt_kept>[\*\+]*)/"""
    r"""(?P<fielded>[0-9.]+)/"""
    r"""(?P<bdries>[0-9.]+)"""
)


@dateformat("%Y-%m-%d %H:%M:%S")
@dataclass
class MatchBatting:
    id: int = -1
    match_id: int = -1
    match_date: date = date(1900, 1, 1)
    opp: str = ""
    name: str = ""
    player_id: int = 0
    position: int = 0
    runs: int = 0
    out: bool = False
    how_out: str = ""
    captain: bool = False
    kept_wicket: bool = False
    caught: int = 0
    caught_wkt: int = 0
    stumped: int = 0
    fours: int = 0
    sixes: int = 0

    @property
    def capt_wkt_flags(self) -> str:
        c = "*" if self.captain else " "
        w = "+" if self.kept_wicket else " "
        return f"{(c + w).strip():>2}"

    @property
    def fielding(self) -> str:
        ret = []
        if (catches := self.caught + self.caught_wkt) > 0:
            ret.append(f"{catches} ct")
        if self.stumped > 0:
            ret.append(f"{self.stumped} st")
        return f"[{','.join(ret)}]" if ret else ""

    def __str__(self) -> str:
        name_plus = f"{self.name} {self.fielding}"
        run_str = f"{self.runs:3d}" if self.how_out != "dnb" else "   "
        return f"{self.position:2d} {self.capt_wkt_flags} {name_plus:40}{self.how_out:^3} {run_str}"

    @staticmethod
    def from_string(name: str, entry: str, match_date: date, opp: str) -> MatchBatting:
        obj = MatchBatting(name=name, match_date=match_date, opp=opp)
        if not entry:
            return obj
        if not (match := batre.search(entry)):
            return obj

        fields = match.groupdict()
        obj.position = int(fields["position"])
        obj.runs = int(fields["runs"])
        obj.out = fields["how_out"] not in ["no", "dnb"]
        obj.how_out = fields["how_out"]
        obj.captain = "*" in fields["capt_kept"]
        obj.kept_wicket = "+" in fields["capt_kept"]

        def split_dotted(dotted: str) -> tuple:
            parts = [int(p) for p in dotted.split(".")]
            return tuple(parts) if len(parts) == 2 else (parts[0], 0)

        if obj.kept_wicket:
            obj.caught_wkt, obj.stumped = split_dotted(fields["fielded"])
        else:
            obj.caught, obj.stumped = split_dotted(fields["fielded"])

        obj.fours, obj.sixes = split_dotted(fields["bdries"])

        return obj

    @classmethod
    def for_player(cls, db: sqlite3.Connection, player_id: int) -> list[MatchBatting]:
        with closing(db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM match_batting WHERE player_id = :player_id ORDER BY match_date",
                {"player_id": player_id},
            )
            rows = csr.fetchall()
        return [MatchBatting(**row) for row in rows]

    def how_out_text(self) -> str:
        return {
            "b": "bowled",
            "c": "caught",
            "lb": "lbw",
            "st": "stumped",
            "ro": "run out",
            "no": "not out",
            "dnb": "did not bat",
        }.get(self.how_out, self.how_out)

    def row_dict(self) -> dict:
        fldg = []
        if self.caught > 0:
            fldg.append(f"{self.caught}c")
        if self.caught_wkt > 0:
            fldg.append(f"{self.caught_wkt}c")
        if self.stumped > 0:
            fldg.append(f"{self.stumped}st")
        return asdict(self) | {
            "how_out_text": self.how_out_text(),
            "fancy_name": f"{'*' if self.captain else ''}{'+' if self.kept_wicket else ''}{self.name}",
            "fielding": ",".join(fldg),
        }

    @staticmethod
    def for_match_id(db: sqlite3.Connection, match_id: int) -> list[MatchBatting]:
        with closing(db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM match_batting WHERE match_id = :match_id ORDER BY position",
                {"match_id": match_id},
            )
            rows = csr.fetchall()
        return [MatchBatting(**row) for row in rows]

    @staticmethod
    def table_cols() -> list[dict]:
        return [
            {
                "name": "position",
                "label": "Pos",
                "field": "position",
                "sortable": False,
            },
            {
                "name": "name",
                "label": "Name",
                "field": "fancy_name",
                "sortable": False,
                "align": "left",
            },
            {
                "name": "how_out",
                "label": "How Out",
                "field": "how_out_text",
                "sortable": False,
            },
            {
                "name": "runs",
                "label": "Runs",
                "field": "runs",
                "sortable": False,
            },
            {
                "name": "fours",
                "label": "4s",
                "field": "fours",
                "sortable": False,
            },
            {
                "name": "sixes",
                "label": "6s",
                "field": "sixes",
                "sortable": False,
            },
            {
                "name": "fielding",
                "label": "",
                "field": "fielding",
                "sortable": False,
            },
        ]
