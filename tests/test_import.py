"""Tests for importing top modules."""

import pytest

def test_import() -> None:
  """Import aioh should work."""
  try:
    import aioh # noqa F541
  except ImportError:
    pytest.fail("Module could not be loaded")
