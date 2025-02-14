def balls_to_overs(balls: int) -> str:
    overs, balls = divmod(balls, 6)
    return f"{overs}.{balls}"


def player_name(firstname: str, initial: str, surname: str) -> str:
    if forename := firstname or initial:
        return f"{surname}, {forename}"
    return surname
