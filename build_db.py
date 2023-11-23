import os
import sqlite3
from contextlib import closing

from app.loaders.csv_loader import CsvLoader
from app.loaders.load_defs import load_defs

os.unlink("stan.sqlite")


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


db = sqlite3.connect("stan.sqlite")
db.row_factory = dict_factory


def count(db: sqlite3.Connection, tablename: str) -> int:
    with closing(db.cursor()) as csr:
        csr.execute(f"SELECT count(*) AS row_count FROM {tablename}")
        return csr.fetchone()["row_count"]


loader = CsvLoader(db)
loader.load_schema()
for tablename, load_def in load_defs.items():
    print("loading", load_def.table)
    loader.load(load_def)
    db.commit()
loader.set_match_ids()
db.commit()
loader.set_player_ids()
db.commit()

for table in load_defs.keys():
    print(table, count(db, table))
db.commit()
db.close()
