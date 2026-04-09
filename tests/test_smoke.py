"""Smoke test so the template passes CI out of the box."""

from medmcp_template import __version__


def test_version_is_string() -> None:
    """The package exposes a ``__version__`` string."""
    assert isinstance(__version__, str)
    assert __version__
