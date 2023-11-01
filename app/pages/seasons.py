from dataclasses import asdict

from nicegui import ui

from app.types import Season


def show_seasons(db):
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label("Seasons").style("color: gold")
    with ui.row():
        seasons = Season.all(db)
        with ui.table(
            rows=[asdict(season) for season in seasons],
            columns=Season.table_cols(),
            pagination=20,
        ).props("dense") as table:
            table.add_slot(
                "body-cell-year",
                r"""
                <td :props="props" style="text-align:center">
                    <a :href="'/season/' + props.row.year">{{props.row.year}}</a>
                </td>
                """,
            )
