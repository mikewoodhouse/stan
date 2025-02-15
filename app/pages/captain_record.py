import sqlite3

from nicegui import ui

from app.pages.sidebar_menu import sidebar
from app.types import Captain, Player

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


def show_captain(db: sqlite3.Connection, player_id: int):
    player = Player.get(db, player_id)

    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"Captaincy by year: {player.name}").style("color: gold").style("font-size: 200%")

    sidebar()

    rows = Captain.for_player(db, player_id)

    # weirdness: can't seem to construct the target in the add_slot() call, so putting it together outside
    for row in rows:
        row["player_year_addr"] = f"{player_id}/{row['year']}"

    with ui.column():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            table.add_slot(
                "body-cell-year",
                r"""
                <td :props="props">
                    <a :href="'/players/' + props.row.player_year_addr" class='nicegui-link'>
                        {{props.row.year}}
                    </a>
                </td>
                """,
            )
