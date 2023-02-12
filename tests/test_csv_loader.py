from app.csv_loader import CsvLoader, load_defs
import sqlite3
import pytest


@pytest.fixture
def loader() -> CsvLoader:
    loader = CsvLoader(sqlite3.connect(":memory:"))
    loader.load_schema()
    return loader


def count(loader: CsvLoader, tablename: str) -> int:
    csr = loader.conn.execute(f"SELECT COUNT(*) FROM {tablename}")
    return csr.fetchone()[0]


def test_construct(loader: CsvLoader):
    assert isinstance(loader.conn, sqlite3.Connection)


def test_schema_loaded(loader: CsvLoader):
    assert count(loader, "players") == 0


@pytest.mark.parametrize(
    "key",
    [
        "players",
    ],
)
def test_load_defs_exist(key):
    assert key in load_defs


def test_players_loaded(loader: CsvLoader):
    loader.load("players")
    assert count(loader, "players") > 0
