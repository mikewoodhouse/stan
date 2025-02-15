from nicegui import ui

from app.config import config
from app.types import Performance

from .sidebar_menu import sidebar

COLS = [
    {"name": "player_name", "label": "Name", "field": "player_name", "align": "left"},
    {"name": "apps", "label": "Apps", "field": "appearances", "align": "right"},
    {"name": "from_yr", "label": "From", "field": "from_year", "align": "center"},
    {"name": "to_yr", "label": "To", "field": "to_year", "align": "center"},
]


def show_appearances():
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label("Career Appearances").style("color: gold").style("font-size: 200%")

    sidebar()

    rows = Performance.career_appearances()
    with ui.row():
        with ui.column():
            ui.label(f"All players with a minimum of {config.MIN_APPS} appearances")
            ui.table(rows=rows, columns=COLS).props("dense").add_slot(
                "body-cell-player_name",
                r"""
                    <td :props="props">
                        <a :href="'/players/' + props.row.player_id" class='nicegui-link'>{{props.row.player_name}}</a>
                    </td>
                    """,
            )
