from nicegui import ui

from app.types import Performance, Player
from app.utils import add_slot_to_table, page_header, sortable

from .sidebar_menu import sidebar

COLS = [
    sortable("year"),
    sortable("matches"),
    sortable("innings", "Inns"),
    sortable("notout", "N/O"),
    sortable("high_score", "High"),
    sortable("runsscored", "Runs"),
    sortable("batting_average", "Avg", decimals=2),
    sortable("fours", "4s"),
    sortable("sixes", "6s"),
    sortable("overs_bowled", "Overs"),
    sortable("maidens"),
    sortable("runs"),
    sortable("wickets"),
    sortable("bowling_average", "Avg", decimals=2),
    sortable("fivewktinn", "5+"),
    sortable("best_bowling", "Best"),
    sortable("caught", "Ct"),
    sortable("stumped", "St"),
    sortable("fifties", "50s"),
    sortable("hundreds", "100s"),
    sortable("caughtwkt", "Ct Wkt"),
    sortable("captain"),
    sortable("keptwicket", "Keeper"),
]


def show_player(player_id: int) -> None:
    player = Player.get(player_id)

    page_header(player.name)

    sidebar()

    rows = [row.row_dict() for row in Performance.for_player(player_id)]
    with ui.row():
        with ui.table(rows=rows, columns=COLS, row_key="year").props("dense") as table:
            add_slot_to_table(table, "year", "players", ["player_id", "year"])
    with ui.row():
        ui.markdown(
            "Notes: *best*: prior to 1997, only best bowling figures reported in the end-of-season averages are recorded."
        )
