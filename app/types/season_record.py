from __future__ import annotations

from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import date

from dataclass_csv import dateformat

from app.config import config
from app.utils import balls_to_overs


@dataclass(kw_only=True)
@dateformat(r"%Y-%m-%d %H:%M:%S")
class SeasonRecord:
    id: int = -1
    year: int
    club: str
    runsscored: int
    wicketslost: int
    highest: int
    highestwkts: int
    highestdate: date = date(1899, 12, 31)
    highestopps: str = ""
    lowest: int
    lowestwkts: int
    lowestdate: date = date(1899, 12, 31)
    lowestopps: str = ""
    byes: int
    legbyes: int
    wides: int
    noballs: int
    ballsbowled: int = -1
    ballsreceived: int = -1

    @property
    def overs_bowled(self) -> str:
        return balls_to_overs(self.ballsbowled) if self.ballsbowled > 0 else ""

    @property
    def overs_faced(self) -> str:
        return balls_to_overs(self.ballsreceived) if self.ballsreceived > 0 else ""

    def row_dict(self) -> dict:
        return asdict(self) | {
            "overs_bowled": self.overs_bowled,
            "overs_faced": self.overs_faced,
            "highest_score": f"{self.highest}-{self.highestwkts}",
            "lowest_score": f"{self.lowest}-{self.lowestwkts}",
        }

    @classmethod
    def for_year(cls, year: int) -> list[dict]:
        with closing(config.db.cursor()) as csr:
            csr.execute("SELECT * FROM season_records WHERE year = :year", {"year": year})
            records = [SeasonRecord(**row) for row in csr.fetchall()]
            return [record.row_dict() for record in records]

    @staticmethod
    def table_cols() -> list[dict]:
        return [
            {"name": "club", "label": "Club", "field": "club"},
            {"name": "runsscored", "label": "Runs", "field": "runsscored"},
            {"name": "wicketslost", "label": "Wickets Lost", "field": "wicketslost"},
            {"name": "highest", "label": "Highest", "field": "highest_score"},
            {"name": "highestdate", "label": "Date", "field": "highestdate"},
            {"name": "highestopps", "label": "Vs", "field": "highestopps"},
            {"name": "lowest", "label": "Lowest", "field": "lowest_score"},
            {"name": "lowestdate", "label": "Date", "field": "lowestdate"},
            {"name": "lowestopps", "label": "Vs", "field": "lowestopps"},
            {"name": "byes", "label": "Byes", "field": "byes"},
            {"name": "legbyes", "label": "Legbyes", "field": "legbyes"},
            {"name": "wides", "label": "Wides", "field": "wides"},
            {"name": "noballs", "label": "Noballs", "field": "noballs"},
            {"name": "overs_bowled", "label": "Overs Bowled", "field": "overs_bowled"},
            {"name": "overs_faced", "label": "Overs Faced", "field": "overs_faced"},
        ]
