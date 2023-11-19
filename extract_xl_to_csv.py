from pathlib import Path

from app.loaders.xl.excel_loader import load_matches


def clear_csv_files(path: Path) -> None:
    for filepath in path.glob("*.csv"):
        print(f"deleting {filepath}")
        filepath.unlink()


if __name__ == "__main__":
    path = Path("./data/xldata")
    clear_csv_files(path)
    for filepath in path.glob("*.xlsm"):
        print(filepath)
        load_matches(filepath)
