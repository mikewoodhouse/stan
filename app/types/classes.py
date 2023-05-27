from dataclasses import dataclass
from datetime import date


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
