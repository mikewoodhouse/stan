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
    def overs_bowled(self):
        return balls_to_overs(self.ballsbowled)

    @property
    def overs_faced(self):
        return balls_to_overs(self.ballsreceived)

    def row_dict(self) -> dict:
        return asdict(self) | {
            "overs_bowled": self.overs_bowled,
            "overs_faced": self.overs_faced,
        }

    @classmethod
    def for_year(cls, year: int) -> list[SeasonRecord]:
        with closing(config.db.cursor()) as csr:
            csr.execute("SELECT * FROM season_records WHERE year = :year", {"year": year})
            rows: list[dict] = csr.fetchall()
            return [SeasonRecord(**row) for row in rows]

    @staticmethod
    def table_cols() -> list[dict]:
        return [
            {"name": "club", "label": "club", "field": "club"},
            {"name": "runsscored", "label": "runsscored", "field": "runsscored"},
            {"name": "wicketslost", "label": "wicketslost", "field": "wicketslost"},
            {"name": "highest", "label": "highest", "field": "highest"},
            {"name": "highestwkts", "label": "highestwkts", "field": "highestwkts"},
            {"name": "highestdate", "label": "highestdate", "field": "highestdate"},
            {"name": "highestopps", "label": "highestopps", "field": "highestopps"},
            {"name": "lowest", "label": "lowest", "field": "lowest"},
            {"name": "lowestwkts", "label": "lowestwkts", "field": "lowestwkts"},
            {"name": "lowestdate", "label": "lowestdate", "field": "lowestdate"},
            {"name": "lowestopps", "label": "lowestopps", "field": "lowestopps"},
            {"name": "byes", "label": "byes", "field": "byes"},
            {"name": "legbyes", "label": "legbyes", "field": "legbyes"},
            {"name": "wides", "label": "wides", "field": "wides"},
            {"name": "noballs", "label": "noballs", "field": "noballs"},
            {"name": "overs_bowled", "label": "overs_bowled", "field": "overs_bowled"},
            {
                "name": "overs_faced",
                "label": "overs_faced",
                "field": "overs_faced",
            },
        ]
