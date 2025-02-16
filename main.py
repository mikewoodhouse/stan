from nicegui import ui

from app.pages import (
    hundreds_report,
    show_appearances,
    show_batting,
    show_bowling,
    show_captain,
    show_captains,
    show_fielding,
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


@ui.page("/", title="Stan")
def main_page():
    sidebar()


@ui.page("/players/{player_id}", title="player • Stan")
def players(player_id: int):
    show_player(player_id)


@ui.page("/players", title="players • Stan")
def player_search():
    show_player_list()


@ui.page("/hundreds", title="hundreds • Stan")
def hundreds_page():
    hundreds_report()


@ui.page("/seasons", title="seasons • Stan")
def seasons():
    show_seasons()


@ui.page("/season/{year}", title="season • Stan")
def season(year: int):
    show_season(year)


@ui.page("/players/{player_id}/{year}", title="player • Stan")
def player_year(player_id: int, year: int):
    show_player_year(player_id, year)


@ui.page("/matches/{year}", title="matches • Stan")
def matches(year: int):
    show_matches(year)


@ui.page("/match/{match_id}", title="matches • Stan")
def match(match_id: int):
    show_match(match_id)


@ui.page("/partnerships/{wicket}", title="partnerships • Stan")
def partnerships(wicket: int):
    show_partnerships(wicket)


@ui.page("/appearances", title="appearances • Stan")
def appearances():
    show_appearances()


@ui.page("/captains", title="captains • Stan")
def captains():
    show_captains()


@ui.page("/captains/{player_id}", title="captains • Stan")
def captain(player_id: int):
    show_captain(player_id)


@ui.page("/batting", title="batting • Stan")
def batting():
    show_batting()


@ui.page("/bowling", title="bowling • Stan")
def bowling():
    show_bowling()


@ui.page("/fielding", title="fielding • Stan")
def fielding():
    show_fielding()


ui.run(favicon="ico/tocc-32x32.png")
