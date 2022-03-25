"""Test text analysis."""

import pytest

from data import text_analysis


def test_text_preparation():
    """Test text preparation."""
    text = '- MINU, ja coop! 3,5  % 3 * 0,5l kg. % plus+ l! leib- sai a b c g'
    expected_text = 'minu 3.5% 3x0.5l 1kg plus 1l leib sai 1g'
    assert ' '.join(text_analysis.prepare(text)[0]) == expected_text
