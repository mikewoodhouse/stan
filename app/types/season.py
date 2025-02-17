from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass

from app.config import config


@dataclass(kw_only=True)
class Season:
    id: int = -1
    year: int
    played: int
    won: int
    lost: int
    drawn: int
    tied: int
    noresult: int
    maxpossiblegames: int

    @classmethod
    def all(cls) -> list[Season]:
        with closing(config.db.cursor()) as csr:
            csr.execute("SELECT * FROM seasons ORDER BY year DESC")
            rows = list(csr.fetchall())
            return [Season(**row) for row in rows]

    @classmethod
    def for_year(cls, year: int) -> Season:
        with closing(config.db.cursor()) as csr:
            csr.execute("SELECT * FROM seasons WHERE year = :year", {"year": year})
            row = csr.fetchone()
            return Season(**row)
