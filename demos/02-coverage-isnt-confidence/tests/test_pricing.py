"""Tests that execute every line of pricing.py and still prove very little.

This is what you often get when you ask an assistant to "add tests to reach 100%
coverage". Every function runs, so the coverage report is perfect, but most
assertions only check that something came back.
"""

from decimal import Decimal

from shop.pricing import (
    LineItem,
    add_tax,
    apply_bulk_discount,
    order_total,
    shipping_cost,
    subtotal,
)


def test_subtotal_returns_decimal():
    items = [LineItem("MUG", Decimal("12.00"), 2)]
    assert isinstance(subtotal(items), Decimal)


def test_bulk_discount_runs_for_small_and_large_orders():
    assert apply_bulk_discount(Decimal("20.00")) is not None
    assert apply_bulk_discount(Decimal("250.00")) is not None


def test_shipping_cost_runs_for_both_branches():
    assert shipping_cost(Decimal("10.00")) >= 0
    assert shipping_cost(Decimal("75.00")) >= 0


def test_add_tax_makes_the_amount_bigger():
    assert add_tax(Decimal("10.00")) > Decimal("10.00")


def test_order_total_is_positive():
    items = [LineItem("TEE", Decimal("20.00"), 3)]
    assert order_total(items) > 0
