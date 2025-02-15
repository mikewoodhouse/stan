from nicegui import ui

from app.pages.sidebar_menu import sidebar
from app.types import Captain

COLS = [
    {"name": "player_name", "label": "Name", "field": "player_name", "align": "left", "sortable": True},
    {"name": "matches", "label": "Matches", "field": "matches", "sortable": True},
    {"name": "won", "label": "W", "field": "won", "sortable": True},
    {"name": "lost", "label": "L", "field": "lost", "sortable": True},
    {"name": "drawn", "label": "D", "field": "drawn", "sortable": True},
    {"name": "nodecision", "label": "N/D", "field": "nodecision", "sortable": True},
    {"name": "tied", "label": "T", "field": "tied", "sortable": True},
    {"name": "won_pct", "label": "Won", "field": "won_pct", "sortable": True},
    {"name": "not_lost_pct", "label": "Not Lost", "field": "not_lost_pct", "sortable": True},
]


def show_captains():
    sidebar()

    rows = Captain.all()

    with ui.column():
        ui.table(rows=rows, columns=COLS).props("dense").add_slot(
            "body-cell-player_name",
            r"""
                    <td :props="props">
                        <a :href="'/captains/' + props.row.player_id" class='nicegui-link'>{{props.row.player_name}}</a>
                    </td>
                    """,
        )
