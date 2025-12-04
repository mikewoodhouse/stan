from __future__ import annotations

from dataclasses import dataclass
from datetime import date as pydate
from datetime import time


@dataclass
class XlMatchCard:
    """
    transposed from Matches worksheet, so should be matchable against Match
    """

    date: pydate
    opp: str = ""
    venue: str = ""
    result: str = ""

    @property
    def is_empty(self) -> bool:
        return self.date == time(0, 0)

    @staticmethod
    def from_worksheet(ws, col: int) -> XlMatchCard:
        return XlMatchCard(
            ws.cell(1, col).value,
            ws.cell(2, col).value,
            ws.cell(3, col).value,
            ws.cell(4, col).value,
        )
