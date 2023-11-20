from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

batre = re.compile(
    r"""(?P<position>\d+)/"""
    r"""(?P<runs>\d+)/"""
    r"""(?P<how_out>[a-z]+)(?P<capt_kept>[\*\+]*)/"""
    r"""(?P<fielded>[0-9.]+)/"""
    r"""(?P<bdries>[0-9.]+)"""
)


@dataclass
class MatchBatting:
    id: int = -1
    match_id: int = -1
    match_date: date = date(1900, 1, 1)
    opp: str = ""
    name: str = ""
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
