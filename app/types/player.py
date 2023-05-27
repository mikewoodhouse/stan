from dataclasses import dataclass


@dataclass(kw_only=True)
class Player:
    id: int = -1
    code: str
    surname: str
    active: bool
    initial: str = ""
    firstname: str = ""

    @property
    def name(self) -> str:
        if forename := self.firstname or self.initial:
            return f"{self.surname}, {forename}"
        return self.surname
