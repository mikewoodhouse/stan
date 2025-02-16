from nicegui import ui

from app.types import Player, PlayerMatchPerf
from app.utils import page_header

from .sidebar_menu import sidebar


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
            columns=PlayerMatchPerf.table_cols(),
        ).props("dense")
