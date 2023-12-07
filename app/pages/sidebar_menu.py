from nicegui import ui


def sidebar() -> None:
    with ui.left_drawer() as sidebar:
        sidebar.props("width=100")
        with ui.column():
            ui.link("Hundreds", "/hundreds")
            ui.link("Seasons", "/seasons")
            ui.link("Players", "/players")
