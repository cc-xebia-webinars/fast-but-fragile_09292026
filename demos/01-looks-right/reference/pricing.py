"""Corrected order pricing, kept for side-by-side comparison with src/shop/pricing.py.

Each fix is marked with a FIX comment so it's easy to walk through during the demo.
"""

import secrets
import sqlite3
import statistics
import string
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

# FIX: money is Decimal end to end. Binary floats can't represent most cent values,
# so rounding lands on the wrong cent for amounts like 10.825.
TAX_RATE = Decimal("0.0825")
BULK_DISCOUNT_THRESHOLD = Decimal("100.00")
BULK_DISCOUNT_RATE = Decimal("0.10")
CENT = Decimal("0.01")
COUPON_ALPHABET = string.ascii_uppercase + string.digits


@dataclass
class LineItem:
    """A single product line in a shopping cart."""

    sku: str
    unit_price: Decimal
    quantity: int


def subtotal(items: list[LineItem]) -> Decimal:
    """Return the cart subtotal before discounts and tax."""
    return sum((item.unit_price * item.quantity for item in items), Decimal("0"))


def apply_bulk_discount(amount: Decimal) -> Decimal:
    """Apply the 10% bulk discount for larger orders."""
    # FIX: the requirement says "$100 or more", so exactly $100 has to qualify.
    if amount >= BULK_DISCOUNT_THRESHOLD:
        return amount * (1 - BULK_DISCOUNT_RATE)
    return amount


def order_total(items: list[LineItem]) -> Decimal:
    """Return the final order total, rounded to the cent."""
    discounted = apply_bulk_discount(subtotal(items))
    # FIX: finance rounds half a cent up; Python's round() uses banker's rounding.
    return (discounted * (1 + TAX_RATE)).quantize(CENT, rounding=ROUND_HALF_UP)


def make_coupon_code(length: int = 8) -> str:
    """Create a random, human-friendly coupon code."""
    # FIX: coupons are worth money, so they need an unpredictable source.
    # The random module is seeded and can be reproduced by anyone who learns its state.
    return "".join(secrets.choice(COUPON_ALPHABET) for _ in range(length))


def coupon_expiry(days: int = 30) -> datetime:
    """Return the moment a newly issued coupon expires."""
    # FIX: utcnow() is deprecated and returns a naive datetime that's easy to compare
    # against local time by mistake. An aware UTC timestamp removes the ambiguity.
    return datetime.now(UTC) + timedelta(days=days)


def find_customer_orders(conn: sqlite3.Connection, email: str) -> list[tuple[int, Decimal]]:
    """Return (order_id, total) pairs for a customer's past orders."""
    # FIX: a parameterized query lets SQLite treat the email strictly as data.
    rows = conn.execute(
        "SELECT id, total FROM orders WHERE email = ? ORDER BY id", (email,)
    ).fetchall()
    return [(order_id, Decimal(str(total))) for order_id, total in rows]


def p95_order_value(totals: list[Decimal]) -> Decimal:
    """Return the 95th percentile order value for the finance dashboard."""
    # FIX: statistics.quantile doesn't exist. quantiles() with n=20 returns the
    # 5th, 10th, ... 95th percentile cut points, so the last one is the 95th.
    return statistics.quantiles(totals, n=20)[-1]
