from dataclasses import asdict

from nicegui import ui

from app.config import config
from app.pages.sidebar_menu import sidebar
from app.types import AllTimeBowling
from app.utils import add_slot_to_table, page_header, balls_to_overs

COLS = [
    {"name": "name", "label": "Name", "field": "name", "align": "left", "sortable": True},
    {"name": "from", "label": "From", "field": "from_yr", "align": "", "sortable": True},
    {"name": "to", "label": "To", "field": "to_yr", "align": "", "sortable": True},
    {"name": "seasons", "label": "Seasons", "field": "seasons", "align": "", "sortable": True},
    {"name": "overs", "label": "Overs", "field": "overs", "align": "", "sortable": True},
    {"name": "maidens", "label": "Maidens", "field": "maidens", "align": "", "sortable": True},
    {"name": "wickets", "label": "Wickets", "field": "wickets", "align": "", "sortable": True},
    {"name": "runs", "label": "Runs", "field": "runs_conceded", "align": "", "sortable": True},
    {
        "name": "bowlave",
        "label": "Avg",
        "field": "bowlave",
        "align": "",
        "sortable": True,
        ":format": "value => value ? value.toFixed(2) : ''",
    },
    {
        "name": "strike",
        "label": "Strike",
        "field": "strike_rate",
        "align": "",
        "sortable": True,
        ":format": "value => value ? value.toFixed(2) : ''",
    },
    {
        "name": "econ",
        "label": "Econ",
        "field": "econ",
        "align": "",
        "sortable": True,
        ":format": "value => value ? value.toFixed(2) : ''",
    },
]


def show_bowling():
    page_header(f"Bowling Averages (min: {config.MIN_WICKETS} wickets)")

    sidebar()

    records = AllTimeBowling.all(config.MIN_WICKETS)

    rows = [
        asdict(row)
        | {
            "position": pos + 1,
            "overs": balls_to_overs(row.ballsbowled),
        }
        for pos, row in enumerate(records)
    ]

    with ui.row():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            add_slot_to_table(table, "name", "players", ["player_id"])
