from __future__ import annotations

import sqlite3
from dataclasses import Field, dataclass, fields
from typing import Any

from app.types.performance import Performance
from app.utils import balls_to_overs


@dataclass(kw_only=True)
class BowlingAverage:
    player_id: int = -1
    position: int = -1
    name: str = ""
    overs: int
    balls: int
    overs_bowled: str = ""
    maidens: str
    runs: int
    wickets: int
    average: float = 0
    fifties: int
    hundreds: int
    fours: int
    sixes: int

    @classmethod
    def for_year(
        cls, db: sqlite3.Connection, year: int, min_wickets: int = 1
    ) -> tuple[list[BowlingAverage], list[BowlingAverage]]:
        perfs = [perf for perf in Performance.for_year(db, year) if perf.innings > 0]
        flds = fields(cls)

        def build_row(
            flds: tuple[Field[Any], ...], perf: Performance
        ) -> BowlingAverage:
            attrs = {field.name: getattr(perf, field.name, None) for field in flds}
            item: BowlingAverage = BowlingAverage(
                **{k: v for k, v in attrs.items() if v is not None}
            )
            item.average = perf.bowling_average
            item.overs_bowled = balls_to_overs(item.overs * 6 + item.balls)
            return item

        avgs = [build_row(flds, perf) for perf in perfs]
        main_set = list(filter(lambda avg: avg.wickets >= min_wickets, avgs))
        also_bowled = list(
            filter(
                lambda avg: avg.wickets < min_wickets and avg.overs + avg.balls > 0,
                avgs,
            )
        )
        main_set.sort(key=lambda b: b.average, reverse=False)
        for idx, item in enumerate(main_set):
            item.position = idx + 1
        also_bowled.sort(key=lambda b: b.name)
        return main_set, also_bowled

    @staticmethod
    def table_cols():
        return [
            {
                "name": "position",
                "label": "position",
                "field": "position",
                "sortable": True,
            },
            {
                "name": "name",
                "label": "name",
                "field": "name",
                "align": "left",
                "sortable": True,
            },
            {
                "name": "overs",
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
                "name": "average",
                "label": "average",
                "field": "average",
                "sortable": True,
            },
            {
                "name": "strike",
                "label": "strike",
                "field": "strike",
                "sortable": True,
            },
            {
                "name": "economy",
                "label": "economy",
                "field": "economy",
                "sortable": True,
            },
            {
                "name": "five+",
                "label": "five+",
                "field": "five+",
                "sortable": True,
            },
        ]
