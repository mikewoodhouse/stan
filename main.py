import sqlite3

from nicegui import ui

from app.pages import hundreds_report, show_player, show_season, show_seasons


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


db = sqlite3.connect("stan.sqlite")
db.row_factory = dict_factory


@ui.page("/", title="Stan")
def main_page():
    with ui.left_drawer():
        with ui.column():
            ui.link("Hundreds", "/hundreds")
            ui.link("Seasons", "/seasons")


@ui.page("/hundreds", title="hundreds • Stan")
async def hundreds_page():
    hundreds_report(db)


@ui.page("/players/{player_id}", title="player • Stan")
async def players(player_id: int):
    show_player(db, player_id)


@ui.page("/seasons", title="seasons • Stan")
async def seasons():
    show_seasons(db)


@ui.page("/season/{year}", title="season • Stan")
async def season(year: int):
    show_season(db, year)


ui.run()
