from dataclasses import asdict

from nicegui import ui

from app.types import Season

from .sidebar_menu import sidebar


def show_seasons(db):
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label("Seasons").style("color: gold")

    sidebar()

    with ui.row():
        seasons = Season.all(db)

        table = ui.table(
            rows=[asdict(season) for season in seasons],
            columns=Season.table_cols(),
            pagination=30,
        ).props("dense")

        table.add_slot(
            "body-cell-year",
            r"""
            <td :props="props" style="text-align:center">
                <a :href="'/season/' + props.row.year" class='nicegui-link'>{{props.row.year}}</a>
            </td>
            """,
        )
