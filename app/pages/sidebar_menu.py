from nicegui import ui


def sidebar() -> None:
    with ui.left_drawer() as sidebar:
        sidebar.props("width=100")
        with ui.column():
            ui.link("Seasons", "/seasons")
            ui.link("Players", "/players")
            ui.link("Partnerships", "/partnerships/1")
            ui.link("Appearances", "/appearances")
            ui.label("Batting")
            ui.label("Bowling")
            ui.label("Fielding")
            ui.link("Hundreds", "/hundreds")
            ui.label("Captains")
