"""A stronger suite for the same module, used as a fallback if the live Copilot run
goes sideways. Run the mutation check against it with:

    uv run python tools/mutation_check.py --tests reference/test_pricing_strong.py
"""

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


def test_subtotal_multiplies_price_by_quantity_and_adds_lines():
    items = [LineItem("MUG", Decimal("12.50"), 2), LineItem("TEE", Decimal("20.00"), 1)]
    assert subtotal(items) == Decimal("45.00")


def test_empty_cart_has_zero_subtotal():
    assert subtotal([]) == Decimal("0")


# Boundaries are where assistants most often slip, so each one gets an exact check
# just below, at, and above the threshold.
@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        ("99.99", "99.99"),
        ("100.00", "90.0000"),
        ("100.01", "90.0090"),
    ],
)
def test_bulk_discount_boundary(amount, expected):
    assert apply_bulk_discount(Decimal(amount)) == Decimal(expected)


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        ("49.99", "5.99"),
        ("50.00", "0.00"),
        ("50.01", "0.00"),
    ],
)
def test_shipping_boundary(amount, expected):
    assert shipping_cost(Decimal(amount)) == Decimal(expected)


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        ("10.00", "10.83"),  # 10.825 rounds half up, not to the even cent
        ("100.00", "108.25"),
        ("0.00", "0.00"),
    ],
)
def test_add_tax_rounds_half_up(amount, expected):
    assert add_tax(Decimal(amount)) == Decimal(expected)


def test_order_total_for_a_small_order_includes_shipping():
    items = [LineItem("NOTEBOOK", Decimal("10.00"), 1)]
    # (10.00 + 5.99) * 1.0825 = 17.309...
    assert order_total(items) == Decimal("17.31")


def test_order_total_for_a_bulk_order_ships_free():
    items = [LineItem("DESK-LAMP", Decimal("100.00"), 1)]
    # 100.00 - 10% = 90.00, free shipping, then tax: 97.425 -> 97.43
    assert order_total(items) == Decimal("97.43")


# A property test states a rule that must hold for every cart, and Hypothesis goes
# looking for the cart that breaks it.
@given(st.lists(st.tuples(prices, quantities), min_size=1, max_size=5))
def test_total_is_never_less_than_discounted_goods(lines):
    items = [LineItem(f"SKU{i}", price, qty) for i, (price, qty) in enumerate(lines)]
    discounted = apply_bulk_discount(subtotal(items))
    assert order_total(items) >= discounted.quantize(Decimal("0.01"))
    assert order_total(items).as_tuple().exponent == -2
