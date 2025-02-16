from nicegui import ui

from app.types import Performance, Player
from app.utils import add_slot_to_table, page_header

from .sidebar_menu import sidebar


def show_player(player_id: int) -> None:
    player = Player.get(player_id)

    page_header(player.name)

    sidebar()

    rows = [row.row_dict() for row in Performance.for_player(player_id)]
    with ui.row():
        with ui.table(rows=rows, columns=Performance.table_cols(), row_key="year").props("dense") as table:
            add_slot_to_table(table, "year", "players", ["player_id", "year"])
    with ui.row():
        ui.markdown(
            "Notes: *best*: prior to 1997, only best bowling figures reported in the end-of-season averages are recorded."
        )
