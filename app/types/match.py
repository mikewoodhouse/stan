from __future__ import annotations

from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import date

from dataclass_csv import dateformat

from app.config import config


@dateformat("%Y-%m-%d %H:%M:%S")
@dataclass(kw_only=True)
class Match:
    id: int = -1
    date: date
    oppo: str
    venue: str = "?"
    result: str = "?"
    bat_first: str = "?"
    first_runs: int = 0
    first_wkts: int = 0
    first_all_out: bool = False
    first_notes: str = ""
    second_runs: int = 0
    second_wkts: int = 0
    second_all_out: bool = False
    second_notes: str = ""
    overs_opp: float = 0
    overs_tocc: float = 0
    tocc_w: int = 0
    tocc_nb: int = 0
    tocc_b: int = 0
    tocc_lb: int = 0
    opp_w: int = 0
    opp_nb: int = 0
    opp_b: int = 0
    opp_lb: int = 0

    def overs(self, inns: int) -> str:
        if self.bat_first == "Opp":
            ov = self.overs_tocc if inns == 1 else self.overs_opp
        else:
            ov = self.overs_tocc if inns == 2 else self.overs_opp
        return f"{ov:.1f}"

    def row_dict(self) -> dict:
        return asdict(self) | {
            "match_date": self.date.strftime("%d-%b"),
            "score_1": f"{self.first_runs}-{self.first_wkts} ({self.overs(1)})",
            "score_2": f"{self.second_runs}-{self.second_wkts} ({self.overs(2)})",
            "bat_second": "TOCC" if self.bat_first == "Opp" else self.oppo,
        }

    @classmethod
    def for_year(cls, year: int) -> list[Match]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM matches WHERE date between :soy AND :eoy ORDER BY date",
                {"soy": f"{year}-01-01", "eoy": f"{year}-12-31"},
            )
            rows = csr.fetchall()
        matches = [Match(**row) for row in rows]
        return matches

    @classmethod
    def for_id(cls, match_id: int) -> list[Match]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                "SELECT * FROM matches WHERE id = :match_id",
                {"match_id": match_id},
            )
            rows = csr.fetchall()
        matches = [Match(**row) for row in rows]
        return matches
