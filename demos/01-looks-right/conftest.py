"""Shared fixtures, plus a switch that lets the probes run against either the
AI-generated module or the corrected one."""

import importlib
import sqlite3
from collections.abc import Iterator

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    # A command-line switch keeps the demo to one command on every shell, which is
    # friendlier on stage than setting environment variables in PowerShell vs. bash.
    parser.addoption(
        "--impl",
        choices=["generated", "reference"],
        default="generated",
        help="Which pricing module the probes should exercise.",
    )


@pytest.fixture
def pricing(request: pytest.FixtureRequest):
    use_reference = request.config.getoption("--impl") == "reference"
    return importlib.import_module("reference.pricing" if use_reference else "shop.pricing")


@pytest.fixture
def conn() -> Iterator[sqlite3.Connection]:
    """An in-memory orders table with two customers, closed after each test."""
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, email TEXT, total REAL)")
    connection.executemany(
        "INSERT INTO orders (email, total) VALUES (?, ?)",
        [("ana@example.com", 43.30), ("ana@example.com", 12.00), ("raj@example.com", 99.00)],
    )
    yield connection
    connection.close()
