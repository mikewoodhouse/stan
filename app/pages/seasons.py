import sqlite3
from contextlib import closing
from dataclasses import asdict

from nicegui import ui

from app.types import Season


def get_seasons(db: sqlite3.Connection) -> list[Season]:
    with closing(db.cursor()) as csr:
        csr.execute("SELECT * FROM seasons ORDER BY year")
        rows: list[dict] = csr.fetchall()
        return [Season(**row) for row in rows]


def show_seasons(db):
    cols = [
        {"name": "year", "label": "Year", "field": "year", "align": "center"},
        {"name": "played", "label": "P", "field": "played"},
        {"name": "won", "label": "W", "field": "won"},
        {"name": "lost", "label": "L", "field": "lost"},
        {"name": "drawn", "label": "D", "field": "drawn"},
        {"name": "tied", "label": "T", "field": "tied"},
        {"name": "noresult", "label": "N/R", "field": "noresult"},
    ]
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label("Seasons").style("color: gold")
    with ui.row():
        seasons = get_seasons(db)
        with ui.table(
            rows=[asdict(season) for season in seasons], columns=cols, pagination=20
        ).props("dense") as table:
            table.add_slot(
                "body-cell-year",
                r"""
                <td :props="props" style="text-align:center">
                    <a :href="'/season/' + props.row.year">{{props.row.year}}</a>
                </td>
                """,
            )
