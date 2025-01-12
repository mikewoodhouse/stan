from nicegui import ui
from .sidebar_menu import sidebar
from app.types import Partnership


def show_partnerships(db):
    sidebar()

    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label("Partnerships").style("color: gold").style("font-size: 200%")

    rows = [row.row_dict() for row in Partnership.all(db)]

    with ui.row():
        ui.table(rows=rows, columns=Partnership.table_cols())
