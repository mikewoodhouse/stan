import sqlite3
from datetime import date

from nicegui import ui

from app.pages import (
    hundreds_report,
    show_appearances,
    show_captain,
    show_captains,
    show_match,
    show_matches,
    show_partnerships,
    show_player,
    show_player_list,
    show_player_year,
    show_season,
    show_seasons,
)
from app.pages.sidebar_menu import sidebar


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


sqlite3.register_adapter(date, lambda d: d.isoformat())
sqlite3.register_converter("DATE", lambda s: date.fromisoformat(s.decode("utf-8")))

db = sqlite3.connect("stan.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
db.row_factory = dict_factory


@ui.page("/", title="Stan")
def main_page():
    sidebar()


@ui.page("/players/{player_id}", title="player • Stan")
def players(player_id: int):
    show_player(db, player_id)


@ui.page("/players", title="players • Stan")
def player_search():
    show_player_list(db)


@ui.page("/hundreds", title="hundreds • Stan")
def hundreds_page():
    hundreds_report(db)


@ui.page("/seasons", title="seasons • Stan")
def seasons():
    show_seasons(db)


@ui.page("/season/{year}", title="season • Stan")
def season(year: int):
    show_season(db, year)


@ui.page("/players/{player_id}/{year}", title="player • Stan")
def player_year(player_id: int, year: int):
    show_player_year(db, player_id, year)


@ui.page("/matches/{year}", title="matches • Stan")
def matches(year: int):
    show_matches(db, year)


@ui.page("/match/{match_id}", title="matches • Stan")
def match(match_id: int):
    show_match(db, match_id)


@ui.page("/partnerships/{wicket}", title="partnerships • Stan")
def partnerships(wicket: int):
    show_partnerships(db, wicket)


@ui.page("/appearances", title="appearances • Stan")
def appearances():
    show_appearances(db)


@ui.page("/captains", title="captains • Stan")
def captains():
    show_captains(db)


@ui.page("/captains/{player_id}", title="captains • Stan")
def captain(player_id: int):
    show_captain(db, player_id)


ui.run()
