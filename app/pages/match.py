from nicegui import ui

from app.types import Match, MatchBatting, MatchBowling
from app.utils import coldef, page_header

from .sidebar_menu import sidebar

BATTING_COLS = [
    coldef("position"),
    coldef("fancy_name", "Name"),
    coldef("how_out_text", "How Out"),
    coldef("runs"),
    coldef("fours", "4s"),
    coldef("sixes", "6s"),
    coldef("fielding", "_"),
]


BOWLING_COLS = [
    coldef("name"),
    coldef("overs_and_balls", "Overs"),
    coldef("maidens"),
    coldef("runs_conceded", "Runs"),
    coldef("wickets"),
    coldef("econ"),
    coldef("strike_rate"),
]


def show_match(match_id: int) -> None:
    batting = MatchBatting.for_match_id(match_id)
    bowling = MatchBowling.for_match_id(match_id)
    match: dict = [match.row_dict() for match in Match.for_id(match_id)][0]

    hdr = f"{match['date']} vs {match['oppo']} ({match['venue']}) - {match['result']} - {match['bat_first']} {match['score_1']} {match['bat_second']} {match['score_2']}"

    page_header(hdr)

    sidebar()

    with ui.row():
        ui.table(
            rows=[row.row_dict() for row in batting],
            columns=BATTING_COLS,
        ).props("dense")

    with ui.row():
        ui.table(
            rows=[row.row_dict() for row in bowling],
            columns=BOWLING_COLS,
        ).props("dense")
