from contextlib import closing

from nicegui import ui

from app.config import config

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
    # print(f"got {len(players)} players")
    return players


def show_player_list() -> None:
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label("Players").style("color: gold").style("font-size: 200%")

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
        table.add_slot(
            "body-cell-name",
            r"""
            <td :props="props">
                <a :href="'/players/' + props.row.player_id" class='nicegui-link'>
                    {{props.row.name}}
                </a>
            </td>
        """,
        )
