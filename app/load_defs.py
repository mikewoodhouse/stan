from dataclasses import dataclass, field
from app.types.classes import Player, Season, HundredPlus, Partnership
from typing import Type


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
        klass=Player,
        table="players",
        headers="Code|Surname|Initial|Active|FirstName",
    ),
    "seasons": LoadDefinition(
        klass=Season,
        table="seasons",
        headers="Year|Played|Won|Lost|Drawn|Tied|NoResult|MaxPossibleGames",
    ),
    "hundred_plus": LoadDefinition(
        klass=HundredPlus,
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
}
