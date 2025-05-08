from dataclasses import asdict

from nicegui import ui

from app.types import BattingAverage, BowlingAverage, Partnership, Season, SeasonRecord
from app.utils import add_slot_to_table, coldef, page_header, sortable

from .sidebar_menu import sidebar

SEASON_COLS = [
    coldef("year", align="left"),
    coldef("played", "P"),
    coldef("won", "W"),
    coldef("lost", "L"),
    coldef("drawn", "D"),
    coldef("tied", "T"),
    coldef("noresult", "N/D"),
]

SEASON_RECORD_COLS = [
    coldef("club"),
    coldef("runsscored", "Runs"),
    coldef("wicketslost", "Wickets Lost"),
    coldef("highest_score", "Highest"),
    coldef("highestdate", "Date"),
    coldef("highestopps", "Vs", align="left"),
    coldef("lowest_score", "Lowest"),
    coldef("lowestdate", "Date"),
    coldef("lowestopps", "Vs", align="left"),
    coldef("byes"),
    coldef("legbyes"),
    coldef("wides"),
    coldef("noballs"),
    coldef("overs_bowled"),
    coldef("overs_faced"),
]

BATTING_COLS = [
    sortable("position", "Pos"),
    sortable("name", align="left"),
    sortable("innings", "Inns"),
    sortable("notout", "N/O"),
    sortable("high_score", "High"),
    sortable("runsscored", "Runs"),
    sortable("average", "Avg", decimals=2),
    sortable("fifties", "50s"),
    sortable("hundreds", "100s"),
    sortable("fours", "4s"),
    sortable("sixes", "6s"),
]

BOWLING_COLS = [
    sortable("position", "Pos"),
    sortable("name", align="left"),
    sortable("overs_bowled", "Overs"),
    sortable("maidens"),
    sortable("runs"),
    sortable("wickets"),
    sortable("average", "Avg", decimals=2),
    sortable("strike_rate", decimals=2),
    sortable("economy", decimals=2),
    sortable("five+", "5+"),
]


def show_season(year: int) -> None:
    min_innings = 5
    min_wickets = 10
    min_partnership_total = 75

    page_header(f"{year} Season")

    sidebar()

    with ui.row():
        season = Season.for_year(year)
        ui.table(rows=[asdict(season)], columns=SEASON_COLS).props("dense")
        with ui.card():
            ui.link("Matches", f"/matches/{year}")
        with ui.card():
            with ui.row():
                if season.prev_year:
                    ui.link("Previous", f"/season/{year - 1}")
                if season.next_year:
                    ui.link("Next", f"/season/{year + 1}")
    with ui.row():
        records = SeasonRecord.for_year(year)
        ui.table(rows=records, columns=SEASON_RECORD_COLS).props("dense")
    with ui.row():
        with ui.card():
            averages, also_batted = BattingAverage.for_year(year, min_innings)
            show_batting(min_innings, averages, show_position=True)
            show_batting(min_innings, also_batted, show_position=False)
        with ui.card():
            bowl_aves, also_bowled = BowlingAverage.for_year(year, min_wickets)
            show_bowling(min_wickets, bowl_aves, show_position=True)
            show_bowling(min_wickets, also_bowled, show_position=False)
    with ui.row():
        with ui.card():
            ui.label(f"Where recorded, best for each wicket and any others of {min_partnership_total} or over").style(
                "font-style: italic"
            )
            rows = [row.row_dict() for row in Partnership.for_season(year, min_partnership_total)]
            ui.table(rows=rows, columns=Partnership.table_cols(True), title="Partnerships").props("dense")


def show_batting(min_innings, averages, show_position=True):
    records = [asdict(row) for row in averages]
    table = ui.table(
        rows=records,
        columns=BATTING_COLS,
        title=(f"Batting (min {min_innings} innings)" if show_position else "Also batted"),
    ).props("dense")
    add_slot_to_table(table, "name", "players", "player_id")
    if not show_position:
        table.add_slot(
            "body-cell-position",
            r"""<td>&nbsp;</td>""",
        )


def show_bowling(min_wickets, averages, show_position=True):
    records = [asdict(row) for row in averages]
    with ui.table(
        rows=records,
        columns=BOWLING_COLS,
        title=(f"Bowling (min {min_wickets} wickets)" if show_position else "Also bowled"),
    ).props("dense") as table:
        add_slot_to_table(table, "name", "players", "player_id")
        if not show_position:
            table.add_slot(
                "body-cell-position",
                r"""<td>&nbsp;</td>""",
            )
