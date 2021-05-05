from util.db import db_connection


class PlayerRecord:
    def __init__(self, code) -> None:
        self.code = code

        with db_connection() as conn:
            csr = conn.cursor()
            res = csr.execute("""
            SELECT p.surname || ', ' || IfNull(p.firstname, IfNull(p.initial, '?')) name
            FROM players p
            WHERE code = ?
            """, (code,)).fetchone()
            self.name = res.name
            csr.close()
            csr = conn.cursor()
            csr.execute("""
            SELECT
            *
            , CASE highest_not_out
                WHEN 1 THEN '*'
                ELSE ''
            END high_not_out_flag
            , CASE innings
                WHEN 0 THEN 0.0
                ELSE
                    CASE not_out
                        WHEN innings THEN 0.0
                        ELSE Round(Cast(runs_scored AS REAL) / (Cast(innings - not_out AS REAL)), 2)
                    END
                END bat_ave
            , CASE wickets
                WHEN 0 THEN 0
                ELSE Cast(runs_conceded AS REAL) / Cast(wickets AS REAL)
            END bowl_ave
            FROM performances
            WHERE code = ?
            ORDER BY year
            """, (code,))
            self.performances = [Performance(row) for row in csr.fetchall()]
            csr.close()


class Performance:
    def __init__(self, flds) -> None:
        self.__dict__ = flds._asdict()