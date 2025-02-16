from contextlib import closing

from nicegui import ui

from app.config import config


def balls_to_overs(balls: int) -> str:
    overs, balls = divmod(balls, 6)
    return f"{overs}.{balls}"


def player_name(firstname: str, initial: str, surname: str) -> str:
    if forename := firstname or initial:
        return f"{surname}, {forename}"
    return surname


def count(tablename: str) -> int:
    with closing(config.db.cursor()) as csr:
        csr.execute(f"SELECT count(*) AS row_count FROM {tablename}")
        return csr.fetchone()["row_count"]


def page_header(text: str) -> None:
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(text).style("color: gold").style("font-size: 200%")


def table_link_slot_html(cell_name_suffix: str, target: str, href_row_props: list[str]) -> str:
    h = f"'/{target}/' + " + " + '/' + ".join(f"props.row.{p}" for p in href_row_props)
    return (
        '<td :props="props"><a :href="' + h + '"'
        " class='nicegui-link'>{{props.row." + cell_name_suffix + "}}</a></td>"
    )


def add_slot_to_table(table: ui.table, cell_name_suffix: str, target: str, href_row_props: str | list[str]) -> None:
    if isinstance(href_row_props, str):
        href_row_props = [href_row_props]
    table.add_slot(f"body-cell-{cell_name_suffix}", table_link_slot_html(cell_name_suffix, target, href_row_props))
