from nicegui import ui

from app.pages.sidebar_menu import sidebar
from app.types import Captain, Player
from app.utils import add_slot_to_table, page_header

COLS = [
    {"name": "year", "label": "Year", "field": "year", "sortable": True},
    {"name": "matches", "label": "Matches", "field": "matches", "sortable": True},
    {"name": "won", "label": "W", "field": "won", "sortable": True},
    {"name": "lost", "label": "L", "field": "lost", "sortable": True},
    {"name": "drawn", "label": "D", "field": "drawn", "sortable": True},
    {"name": "nodecision", "label": "N/D", "field": "nodecision", "sortable": True},
    {"name": "tied", "label": "T", "field": "tied", "sortable": True},
    {"name": "won_pct", "label": "Won", "field": "won_pct", "sortable": True},
    {"name": "not_lost_pct", "label": "Not Lost", "field": "not_lost_pct", "sortable": True},
]


def show_captain(player_id: int):
    player = Player.get(player_id)

    page_header(f"Captaincy by year: {player.name}")

    sidebar()

    rows = Captain.for_player(player_id)

    with ui.column():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            add_slot_to_table(table, "year", "players", ["player_id", "year"])
