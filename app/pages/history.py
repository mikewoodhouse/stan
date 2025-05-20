from nicegui import ui

from app.types import HistoryPage
from app.utils import page_header

from .sidebar_menu import sidebar


def show_history():
    page_header("Club History")

    sidebar()

    pages = HistoryPage.pages()

    with ui.splitter(limits=(0, 400)).props("model-value=1000 unit='px'") as splitter:
        with splitter.before:
            with ui.tabs().props("vertical") as tabs:
                for page in pages:
                    ui.tab(page.title)

        with splitter.after:
            with ui.tab_panels(tabs).classes("w-full"):
                for page in pages:
                    with ui.tab_panel(page.title):
                        ui.markdown(content=page.content)

    # with ui.row():
    # with ui.column():
    #     for page in pages:
    #         ui.label(page.title)
    # with ui.column():
    #     with ui.card():
    #         ui.markdown(pages[0].content)
