from dataclasses import dataclass, field
from typing import Type

from app.types import (
    BestBowling,
    Captain,
    Match,
    MatchBatting,
    MatchBowling,
    Partnership,
    Performance,
    Season,
    SeasonRecord,
)
from app.types.importables import HundredPlusImport, PlayerImport


@dataclass
class LoadDefinition:
    klass: Type
    table: str
    headers: str
    player_id_cols: dict = field(default_factory=dict)
    exclude_from_insert: list[str] = field(default_factory=list)

    @property
    def header_map(self) -> list[tuple]:
        return [(h, h.lower()) for h in self.headers.split("|")]


#
# TODO: no need for this to be a dict, key is always == table, if that ceases
# to be the case (or we need a different filename) then the class definition
# can always be extended
#
load_defs = {
    "players": LoadDefinition(
        klass=PlayerImport,  # type: ignore
        table="players",
        headers="Code|Surname|Initial|Active|FirstName",
    ),
    "seasons": LoadDefinition(
        klass=Season,
        table="seasons",
        headers="Year|Played|Won|Lost|Drawn|Tied|NoResult|MaxPossibleGames",
    ),
    "hundred_plus": LoadDefinition(
        klass=HundredPlusImport,  # type: ignore
        table="hundred_plus",
        headers="Year|Code|Date|Score|NotOut|Opponents|Minutes",
        player_id_cols={
            "player_id": "code",
        },
    ),
    "partnerships": LoadDefinition(
        klass=Partnership,
        table="partnerships",
        headers="Year|Wicket|Date|Total|Undefeated|Bat1|Bat1Score|Bat1NotOut|Bat2|Bat2Score|Bat2NotOut|Opp",
        player_id_cols={
            "bat1_id": "bat1",
            "bat2_id": "bat2",
        },
        exclude_from_insert=[
            "bat1_name",
            "bat2_name",
        ],
    ),
    "performances": LoadDefinition(
        klass=Performance,
        table="performances",
        headers="Code|Year|Matches|Innings|NotOut|Highest|HighestNotOut|RunsScored|Fours|Sixes"
        "|Overs|Balls|Maidens|Wides|NoBalls|Runs|Wickets|FiveWktInn|Caught|Stumped|Fifties|Hundreds"
        "|Fives|CaughtWkt|Captain|KeptWicket",
        player_id_cols={
            "player_id": "code",
        },
        exclude_from_insert=[
            "best_bowling",
        ],
    ),
    "season_records": LoadDefinition(
        klass=SeasonRecord,
        table="season_records",
        headers="Year|Club|RunsScored|WicketsLost|Highest|HighestWkts|HighestDate|HighestOpps"
        "|Lowest|LowestWkts|LowestDate|LowestOpps|Byes|LegByes|Wides|NoBalls|BallsBowled|BallsReceived",
    ),
    "matches": LoadDefinition(
        klass=Match,
        table="matches",
        headers="date|oppo|venue|result|bat_first|first_runs|first_wkts|first_all_out|first_notes"
        "|second_runs|second_wkts|second_all_out|second_notes|overs_opp|overs_tocc|tocc_w|tocc_nb"
        "|tocc_b|tocc_lb|opp_w|opp_nb|opp_b|opp_lb",
    ),
    "match_batting": LoadDefinition(
        klass=MatchBatting,
        table="match_batting",
        headers="match_date|opp|name|position|runs|out|how_out|captain|kept_wicket|caught"
        "|caught_wkt|stumped|fours|sixes",
    ),
    "match_bowling": LoadDefinition(
        klass=MatchBowling,
        table="match_bowling",
        headers="match_date|opp|name|overs|balls|maidens|runs_conceded|wickets|wides|noballs",
    ),
    "best_bowling": LoadDefinition(
        klass=BestBowling,
        table="best_bowling",
        headers="Year|Code|Date|Inns|Wkts|Runs|Opp",
        player_id_cols={
            "player_id": "code",
        },
    ),
    "captains": LoadDefinition(
        klass=Captain,
        table="captains",
        headers="Code|Year|Matches|Won|Lost|Drawn|NoDecision|Tied",
        player_id_cols={
            "player_id": "code",
        },
    ),
}
