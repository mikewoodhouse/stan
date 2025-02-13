# pyplaycricket: Retrieving data from play-cricket.com in python for analysis and social media

https://ewanharris.medium.com/pyplaycricket-retrieving-data-from-play-cricket-com-in-python-for-analysis-and-social-media-eed14a3c2441

Ewan Harris


Dec 1, 2024
Why has this been created?

pyplaycricket is my first foray into open source python library development and I hope allows other cricket fans/analysts/nerds/badgers/whoever to retrieve data out of play-cricket in an easily interrogatable format.

I create social media posts for my club (for instagram and twitter) and this library is born out of frustrations copying and pasting data from playcricket when posting results, league tables, stats leaders and more.

Now through pyplaycricket, I am able to retrieve fixtures, filter these by any logic I wish (more advanced than online if required), format individual performances on a given weekend or season run totals into strings which are copied and pasted straight into my templates. No human error working out whose 2fer was more expensive or whose 32 came off fewer balls and the process is now done in seconds rather than laboriously clicking through scorecards.
3 different social media templates, all produced from data in playcricket. Easily copied and pasted from pyplaycricket.

The structure of the library is such that most users will be happy with the playcricket module — a generic module allowing you to retrieve statstics in a club agnostic manner. The alleyn module is more specific for my social media needs and can be configured for your individual club.
How do I get started with the library?

pip install pyplaycricket

This command line item will install the package into your local python environment.

The only access requirement is receiving an API key from playcricket.com which you will need to autheticate against the various playcricket API endpoints.

This can be requested by:

    Emailing play.cricket@ecb.co.uk
    You will need to be a PlayCricket admin for your club’s site.
    You will need to share a fair usage agreement on behalf of your club.

They will confirm your site id and your API key.

To substantiate the pc class, which holds all the generic playcricket methods within it, run the below python snippet:

from playcric.playcricket import pc
site_id = 'insert_your_site_id_here'
api_key = 'insert_your_api_key_here'

playc = pc(api_key=api_key, site_id=site_id)

You are now ready to perform any analysis you wish.
Example Functions
get_all_matches

matches = playc.get_all_matches(season=2024)

get_all_matches returns a dataframe of all fixtures in the given season for the site_id passed in the substantiation of pc.

Example output:

|    |      id | status   | published   | last_updated        | league_name                        | league_id   | competition_name      | competition_id   | competition_type   | match_type    | game_type   |   season | match_date          | match_time   | ground_name            |   ground_id |   ground_latitude |   ground_longitude | home_club_name     | home_team_name   |   home_team_id |   home_club_id | away_club_name   | away_team_name   |   away_team_id |   away_club_id | umpire_1_name   | umpire_1_id   | umpire_2_name   | umpire_2_id   | umpire_3_name   | umpire_3_id   | referee_name   | referee_id   | scorer_1_name   | scorer_1_id   | scorer_2_name   | scorer_2_id   |
|---:|--------:|:---------|:------------|:--------------------|:-----------------------------------|:------------|:----------------------|:-----------------|:-------------------|:--------------|:------------|---------:|:--------------------|:-------------|:-----------------------|------------:|------------------:|-------------------:|:-------------------|:-----------------|---------------:|---------------:|:-----------------|:-----------------|---------------:|---------------:|:----------------|:--------------|:----------------|:--------------|:----------------|:--------------|:---------------|:-------------|:----------------|:--------------|:----------------|:--------------|
|  0 | 6571330 | New      | Yes         | 2024-04-19 00:00:00 |                                    |             |                       |                  | Friendly           | Limited Overs | Standard    |     2024 | 2024-04-27 00:00:00 | 10:00        | Edward Alleyn Club     |        9352 |           51.4491 |         -0.0915547 | Alleyn CC          | Friendly XI      |         320697 |            672 | Alleyn CC        | Burbage Badgers  |         268144 |            672 |                 |               |                 |               |                 |               |                |              |                 |               |                 |               |
|  1 | 6242035 | New      | Yes         | 2024-07-31 00:00:00 | Surrey Junior Cricket Championship | 10881       | U11 Surrey County Cup | 63219            | Cup                | Limited Overs | Standard    |     2024 | 2024-05-05 00:00:00 | 09:00        | Battersea Park         |       56639 |           51.4802 |         -0.155702  | Spencer CC, Surrey | BU11 Tier1A      |         256417 |           5853 | Alleyn CC        | Under 11         |          90654 |            672 |                 |               |                 |               |                 |               |                |              |                 |               |                 |               |
|  2 | 6242558 | New      | Yes         | 2024-07-31 00:00:00 | Surrey Junior Cricket Championship | 10881       | U14 Surrey County Cup | 63217            | Cup                | Limited Overs | Standard    |     2024 | 2024-05-05 00:00:00 | 09:30        | Morden Park Main Pitch |       57159 |           51.3888 |         -0.210369  | AJ Cricket Academy | Under 14         |         257934 |          14870 | Alleyn CC        | Under 14         |          59853 |            672 |                 |               |                 |               |                 |               |                |              |                 |               |                 |               |

Without passing a team_ids, competition_ids or competition_types list, all fixtures will be returned. Unfortunately, there is no playcricket field returned in this dataframe which directly differentiates between senior and junior fixtures. If you want to get all the fixtures for another club, you must find their site_id from the bottom of their playcricket home page.

An example to find a different club’s site_id:

    Visit their playcricket home page (e.g. https://dulwich.play-cricket.com/home)
    Scroll the bottom right of the page where you will see something along the lines of: “©2024 Play-Cricket. All rights reserved. | Site ID 2384”
    Use site_id = 2384 in get_all_matches to retrieve all Dulwich CC fixtures for a given season.

get_league_table

league_id = 117611
league_table, key = playc.get_league_table(league_id, simple=True, clean_names=False)

get_league_table returns two outputs: a league table in dataframe form and a dictionary of column headers defined

Example output:

|    |   POSITION | TEAM                   |   W |   D |   L |   PTS |
|---:|-----------:|:-----------------------|----:|----:|----:|------:|
|  0 |          1 | Horley CC, Surrey      |   8 |   2 |   1 |   219 |
|  1 |          2 | Alleyn CC              |   8 |   2 |   2 |   198 |
|  2 |          3 | Egham CC               |   6 |   1 |   4 |   170 |
|  3 |          4 | Cobham Avorians CC     |   6 |   1 |   5 |   166 |
|  4 |          5 | Byfleet CC             |   6 |   0 |   6 |   158 |
|  5 |          6 | Kingstonian CC, Surrey |   6 |   1 |   6 |   149 |
|  6 |          7 | Thames Ditton CC       |   5 |   1 |   4 |   147 |
|  7 |          8 | Effingham CC           |   4 |   2 |   5 |   118 |
|  8 |          9 | Old Pauline CC         |   4 |   0 |   8 |   111 |
|  9 |         10 | Churt and Hindhead CC  |   2 |   0 |  10 |    79 |

simple = True is used to return a more basic league table just showing wins, draws and losses. If this is set as False, the function will return all the columns playcricket breaks results down into.
get_all_players_involved

match_id_list = [6178602]
players = acc.get_all_players_involved(match_id_list)

get_all_players involved is a basic method to extract teamsheets from match_ids.

The method returns actual names but I have removed them to preserve some anonymity within this article.

|    |   position | player_name   |       player_id | captain   | wicket_keeper   |   team_id |   club_id |   match_id |
|---:|-----------:|:--------------|----------------:|:----------|:----------------|----------:|----------:|-----------:|
|  0 |          1 | Player 1      |           23340 | False     | False           |     59723 |       672 |    6178602 |
|  1 |          2 | Player 2      |     5.83453e+06 | False     | False           |     59723 |       672 |    6178602 |
|  2 |          3 | Player 3      |     4.47386e+06 | False     | False           |     59723 |       672 |    6178602 |

get_individual_stats_from_all_games

match_id_list = [6178602]
batting, bowling, fielding = acc.get_individual_stats_from_all_games(match_id_list)

This method iterates through multiple matches, stacking 3 dataframes: batting, bowling and fielding. From these dataframes, you can perform analysis like averages, strike rates etc across multiple fixtures.

If you don’t pass a list of team_ids to the function to filter on, the batting dataframe will look identical to fielding. However, if you do filter on team_ids (usually to just include your own teams), then the fielding dataframe is just the opposition batters so you can aggregate by the fielder_id column to tot up catches, stumpings etc.

The method returns actual names but I have removed them to preserve some anonymity within this article.

Batting:

|    |   position | batsman_name   |   batsman_id | how_out   | fielder_name   | fielder_id   | bowler_name   | bowler_id   |   runs |   fours |   sixes |   balls | team_name                 |   team_id | opposition_name           |   opposition_id |   innings |   match_id |   not_out | initial_name   |
|---:|-----------:|:---------------|-------------:|:----------|:---------------|:-------------|:--------------|:------------|-------:|--------:|--------:|--------:|:--------------------------|----------:|:--------------------------|----------------:|----------:|-----------:|----------:|:---------------|
|  0 |          7 | Batter 7       |      6139217 | not out   |                |              |               |             |     48 |       5 |       0 |      72 | Alleyn CC - 1st XI        |     59723 | Thames Ditton CC - 1st XI |           27896 |         2 |    6178602 |         1 | B 7            |
|  1 |          1 | Batter 1       |        24019 | b         |                |              | Bowler 1      | 6139217     |     46 |       5 |       2 |      48 | Thames Ditton CC - 1st XI |     27896 | Alleyn CC - 1st XI        |           59723 |         1 |    6178602 |         0 | B 1            |
|  2 |          3 | Batter 3       |      4473865 | ct        | Fielder 1      | 700861       | Bowler 2      | 700861      |     43 |       7 |       0 |      56 | Alleyn CC - 1st XI        |     59723 | Thames Ditton CC - 1st XI |           27896 |         2 |    6178602 |         0 | B 3            |

Bowling:

|    | bowler_name   |   bowler_id |   overs |   maidens |   runs |   wides |   wickets |   no_balls | team_name                 |   team_id | opposition_name           |   opposition_id |   innings |   match_id | initial_name   |   balls |
|---:|:--------------|------------:|--------:|----------:|-------:|--------:|----------:|-----------:|:--------------------------|----------:|:--------------------------|----------------:|----------:|-----------:|:---------------|--------:|
|  0 | Bowler 1      |     6139217 |      10 |         3 |     20 |       0 |         3 |          2 | Alleyn CC - 1st XI        |     59723 | Thames Ditton CC - 1st XI |           27896 |         1 |    6178602 | B1             |      60 |
|  1 | Bowler 2      |       24019 |      10 |         3 |     23 |       0 |         2 |          0 | Thames Ditton CC - 1st XI |     27896 | Alleyn CC - 1st XI        |           59723 |         2 |    6178602 | B2             |      60 |
|  2 | Bowler 3      |     5364238 |      10 |         2 |     26 |       3 |         2 |          0 | Thames Ditton CC - 1st XI |     27896 | Alleyn CC - 1st XI        |           59723 |         2 |    6178602 | B3             |      60 |

Fielding:

|    |   position | batsman_name   |   batsman_id | how_out   | fielder_name   | fielder_id   | bowler_name   | bowler_id   |   runs |   fours |   sixes |   balls | team_name                 |   team_id | opposition_name           |   opposition_id |   innings |   match_id |   not_out | initial_name   |
|---:|-----------:|:---------------|-------------:|:----------|:---------------|:-------------|:--------------|:------------|-------:|--------:|--------:|--------:|:--------------------------|----------:|:--------------------------|----------------:|----------:|-----------:|----------:|:---------------|
|  0 |          7 | Batter 7       |      6139217 | not out   |                |              |               |             |     48 |       5 |       0 |      72 | Alleyn CC - 1st XI        |     59723 | Thames Ditton CC - 1st XI |           27896 |         2 |    6178602 |         1 | B 7            |
|  1 |          1 | Batter 1       |        24019 | b         |                |              | Bowler 1      | 6139217     |     46 |       5 |       2 |      48 | Thames Ditton CC - 1st XI |     27896 | Alleyn CC - 1st XI        |           59723 |         1 |    6178602 |         0 | B 1            |
|  2 |          3 | Batter 3       |      4473865 | ct        | Fielder 1      | 700861       | Bowler 2      | 700861      |     43 |       7 |       0 |      56 | Alleyn CC - 1st XI        |     59723 | Thames Ditton CC - 1st XI |           27896 |         2 |    6178602 |         0 | B 3            |

Alleyn module and Social Media Usage

If you initiate the acc class, these are variants of the playcricket functions used to copy and paste into Adobe InDesign and post on twitter or instagram. These functions often include a for_graphics or equivalent parameter. This will take the dataframe and convert all the information into one string.
Further Development

The full repo and source code can be found on GitHub. I’d welcome any efforts to extend the library to the rest of the APIs which PlayCricket provide or to automate more advanced analysis.

For small bug fixes etc, please just create a new branch and tag me in a PR. More advanced issues should be dealt with by creating an issue for discussion.