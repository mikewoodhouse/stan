import os
import pathlib
import sqlite3

from app.loaders.excel_loader import ExcelLoader

os.unlink("stanxl.sqlite")
db = sqlite3.connect("stanxl.sqlite")

with open("xl_schema.sql") as f:
    db.executescript(f.read())


workbooks = sorted(iter(pathlib.Path("xldata").glob("*.xlsm")))

for xlpath in workbooks:
    loader = ExcelLoader(xlpath.anchor)
