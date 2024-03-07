from __future__ import annotations

from app.loaders.xl.importer_base import XlImporter
from app.types import Partnership


class XlPartnershipsImporter(XlImporter):
    def ingest(self) -> None:
        if "Partnerships" not in self.wb.sheetnames:
            return
        sheet = self.wb["Partnerships"]
        partnerships: list[Partnership] = []
        for row in sheet.iter_rows(min_col=2, max_col=12, values_only=True):
            values = list(row)
            if values[0]:
                print(values)
        print("retrieved", len(partnerships), "partnerships")
