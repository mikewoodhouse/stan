from collections import Counter

from nicegui import ui

from app.pages.sidebar_menu import sidebar
from app.types import HundredPlus, Player
from app.utils import add_slot_to_table, page_header


def hundreds_report():
    sidebar()

    page_header("Hundreds")

    with ui.row():
        ui.link("Back", "/")

    players = Player.all()
    rows = [row.row_dict(players) for row in HundredPlus.all()]

    with ui.row():
        show_hundreds_data_row(rows, players)


# TODO Rename this here and in `hundreds_report`
def show_hundreds_data_row(rows: list[dict], players: dict[int, Player]):
    with ui.table(rows=rows, columns=HundredPlus.table_cols(), row_key="id").props("dense") as table:
        add_slot_to_table(table, "name", "players", "player_id")

    players_by_name = {p.name: p.id for p in players.values()}
    ton_count = Counter(row["name"] for row in rows)
    ton_rows = [{"name": k, "hundreds": v, "player_id": players_by_name[k]} for k, v in ton_count.items()]
    ton_cols = [
        {
            "name": "name",
            "label": "Name",
            "field": "name",
            "sortable": True,
        },
        {
            "name": "count",
            "label": "Hundreds",
            "field": "hundreds",
            "sortable": True,
        },
    ]

    with ui.table(rows=ton_rows, columns=ton_cols).props("dense") as table:
        add_slot_to_table(table, "name", "players", "player_id")
