from contextlib import closing

from nicegui import ui

from app.config import config
from app.utils import add_slot_to_table, coldef, page_header, sql_query

from .sidebar_menu import sidebar

tbl = ui.table(columns=[], rows=[])

COLS = [
    coldef("name", align="left"),
    coldef("from_year", "From"),
    coldef("to_year", "To"),
]


def players_like(starts_with: str = "") -> list[dict]:
    with closing(config.db.cursor()) as csr:
        csr.execute(
            sql_query("player_list"),
            {"starts_with": f"{starts_with}%"},
        )
        players = csr.fetchall()
    return players


def show_player_list() -> None:
    page_header("Players")

    sidebar()

    players = players_like("%")

    with ui.table(columns=COLS, rows=players, pagination=30).props("dense") as table:
        with table.add_slot("top-right"):
            with ui.input(placeholder="Search").props("type=search").bind_value(table, "filter").add_slot("append"):
                ui.icon("search")
        add_slot_to_table(table, "name", "players", "player_id")
