import os
from contextlib import closing

from app.config import config
from app.loaders.csv_loader import CsvLoader
from app.loaders.load_defs import load_defs

os.unlink("stan.sqlite")


def count(tablename: str) -> int:
    with closing(config.db.cursor()) as csr:
        csr.execute(f"SELECT count(*) AS row_count FROM {tablename}")
        return csr.fetchone()["row_count"]


loader = CsvLoader(config.db)
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
    print(table, count(table))
db.commit()
db.close()
