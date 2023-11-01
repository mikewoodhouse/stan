from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date  # noqa

from app.types import MatchBatting


@dataclass
class MatchInfo:
    """
    transposed from Matches worksheet, so should be matchable against Match
    """

    date: date
    opp: str = ""
    venue: str = ""
    result: str = ""

    # individual batting data
    bat_card: list[MatchBatting] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return len(self.opp) == 0

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

        MATCH_OFFSET = 4
        BATENTRY_OFFSET = 5

        for match_idx, match in enumerate(matches):
            col = match_idx + MATCH_OFFSET
            for player_idx, player in enumerate(players):
                row = player_idx + BATENTRY_OFFSET
                if cel_value := self.sheet.cell(row, col).value:
                    match.bat_card.append(
                        MatchBatting.from_worksheet(player, cel_value)
                    )
