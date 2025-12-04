import os

from stan.config import config
from stan.loaders.csv_loader import CsvLoader
from stan.loaders.load_defs import load_defs
from stan.stopwatch import StopWatch
from stan.utils import count

os.unlink("stan.sqlite")


with StopWatch("database build", decimals=2):
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
