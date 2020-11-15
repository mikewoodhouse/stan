from models.season_record import SeasonRecord
from models.season import Season


def test_season_creation():
    season = Season(1949, 12, 4, 7, 1, 0, 0, 12)
    assert season.year == 1949
    assert season.max_games == 12


def test_season_retrieval():
    for year in range(1949, 1952):
        season = Season.get(year)
        assert season.year == year


def test_all_season_records():
    recs = SeasonRecord.all()
    assert len(recs) > 0
    assert recs[0].year == 1949
    season_1949 = {rec.club: rec for rec in recs if rec.year == 1949}
    assert len(season_1949) == 2


def test_season_record_for_year():
    res = SeasonRecord.get(1949)
    assert len(res) == 2
    assert res[0].highestdate.year == 1949


def test_season_record_has_balls():
    r = SeasonRecord(0, '', 0, 0, 0, 0, None, '', 0, 0, None, '', 0, 0, 0, 0, 0, 0)
    assert not r.has_balls
    r = SeasonRecord(0, '', 0, 0, 0, 0, None, '', 0, 0, None, '', 0, 0, 0, 0, 0, 1)
    assert r.has_balls
