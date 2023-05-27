import sqlite3
from collections import Counter

from nicegui import ui

from app.types import HundredPlus, Player


def hundreds_report(db: sqlite3.Connection):
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label("Hundreds").style("color: gold")

    with ui.row():
        ui.link("Back", "/")

    players = Player.all(db)
    rows = [row.row_dict(players) for row in HundredPlus.all(db)]

    with ui.row():
        with ui.table(rows=rows, columns=HundredPlus.table_cols(), row_key="id").props(
            "dense"
        ) as table:
            table.add_slot(
                "body-cell-name",
                r"""
                <td :props="props">
                    <a :href="'/players/' + props.row.player_id">{{props.row.name}}</a>
                </td>
                """,
            )

        ton_count = Counter(row["name"] for row in rows)
        ton_rows = [{"name": k, "hundreds": v} for k, v in ton_count.items()]
        ton_cols = [
            {"name": "name", "label": "Name", "field": "name", "sortable": True},
            {
                "name": "count",
                "label": "Hundreds",
                "field": "hundreds",
                "sortable": True,
            },
        ]

        ui.table(rows=ton_rows, columns=ton_cols).props("dense")
