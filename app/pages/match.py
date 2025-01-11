import sqlite3
from dataclasses import asdict

from nicegui import ui

from app.types import Match, MatchBatting, MatchBowling


def show_match(db: sqlite3.Connection, match_id: int) -> None:
    batting = MatchBatting.for_match_id(db, match_id)
    bowling = MatchBowling.for_match_id(db, match_id)
    table_rows = [match.row_dict() for match in Match.for_id(db, match_id)]
    with ui.row():
        table = ui.table(
            rows=table_rows,
            columns=Match.table_cols(),
        ).props("dense")

    with ui.row():
        ui.table(
            rows=[row.row_dict() for row in batting],
            columns=MatchBatting.table_cols(),
        ).props("dense")

    with ui.row():
        ui.table(
            rows=[asdict(row) for row in bowling],
            columns=MatchBowling.table_cols(),
        ).props("dense")
