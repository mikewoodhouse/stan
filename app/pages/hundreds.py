from itertools import groupby

from nicegui import ui

from app.pages.sidebar_menu import sidebar
from app.types import HundredPlus
from app.utils import add_slot_to_table, page_header, sortable

COLS = [
    sortable("name", align="left"),
    sortable("score"),
    sortable("opponents", "vs"),
    sortable("date"),
]

TON_COLS = [
    sortable("name", align="left"),
    sortable("hundreds"),
]


def hundreds_report():
    sidebar()

    page_header("Hundreds")

    rows = [row.row_dict() for row in HundredPlus.all()]

    with ui.row():
        with ui.table(rows=rows, columns=COLS, row_key="id").props("dense") as table:
            add_slot_to_table(table, "name", "players", "player_id")

        ton_rows = [
            {"name": key[0], "hundreds": len(list(grp)), "player_id": key[1]}
            for key, grp in groupby(
                sorted(rows, key=lambda r: r["name"]), key=lambda row: (row["name"], row["player_id"])
            )
        ]

        ton_rows.sort(key=lambda row: row["hundreds"], reverse=True)

        with ui.table(rows=ton_rows, columns=TON_COLS).props("dense") as table:
            add_slot_to_table(table, "name", "players", "player_id")
