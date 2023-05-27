from dataclasses import asdict, dataclass
from datetime import date

from dataclass_csv import dateformat

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
