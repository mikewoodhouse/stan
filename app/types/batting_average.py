from __future__ import annotations

from dataclasses import Field, dataclass, fields
from typing import Any

from app.types.performance import Performance


@dataclass(kw_only=True)
class BattingAverage:
    player_id: int = -1
    position: int = -1
    name: str = ""
    innings: int
    notout: int
    high_score: str
    runsscored: int
    average: float = 0
    fifties: int
    hundreds: int
    fours: int
    sixes: int

    @classmethod
    def for_year(cls, year: int, min_innings: int = 1) -> tuple[list[BattingAverage], list[BattingAverage]]:
        perfs = [perf for perf in Performance.for_year(year) if perf.innings > 0]
        flds = fields(cls)

        def build_row(flds: tuple[Field[Any], ...], perf: Performance) -> BattingAverage:
            attrs = {field.name: getattr(perf, field.name, None) for field in flds}
            item: BattingAverage = BattingAverage(**{k: v for k, v in attrs.items() if v is not None})
            item.average = perf.batting_average
            item.high_score = perf.high_score
            return item

        avgs = [build_row(flds, perf) for perf in perfs]
        main_set = list(filter(lambda avg: avg.innings >= min_innings, avgs))
        also_batted = list(filter(lambda avg: avg.innings < min_innings, avgs))
        main_set.sort(key=lambda b: b.average, reverse=True)
        for idx, item in enumerate(main_set):
            item.position = idx + 1
        also_batted.sort(key=lambda b: b.name)
        return main_set, also_batted

    @staticmethod
    def table_cols():
        return [
            {"name": "position", "label": "Pos", "field": "position", "sortable": True},
            {"name": "name", "field": "Name", "align": "left", "sortable": True},
            {"name": "innings", "label": "Inns", "field": "innings", "sortable": True},
            {"name": "notout", "label": "N/O", "field": "notout", "sortable": True},
            {"name": "high_score", "label": "High", "field": "high_score", "sortable": True},
            {"name": "runsscored", "label": "Runs", "field": "runsscored", "sortable": True},
            {
                "name": "average",
                "label": "Avg",
                "field": "average",
                "sortable": True,
                ":format": "value => value ? value.toFixed(2) : ''",
            },
            {"name": "fifties", "label": "50s", "field": "fifties", "sortable": True},
            {"name": "hundreds", "label": "100s", "field": "hundreds", "sortable": True},
            {"name": "fours", "label": "4s", "field": "fours", "sortable": True},
            {"name": "sixes", "label": "6s", "field": "sixes", "sortable": True},
        ]
