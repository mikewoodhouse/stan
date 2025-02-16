from dataclasses import asdict

from nicegui import ui

from app.types import BattingAverage, BowlingAverage, Partnership, Player, Season, SeasonRecord
from app.utils import add_slot_to_table, page_header

from .sidebar_menu import sidebar


def show_season(year: int) -> None:
    min_innings = 5
    min_wickets = 10
    min_partnership_total = 75
    players = Player.all()

    page_header(f"{year} Season")

    sidebar()

    with ui.row():
        season = Season.for_year(year)
        ui.table(rows=[asdict(season)], columns=Season.table_cols()).props("dense")
        with ui.card():
            ui.link("Matches", f"/matches/{year}")
    with ui.row():
        records = SeasonRecord.for_year(year)
        ui.table(rows=records, columns=SeasonRecord.table_cols()).props("dense")
    with ui.row():
        with ui.card():
            averages, also_batted = BattingAverage.for_year(year, min_innings)
            show_batting(min_innings, players, averages, show_position=True)
            show_batting(min_innings, players, also_batted, show_position=False)
        with ui.card():
            bowl_aves, also_bowled = BowlingAverage.for_year(year, min_wickets)
            show_bowling(min_wickets, players, bowl_aves, show_position=True)
            show_bowling(min_wickets, players, also_bowled, show_position=False)
    with ui.row():
        with ui.card():
            ui.label(f"Where recorded, best for each wicket and any others of {min_partnership_total} or over").style(
                "font-style: italic"
            )
            rows = [row.row_dict() for row in Partnership.for_season(year, min_partnership_total)]
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
    add_slot_to_table(table, "name", "players", "player_id")
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
        add_slot_to_table(table, "name", "players", "player_id")
        if not show_position:
            table.add_slot(
                "body-cell-position",
                r"""<td>&nbsp;</td>""",
            )
