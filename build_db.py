import os
import sqlite3
from contextlib import closing

from app.loaders.csv_loader import CsvLoader
from app.loaders.load_defs import load_defs

os.unlink("stan.sqlite")
db = sqlite3.connect("stan.sqlite")


def count(db: sqlite3.Connection, tablename: str) -> int:
    with closing(db.cursor()) as csr:
        csr.execute(f"SELECT count(*) FROM {tablename}")
        return csr.fetchone()[0]


loader = CsvLoader(db)
loader.load_schema()
for tablename, load_def in load_defs.items():
    print("loading", load_def.table)
    loader.load(load_def)
for table in load_defs.keys():
    print(table, count(db, table))
db.commit()
db.close()
