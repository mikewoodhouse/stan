import sqlite3
from contextlib import closing

from nicegui import ui

from .sidebar_menu import sidebar

tbl = ui.table(columns=[], rows=[])


def players_like(db: sqlite3.Connection, starts_with: str = "") -> list[dict]:
    with closing(db.cursor()) as csr:
        csr.execute(
            """
            SELECT
                f.player_id
            ,   p.surname ||
                CASE
                    WHEN p.firstname != ''
                    THEN ', ' || p.firstname
                    ELSE
                        CASE
                            WHEN p.initial != ''
                            THEN ', ' || p.initial
                            ELSE ''
                        END
                END AS name
            ,   MIN(f.year) AS from_year
            ,   MAX(f.year) AS to_year
            FROM players p
                JOIN performances f
                ON f.player_id = p.id
            WHERE p.surname LIKE :starts_with
            GROUP BY
                p.surname
            ,   p.initial
            ,   p.firstname
            ,   f.player_id
            ORDER BY p.surname, p.initial, p.firstname
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

    table_cols = [
        {
            "name": "name",
            "label": "Name",
            "field": "name",
            "align": "left",
        },
        {
            "name": "from_year",
            "label": "From",
            "field": "from_year",
            "align": "center",
        },
        {
            "name": "to_year",
            "label": "To",
            "field": "to_year",
            "align": "center",
        },
    ]

    players = players_like(db, "%")

    tbl = (
        ui.table(
            rows=players,
            columns=table_cols,
            row_key="id",
            pagination=30,
        )
        .props("dense")
        .add_slot(
            "body-cell-name",
            r"""
            <td :props="props">
                <a :href="'/players/' + props.row.player_id">
                    {{props.row.name}}
                </a>
            </td>
        """,
        )
    )

    def refresh_table():
        tbl.children.clear()
        tbl.options.append(players_like(db, name_search.value))

    with ui.row():
        name_search = ui.input(label="Name").props("clearable")
        ui.button("search", on_click=refresh_table)
