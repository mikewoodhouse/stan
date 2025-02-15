import os

from app.config import config
from app.loaders.csv_loader import CsvLoader
from app.loaders.load_defs import load_defs
from app.utils import count

os.unlink("stan.sqlite")


loader = CsvLoader()
loader.load_schema()

for tablename, load_def in load_defs.items():
    # if tablename in ["matches", "match_batting", "match_bowling"]:
    print("loading", load_def.table)
    loader.load(load_def)


loader.set_match_ids()
config.db.commit()

loader.set_player_ids()
config.db.commit()

for table in load_defs.keys():
    print(table, count(table))
config.db.commit()
config.db.close()
