import sqlite3
from dataclasses import asdict

from nicegui import ui

from app.types import BattingAverage, BowlingAverage, Partnership, Player, Season, SeasonRecord

from .sidebar_menu import sidebar


def show_season(db: sqlite3.Connection, year: int) -> None:
    min_innings = 5
    min_wickets = 10
    min_partnership_total = 75
    players = Player.all(db)

    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"{year} Season").style("color: gold").style("font-size: 200%")

    sidebar()

    with ui.row():
        season = Season.for_year(db, year)
        ui.table(rows=[asdict(season)], columns=Season.table_cols()).props("dense")
        with ui.card():
            ui.link("Matches", f"/matches/{year}")
    with ui.row():
        records = [row.row_dict() for row in SeasonRecord.for_year(db, year)]
        ui.table(rows=records, columns=SeasonRecord.table_cols()).props("dense")
    with ui.row():
        with ui.card():
            averages, also_batted = BattingAverage.for_year(db, year, min_innings)
            show_batting(min_innings, players, averages, show_position=True)
            show_batting(min_innings, players, also_batted, show_position=False)
        with ui.card():
            bowl_aves, also_bowled = BowlingAverage.for_year(db, year, min_wickets)
            show_bowling(min_wickets, players, bowl_aves, show_position=True)
            show_bowling(min_wickets, players, also_bowled, show_position=False)
    with ui.row():
        with ui.card():
            ui.label(f"Where recorded, best for each wicket and any others of {min_partnership_total} or over").style(
                "font-style: italic"
            )
            rows = [row.row_dict() for row in Partnership.for_season(db, year, min_partnership_total)]
            ui.table(rows=rows, columns=Partnership.table_cols(True), title="Partnerships").props("dense")


def show_batting(min_innings, players, averages, show_position=True):
    for average in averages:
        average.name = players[average.player_id].name
    records = [asdict(row) for row in averages]
    table = ui.table(
        rows=records,
        columns=BattingAverage.table_cols(),
        title=(f"Batting (min {min_innings} innings)" if show_position else "Also batted"),
    ).props("dense")

    table.add_slot(
        "body-cell-name",
        r"""
                <td :props="props">
                    <a :href="'/players/' + props.row.player_id" class='nicegui-link'>{{props.row.name}}</a>
                </td>
                """,
    )
    if not show_position:
        table.add_slot(
            "body-cell-position",
            r"""<td>&nbsp;</td>""",
        )


def show_bowling(min_wickets, players, averages, show_position=True):
    for average in averages:
        average.name = players[average.player_id].name
    records = [asdict(row) for row in averages]
    with ui.table(
        rows=records,
        columns=BowlingAverage.table_cols(),
        title=(f"Bowling (min {min_wickets} wickets)" if show_position else "Also bowled"),
    ).props("dense") as table:
        table.add_slot(
            "body-cell-name",
            r"""
                <td :props="props">
                    <a :href="'/players/' + props.row.player_id" class='nicegui-link'>{{props.row.name}}</a>
                </td>
                """,
        )
        if not show_position:
            table.add_slot(
                "body-cell-position",
                r"""<td>&nbsp;</td>""",
            )
