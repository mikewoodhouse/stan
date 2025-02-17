from nicegui import ui

from app.pages.sidebar_menu import sidebar
from app.types import Captain, Player
from app.utils import add_slot_to_table, page_header, sortable

COLS = [
    sortable("year"),
    sortable("matches"),
    sortable("won", "W"),
    sortable("lost", "L"),
    sortable("drawn", "D"),
    sortable("nodecision", "N/D"),
    sortable("tied", "T"),
    sortable("won_pct", "Won%"),
    sortable("not_lost_pct", "Not Lost%"),
]


def show_captain(player_id: int):
    player = Player.get(player_id)

    page_header(f"Captaincy by year: {player.name}")

    sidebar()

    rows = Captain.for_player(player_id)

    with ui.column():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            add_slot_to_table(table, "year", "players", ["player_id", "year"])
