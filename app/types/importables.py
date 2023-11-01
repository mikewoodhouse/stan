from dataclass_csv import accept_whitespaces

from app.types import HundredPlus, Player

"""
Some classes need to have `accept_whitespaces` set, but that wrapper appears
to change the type, which really upsets mypy. So for importing from CSV, using
these versions, where defined, seems to handle the situation (relatively) cleanly.
"""


@accept_whitespaces
class PlayerImport(Player):
    pass


@accept_whitespaces
class HundredPlusImport(HundredPlus):
    pass
