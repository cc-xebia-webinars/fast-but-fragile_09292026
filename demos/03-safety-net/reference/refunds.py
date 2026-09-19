"""Refund handling for the demo shop, after the gate findings and the review were addressed.

This is the fallback for the live fix. To use it:

    Copy-Item reference/refunds.py src/shop/refunds.py     # PowerShell
    cp reference/refunds.py src/shop/refunds.py            # macOS / Linux
"""

import secrets
import sqlite3
import statistics
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

REFUND_WINDOW = timedelta(days=30)
RESTOCKING_FEE_RATE = Decimal("0.15")
CENT = Decimal("0.01")


def is_refundable(purchased_at: datetime, now: datetime | None = None) -> bool:
    """Return True when a purchase is still inside the refund window."""
    # Aware UTC timestamps on both sides, so a naive local time can't sneak in and
    # shift the window by the server's UTC offset.
    now = now or datetime.now(UTC)
    # The requirement says the 30th day still counts, which makes the window inclusive.
    # The gates can't know that; only a reviewer reading the requirement will catch it.
    return now - purchased_at <= REFUND_WINDOW


def refund_amount(price: Decimal) -> Decimal:
    """Return the amount refunded after the restocking fee."""
    # round() on a Decimal follows the decimal context, which defaults to banker's
    # rounding. Finance rounds half a cent up, so say so explicitly.
    return (price - price * RESTOCKING_FEE_RATE).quantize(CENT, rounding=ROUND_HALF_UP)


def new_refund_reference() -> str:
    """Create a reference number for support staff and the customer."""
    # Reference numbers authorize money moving, so they must not be guessable.
    return f"RF-{secrets.randbelow(900000) + 100000}"


def find_refunds(conn: sqlite3.Connection, order_id: str) -> list[tuple[int, str]]:
    """Return (refund_id, amount) rows for an order."""
    # No blanket except here: a broken query should fail loudly, not look like
    # "this order has no refunds".
    rows: list[tuple[int, str]] = conn.execute(
        "SELECT id, amount FROM refunds WHERE order_id = ? ORDER BY id", (order_id,)
    ).fetchall()
    return rows


def median_refund(amounts: list[Decimal]) -> Decimal:
    """Return the median refund amount for the support dashboard."""
    return statistics.median(amounts)
