from nicegui import ui

from app.types import Match
from app.utils import add_slot_to_table, coldef, page_header

from .sidebar_menu import sidebar

COLS = [
    coldef("match_date", "Date", sortable=True),
    coldef("oppo", "Opponents"),
    coldef("venue", "H/A"),
    coldef("result"),
    coldef("bat_first", "1st Inns"),
    coldef("score_1", "Score"),
    coldef("first_notes", "_"),
    coldef("score_2", "2nd Inns"),
    coldef("second_notes", "_"),
]


def show_matches(year: int) -> None:
    page_header(f"Season {year} matches")

    sidebar()

    table_rows = [match.row_dict() for match in Match.for_year(year)]
    with ui.row():
        table = ui.table(
            rows=table_rows,
            columns=COLS,
        ).props("dense")

        add_slot_to_table(table, "oppo", "match", "id")
