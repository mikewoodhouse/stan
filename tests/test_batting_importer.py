from datetime import date

from app.loaders.xl.match_batting_importer import MatchBatting


def test_match_batting():
    entry = MatchBatting.from_string("Abc D", "6/4/b/0/1", date.today(), "banana")
    assert entry.name == "Abc D"
    assert entry.position == 6
    assert entry.runs == 4
    assert entry.out
    assert entry.how_out == "b"
    assert not entry.captain
    assert not entry.kept_wicket
    assert entry.caught == 0
    assert entry.caught_wkt == 0
    assert entry.stumped == 0
    assert entry.fours == 1
    assert entry.sixes == 0


def test_empty_cell():
    entry = MatchBatting.from_string("Abc D", "", date.today(), "banana")
    assert entry == MatchBatting(name="Abc D", match_date=date.today(), opp="banana")
