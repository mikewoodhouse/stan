import os
import sqlite3
from contextlib import closing

from app.csv_loader import CsvLoader

os.unlink("stan.sqlite")
db = sqlite3.connect("stan.sqlite")

TABLES = [
    "players",
    "seasons",
    "hundred_plus",
    "partnerships",
]


def count(db: sqlite3.Connection, tablename: str) -> int:
    with closing(db.cursor()) as csr:
        csr.execute(f"SELECT count(*) FROM {tablename}")
        return csr.fetchone()[0]


loader = CsvLoader(db)
loader.load_schema()
for table in TABLES:
    print("loading", table)
    loader.load(table)
for table in TABLES:
    print(table, count(db, table))
db.commit()
db.close()
