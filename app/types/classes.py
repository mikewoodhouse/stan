from dataclasses import dataclass
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


@dataclass
class SeasonRecord:
    year: int
    club: str
    runsscored: int
    wicketslost: int
    highest: int
    highestwkts: int
    highestdate: date
    highestopps: str
    lowest: int
    lowestwkts: int
    lowestdate: date
    lowestopps: str
    byes: int
    legbyes: int
    wides: int
    noballs: int
    ballsbowled: int
    ballsreceived: int


@dataclass
class Season:
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
            "name": name,
            "score": f"{self.score}{'*' if self.notout else ''}",
            "opponents": self.opponents,
            "date": self.date,
        }


@dataclass
class Performance:
    player_id: int
    code: str
    year: int
    matches: int
    innings: int
    notout: int
    highest: int
    highestnotout: bool
    runsscored: int
    fours: int
    sixes: int
    overs: int
    balls: int
    maidens: int
    wides: int
    noballs: int
    runs: int
    wickets: int
    fivewktinn: int
    caught: int
    stumped: int
    fifties: int
    hundreds: int
    fives: int
    caughtwkt: int
    captain: int
    keptwicket: int
