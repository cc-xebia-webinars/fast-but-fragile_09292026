"""Tests the assistant wrote alongside refunds.py.

They're reasonable, and they'd pass on a machine that ignored deprecation warnings.
The gate treats deprecations as errors, which is where the first surprise comes from.
"""

import sqlite3
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from shop.refunds import (
    find_refunds,
    is_refundable,
    median_refund,
    new_refund_reference,
    refund_amount,
)

NOW = datetime(2026, 9, 29, 15, 0, tzinfo=UTC)


def test_recent_purchase_is_refundable() -> None:
    assert is_refundable(NOW - timedelta(days=3), now=NOW)


def test_old_purchase_is_not_refundable() -> None:
    assert not is_refundable(NOW - timedelta(days=45), now=NOW)


def test_refund_window_defaults_to_the_current_time() -> None:
    assert is_refundable(datetime.now(UTC) - timedelta(days=1))


def test_restocking_fee_is_deducted() -> None:
    assert refund_amount(Decimal("100.00")) == Decimal("85.00")


def test_reference_numbers_have_the_expected_shape() -> None:
    reference = new_refund_reference()
    assert reference.startswith("RF-")
    assert len(reference) == 9


def test_median_refund_for_the_dashboard() -> None:
    assert median_refund([Decimal("10.00"), Decimal("20.00"), Decimal("90.00")]) == Decimal("20.00")


@pytest.fixture
def conn() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(":memory:")
    yield connection
    connection.close()


def test_find_refunds_for_an_order(conn: sqlite3.Connection) -> None:
    conn.execute("CREATE TABLE refunds (id INTEGER PRIMARY KEY, order_id TEXT, amount TEXT)")
    conn.executemany(
        "INSERT INTO refunds (order_id, amount) VALUES (?, ?)",
        [("A-100", "85.00"), ("A-100", "12.75"), ("B-200", "40.00")],
    )
    assert [refund_id for refund_id, _ in find_refunds(conn, "A-100")] == [1, 2]
