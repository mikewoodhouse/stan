from nicegui import ui

from app.types import Player
from app.utils import coldef, page_header

from .sidebar_menu import sidebar

COLS = [
    coldef("match_date", "Date"),
    coldef("opp", align="left"),
    coldef("position", "Pos"),
    coldef("how_out"),
    coldef("runs_scored", "Runs"),
    coldef("fours", "4s"),
    coldef("sixes", "6s"),
    coldef("overs_balls", "Overs"),
    coldef("maidens"),
    coldef("runs_conceded", "Runs"),
    coldef("wickets"),
    coldef("fielding"),
]


def show_player_year(player_id: int, year: int):
    player = Player.get(player_id)

    page_header(f"{player.name}: Performances for {year}")

    sidebar()

    years = player.match_perf_years()
    perfs = player.match_perfs(year)

    with ui.row():
        for yr in years:
            if yr == year:
                ui.label(str(yr))
            else:
                ui.link(str(yr), f"/players/{player_id}/{yr}")
    with ui.row():
        ui.table(
            rows=[perf.row_dict() for perf in perfs],
            columns=COLS,
        ).props("dense")
