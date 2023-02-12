from app.csv_loader import CsvLoader, load_defs
import sqlite3
import pytest

TABLES = [
    "players",
    "seasons",
    "hundred_plus",
]


@pytest.fixture
def loader() -> CsvLoader:
    loader = CsvLoader(sqlite3.connect(":memory:"))
    loader.load_schema()
    return loader


@pytest.fixture
def fully_loaded() -> CsvLoader:
    loader = CsvLoader(sqlite3.connect(":memory:"))
    loader.load_schema()
    for table in TABLES:
        loader.load(table)
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
    TABLES,
)
def test_load_defs_exist(key):
    assert key in load_defs


def test_data_loaded(fully_loaded: CsvLoader):
    assert all(count(fully_loaded, table) > 0 for table in TABLES)


def test_player_ids_set(fully_loaded: CsvLoader):
    sql = """
        select
            count(*) row_count, count(distinct player_id) player_ids
        from hundred_plus
        """
    row_count, player_ids = fully_loaded.conn.execute(sql).fetchone()
    assert player_ids > 1
    assert row_count > 0
