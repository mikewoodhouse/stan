from dataclasses import dataclass


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
