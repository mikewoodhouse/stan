import os
import pathlib
import sqlite3

from app.loaders.xl.excel_loader import load_matches

os.unlink("stanxl.sqlite")
db = sqlite3.connect("stanxl.sqlite")

with open("xl_schema.sql") as f:
    db.executescript(f.read())


workbooks = sorted(iter(pathlib.Path("xldata").glob("*.xlsm")))

for xlpath in workbooks:
    wbpath = xlpath.anchor
    load_matches(wbpath)
