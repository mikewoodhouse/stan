from collections import Counter

from nicegui import ui

from app.pages.sidebar_menu import sidebar
from app.types import HundredPlus, Player
from app.utils import add_slot_to_table, page_header, sortable

COLS = [
    sortable("name", align="left"),
    sortable("score"),
    sortable("opponents", "vs"),
    sortable("date"),
]

TON_COLS = [
    sortable("name", align="left"),
    sortable("hundreds"),
]


def hundreds_report():
    sidebar()

    page_header("Hundreds")

    players = Player.all()

    rows = [row.row_dict(players) for row in HundredPlus.all()]

    with ui.row():
        with ui.table(rows=rows, columns=COLS, row_key="id").props("dense") as table:
            add_slot_to_table(table, "name", "players", "player_id")

        players_by_name = {p.name: p.id for p in players.values()}
        ton_count = Counter(row["name"] for row in rows)
        ton_rows = [{"name": k, "hundreds": v, "player_id": players_by_name[k]} for k, v in ton_count.items()]
        ton_rows.sort(key=lambda row: row["hundreds"], reverse=True)

        with ui.table(rows=ton_rows, columns=TON_COLS).props("dense") as table:
            add_slot_to_table(table, "name", "players", "player_id")
