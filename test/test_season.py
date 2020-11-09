from models.season import Season


def test_season_creation():
    season = Season(1949, 12, 4, 7, 1, 0, 0, 12)
    assert season.year == 1949
