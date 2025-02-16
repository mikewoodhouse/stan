from contextlib import closing

from nicegui import ui

from app.config import config
from app.utils import add_slot_to_table, page_header

from .sidebar_menu import sidebar

tbl = ui.table(columns=[], rows=[])


def players_like(starts_with: str = "") -> list[dict]:
    with closing(config.db.cursor()) as csr:
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
    return players


def show_player_list() -> None:
    page_header("Players")

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

    players = players_like("%")

    with ui.table(columns=table_cols, rows=players, pagination=30).props("dense") as table:
        with table.add_slot("top-right"):
            with ui.input(placeholder="Search").props("type=search").bind_value(table, "filter").add_slot("append"):
                ui.icon("search")
        add_slot_to_table(table, "name", "players", "player_id")
