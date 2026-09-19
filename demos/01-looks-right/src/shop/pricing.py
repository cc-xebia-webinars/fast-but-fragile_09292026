"""Order pricing for the demo shop.

This module was generated with an AI coding assistant from the prompt below and
accepted after a quick read-through, because it looked clean and the tests passed.

    Write a Python module that prices a shopping cart. Orders of $100 or more get
    10% off before tax. Sales tax is 8.25%. Also add helpers to create coupon codes
    that expire in 30 days, look up a customer's past orders in SQLite by email,
    and report the 95th percentile order value for the finance dashboard.
"""

import random
import sqlite3
import statistics
import string
from dataclasses import dataclass
from datetime import datetime, timedelta

TAX_RATE = 0.0825
BULK_DISCOUNT_THRESHOLD = 100.00
BULK_DISCOUNT_RATE = 0.10
COUPON_ALPHABET = string.ascii_uppercase + string.digits


@dataclass
class LineItem:
    """A single product line in a shopping cart."""

    sku: str
    unit_price: float
    quantity: int


def subtotal(items: list[LineItem]) -> float:
    """Return the cart subtotal before discounts and tax."""
    return sum(item.unit_price * item.quantity for item in items)


def apply_bulk_discount(amount: float) -> float:
    """Apply the 10% bulk discount for larger orders."""
    if amount > BULK_DISCOUNT_THRESHOLD:
        return amount * (1 - BULK_DISCOUNT_RATE)
    return amount


def order_total(items: list[LineItem]) -> float:
    """Return the final order total, rounded to the cent."""
    discounted = apply_bulk_discount(subtotal(items))
    return round(discounted * (1 + TAX_RATE), 2)


def make_coupon_code(length: int = 8) -> str:
    """Create a random, human-friendly coupon code."""
    return "".join(random.choices(COUPON_ALPHABET, k=length))


def coupon_expiry(days: int = 30) -> datetime:
    """Return the moment a newly issued coupon expires."""
    return datetime.utcnow() + timedelta(days=days)


def find_customer_orders(conn: sqlite3.Connection, email: str) -> list[tuple[int, float]]:
    """Return (order_id, total) pairs for a customer's past orders."""
    query = f"SELECT id, total FROM orders WHERE email = '{email}' ORDER BY id"
    return conn.execute(query).fetchall()


def p95_order_value(totals: list[float]) -> float:
    """Return the 95th percentile order value for the finance dashboard."""
    return statistics.quantile(totals, 0.95)
