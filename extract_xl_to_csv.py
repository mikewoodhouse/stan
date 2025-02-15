import warnings
from pathlib import Path

from openpyxl import load_workbook

from app.loaders.xl import (
    XlBattingImporter,  # XlPartnershipsImporter,
    XlBowlingImporter,
    XlMatchImporter,
)
from app.types import Match, MatchBatting, MatchBowling  # , Partnership


def clear_csv_files(path: Path) -> None:
    for filepath in path.glob("*.csv"):
        print(f"deleting {filepath}")
        filepath.unlink()


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

    path = Path("./data/xldata")
    csv_path = Path("./data/csvdata")

    for filepath in sorted(path.glob("*.xlsm"), key=lambda p: p.name):
        year = int(filepath.stem[-4:])
        if filepath.name.startswith("~"):
            continue
        print(f"importing {filepath} for {year}")
        workbook = load_workbook(str(filepath), data_only=True)
        XlMatchImporter(workbook, csv_path, "matches", Match).ingest()
        XlBattingImporter(workbook, csv_path, "match_batting", MatchBatting).ingest()
        XlBowlingImporter(workbook, csv_path, "match_bowling", MatchBowling).ingest()
        # NOTE: partnerships are only needed if they aren't already in the database, which they were until 2022
        # if year >= 2023:
        #     XlPartnershipsImporter(
        #         workbook, csv_path, "partnerships", Partnership
        #     ).ingest()
    print("done!")
