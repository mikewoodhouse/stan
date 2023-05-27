from dataclasses import asdict, dataclass

from app.utils import balls_to_overs


@dataclass(kw_only=True)
class Performance:
    id: int = -1
    player_id: int = -1
    code: str
    year: int
    matches: int
    innings: int = 0
    notout: int = 0
    highest: int = 0
    highestnotout: bool = False
    runsscored: int = 0
    fours: int = 0
    sixes: int = 0
    overs: int = 0
    balls: int = 0
    maidens: int = 0
    wides: int = 0
    noballs: int = 0
    runs: int = 0
    wickets: int = 0
    fivewktinn: int = 0
    caught: int = 0
    stumped: int = 0
    fifties: int = 0
    hundreds: int = 0
    fives: int = 0
    caughtwkt: int = 0
    captain: int = 0
    keptwicket: int = 0

    @property
    def high_score(self) -> str:
        return f"{self.highest}{'*' if self.highestnotout else ''}"

    @property
    def overs_bowled(self) -> str:
        return balls_to_overs(self.overs * 6 + self.balls)

    @property
    def batting_average(self) -> float:
        if (self.innings - self.notout) > 0:
            return round(self.runsscored / (self.innings - self.notout), 2)
        else:
            return 0

    @property
    def bowling_average(self) -> float:
        return round(self.runs / self.wickets, 2) if self.wickets > 0 else 0

    def row_dict(self) -> dict:
        return asdict(self) | {
            "high_score": self.high_score,
            "overs_bowled": self.overs_bowled,
            "batting_average": self.batting_average,
            "bowling_average": self.bowling_average,
        }
