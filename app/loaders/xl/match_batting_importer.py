from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date as pydate

from app.loaders.xl.xl_importer_base import XlImporter
from app.types import MatchBatting


@dataclass
class XlMatchBattingCard:
    """
    transposed from Matches worksheet, so should be matchable against Match
    """

    date: pydate
    opp: str = ""
    venue: str = ""
    result: str = ""

    # individual batting data
    bat_card: list[MatchBatting] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return self.opp == 0

    @staticmethod
    def from_worksheet(ws, col: int) -> XlMatchBattingCard:
        return XlMatchBattingCard(
            ws.cell(1, col).value,
            ws.cell(2, col).value,
            ws.cell(3, col).value,
            ws.cell(4, col).value,
        )


class XlBattingImporter(XlImporter):
    def ingest(self) -> None:
        sheet = self.wb["Batting"]
        for c in range(3, sheet.max_column + 1):
            for r in range(1, sheet.max_row + 1):
                print(sheet.cell(r, c).value)
                if r > 5:
                    break
            if c > 5:
                break
        # build name list from column 3, starting at row 5. Note: 1-indexed.
        players: list[str] = []
        for row in range(5, sheet.max_row):
            cell_value = sheet.cell(row, 3).value
            if cell_value is None:
                break
            players.append(str(cell_value))
        print("retrieved", len(players), "players")

        # get cards for each match, iterating over columns
        matches: list[XlMatchBattingCard] = []
        for col in range(4, sheet.max_column):
            match_info = XlMatchBattingCard.from_worksheet(sheet, col)
            if match_info.is_empty:
                break
            matches.append(match_info)
        print("retrieved", len(matches), "matches")

        MATCH_OFFSET = 4
        BATENTRY_OFFSET = 5

        items = []

        for match_idx, match in enumerate(matches):
            if match.result == 0:
                continue
            col = match_idx + MATCH_OFFSET
            for player_idx, player in enumerate(players):
                row = player_idx + BATENTRY_OFFSET
                if cel_value := sheet.cell(row, col).value:
                    items.append(
                        MatchBatting.from_string(
                            player, str(cel_value), match.date, match.opp
                        )
                    )

        self.write_csv(items)
