def balls_to_overs(balls: int) -> str:
    overs, balls = divmod(balls, 6)
    return f"{overs}.{balls}"
