from app.loaders.batting_importer import MatchBatting


def test_match_batting():
    entry = MatchBatting.from_worksheet("Abc D", "6/4/b/0/1")
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
    entry = MatchBatting.from_worksheet("Abc D", "")
    assert entry == MatchBatting(name="Abc D")
