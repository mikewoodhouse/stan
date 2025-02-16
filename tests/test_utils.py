from app.utils import table_link_slot_html


def test_table_link_slot_html():
    expected = (
        r"""<td :props="props"><a :href="'/players/' + props.row.player_id + '/' + props.row.year" """
        r"""class='nicegui-link'>{{props.row.year}}</a></td>"""
    )
    assert table_link_slot_html("year", "players", ["player_id", "year"]) == expected
