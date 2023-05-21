from app.excel_loader import ExcelLoader
import pytest


@pytest.fixture
def loader() -> ExcelLoader:
    return ExcelLoader("")


def test_construction(loader):
    assert isinstance(loader, ExcelLoader)
    assert loader.filepath == ""
