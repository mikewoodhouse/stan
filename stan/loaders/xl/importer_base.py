from pathlib import Path

from dataclass_csv import DataclassWriter
from openpyxl import Workbook


class XlImporter:
    def __init__(
        self, workbook: Workbook, csv_path: Path, csv_filename: str, klass: type
    ) -> None:
        self.wb = workbook
        self.csv_path = csv_path
        self.csv_filename = csv_filename
        self.klass = klass

    def write_csv(self, items: list) -> None:
        output_path = self.csv_path / f"{self.csv_filename}.csv"

        print(f"writing to {output_path}")

        skip_header = output_path.exists()

        with output_path.open("a") as f:
            writer = DataclassWriter(f, items, self.klass)
            writer.write(skip_header=skip_header)
