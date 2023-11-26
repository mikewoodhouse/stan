import sqlite3

from nicegui import ui

from app.pages import hundreds_report, show_player, show_season, show_seasons
from app.pages.sidebar_menu import sidebar


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


db = sqlite3.connect("stan.sqlite")
db.row_factory = dict_factory


@ui.page("/", title="Stan")
def main_page():
    sidebar()


@ui.page("/players/{player_id}", title="player • Stan")
def players(player_id: int):
    show_player(db, player_id)


@ui.page("/hundreds", title="hundreds • Stan")
def hundreds_page():
    hundreds_report(db)


@ui.page("/seasons", title="seasons • Stan")
def seasons():
    show_seasons(db)


@ui.page("/season/{year}", title="season • Stan")
def season(year: int):
    show_season(db, year)


ui.run()
