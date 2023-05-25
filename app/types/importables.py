from dataclass_csv import accept_whitespaces

from app.types.classes import HundredPlus, Player


@accept_whitespaces
class PlayerImport(Player):
    pass


@accept_whitespaces
class HundredPlusImport(HundredPlus):
    pass
