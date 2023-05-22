CREATE TABLE
  IF NOT EXISTS "matches" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "date" DATE
  , "oppo" VARCHAR
  , "venue" VARCHAR
  , "result" VARCHAR
  , "bat_first" VARCHAR
  , "first_runs" INTEGER
  , "first_wkts" INTEGER
  , "first_all_out" BOOLEAN
  , "first_notes" VARCHAR
  , "second_runs" INTEGER
  , "second_wkts" INTEGER
  , "second_all_out" BOOLEAN
  , "second_notes" VARCHAR
  , "overs_opp" REAL
  , "overs_tocc" REAL
  , "tocc_w" INTEGER
  , "tocc_nb" INTEGER
  , "tocc_b" INTEGER
  , "tocc_lb" INTEGER
  , "opp_w" INTEGER
  , "opp_nb" INTEGER
  , "opp_b" INTEGER
  , "opp_lb" INTEGER
  );

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
  IF NOT EXISTS "best_bowlings" (
    "id" INTEGER NOT NULL PRIMARY KEY
  , "player_id" INTEGER DEFAULT NULL
  , "year" INTEGER DEFAULT NULL
  , "code" VARCHAR DEFAULT NULL
  , "date" DATE DEFAULT NULL
  , "inns" INTEGER DEFAULT NULL
  , "wkts" INTEGER DEFAULT NULL
  , "runs" INTEGER DEFAULT NULL
  , "opp" VARCHAR DEFAULT NULL
  , CONSTRAINT "fk_rails_69d9640b09" FOREIGN KEY ("player_id") REFERENCES "players" ("id")
  );

CREATE INDEX "index_best_bowlings_on_player_id" ON "best_bowlings" ("player_id");

CREATE TABLE
  IF NOT EXISTS "captains" (
    "id" INTEGER NOT NULL PRIMARY KEY
  , "player_id" INTEGER DEFAULT NULL
  , "code" VARCHAR DEFAULT NULL
  , "year" INTEGER DEFAULT NULL
  , "matches" INTEGER DEFAULT NULL
  , "won" INTEGER DEFAULT NULL
  , "lost" INTEGER DEFAULT NULL
  , "drawn" INTEGER DEFAULT NULL
  , "nodecision" INTEGER DEFAULT NULL
  , "tied" INTEGER DEFAULT NULL
  , CONSTRAINT "fk_rails_7c87bce208" FOREIGN KEY ("player_id") REFERENCES "players" ("id")
  );

CREATE INDEX "index_captains_on_player_id" ON "captains" ("player_id");

CREATE TABLE
  IF NOT EXISTS "hundred_plus" (
    "id" INTEGER NOT NULL PRIMARY KEY
  , "player_id" INTEGER DEFAULT NULL
  , "year" INTEGER DEFAULT NULL
  , "code" VARCHAR DEFAULT NULL
  , "date" DATE DEFAULT NULL
  , "score" INTEGER DEFAULT NULL
  , "notout" BOOLEAN DEFAULT NULL
  , "opponents" VARCHAR DEFAULT NULL
  , "minutes" INTEGER DEFAULT NULL
  , CONSTRAINT "fk_rails_0df0777f98" FOREIGN KEY ("player_id") REFERENCES "players" ("id")
  );

CREATE INDEX "index_hundred_plus_on_player_id" ON "hundred_plus" ("player_id");

CREATE TABLE
  IF NOT EXISTS "performances" (
    "id" INTEGER NOT NULL PRIMARY KEY
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
  , CONSTRAINT "fk_rails_4dbc0f9804" FOREIGN KEY ("player_id") REFERENCES "players" ("id")
  );

CREATE INDEX "index_performances_on_player_id" ON "performances" ("player_id");