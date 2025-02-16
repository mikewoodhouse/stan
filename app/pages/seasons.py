from dataclasses import asdict

from nicegui import ui

from app.types import Season
from app.utils import add_slot_to_table, page_header

from .sidebar_menu import sidebar


def show_seasons():
    page_header("Seasons")

    sidebar()

    with ui.row():
        seasons = Season.all()

        table = ui.table(
            rows=[asdict(season) for season in seasons],
            columns=Season.table_cols(),
            pagination=30,
        ).props("dense")

        add_slot_to_table(table, "year", "season", "year")
