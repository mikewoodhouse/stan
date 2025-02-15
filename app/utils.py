from contextlib import closing

from app.config import config


def balls_to_overs(balls: int) -> str:
    overs, balls = divmod(balls, 6)
    return f"{overs}.{balls}"


def player_name(firstname: str, initial: str, surname: str) -> str:
    if forename := firstname or initial:
        return f"{surname}, {forename}"
    return surname


def count(tablename: str) -> int:
    with closing(config.db.cursor()) as csr:
        csr.execute(f"SELECT count(*) AS row_count FROM {tablename}")
        return csr.fetchone()["row_count"]
