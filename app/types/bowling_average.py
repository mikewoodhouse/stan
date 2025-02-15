from __future__ import annotations

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
    strike_rate: float | None = None
    economy: float = 0

    @classmethod
    def for_year(cls, year: int, min_wickets: int = 1) -> tuple[list[BowlingAverage], list[BowlingAverage]]:
        perfs = [perf for perf in Performance.for_year(year) if perf.balls_bowled > 0]
        flds = fields(cls)

        def build_row(flds: tuple[Field[Any], ...], perf: Performance) -> BowlingAverage:
            attrs = {field.name: getattr(perf, field.name, None) for field in flds}
            item: BowlingAverage = BowlingAverage(**{k: v for k, v in attrs.items() if v is not None})
            item.average = perf.bowling_average
            item.overs_bowled = balls_to_overs(item.overs * 6 + item.balls)
            item.strike_rate = perf.strike_rate
            item.economy = perf.economy
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
            {"name": "position", "label": "Pos", "field": "position", "sortable": True},
            {"name": "name", "label": "Name", "field": "name", "align": "left", "sortable": True},
            {"name": "overs", "label": "Overs", "field": "overs_bowled", "sortable": True},
            {"name": "maidens", "label": "Maidens", "field": "maidens", "sortable": True},
            {"name": "runs", "label": "Runs", "field": "runs", "sortable": True},
            {"name": "wickets", "label": "Wickets", "field": "wickets", "sortable": True},
            {
                "name": "average",
                "label": "Avg",
                "field": "average",
                "sortable": True,
                ":format": "value => value ? value.toFixed(2) : ''",
            },
            {
                "name": "strike",
                "label": "Strike",
                "field": "strike_rate",
                "sortable": True,
                ":format": "value => value ? value.toFixed(2) : ''",
            },
            {
                "name": "economy",
                "label": "Economy",
                "field": "economy",
                "sortable": True,
                ":format": "value => value ? value.toFixed(2) : ''",
            },
            {"name": "five+", "label": "5+", "field": "five+", "sortable": True},
        ]
