import sqlite3
from collections import Counter

from nicegui import ui

from app.pages.sidebar_menu import sidebar
from app.types import HundredPlus, Player


def hundreds_report(db: sqlite3.Connection):
    sidebar()

    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label("Hundreds").style("color: gold").style("font-size: 200%")

    with ui.row():
        ui.link("Back", "/")

    players = Player.all(db)
    rows = [row.row_dict(players) for row in HundredPlus.all(db)]

    with ui.row():
        show_hundreds_data_row(rows, players)


# TODO Rename this here and in `hundreds_report`
def show_hundreds_data_row(rows: list[dict], players: dict[int, Player]):
    ui.table(rows=rows, columns=HundredPlus.table_cols(), row_key="id").props("dense").add_slot(
        "body-cell-name",
        r"""
                <td :props="props">
                    <a :href="'/players/' + props.row.player_id" class='nicegui-link'>{{props.row.name}}</a>
                </td>
                """,
    )

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

    ui.table(rows=ton_rows, columns=ton_cols).props("dense").add_slot(
        "body-cell-name",
        r"""
                <td :props="props">
                    <a :href="'/players/' + props.row.player_id" class='nicegui-link'>{{props.row.name}}</a>
                </td>
                """,
    )
