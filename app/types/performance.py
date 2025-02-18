from __future__ import annotations

from contextlib import closing
from dataclasses import asdict, dataclass

from app.config import config
from app.utils import balls_to_overs, sql_query


@dataclass(kw_only=True)
class Performance:
    id: int = -1
    player_id: int = -1
    name: str = ""
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
                sql_query("player_perfs"),
                {"player_id": player_id},
            )
            rows = csr.fetchall()
        perfs = [Performance(**row) for row in rows]

        with closing(config.db.cursor()) as csr:
            rows = csr.execute(
                sql_query("best_bowling"),
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
                sql_query("perfs_for_year"),
                {"year": year},
            )
            rows = csr.fetchall()
        return [Performance(**row) for row in rows]

    @staticmethod
    def career_appearances() -> list[dict]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                sql_query("appearances"),
                {"min_apps": config.MIN_APPS},
            )
            rows = [dict(row) for row in csr.fetchall()]
            return rows
