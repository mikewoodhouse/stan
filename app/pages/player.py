from nicegui import ui
from contextlib import closing
from app.types.classes import Player, Performance
import sqlite3
from dataclasses import asdict

COLS = [
    {"name": "year", "label": "year", "field": "year", "sortable": True},
    {"name": "matches", "label": "matches", "field": "matches", "sortable": True},
    {"name": "innings", "label": "innings", "field": "innings", "sortable": True},
    {"name": "notout", "label": "notout", "field": "notout", "sortable": True},
    {"name": "highest", "label": "highest", "field": "highest", "sortable": True},
    {
        "name": "highestnotout",
        "label": "highestnotout",
        "field": "highestnotout",
        "sortable": True,
    },
    {
        "name": "runsscored",
        "label": "runsscored",
        "field": "runsscored",
        "sortable": True,
    },
    {"name": "fours", "label": "fours", "field": "fours", "sortable": True},
    {"name": "sixes", "label": "sixes", "field": "sixes", "sortable": True},
    {"name": "overs", "label": "overs", "field": "overs", "sortable": True},
    {"name": "balls", "label": "balls", "field": "balls", "sortable": True},
    {"name": "maidens", "label": "maidens", "field": "maidens", "sortable": True},
    {"name": "wides", "label": "wides", "field": "wides", "sortable": True},
    {"name": "noballs", "label": "noballs", "field": "noballs", "sortable": True},
    {"name": "runs", "label": "runs", "field": "runs", "sortable": True},
    {"name": "wickets", "label": "wickets", "field": "wickets", "sortable": True},
    {
        "name": "fivewktinn",
        "label": "fivewktinn",
        "field": "fivewktinn",
        "sortable": True,
    },
    {"name": "caught", "label": "caught", "field": "caught", "sortable": True},
    {"name": "stumped", "label": "stumped", "field": "stumped", "sortable": True},
    {"name": "fifties", "label": "fifties", "field": "fifties", "sortable": True},
    {"name": "hundreds", "label": "hundreds", "field": "hundreds", "sortable": True},
    {"name": "fives", "label": "fives", "field": "fives", "sortable": True},
    {"name": "caughtwkt", "label": "caughtwkt", "field": "caughtwkt", "sortable": True},
    {"name": "captain", "label": "captain", "field": "captain", "sortable": True},
    {
        "name": "keptwicket",
        "label": "keptwicket",
        "field": "keptwicket",
        "sortable": True,
    },
]


def get_player(db: sqlite3.Connection, player_id: int) -> Player:
    with closing(db.cursor()) as csr:
        csr.execute(
            "SELECT * FROM players WHERE id = :player_id", {"player_id": player_id}
        )
        row: dict = csr.fetchone()
        return Player(**row)


def performances(db: sqlite3.Connection, player_id: int) -> list[Performance]:
    with closing(db.cursor()) as csr:
        csr.execute(
            "SELECT * FROM performances WHERE player_id = :player_id ORDER BY year",
            {"player_id": player_id},
        )
        rows = csr.fetchall()
        return [Performance(**row) for row in rows]


def show_player(db: sqlite3.Connection, player_id: int) -> None:
    player = get_player(db, player_id)
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(player.name).style("color: gold")
    rows = [asdict(row) for row in performances(db, player_id)]
    print(rows[:5])
    with ui.row():
        ui.table(rows=rows, columns=COLS, row_key="year").props("dense")
