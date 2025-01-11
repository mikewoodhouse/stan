import sqlite3

from nicegui import ui

from app.types import Match

from .sidebar_menu import sidebar


def show_matches(db: sqlite3.Connection, year: int) -> None:
    sidebar()

    with ui.row():
        ui.label(f"{year} Matches")

    table_rows = [match.row_dict() for match in Match.for_year(db, year)]
    with ui.row():
        table = ui.table(
            rows=table_rows,
            columns=Match.table_cols(),
        ).props("dense")

        table.add_slot(
            "body-cell-oppo",
            r"""
            <td :props="props" style="text-align:center">
                <a :href="'/match/' + props.row.id">{{props.row.oppo}}</a>
            </td>
            """,
        )
