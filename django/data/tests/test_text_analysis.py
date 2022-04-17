"""Test text analysis."""

import pytest
import pytest_dependency

from data import text_analysis as ta


@pytest.mark.dependency()
def test_text_preparation():
    """Test text preparation."""
    text = '- 3 km MINU, ja coop! 3,5  % 3 * 0,5l kg. % plus+ l! 7 tk leib- tk sai a b c g 4 km'
    expected_text = '3km minu 3.5% 3x0.5l 1kg plus 1l 7tk leib tk sai 1g 4km'
    assert ' '.join(ta.prepare(text)) == expected_text


def test_empty_text_preparation():
    """Test empty text preparation."""
    text = ' x     !  \n   a   '
    assert len(ta.prepare(text)) == 0


@pytest.mark.dependency(depends=['test_text_preparation'])
def test_quantity_parsing():
    """Test quantity parsing."""
    text = ta.prepare('token 3 kg 5,5% 1.234% 5l!')
    expected = ((3000, 'g'), (5.5, '%'), (1.234, '%'), (5, 'l'))
    _, actual = ta.parse_quantity(text)
    for q in expected:
        assert ta.Quantity(*q) in actual
