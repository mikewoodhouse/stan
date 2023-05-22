from nicegui import ui
from contextlib import closing
import sqlite3
from app.types.classes import Player, HundredPlus

from collections import Counter


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


db = sqlite3.connect("stan.sqlite")
db.row_factory = dict_factory


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


cols = [
    {"name": "name", "label": "Name", "field": "name", "sortable": True},
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
    {"name": "date", "label": "Date", "field": "date", "sortable": True},
]

players = all_players(db)

rows = [row.row_dict(players) for row in hundreds(db)]

with ui.header():
    ui.label("Hundreds")

with ui.row():
    ui.table(rows=rows, columns=cols, row_key="code").classes(remove="q-table")

    ton_count = Counter(row["name"] for row in rows)

    ton_rows = [{"name": k, "hundreds": v} for k, v in ton_count.items()]
    ton_cols = [
        {"name": "name", "label": "Name", "field": "name", "sortable": True},
        {"name": "count", "label": "Hundreds", "field": "hundreds", "sortable": True},
    ]

    ui.table(rows=ton_rows, columns=ton_cols)

ui.run()
