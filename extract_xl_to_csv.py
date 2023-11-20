import warnings
from pathlib import Path

from openpyxl import load_workbook

from app.loaders.xl import XlBattingImporter, XlBowlingImporter, XlMatchImporter
from app.types import Match, MatchBatting, MatchBowling


def clear_csv_files(path: Path) -> None:
    for filepath in path.glob("*.csv"):
        print(f"deleting {filepath}")
        filepath.unlink()


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

    path = Path("./data/xldata")
    csv_path = Path("./data/csvdata")

    clear_csv_files(path)

    for filepath in path.glob("*.xlsm"):
        print(f"importing {filepath}")
        workbook = load_workbook(str(filepath))
        XlMatchImporter(workbook, csv_path, "matches", Match).ingest()
        XlBattingImporter(workbook, csv_path, "match_batting", MatchBatting).ingest()
        XlBowlingImporter(workbook, csv_path, "match_bowling", MatchBowling).ingest()
