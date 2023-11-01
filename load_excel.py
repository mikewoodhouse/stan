from pathlib import Path

from app.loaders.xl.excel_loader import load_matches

if __name__ == "__main__":
    path = Path("./xldata")
    for filepath in path.glob("*.xlsm"):
        load_matches(str(filepath))
