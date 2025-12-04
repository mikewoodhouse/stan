from nicegui import ui

from stan.types import HistoryPage
from stan.utils import page_header

from .sidebar_menu import sidebar


def show_history():
    page_header("Club History")

    sidebar()

    pages = HistoryPage.pages()
    print(f"History pages: {[p.title for p in pages]}")

    with ui.splitter(limits=(0, 10)).props("model-value=150 unit='px'") as splitter:
        with splitter.before:
            with ui.tabs().props("vertical") as tabs:
                for page in pages:
                    ui.tab(page.title)

        with splitter.after:
            with ui.tab_panels(tabs).classes("w-full"):
                for page in pages:
                    with ui.tab_panel(page.title):
                        ui.markdown(content=page.content)
