from __future__ import annotations

from contextlib import closing
from dataclasses import asdict, dataclass

from app.config import config
from app.utils import balls_to_overs, player_name

BEST_BOWLING_SQL = """
WITH
	mb AS (
	SELECT
		CAST(player_id AS integer) AS player_id
	,	CAST(strftime('%Y', datetime(match_date)) AS integer) AS year
	,	CAST(wickets AS INTEGER) AS wickets
	,	CAST(runs_conceded AS INTEGER) AS runs
	,	match_date
	,	opp
	FROM match_bowling
)
, most_wickets AS (
	SELECT
		player_id
	,	year
	,	MAX(wickets) AS wickets
	FROM mb
	WHERE player_id = :player_id
	GROUP BY player_id, year
)
, bb AS (
	SELECT
		w.player_id
	,	w.year
	,	w.wickets
	,	MIN(mb.runs) AS runs
	FROM most_wickets w
		JOIN mb ON mb.player_id = w.player_id AND mb.year = w.year AND w.wickets = mb.wickets
	GROUP BY
		w.player_id
	,	w.year
	,	w.wickets
)
, maxed AS (
	SELECT
		player_id
	,	year
	,	wkts AS wickets
	,	runs
	,	wkts * 1000 - runs AS sort_key
	FROM best_bowling
	WHERE player_id = :player_id
	AND year < 1997
),
by_year AS (
	SELECT
		player_id
	,	year
	,	MAX(sort_key) AS best
	FROM maxed
	GROUP BY
		player_id
	,	year
)
SELECT
	bb.year
,   bb.wickets
,   bb.runs
,   bb.wickets * 1000 - bb.runs AS sort_key
FROM bb
	LEFT JOIN mb ON bb.player_id = mb.player_id
    AND bb.wickets = mb.wickets
    AND bb.runs = mb.runs
    AND bb.year = mb.year
UNION
SELECT
	x.year
,	x.wickets
,	x.runs
,	x.sort_key
FROM maxed x
	JOIN by_year y ON y.player_id = x.player_id AND y.year = x.year AND y.best = x.sort_key
"""


@dataclass(kw_only=True)
class Performance:
    id: int = -1
    player_id: int = -1
    code: str = ""
    year: str = ""
    matches: int = 0
    innings: int = 0
    notout: int = 0
    highest: int = 0
    highestnotout: bool = False
    runsscored: int = 0
    fours: int = 0
    sixes: int = 0
    overs: int = 0
    balls: int = 0
    maidens: int = 0
    wides: int = 0
    noballs: int = 0
    runs: int = 0
    wickets: int = 0
    fivewktinn: int = 0
    caught: int = 0
    stumped: int = 0
    fifties: int = 0
    hundreds: int = 0
    fives: int = 0
    caughtwkt: int = 0
    captain: int = 0
    keptwicket: int = 0

    best_bowling: str = ""

    @property
    def high_score(self) -> str:
        return f"{self.highest}{'*' if self.highestnotout else ''}"

    @property
    def overs_bowled(self) -> str:
        return balls_to_overs(self.balls_bowled)

    @property
    def batting_average(self) -> float:
        if (self.innings - self.notout) > 0:
            return round(self.runsscored / (self.innings - self.notout), 2)
        else:
            return 0

    @property
    def bowling_average(self) -> float:
        return round(self.runs / self.wickets, 2) if self.wickets > 0 else 0

    @property
    def strike_rate(self) -> float | None:
        return round(self.balls_bowled / self.wickets, 2) if self.wickets else None

    @property
    def balls_bowled(self) -> int:
        return self.overs * 6 + self.balls

    @property
    def economy(self) -> float:
        return round(self.runs * 6 / self.balls_bowled, 2)

    def row_dict(self) -> dict:
        return asdict(self) | {
            "high_score": self.high_score,
            "overs_bowled": self.overs_bowled,
            "batting_average": self.batting_average,
            "bowling_average": self.bowling_average,
        }

    @staticmethod
    def sumof(field_name: str, perfs: list[Performance]):
        return sum(getattr(p, field_name) for p in perfs)

    @classmethod
    def for_player(cls, player_id: int) -> list[Performance]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM performances WHERE player_id = :player_id ORDER BY year",
                {"player_id": player_id},
            )
            rows = csr.fetchall()
        perfs = [Performance(**row) for row in rows]

        with closing(config.db.cursor()) as csr:
            rows = csr.execute(
                BEST_BOWLING_SQL,
                {"player_id": player_id},
            ).fetchall()
            best_bowling_by_year = {row["year"]: f"{row['wickets']}-{row['runs']}" for row in rows}

            best_bb = max(rows, key=lambda bb: bb["sort_key"]) if best_bowling_by_year else None
        for perf in perfs:
            perf.best_bowling = best_bowling_by_year.get(perf.year, "")

        totals = Performance(
            code="",
            year="Total",
            matches=Performance.sumof("matches", perfs),
            innings=Performance.sumof("innings", perfs),
            notout=Performance.sumof("notout", perfs),
            runsscored=Performance.sumof("runsscored", perfs),
            fours=Performance.sumof("fours", perfs),
            sixes=Performance.sumof("sixes", perfs),
            overs=Performance.sumof("overs", perfs),
            balls=Performance.sumof("balls", perfs),
            maidens=Performance.sumof("maidens", perfs),
            runs=Performance.sumof("runs", perfs),
            wickets=Performance.sumof("wickets", perfs),
            fivewktinn=Performance.sumof("fivewktinn", perfs),
            caught=Performance.sumof("caught", perfs),
            stumped=Performance.sumof("stumped", perfs),
            fifties=Performance.sumof("fifties", perfs),
            hundreds=Performance.sumof("hundreds", perfs),
            caughtwkt=Performance.sumof("caughtwkt", perfs),
            captain=Performance.sumof("captain", perfs),
            keptwicket=Performance.sumof("keptwicket", perfs),
            best_bowling=f"{best_bb['wickets']}-{best_bb['runs']}" if best_bb else "",
        )

        totals.highest, totals.highestnotout = max((p.highest, p.highestnotout) for p in perfs)

        perfs.append(totals)
        return perfs

    @classmethod
    def for_year(cls, year: int) -> list[Performance]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM performances WHERE year = :year",
                {"year": year},
            )
            rows = csr.fetchall()
        return [Performance(**row) for row in rows]

    @staticmethod
    def career_appearances() -> list[dict]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                """
                SELECT
                    pl.id AS player_id
                ,	pl.surname
                ,	pl.initial
                ,	pl.firstname
                ,	Sum(pe.matches) AS appearances
                ,	MIN(pe.year) AS from_year
                ,	MAX(pe.year) AS to_year
                FROM players pl JOIN performances pe ON pe.player_id = pl.id
                GROUP BY
                    pl.id
                ,	pl.surname
                ,	pl.initial
                ,	pl.firstname
                HAVING SUM(pe.matches) >= :min_apps
                ORDER BY 5 DESC
            """,
                {"min_apps": config.MIN_APPS},
            )
            rows = [dict(row) for row in csr.fetchall()]
            for row in rows:
                row["player_name"] = player_name(row["firstname"], row["initial"], row["surname"])
            return rows

    @staticmethod
    def table_cols() -> list[dict]:
        return [
            {
                "name": "year",
                "label": "year",
                "field": "year",
                "sortable": True,
                "align": "center",
            },
            {
                "name": "matches",
                "label": "matches",
                "field": "matches",
                "sortable": True,
            },
            {
                "name": "innings",
                "label": "innings",
                "field": "innings",
                "sortable": True,
            },
            {
                "name": "notout",
                "label": "not out",
                "field": "notout",
                "sortable": True,
            },
            {
                "name": "high_score",
                "label": "highest",
                "field": "high_score",
                "sortable": True,
            },
            {
                "name": "runsscored",
                "label": "runs",
                "field": "runsscored",
                "sortable": True,
            },
            {
                "name": "batave",
                "label": "ave",
                "field": "batting_average",
                "sortable": True,
            },
            {
                "name": "fours",
                "label": "fours",
                "field": "fours",
                "sortable": True,
            },
            {
                "name": "sixes",
                "label": "sixes",
                "field": "sixes",
                "sortable": True,
            },
            {
                "name": "overs_bowled",
                "label": "overs",
                "field": "overs_bowled",
                "sortable": True,
            },
            {
                "name": "maidens",
                "label": "maidens",
                "field": "maidens",
                "sortable": True,
            },
            {
                "name": "runs",
                "label": "runs",
                "field": "runs",
                "sortable": True,
            },
            {
                "name": "wickets",
                "label": "wickets",
                "field": "wickets",
                "sortable": True,
            },
            {
                "name": "bowlave",
                "label": "ave",
                "field": "bowling_average",
                "sortable": True,
            },
            {
                "name": "fivewktinn",
                "label": "five-for",
                "field": "fivewktinn",
                "sortable": True,
            },
            {
                "name": "best",
                "label": "best",
                "field": "best_bowling",
                "sortable": False,
                "align": "center",
            },
            {
                "name": "caught",
                "label": "caught",
                "field": "caught",
                "sortable": True,
            },
            {
                "name": "stumped",
                "label": "stumped",
                "field": "stumped",
                "sortable": True,
            },
            {
                "name": "fifties",
                "label": "fifties",
                "field": "fifties",
                "sortable": True,
            },
            {
                "name": "hundreds",
                "label": "hundreds",
                "field": "hundreds",
                "sortable": True,
            },
            {
                "name": "caughtwkt",
                "label": "caught wkt",
                "field": "caughtwkt",
                "sortable": True,
            },
            {
                "name": "captain",
                "label": "captain",
                "field": "captain",
                "sortable": True,
            },
            {
                "name": "keptwicket",
                "label": "kept wicket",
                "field": "keptwicket",
                "sortable": True,
            },
        ]
