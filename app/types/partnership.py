from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import date
import sqlite3
from dataclass_csv import dateformat
from contextlib import closing


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

    def row_dict(self) -> dict:
        return asdict(self) | {}

    @staticmethod
    def all(db: sqlite3.Connection) -> list[Partnership]:
        with closing(db.cursor()) as csr:
            csr.execute("SELECT * FROM partnerships")
            return [Partnership(**row) for row in csr.fetchall()]

    @staticmethod
    def table_cols() -> list[dict]:
        return {}
