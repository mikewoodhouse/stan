from nicegui import ui

from app.types import Match
from app.utils import add_slot_to_table, page_header

from .sidebar_menu import sidebar


def show_matches(year: int) -> None:
    page_header(f"Season {year} matches")

    sidebar()

    table_rows = [match.row_dict() for match in Match.for_year(year)]
    with ui.row():
        table = ui.table(
            rows=table_rows,
            columns=Match.table_cols(),
        ).props("dense")

        add_slot_to_table(table, "oppo", "match", "id")
