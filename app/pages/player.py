import sqlite3

from nicegui import ui

from app.types import Performance, Player

from .sidebar_menu import sidebar


def show_player(db: sqlite3.Connection, player_id: int) -> None:
    player = Player.get(db, player_id)
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(player.name).style("color: gold").style("font-size: 200%")

    sidebar()

    rows = [row.row_dict() for row in Performance.for_player(db, player_id)]
    with ui.row():
        with ui.table(rows=rows, columns=Performance.table_cols(), row_key="year").props("dense") as table:
            table.add_slot(
                "body-cell-year",
                r"""<td :props="props"><a :href="'/season/' + props.row.year" """
                r"""class='nicegui-link'>{{props.row.year}}</a></td>""",
            )
    with ui.row():
        ui.markdown(
            "Notes: *best*: prior to 1997, only best bowling figures reported in the end-of-season averages are recorded."
        )
