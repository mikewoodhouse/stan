import pytest

from app.types.match_bowling import MatchBowling


@pytest.mark.parametrize(
    "input,expected",
    [
        ("0.1/0/0/0/0/0", (0, 1, 0, 0, 0, 0, 0)),
        ("4.3/1/20/2/5/6", (4, 3, 1, 20, 2, 5, 6)),
        ("4.3/1/20/2", (4, 3, 1, 20, 2, None, None)),
    ],
)
def test_parse_from_string(input, expected):
    o, b, m, r, w, wd, nb = expected
    obj = MatchBowling.from_string(input)

    assert obj.overs == o
    assert obj.balls == b
    assert obj.maidens == m
    assert obj.runs_conceded == r
    assert obj.wickets == w
    assert obj.wides == (wd or 0)
    assert obj.noballs == (nb or 0)
