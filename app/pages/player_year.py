import sqlite3

from nicegui import ui

from app.types import MatchBatting, Player

from .sidebar_menu import sidebar


def show_player_year(db: sqlite3.Connection, player_id: int, year: int):
    player = Player.get(db, player_id)
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(player.name).style("color: gold")

    sidebar()

    # batting
    batting_data = MatchBatting.for_player(db, player_id)
    rows = [row.row_dict() for row in batting_data]
    years = {row.match_date.year for row in batting_data}
    with ui.row():
        with ui.table(rows=rows, columns=[]):
            pass
