from datetime import date

import pytest

from app.types import MatchBowling


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "test_id, name, input_str, match_date, opp, expected",
    [
        (
            "happy-1",
            "John Doe",
            "10.3/2/50/3/1/0",
            date(2021, 5, 20),
            "TeamA",
            MatchBowling(
                match_date=date(2021, 5, 20),
                opp="TeamA",
                name="John Doe",
                overs=10,
                balls=3,
                maidens=2,
                runs_conceded=50,
                wickets=3,
                wides=1,
                noballs=0,
            ),
        ),
        (
            "happy-2",
            "Jane Smith",
            "8/1/30/2",
            date(2021, 5, 21),
            "TeamB",
            MatchBowling(
                match_date=date(2021, 5, 21),
                opp="TeamB",
                name="Jane Smith",
                overs=8,
                balls=0,
                maidens=1,
                runs_conceded=30,
                wickets=2,
                wides=0,
                noballs=0,
            ),
        ),
        # Add more test cases as needed for different variations of input
    ],
)
def test_from_string_happy_path(test_id, name, input_str, match_date, opp, expected):
    # Act
    result = MatchBowling.from_string(name, input_str, match_date, opp)

    # Assert
    assert result == expected, f"Test {test_id} failed."


# Edge cases
@pytest.mark.parametrize(
    "test_id, name, input_str, match_date, opp, expected",
    [
        (
            "edge-1",
            "John Doe",
            "0/0/0/0",
            date(2021, 5, 20),
            "TeamA",
            MatchBowling(
                match_date=date(2021, 5, 20),
                opp="TeamA",
                name="John Doe",
                overs=0,
                balls=0,
                maidens=0,
                runs_conceded=0,
                wickets=0,
                wides=0,
                noballs=0,
            ),
        ),
        # Add more edge cases as needed
    ],
)
def test_from_string_edge_cases(test_id, name, input_str, match_date, opp, expected):
    # Act
    result = MatchBowling.from_string(name, input_str, match_date, opp)

    # Assert
    assert result == expected, f"Test {test_id} failed."


# Error cases
@pytest.mark.parametrize(
    "test_id, name, input_str, match_date, opp, expected_exception",
    [
        (
            "error-1",
            "John Doe",
            "10.3/2/50/3/1/not_a_number",
            date(2021, 5, 20),
            "TeamA",
            ValueError,
        ),
        (
            "error-2",
            "Jane Smith",
            "not_a_number/1/30/2",
            date(2021, 5, 21),
            "TeamB",
            ValueError,
        ),
        # Add more error cases as needed for different types of incorrect input
    ],
)
def test_from_string_error_cases(
    test_id, name, input_str, match_date, opp, expected_exception
):
    # Act & Assert
    with pytest.raises(expected_exception):
        MatchBowling.from_string(name, input_str, match_date, opp)
