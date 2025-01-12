from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import date

from dataclass_csv import dateformat


@dataclass(kw_only=True)
@dateformat(r"%Y-%m-%d %H:%M:%S")
class Partnership:
    id: int = 0
    year: int
    wicket: int
    date: date
    total: int
    undefeated: bool
    bat1: str
    bat1score: int
    bat1notout: bool
    bat2: str
    bat2score: int
    bat2notout: bool
    opp: str
    bat1_id: int = -1
    bat2_id: int = -1

    bat1_name: str = ""
    bat2_name: str = ""

    def row_dict(self) -> dict:
        return asdict(self) | {
            "display_undefeated": f"{'*' if self.undefeated else ''}",
            "display_bat1_notout": f"{'*' if self.bat1notout else ''}",
            "display_bat2_notout": f"{'*' if self.bat2notout else ''}",
        }

    @staticmethod
    def for_wicket(db: sqlite3.Connection, wicket: int) -> list[Partnership]:
        with closing(db.cursor()) as csr:
            csr.execute(
                """SELECT pt.*
                        , b1.surname || CASE WHEN b1.initial BETWEEN 'A' AND 'Z' THEN ', ' || b1.initial ELSE '' END AS bat1_name
                        , b2.surname || CASE WHEN b2.initial BETWEEN 'A' AND 'Z' THEN ', ' || b2.initial ELSE '' END AS bat2_name
                        FROM partnerships pt
                        JOIN players b1 ON b1.id = pt.bat1_id
                        JOIN players b2 ON b2.id = pt.bat2_id
                        WHERE wicket = :wicket
                        ORDER BY wicket, total DESC""",
                {"wicket": wicket},
            )
            return [Partnership(**row) for row in csr.fetchall()]

    @staticmethod
    def table_cols() -> list[dict]:
        return [
            {"name": "total", "label": "Runs", "field": "total", "sortable": True, "align": "right"},
            {"name": "undefeated", "label": "", "field": "display_undefeated", "sortable": False, "align": "left"},
            {"name": "bat_1", "label": "Bat 1", "field": "bat1_name", "sortable": False, "align": "left"},
            {"name": "bat1score", "label": "", "field": "bat1score", "sortable": False, "align": "right"},
            {"name": "bat1no", "label": "", "field": "display_bat1_notout", "sortable": False, "align": "left"},
            {"name": "bat_2", "label": "Bat 2", "field": "bat2_name", "sortable": False, "align": "left"},
            {"name": "bat2score", "label": "", "field": "bat1score", "sortable": False, "align": "right"},
            {"name": "bat2no", "label": "", "field": "display_bat2_notout", "sortable": False, "align": "left"},
            {"name": "opp", "label": "Vs", "field": "opp", "sortable": False, "align": "left"},
            {"name": "date", "label": "Date", "field": "date", "sortable": True, "align": "center"},
            {"name": "", "label": "", "field": "", "sortable": False, "align": "left"},
            {"name": "", "label": "", "field": "", "sortable": False, "align": "left"},
        ]
