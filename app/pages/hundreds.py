import sqlite3
from collections import Counter
from contextlib import closing

from nicegui import ui

from app.types.classes import HundredPlus, Player

HUNDREDS_COLS = [
    {
        "name": "name",
        "label": "Name",
        "field": "name",
        "sortable": True,
        "align": "left",
    },
    {
        "name": "score",
        "label": "Score",
        "field": "score",
        "sortable": True,
        "align": "center",
    },
    {
        "name": "opps",
        "label": "Vs",
        "field": "opponents",
        "sortable": True,
        "align": "left",
    },
    {
        "name": "date",
        "label": "Date",
        "field": "date",
        "sortable": True,
        "align": "center",
    },
]


def all_players(conn: sqlite3.Connection) -> dict[int, Player]:
    with closing(conn.cursor()) as csr:
        csr.execute("SELECT * FROM players")
        rows = csr.fetchall()
    player_list = [Player(**row) for row in rows]
    return {player.id: player for player in player_list}


def hundreds(db):
    with closing(db.cursor()) as csr:
        csr.execute("SELECT * FROM hundred_plus")
        rows = list(csr.fetchall())
        return [HundredPlus(**row) for row in rows]


def handle_cell_click(msg):
    print(msg)


def hundreds_report(db: sqlite3.Connection):
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label("Hundreds").style("color: gold")

    with ui.row():
        ui.link("Back", "/")

    players = all_players(db)
    rows = [row.row_dict(players) for row in hundreds(db)]

    with ui.row():
        with ui.table(rows=rows, columns=HUNDREDS_COLS, row_key="id").props(
            "dense"
        ) as table:
            table.add_slot(
                "body-cell-name",
                r"""
                <td :props="props"><a :href="'/players/' + props.row.player_id">{{props.row.name}}</a></td>
                """,
            )

        ton_count = Counter(row["name"] for row in rows)
        ton_rows = [{"name": k, "hundreds": v} for k, v in ton_count.items()]
        ton_cols = [
            {"name": "name", "label": "Name", "field": "name", "sortable": True},
            {
                "name": "count",
                "label": "Hundreds",
                "field": "hundreds",
                "sortable": True,
            },
        ]

        ui.table(rows=ton_rows, columns=ton_cols).props("dense")
