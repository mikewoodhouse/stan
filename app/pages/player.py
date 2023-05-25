import sqlite3
from contextlib import closing

from nicegui import ui

from app.types.classes import Performance, Player

COLS = [
    {
        "name": "year",
        "label": "year",
        "field": "year",
        "sortable": True,
        "align": "center",
    },
    {"name": "matches", "label": "matches", "field": "matches", "sortable": True},
    {"name": "innings", "label": "innings", "field": "innings", "sortable": True},
    {"name": "notout", "label": "not out", "field": "notout", "sortable": True},
    {"name": "high_score", "label": "highest", "field": "high_score", "sortable": True},
    {
        "name": "runsscored",
        "label": "runs",
        "field": "runsscored",
        "sortable": True,
    },
    {
        "name": "batave",
        "label": "ave",
        "field": "batting_average",
        "sortable": True,
    },
    {"name": "fours", "label": "fours", "field": "fours", "sortable": True},
    {"name": "sixes", "label": "sixes", "field": "sixes", "sortable": True},
    {
        "name": "overs_bowled",
        "label": "overs",
        "field": "overs_bowled",
        "sortable": True,
    },
    {"name": "maidens", "label": "maidens", "field": "maidens", "sortable": True},
    {"name": "runs", "label": "runs", "field": "runs", "sortable": True},
    {"name": "wickets", "label": "wickets", "field": "wickets", "sortable": True},
    {
        "name": "bowlave",
        "label": "ave",
        "field": "bowling_average",
        "sortable": True,
    },
    {
        "name": "fivewktinn",
        "label": "five-for",
        "field": "fivewktinn",
        "sortable": True,
    },
    {"name": "caught", "label": "caught", "field": "caught", "sortable": True},
    {"name": "stumped", "label": "stumped", "field": "stumped", "sortable": True},
    {"name": "fifties", "label": "fifties", "field": "fifties", "sortable": True},
    {"name": "hundreds", "label": "hundreds", "field": "hundreds", "sortable": True},
    {
        "name": "caughtwkt",
        "label": "caught wkt",
        "field": "caughtwkt",
        "sortable": True,
    },
    {"name": "captain", "label": "captain", "field": "captain", "sortable": True},
    {
        "name": "keptwicket",
        "label": "kept wicket",
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
    rows = [row.row_dict() for row in performances(db, player_id)]
    with ui.row():
        with ui.table(rows=rows, columns=COLS, row_key="year").props("dense") as table:
            table.add_slot(
                "body-cell-year",
                r"""
                <td :props="props"><a :href="'/seasons/' + props.row.year">{{props.row.year}}</a></td>
                """,
            )
