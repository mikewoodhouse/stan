import re
from contextlib import closing
from functools import partial
from pathlib import Path
from typing import Any

from nicegui import ui

from app.config import config


def balls_to_overs(balls: int) -> str:
    overs, balls = divmod(balls, 6)
    return f"{overs}.{balls}"


def count(tablename: str) -> int:
    with closing(config.db.cursor()) as csr:
        csr.execute(f"SELECT count(*) AS row_count FROM {tablename}")
        return csr.fetchone()["row_count"]


def page_header(text: str) -> None:
    """
    Creates a page header with the given text. Ensures that all pages use the same style.
    """
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(text).style("color: gold").style("font-size: 200%")


def table_link_slot_html(cell_name_suffix: str, target: str, href_row_props: list[str]) -> str:
    """
    Builds the HTML for a slot to be added to a table cell that contains a link.
    """
    h = f"'/{target}/' + " + " + '/' + ".join(f"props.row.{p}" for p in href_row_props)
    return (
        '<td :props="props"><a :href="' + h + "\" class='nicegui-link'>{{props.row." + cell_name_suffix + "}}</a></td>"
    )


def add_slot_to_table(table: ui.table, cell_name_suffix: str, target: str, href_row_props: str | list[str]) -> None:
    """
    Adds a slot to a table cell that contains a link.
    """
    if isinstance(href_row_props, str):
        href_row_props = [href_row_props]
    table.add_slot(f"body-cell-{cell_name_suffix}", table_link_slot_html(cell_name_suffix, target, href_row_props))


def coldef(
    field: str, label: str = "", *, name: str = "", align: str = "", decimals: int = -1, sortable: bool = False
) -> dict:
    """
    Produces a column definition for a nicegui table. Minimum input is the `field` parameter that
    specifies the value for the column. If not provided, `label` is set to the same string, with the
    first letter capitalised.
    Other (named) parameters are optional and are set as and when supplied.
    THe `sortable()` function uses this function but sets the `sortable` parameter to True.
    """
    result: dict[str, Any] = {
        "name": name or field,
        "field": field,
        "label": (label or field.capitalize()).replace("_", " "),
    }
    if align:
        result["align"] = align
    if decimals > 0:
        result[":format"] = f"value => value ? value.toFixed({decimals}) : ''"
    if sortable:
        result["sortable"] = True
    return result


sortable = partial(coldef, sortable=True)


def extract_sql_parameters(sql: str) -> str:
    """
    Convert SQL string, removing the single quotes from named parameters.
    This allows a particular developer conceit of mine: I like to see SQL formatted
    consistently in my editor, and to date I haven't found a formatter that can
    parse the `:parameter` form, so I use `':parameter'` instead.
    """
    return re.sub(r"'(:[^']+)'", r"\1", sql)


def sql_query(filename: str) -> str:
    """
    Reads the SQL file with the given filename and returns the query string, with parameters modified
    from, e.g. `':param'` to remove the single quotes, using `extract_sql_parameters()` above.
    """
    path = Path(__file__).parent / "types" / "sql" / f"{filename}.sql"
    sql = path.read_text()
    return extract_sql_parameters(sql)


def project_root() -> Path:
    return next(p for p in Path(__file__).parents if (p / "app").exists())
