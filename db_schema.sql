CREATE TABLE
  IF NOT EXISTS "partnerships" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "year" INTEGER
  , "wicket" INTEGER
  , "date" DATE
  , "total" INTEGER
  , "undefeated" BOOLEAN
  , "bat1" VARCHAR
  , "bat1score" INTEGER
  , "bat1notout" BOOLEAN
  , "bat2" VARCHAR
  , "bat2score" INTEGER
  , "bat2notout" BOOLEAN
  , "opp" VARCHAR
  , "bat1_id" INTEGER
  , "bat2_id" INTEGER
  );

CREATE TABLE
  IF NOT EXISTS "players" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "code" VARCHAR
  , "surname" VARCHAR
  , "initial" VARCHAR
  , "firstname" VARCHAR
  , "active" BOOLEAN
  );

CREATE TABLE
  IF NOT EXISTS "season_records" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "year" INTEGER
  , "club" VARCHAR
  , "runsscored" INTEGER
  , "wicketslost" INTEGER
  , "highest" INTEGER
  , "highestwkts" INTEGER
  , "highestdate" DATE
  , "highestopps" VARCHAR
  , "lowest" INTEGER
  , "lowestwkts" INTEGER
  , "lowestdate" DATE
  , "lowestopps" VARCHAR
  , "byes" INTEGER
  , "legbyes" INTEGER
  , "wides" INTEGER
  , "noballs" INTEGER
  , "ballsbowled" INTEGER
  , "ballsreceived" INTEGER
  );

CREATE TABLE
  IF NOT EXISTS "seasons" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "year" INTEGER
  , "played" INTEGER
  , "won" INTEGER
  , "lost" INTEGER
  , "drawn" INTEGER
  , "tied" INTEGER
  , "noresult" INTEGER
  , "maxpossiblegames" INTEGER
  );

CREATE TABLE
  IF NOT EXISTS "best_bowling" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "player_id" INTEGER DEFAULT NULL
  , "year" INTEGER DEFAULT NULL
  , "code" VARCHAR DEFAULT NULL
  , "date" DATE DEFAULT NULL
  , "inns" INTEGER DEFAULT NULL
  , "wkts" INTEGER DEFAULT NULL
  , "runs" INTEGER DEFAULT NULL
  , "opp" VARCHAR DEFAULT NULL
  , CONSTRAINT "fk_bb_player_id" FOREIGN KEY ("player_id") REFERENCES "players" ("id")
  );

CREATE INDEX "index_best_bowlings_on_player_id" ON "best_bowling" ("player_id");

CREATE TABLE
  IF NOT EXISTS "captains" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "player_id" INTEGER DEFAULT NULL
  , "code" VARCHAR DEFAULT NULL
  , "year" INTEGER DEFAULT NULL
  , "matches" INTEGER DEFAULT NULL
  , "won" INTEGER DEFAULT NULL
  , "lost" INTEGER DEFAULT NULL
  , "drawn" INTEGER DEFAULT NULL
  , "nodecision" INTEGER DEFAULT NULL
  , "tied" INTEGER DEFAULT NULL
  , CONSTRAINT "fk_capt_player_id" FOREIGN KEY ("player_id") REFERENCES "players" ("id")
  );

CREATE INDEX "index_captains_on_player_id" ON "captains" ("player_id");

CREATE TABLE
  IF NOT EXISTS "hundred_plus" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "player_id" INTEGER DEFAULT NULL
  , "year" INTEGER DEFAULT NULL
  , "code" VARCHAR DEFAULT NULL
  , "date" DATE DEFAULT NULL
  , "score" INTEGER DEFAULT NULL
  , "notout" BOOLEAN DEFAULT NULL
  , "opponents" VARCHAR DEFAULT NULL
  , "minutes" INTEGER DEFAULT NULL
  , CONSTRAINT "fk_hun_player_id" FOREIGN KEY ("player_id") REFERENCES "players" ("id")
  );

CREATE INDEX "index_hundred_plus_on_player_id" ON "hundred_plus" ("player_id");

CREATE TABLE
  IF NOT EXISTS "performances" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "player_id" INTEGER DEFAULT NULL
  , "code" VARCHAR DEFAULT NULL
  , "year" INTEGER DEFAULT NULL
  , "matches" INTEGER DEFAULT NULL
  , "innings" INTEGER DEFAULT NULL
  , "notout" INTEGER DEFAULT NULL
  , "highest" INTEGER DEFAULT NULL
  , "highestnotout" BOOLEAN DEFAULT NULL
  , "runsscored" INTEGER DEFAULT NULL
  , "fours" INTEGER DEFAULT NULL
  , "sixes" INTEGER DEFAULT NULL
  , "overs" INTEGER DEFAULT NULL
  , "balls" INTEGER DEFAULT NULL
  , "maidens" INTEGER DEFAULT NULL
  , "wides" INTEGER DEFAULT NULL
  , "noballs" INTEGER DEFAULT NULL
  , "runs" INTEGER DEFAULT NULL
  , "wickets" INTEGER DEFAULT NULL
  , "fivewktinn" INTEGER DEFAULT NULL
  , "caught" INTEGER DEFAULT NULL
  , "stumped" INTEGER DEFAULT NULL
  , "fifties" INTEGER DEFAULT NULL
  , "hundreds" INTEGER DEFAULT NULL
  , "fives" INTEGER DEFAULT NULL
  , "caughtwkt" INTEGER DEFAULT NULL
  , "captain" INTEGER DEFAULT NULL
  , "keptwicket" INTEGER DEFAULT NULL
  , CONSTRAINT "fk_perf_player_id" FOREIGN KEY ("player_id") REFERENCES "players" ("id")
  );

CREATE INDEX "index_performances_on_player_id" ON "performances" ("player_id");

CREATE TABLE
  IF NOT EXISTS "matches" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "date" DATE DEFAULT NULL
  , "oppo" VARCHAR DEFAULT NULL
  , "venue" VARCHAR DEFAULT NULL
  , "result" VARCHAR DEFAULT NULL
  , "bat_first" VARCHAR DEFAULT NULL
  , "first_runs" INTEGER DEFAULT NULL
  , "first_wkts" INTEGER DEFAULT NULL
  , "first_all_out" BOOLEAN DEFAULT NULL
  , "first_notes" VARCHAR DEFAULT NULL
  , "second_runs" INTEGER DEFAULT NULL
  , "second_wkts" INTEGER DEFAULT NULL
  , "second_all_out" BOOLEAN DEFAULT NULL
  , "second_notes" VARCHAR DEFAULT NULL
  , "overs_opp" REAL DEFAULT NULL
  , "overs_tocc" REAL DEFAULT NULL
  , "tocc_w" INTEGER DEFAULT NULL
  , "tocc_nb" INTEGER DEFAULT NULL
  , "tocc_b" INTEGER DEFAULT NULL
  , "tocc_lb" INTEGER DEFAULT NULL
  , "opp_w" INTEGER DEFAULT NULL
  , "opp_nb" INTEGER DEFAULT NULL
  , "opp_b" INTEGER DEFAULT NULL
  , "opp_lb" INTEGER DEFAULT NULL
  );

CREATE INDEX "index_matches_on_date" ON "matches" ("date");

CREATE TABLE
  IF NOT EXISTS "match_batting" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "match_id" INTEGER NOT NULL
  , "match_date" DATE NOT NULL
  , "opp" VARCHAR DEFAULT NULL
  , "name" VARCHAR DEFAULT NULL
  , "player_id" INTEGER DEFAULT NULL
  , "position" INTEGER DEFAULT NULL
  , "runs" INTEGER DEFAULT NULL
  , "out" BOOLEAN DEFAULT NULL
  , "how_out" VARCHAR DEFAULT NULL
  , "captain" BOOLEAN DEFAULT NULL
  , "kept_wicket" BOOLEAN DEFAULT NULL
  , "caught" INTEGER DEFAULT NULL
  , "caught_wkt" INTEGER DEFAULT NULL
  , "stumped" INTEGER DEFAULT NULL
  , "fours" INTEGER DEFAULT NULL
  , "sixes" INTEGER DEFAULT NULL
  , CONSTRAINT "fk_mbat_player_id" FOREIGN KEY ("player_id") REFERENCES "players" ("id")
  , CONSTRAINT "fk_mbat_match_id" FOREIGN KEY ("match_id") REFERENCES "matches" ("id")
  );

CREATE INDEX "index_match_bat_on_player" ON "match_batting" ("player_id");

CREATE TABLE
  IF NOT EXISTS "match_bowling" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "match_id" INTEGER DEFAULT NULL
  , "match_date" DATE NOT NULL
  , "opp" VARCHAR DEFAULT NULL
  , "name" VARCHAR DEFAULT NULL
  , "player_id" INTEGER DEFAULT NULL
  , "overs" INTEGER DEFAULT NULL
  , "balls" INTEGER DEFAULT NULL
  , "maidens" INTEGER DEFAULT NULL
  , "runs_conceded" INTEGER DEFAULT NULL
  , "wickets" INTEGER DEFAULT NULL
  , "wides" INTEGER DEFAULT NULL
  , "noballs" INTEGER DEFAULT NULL
  , CONSTRAINT "fk_mbowl_player_id" FOREIGN KEY ("player_id") REFERENCES "players" ("id")
  , CONSTRAINT "fk_mbowl_match_id" FOREIGN KEY ("match_id") REFERENCES "matches" ("id")
  );

CREATE INDEX "index_match_bowl_on_player" ON "match_bowling" ("player_id");