"""Unit tests for the engine module."""

from atlas_coder.core.engine import hello

def test_hello():
    """Tests the hello function."""
    assert hello() == "Hello, World!"
