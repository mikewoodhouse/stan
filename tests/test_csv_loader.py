import sqlite3

import pytest

from app.config import config
from app.loaders.csv_loader import CsvLoader
from app.loaders.load_defs import load_defs


def reset_db():
    if config.db is not None:
        config.db.close()
    config.db = sqlite3.connect(":memory:")


@pytest.fixture
def loader() -> CsvLoader:
    reset_db()
    loader = CsvLoader()
    loader.load_schema()
    return loader


@pytest.fixture
def fully_loaded() -> CsvLoader:
    reset_db()
    loader = CsvLoader()
    loader.load_schema()
    for defn in load_defs.values():
        loader.load(defn)
    return loader


def count(loader: CsvLoader, tablename: str) -> int:
    csr = loader.conn.execute(f"SELECT COUNT(*) FROM {tablename}")
    return csr.fetchone()[0]


def test_construct(loader: CsvLoader):
    assert isinstance(loader.conn, sqlite3.Connection)


def test_schema_loaded(loader: CsvLoader):
    assert count(loader, "players") == 0
