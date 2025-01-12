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

    sidebar()

    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"Partnerships for {ordinal(wicket)} wicket").style("color: gold").style("font-size: 200%")

    with ui.row():
        for i in range(1, 12):
            ui.link(ordinal(i), target=f"/partnerships/{i}").style("margin: 10px")

    rows = [row.row_dict() for row in Partnership.for_wicket(db, wicket)]

    ui.table(rows=rows, columns=Partnership.table_cols()).props("dense")
