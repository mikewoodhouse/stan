import sqlite3

from nicegui import ui

from app.types import Partnership

from .sidebar_menu import sidebar


def show_partnerships(db: sqlite3.Connection, wicket: int):
    def ordinal(n: int):
        """
        Nutty but fun function, from https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
        """
        return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10 :: 4])

    if wicket not in range(1, 12):
        wicket = 1

    sidebar()

    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"Partnerships for {ordinal(wicket)} wicket").style("color: gold").style("font-size: 200%")

    rows = [row.row_dict() for row in Partnership.for_wicket(db, wicket)]

    with ui.table(rows=rows, columns=Partnership.table_cols()).props("dense") as table:
        with table.add_slot("top-right"):
            with ui.select(list(range(1, 12)), on_change=lambda e: print(e)) as selector:
                print(selector.value)
