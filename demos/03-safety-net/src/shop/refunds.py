"""Refund handling for the demo shop.

Generated with an AI coding assistant from the prompt below. It's staged here,
uncommitted in spirit, so the quality gate can have a look before a human does.

    Add refund support. Customers can get a refund within 30 days of purchase,
    and the 30th day still counts. We keep a 15% restocking fee. Every refund
    needs a reference number. Support staff need to look up the refunds for an
    order and see the median refund amount.
"""

import random
import sqlite3
import statistics
from datetime import datetime, timedelta
from decimal import Decimal

REFUND_WINDOW = timedelta(days=30)
RESTOCKING_FEE_RATE = Decimal("0.15")


def is_refundable(purchased_at, now=None):
    """Return True when a purchase is still inside the refund window."""
    now = now or datetime.utcnow()
    return now - purchased_at < REFUND_WINDOW


def refund_amount(price: Decimal) -> Decimal:
    """Return the amount refunded after the restocking fee."""
    return round(price - price * RESTOCKING_FEE_RATE, 2)


def new_refund_reference():
    """Create a reference number for support staff and the customer."""
    return "RF-" + str(random.randint(100000, 999999))


def find_refunds(conn: sqlite3.Connection, order_id: str):
    """Return (refund_id, amount) rows for an order."""
    try:
        query = f"SELECT id, amount FROM refunds WHERE order_id = '{order_id}' ORDER BY id"
        return conn.execute(query).fetchall()
    except Exception:
        return []


def median_refund(amounts: list[Decimal]) -> Decimal:
    """Return the median refund amount for the support dashboard."""
    return statistics.quantile(amounts, 0.5)
