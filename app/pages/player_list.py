import sqlite3
from contextlib import closing

from nicegui import ui

from app.types import Player

from .sidebar_menu import sidebar


def players_like(db: sqlite3.Connection, starts_with: str = "") -> list[dict]:
    with closing(db.cursor()) as csr:
        csr.execute(
            """
            SELECT *
            FROM players
            WHERE surname LIKE :starts_with
            ORDER BY surname, initial
            """,
            {"starts_with": f"{starts_with}%"},
        )
        players = csr.fetchall()
    print(f"got {len(players)} players")
    return players


def show_player_list(db: sqlite3.Connection) -> None:
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label("players").style("color: gold")

    sidebar()

    tbl = (
        ui.table(
            rows=[],
            columns=Player.table_cols(),
            row_key="id",
            pagination=30,
        )
        .props("dense")
        .add_slot(
            "body-cell-name",
            r"""
            <td :props="props">
                <a :href="'/players/' + props.row.player_id">
                    {{props.row.surname}}
                </a>
            </td>
        """,
        )
    )

    def refresh_table():
        tbl.children.clear()
        tbl.children.append(players_like(db, name_search.value))

    with ui.row():
        name_search = ui.input(label="Name")
        ui.button("search", on_click=refresh_table)
