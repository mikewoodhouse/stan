from dataclasses import dataclass, field
from typing import Type

from app.types import Partnership, Performance, Season, SeasonRecord
from app.types.importables import HundredPlusImport, PlayerImport


@dataclass
class LoadDefinition:
    klass: Type
    table: str
    headers: str
    player_id_cols: dict = field(default_factory=dict)

    @property
    def header_map(self) -> list[tuple]:
        return [(h, h.lower()) for h in self.headers.split("|")]


load_defs = {
    "players": LoadDefinition(
        klass=PlayerImport,
        table="players",
        headers="Code|Surname|Initial|Active|FirstName",
    ),
    "seasons": LoadDefinition(
        klass=Season,
        table="seasons",
        headers="Year|Played|Won|Lost|Drawn|Tied|NoResult|MaxPossibleGames",
    ),
    "hundred_plus": LoadDefinition(
        klass=HundredPlusImport,
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
    ),
    "season_records": LoadDefinition(
        klass=SeasonRecord,
        table="season_records",
        headers="Year|Club|RunsScored|WicketsLost|Highest|HighestWkts|HighestDate|HighestOpps"
        "|Lowest|LowestWkts|LowestDate|LowestOpps|Byes|LegByes|Wides|NoBalls|BallsBowled|BallsReceived",
    ),
}
