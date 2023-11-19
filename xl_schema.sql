CREATE TABLE
  IF NOT EXISTS "matches" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "year" INTEGER
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
  , "overs_opp" INTEGER
  , "overs_tocc" INTEGER
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
  IF NOT EXISTS "match_batting" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  , "match_id" INTEGER
  , "match_date" DATE
  , "opp" VARCHAR
  , "name" VARCHAR
  , "position" INTEGER
  , "runs" INTEGER
  , "out" BOOLEAN
  , "how_out" VARCHAR
  , "captain" BOOLEAN
  , "kept_wicket" BOOLEAN
  , "caught" INTEGER
  , "caught_wkt" INTEGER
  , "stumped" INTEGER
  , "fours" INTEGER
  , "sixes" INTEGER
  );