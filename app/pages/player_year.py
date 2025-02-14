import sqlite3

from nicegui import ui

from app.types import Player, PlayerMatchPerf

from .sidebar_menu import sidebar


def show_player_year(db: sqlite3.Connection, player_id: int, year: int):
    player = Player.get(db, player_id)

    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"{player.name}: Performances for {year}").style("color: gold").style("font-size: 200%")

    sidebar()

    years = player.match_perf_years(db)
    perfs = player.match_perfs(db, year)

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
