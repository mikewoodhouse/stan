from nicegui import ui

from app.types import Partnership

from .sidebar_menu import sidebar


def show_partnerships(wicket: int):
    def ordinal(n: int):
        """
        Nutty but fun function, from https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
        """
        return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10 :: 4])  # noqa

    sidebar()

    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"Partnerships for {ordinal(wicket)} wicket").style("color: gold").style("font-size: 200%")

    with ui.row():
        ui.markdown(
            """
Note: for several decades the best partnership for each wicket was recorded,
irrespective of score.

More recently, beyond those registering 75+ runs, only partnerships recording
a score deemed sufficiently interesting have been retained."""
        )

    with ui.row():
        for i in range(1, 12):
            ui.link(ordinal(i), target=f"/partnerships/{i}").style("margin: 10px")

    rows = [row.row_dict() for row in Partnership.for_wicket(wicket)]

    ui.table(rows=rows, columns=Partnership.table_cols()).props("dense")
