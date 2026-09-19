"""Behavior-focused tests for pricing.py, carried over from Demo 2."""

from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from shop.pricing import (
    LineItem,
    add_tax,
    apply_bulk_discount,
    order_total,
    shipping_cost,
    subtotal,
)

prices = st.decimals(min_value="0.01", max_value="500.00", places=2)
quantities = st.integers(min_value=1, max_value=10)


def test_subtotal_multiplies_price_by_quantity_and_adds_lines() -> None:
    items = [LineItem("MUG", Decimal("12.50"), 2), LineItem("TEE", Decimal("20.00"), 1)]
    assert subtotal(items) == Decimal("45.00")


@pytest.mark.parametrize(
    ("amount", "expected"),
    [("99.99", "99.99"), ("100.00", "90.0000"), ("100.01", "90.0090")],
)
def test_bulk_discount_boundary(amount: str, expected: str) -> None:
    assert apply_bulk_discount(Decimal(amount)) == Decimal(expected)


@pytest.mark.parametrize(
    ("amount", "expected"),
    [("49.99", "5.99"), ("50.00", "0.00"), ("50.01", "0.00")],
)
def test_shipping_boundary(amount: str, expected: str) -> None:
    assert shipping_cost(Decimal(amount)) == Decimal(expected)


@pytest.mark.parametrize(
    ("amount", "expected"),
    [("10.00", "10.83"), ("100.00", "108.25"), ("0.00", "0.00")],
)
def test_add_tax_rounds_half_up(amount: str, expected: str) -> None:
    assert add_tax(Decimal(amount)) == Decimal(expected)


def test_order_total_for_a_bulk_order_ships_free() -> None:
    items = [LineItem("DESK-LAMP", Decimal("100.00"), 1)]
    assert order_total(items) == Decimal("97.43")


@given(st.lists(st.tuples(prices, quantities), min_size=1, max_size=5))
def test_total_is_never_less_than_discounted_goods(lines: list[tuple[Decimal, int]]) -> None:
    items = [LineItem(f"SKU{i}", price, qty) for i, (price, qty) in enumerate(lines)]
    discounted = apply_bulk_discount(subtotal(items))
    assert order_total(items) >= discounted.quantize(Decimal("0.01"))
