from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date

batre = re.compile(
    r"""(?P<position>\d+)/"""
    r"""(?P<runs>\d+)(?P<out>\*?)/"""
    r"""(?P<how_out>[a-z]+)(?P<capt_kept>[\*\+]*)/"""
    r"""(?P<fielded>[0-9.]+)/"""
    r"""(?P<bdries>[0-9.]+)"""
)


@dataclass
class MatchBatting:
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

    def __str__(self) -> str:
        return f"{self.position:2d} {self.capt_wkt_flags} {self.name:40}{self.how_out:^3} {self.runs:3d}"

    @staticmethod
    def from_worksheet(name: str, entry: str) -> MatchBatting:
        obj = MatchBatting(name=name)
        if not entry:
            return obj
        match = batre.search(entry)
        fields = match.groupdict()
        obj.position = int(fields["position"])
        obj.runs = int(fields["runs"])
        obj.out = fields["out"] != "*"
        obj.how_out = fields["how_out"]
        obj.captain = "*" in fields["capt_kept"]
        obj.kept_wicket = "+" in fields["capt_kept"]
        ct_st = fields["fielded"].split(".")
        if obj.kept_wicket:
            obj.caught_wkt = int(ct_st[0])
            if len(ct_st) > 1:
                obj.stumped = int(ct_st[1])
        else:
            obj.caught = int(fields["fielded"])
        four_six = fields["bdries"].split(".")
        obj.fours = int(four_six[0])
        if len(four_six) > 1:
            obj.sixes = int(four_six[1])
        return obj


@dataclass
class MatchInfo:
    """
    transposed from Matches worksheet, so should be matchable
    """

    date: date
    opp: str
    venue: str
    result: str

    # individual batting data
    bat_card: list[MatchBatting] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not isinstance(self.opp, str)

    def card(self) -> str:
        top_line = (
            f"{self.date:%Y-%m-%d}: {self.opp} ({self.venue}) result: {self.result}"
        )
        bat_lines = [str(pl) for pl in sorted(self.bat_card, key=lambda p: p.position)]
        return "\n".join([top_line] + bat_lines)

    @staticmethod
    def from_worksheet(ws, col: int) -> MatchInfo:
        return MatchInfo(
            ws.cell(1, col).value,
            ws.cell(2, col).value,
            ws.cell(3, col).value,
            ws.cell(4, col).value,
        )


class BattingImporter:
    def __init__(self, ws) -> None:
        self.sheet = ws
        print(f"{ws.min_row=}, {ws.max_row=}")
        print(f"{ws.min_column=}, {ws.max_column=}")
        for c in range(3, ws.max_column + 1):
            for r in range(1, ws.max_row + 1):
                print(ws.cell(r, c).value)
                if r > 5:
                    break
            if c > 5:
                break

    def ingest(self) -> None:
        # build name list
        players: list[str] = []
        for row in range(5, self.sheet.max_row):
            if self.sheet.cell(row, 3).value is None:
                break
            players.append(self.sheet.cell(row, 3).value)
        print("retrieved", len(players), "players")

        matches: list[MatchInfo] = []
        for col in range(4, self.sheet.max_column):
            match_info = MatchInfo.from_worksheet(self.sheet, col)
            if match_info.is_empty:
                break
            matches.append(match_info)
        print("retrieved", len(matches), "matches")

        for match_idx, match in enumerate(matches):
            col = match_idx + 4
            for player_idx, player in enumerate(players):
                row = player_idx + 5
                cel = self.sheet.cell(row, col).value
                if cel:
                    match.bat_card.append(MatchBatting.from_worksheet(player, cel))

        print(matches[0].card())
        # bid match list
        # for cell in data area
        # if not empty
        # - parse & add to card
