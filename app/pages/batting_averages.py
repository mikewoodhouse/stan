from dataclasses import asdict

from nicegui import ui

from app.config import config
from app.pages.sidebar_menu import sidebar
from app.types import AllTimeBatting

COLS = [
    {"name": "pos", "label": "", "field": "position", "align": "center", "sortable": True},
    {"name": "name", "label": "Name", "field": "name", "align": "left", "sortable": True},
    {"name": "from_yr", "label": "From", "field": "from_yr", "align": "", "sortable": True},
    {"name": "to_yr", "label": "To", "field": "to_yr", "align": "", "sortable": True},
    {"name": "seasons", "label": "Seasons", "field": "seasons", "align": "", "sortable": True},
    {"name": "matches", "label": "Matches", "field": "matches", "align": "", "sortable": True},
    {"name": "innings", "label": "Inns", "field": "innings", "align": "", "sortable": True},
    {"name": "notout", "label": "N/O", "field": "notout", "align": "", "sortable": True},
    {"name": "high_score", "label": "High", "field": "high_score", "align": "", "sortable": True},
    {"name": "runsscored", "label": "Runs", "field": "runsscored", "align": "", "sortable": True},
    {
        "name": "batave",
        "label": "Avg",
        "field": "batave",
        "align": "",
        "sortable": True,
        ":format": "value => value ? value.toFixed(2) : ''",
    },
    {"name": "fours", "label": "4s", "field": "fours", "align": "", "sortable": True},
    {"name": "sixes", "label": "6s", "field": "sixes", "align": "", "sortable": True},
    {"name": "fifties", "label": "50s", "field": "fifties", "align": "", "sortable": True},
    {"name": "hundreds", "label": "100s", "field": "hundreds", "align": "", "sortable": True},
]


def show_batting():
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"Batting Averages (min: {config.MIN_INNINGS} innings)").style("color: gold").style("font-size: 200%")

    sidebar()

    records = AllTimeBatting.all(config.MIN_INNINGS)
    rows = [asdict(row) | {"position": pos + 1} for pos, row in enumerate(records)]

    with ui.row():
        ui.table(rows=rows, columns=COLS).props("dense").add_slot(
            "body-cell-name",
            r"""
                <td :props="props">
                    <a :href="'/players/' + props.row.player_id" class='nicegui-link'>{{props.row.name}}</a>
                </td>
                """,
        )
