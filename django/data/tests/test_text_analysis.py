"""Test text analysis."""

import pytest

from data import text_analysis


def test_text_preparation():
    """Test text preparation."""
    text = '- 3 km MINU, ja coop! 3,5  % 3 * 0,5l kg. % plus+ l! 7 tk leib- tk sai a b c g 4 km'
    expected_text = '3km minu 3.5% 3x0.5l 1kg plus 1l 7tk leib tk sai 1g 4km'
    assert ' '.join(text_analysis.prepare(text)) == expected_text


def test_empty_text_preparation():
    """Test empty text preparation."""
    text = ' x     !  \n   a   '
    assert len(text_analysis.prepare(text)) == 0
