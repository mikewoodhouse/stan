import pytest

from app.loaders.excel_loader import ExcelLoader


@pytest.fixture
def loader() -> ExcelLoader:
    return ExcelLoader("")


def test_construction(loader):
    assert isinstance(loader, ExcelLoader)
    assert loader.filepath == ""
