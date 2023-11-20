from datetime import date

import pytest

from app.types import MatchBatting

# Test IDs for parametrization
HAPPY_PATH_ID = "happy_path"
EDGE_CASE_ID = "edge_case"
ERROR_CASE_ID = "error_case"

# Test data for parametrization
test_data = [
    # Happy path tests with various realistic test values
    (
        HAPPY_PATH_ID,
        "Mike",
        "1/50/c/2/4.2",
        date(2021, 5, 15),
        "Opponent",
        1,
        50,
        True,
        "c",
        False,
        False,
        2,
        0,
        0,
        4,
        2,
    ),
    (
        HAPPY_PATH_ID,
        "Alex",
        "2/100/b*/0/6.0",
        date(2021, 5, 15),
        "Opponent",
        2,
        100,
        True,
        "b",
        True,
        False,
        0,
        0,
        0,
        6,
        0,
    ),
    (
        HAPPY_PATH_ID,
        "Sam",
        "3/0/lb+/1.1/0.0",
        date(2021, 5, 15),
        "Opponent",
        3,
        0,
        True,
        "lb",
        False,
        True,
        0,
        1,
        1,
        0,
        0,
    ),
    # Edge case tests
    (
        EDGE_CASE_ID,
        "Chris",
        "4/0/dnb/0.0/0.0",
        date(2021, 5, 15),
        "Opponent",
        4,
        0,
        False,
        "dnb",
        False,
        False,
        0,
        0,
        0,
        0,
        0,
    ),
    (
        EDGE_CASE_ID,
        "Jordan",
        "5/23/st*+/1.2/2.1",
        date(2021, 5, 15),
        "Opponent",
        5,
        23,
        True,
        "st",
        True,
        True,
        0,
        1,
        2,
        2,
        1,
    ),
    # Error case tests
    (
        ERROR_CASE_ID,
        "Taylor",
        "",
        date(2021, 5, 15),
        "Opponent",
        0,
        0,
        False,
        "",
        False,
        False,
        0,
        0,
        0,
        0,
        0,
    ),
    (
        ERROR_CASE_ID,
        "Morgan",
        "invalid/entry/format",
        date(2021, 5, 15),
        "Opponent",
        0,
        0,
        False,
        "",
        False,
        False,
        0,
        0,
        0,
        0,
        0,
    ),
]


@pytest.mark.parametrize(
    "test_id,name,entry,match_date,opp,position,runs,out,how_out,captain,kept_wicket,caught,caught_wkt,stumped,fours,sixes",
    test_data,
    ids=[test_id for test_id, *_ in test_data],
)
def test_match_batting_from_string(
    test_id,
    name,
    entry,
    match_date,
    opp,
    position,
    runs,
    out,
    how_out,
    captain,
    kept_wicket,
    caught,
    caught_wkt,
    stumped,
    fours,
    sixes,
):
    # Act
    result = MatchBatting.from_string(name, entry, match_date, opp)

    # Assert
    assert result.name == name, "name"
    assert result.match_date == match_date, "match_date"
    assert result.opp == opp, "opp"
    assert result.position == position, "pos"
    assert result.runs == runs, "runs"
    assert result.out == out, "was out"
    assert result.how_out == how_out, "how out"
    assert result.captain == captain, "captain"
    assert result.kept_wicket == kept_wicket, "kept wkt"
    assert result.caught == caught, "caught"
    assert result.caught_wkt == caught_wkt, "caught_wkt"
    assert result.stumped == stumped, "stumped"
    assert result.fours == fours, "fours"
    assert result.sixes == sixes, "sixes"
