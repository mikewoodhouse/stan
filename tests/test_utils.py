import pytest

from app.utils import coldef, extract_sql_parameters, table_link_slot_html


def test_table_link_slot_html():
    expected = (
        r"""<td :props="props"><a :href="'/players/' + props.row.player_id + '/' + props.row.year" """
        r"""class='nicegui-link'>{{props.row.year}}</a></td>"""
    )
    assert table_link_slot_html("year", "players", ["player_id", "year"]) == expected


@pytest.mark.parametrize(
    "result,expected",
    [
        (coldef("name"), {"name": "name", "label": "Name", "field": "name"}),
        (coldef("name", label="Banana"), {"name": "name", "label": "Banana", "field": "name"}),
        (coldef("name", name="other_name"), {"name": "other_name", "label": "Name", "field": "name"}),
        (coldef("name", align="left"), {"name": "name", "label": "Name", "field": "name", "align": "left"}),
        (
            coldef("name", decimals=2),
            {"name": "name", "label": "Name", "field": "name", ":format": "value => value ? value.toFixed(2) : ''"},
        ),
        (coldef("name", sortable=True), {"name": "name", "label": "Name", "field": "name", "sortable": True}),
    ],
)
def test_coldef(result, expected):
    assert result == expected


def test_sql_query():
    assert (
        extract_sql_parameters("SELECT * FROM players WHERE id = ':id' AND name = ':name'")
        == "SELECT * FROM players WHERE id = :id AND name = :name"
    )
