from __future__ import annotations

from dataclasses import dataclass

from app.utils import project_root


@dataclass
class HistoryPage:
    filename: str
    content: str

    @property
    def title(self) -> str:
        raw_title = " ".join(self.filename.split(".")[0].split("_")[1:])
        return raw_title

    @staticmethod
    def pages() -> list[HistoryPage]:
        history_dir = project_root() / "data" / "history"
        all_pages = [
            HistoryPage(
                filename=p.name,
                content=p.read_text(),
            )
            for p in history_dir.glob("*.md")
        ]
        return sorted(all_pages, key=lambda f: f.filename)
