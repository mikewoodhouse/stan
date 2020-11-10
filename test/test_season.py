from models.season import Season


def test_season_creation():
    season = Season(1949, 12, 4, 7, 1, 0, 0, 12)
    assert season.year == 1949
    assert season.max_games == 12


def test_season_retrieval():
    for year in range(1949, 1952):
        season = Season.get(year)
        assert season.year == year
