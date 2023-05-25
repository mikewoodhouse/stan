from dataclasses import asdict, dataclass
from datetime import date
from typing import Optional

from dataclass_csv import dateformat


@dataclass(kw_only=True)
class Player:
    id: int = -1
    code: str
    surname: str
    active: bool
    initial: str = ""
    firstname: str = ""

    @property
    def name(self) -> str:
        if forename := self.firstname or self.initial:
            return f"{self.surname}, {forename}"
        return self.surname


@dataclass
class Match:
    date: date
    oppo: str
    venue: str
    result: str
    bat_first: str
    first_runs: int
    first_wkts: int
    first_all_out: bool
    first_notes: str
    second_runs: int
    second_wkts: int
    second_all_out: bool
    second_notes: str
    overs_opp: float
    overs_tocc: float
    tocc_w: int
    tocc_nb: int
    tocc_b: int
    tocc_lb: int
    opp_w: int
    opp_nb: int
    opp_b: int
    opp_lb: int


@dataclass(kw_only=True)
@dateformat(r"%Y-%m-%d %H:%M:%S")
class Partnership:
    year: int
    wicket: int
    date: date
    total: int
    undefeated: bool
    bat1: str
    bat1score: int
    bat1notout: bool
    bat2: str
    bat2score: int
    bat2notout: bool
    opp: str
    bat1_id: int = -1
    bat2_id: int = -1


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


@dataclass(kw_only=True)
class Season:
    id: int = -1
    year: int
    played: int
    won: int
    lost: int
    drawn: int
    tied: int
    noresult: int
    maxpossiblegames: int


@dataclass
class BestBowling:
    player_id: int
    year: int
    code: str
    date: date
    inns: int
    wkts: int
    runs: int
    opp: str


@dataclass
class Captain:
    player_id: int
    code: str
    year: int
    matches: int
    won: int
    lost: int
    drawn: int
    nodecision: int
    tied: int


@dataclass(kw_only=True)
@dateformat(r"%Y-%m-%d %H:%M:%S")
class HundredPlus:
    id: int = -1
    player_id: int = -1
    year: int
    code: str
    date: date
    score: int
    notout: bool
    opponents: str
    minutes: Optional[int] = None

    def row_dict(self, players: dict) -> dict:
        player: Player = players[self.player_id]
        name = player.name
        return {
            "player_id": self.player_id,
            "name": name,
            "score": f"{self.score}{'*' if self.notout else ''}",
            "opponents": self.opponents,
            "date": self.date,
        }


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
        total_overs, total_balls = divmod(self.overs * 6 + self.balls, 6)
        return f"{total_overs}.{total_balls}"

    def row_dict(self) -> dict:
        return asdict(self) | {
            "high_score": self.high_score,
            "overs_bowled": self.overs_bowled,
            "batting_average": self.batting_average,
            "bowling_average": self.bowling_average,
        }

    @property
    def batting_average(self) -> float:
        if (self.innings - self.notout) > 0:
            return round(self.runsscored / (self.innings - self.notout), 2)
        else:
            return 0

    @property
    def bowling_average(self) -> float:
        return round(self.runs / self.wickets, 2) if self.wickets > 0 else 0
