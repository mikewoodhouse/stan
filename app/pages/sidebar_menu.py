from nicegui import ui


def sidebar() -> None:
    with ui.left_drawer() as sidebar:
        sidebar.props("width=120").style("background-color: lemonchiffon;")
        with ui.column():
            ui.link("Seasons", "/seasons")
            ui.link("Players", "/players")
            ui.link("Partnerships", "/partnerships/1")
            ui.link("Appearances", "/appearances")
            ui.link("Batting", "/batting")
            ui.label("Bowling")
            ui.label("Fielding")
            ui.link("Hundreds", "/hundreds")
            ui.link("Captains", "/captains")
