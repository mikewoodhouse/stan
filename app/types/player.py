from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass


@dataclass(kw_only=True)
class Player:
    id: int = -1
    code: str
    surname: str
    active: bool
    initial: str = ""
    firstname: str = ""

    @property
    def name(self) -> str:
        if forename := self.firstname or self.initial:
            return f"{self.surname}, {forename}"
        return self.surname

    @classmethod
    def get(cls, db: sqlite3.Connection, player_id: int) -> Player:
        with closing(db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM players WHERE id = :player_id", {"player_id": player_id}
            )
            row: dict = csr.fetchone()
            return Player(**row)

    @classmethod
    def all(cls, db: sqlite3.Connection) -> dict[int, Player]:
        with closing(db.cursor()) as csr:
            csr.execute("SELECT * FROM players")
            rows: list[dict] = csr.fetchall()
            return {row["id"]: Player(**row) for row in rows}
