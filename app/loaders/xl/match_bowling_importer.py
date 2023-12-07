from __future__ import annotations

from app.loaders.xl.importer_base import XlImporter
from app.loaders.xl.match_card import XlMatchCard
from app.types import MatchBowling


class XlBowlingImporter(XlImporter):
    def ingest(self) -> None:
        sheet = self.wb["Bowling"]

        # build name list from column 3, starting at row 5. Note: 1-indexed.
        players: list[str] = []
        for row in range(5, sheet.max_row):
            cell_value = sheet.cell(row, 2).value
            if cell_value is None:
                break
            players.append(str(cell_value))
        print("retrieved", len(players), "players")

        # get cards for each match, iterating over columns
        matches: list[XlMatchCard] = []
        for col in range(3, sheet.max_column):
            match_info = XlMatchCard.from_worksheet(sheet, col)
            if match_info.is_empty:
                break
            matches.append(match_info)
        print("retrieved", len(matches), "matches")

        MATCH_OFFSET = 3
        ENTRY_OFFSET = 5

        items = []

        for match_idx, match in enumerate(matches):
            if match.result == 0:
                continue
            col = match_idx + MATCH_OFFSET
            for player_idx, player in enumerate(players):
                row = player_idx + ENTRY_OFFSET
                if cel_value := sheet.cell(row, col).value:
                    items.append(
                        MatchBowling.from_string(
                            player, str(cel_value), match.date, match.opp
                        )
                    )
        self.write_csv(items)
