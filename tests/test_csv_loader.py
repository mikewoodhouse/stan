import sqlite3

import pytest

from app.csv_loader import CsvLoader, load_defs


@pytest.fixture
def loader() -> CsvLoader:
    loader = CsvLoader(sqlite3.connect(":memory:"))
    loader.load_schema()
    return loader


@pytest.fixture
def fully_loaded() -> CsvLoader:
    loader = CsvLoader(sqlite3.connect(":memory:"))
    loader.load_schema()
    for filename, _ in load_defs.items():
        loader.load(filename)
    return loader


def count(loader: CsvLoader, tablename: str) -> int:
    csr = loader.conn.execute(f"SELECT COUNT(*) FROM {tablename}")
    return csr.fetchone()[0]


def test_construct(loader: CsvLoader):
    assert isinstance(loader.conn, sqlite3.Connection)


def test_schema_loaded(loader: CsvLoader):
    assert count(loader, "players") == 0


def test_data_loaded(fully_loaded: CsvLoader):
    assert all(count(fully_loaded, table) > 0 for table in load_defs.keys())


def test_player_ids_set(fully_loaded: CsvLoader):
    def count_in_col(table: str, col: str) -> bool:
        sql = f"""
        select
            count(*) row_count
        ,   count(distinct {col}) player_ids
        from {table}
        """
        row_count, player_ids = fully_loaded.conn.execute(sql).fetchone()
        return row_count > 0 and player_ids > 1

    assert all(
        count_in_col(load_def.table, col)
        for load_def in load_defs.values()
        for col in load_def.player_id_cols
    )
