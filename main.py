import sqlite3

from nicegui import ui

from app.pages import hundreds_report, show_player, show_season


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


db = sqlite3.connect("stan.sqlite")
db.row_factory = dict_factory


@ui.page("/")
def main_page():
    with ui.left_drawer():
        ui.link("Hundreds", "/hundreds")


@ui.page("/hundreds")
async def hundreds_page():
    hundreds_report(db)


@ui.page("/players/{player_id}")
async def players(player_id: int):
    show_player(db, player_id)


@ui.page("/seasons/{year}")
async def season(year: int):
    show_season(db, year)


ui.run()
