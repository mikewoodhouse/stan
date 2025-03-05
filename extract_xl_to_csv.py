import warnings
from pathlib import Path

from openpyxl import load_workbook

from app.loaders.xl import (
    XlBattingImporter,
    XlBowlingImporter,
    XlMatchImporter,
)
from app.stopwatch import StopWatch
from app.types import Match, MatchBatting, MatchBowling


def clear_csv_files(path: Path) -> None:
    for filename in ["match_batting", "match_bowling", "matches"]:
        filepath = path / f"{filename}.csv"
        print(f"deleting {filepath}")
        filepath.unlink()


if __name__ == "__main__":
    with StopWatch("Excel->csv extract", decimals=2):
        warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

        path = Path("./data/xldata")
        csv_path = Path("./data/csvdata")

        clear_csv_files(csv_path)

        for filepath in sorted(path.glob("*.xlsm"), key=lambda p: p.name):
            year = int(filepath.stem[-4:])
            if filepath.name.startswith("~"):
                continue
            print(f"importing {filepath} for {year}")
            workbook = load_workbook(str(filepath), data_only=True)
            XlMatchImporter(workbook, csv_path, "matches", Match).ingest()
            XlBattingImporter(workbook, csv_path, "match_batting", MatchBatting).ingest()
            XlBowlingImporter(workbook, csv_path, "match_bowling", MatchBowling).ingest()
