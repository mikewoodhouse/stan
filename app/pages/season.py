import sqlite3
from dataclasses import asdict

from nicegui import ui

from app.types import BattingAverage, Player, Season, SeasonRecord


def show_season(db: sqlite3.Connection, year: int) -> None:
    min_innings = 5
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"{year} Season").style("color: gold")
    with ui.row():
        season = Season.for_year(db, year)
        ui.table(rows=[asdict(season)], columns=Season.table_cols()).props("dense")
    with ui.row():
        records = [row.row_dict() for row in SeasonRecord.for_year(db, year)]
        ui.table(rows=records, columns=SeasonRecord.table_cols()).props("dense")
    with ui.row():
        players = Player.all(db)
        with ui.card():
            averages, also_batted = BattingAverage.for_year(db, year, min_innings)
            for average in averages:
                average.name = players[average.player_id].name
            records = [asdict(row) for row in averages]
            with ui.table(
                rows=records,
                columns=BattingAverage.table_cols(),
                title=f"Batting (min {min_innings} innings)",
            ).props("dense") as table:
                table.add_slot(
                    "body-cell-name",
                    r"""
                <td :props="props">
                    <a :href="'/players/' + props.row.player_id">{{props.row.name}}</a>
                </td>
                """,
                )
            for average in also_batted:
                average.name = players[average.player_id].name
            records = [asdict(row) for row in also_batted]
            columns = BattingAverage.table_cols()
            with ui.table(rows=records, columns=columns, title="Also batted").props(
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
                table.add_slot(
                    "body-cell-position",
                    r"""
                <td>&nbsp;</td>
                """,
                )
        with ui.card():
            ui.label("bowl aves")
        with ui.card():
            ui.label("other stats")
