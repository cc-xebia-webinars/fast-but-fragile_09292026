"""Happy-path tests, the kind an assistant usually writes alongside its own code.

They pass, and they cover most of the module. Notice what they don't ask about:
boundaries, rounding, hostile input, or the code path nobody calls in the demo.
"""

from datetime import timedelta

from shop.pricing import (
    COUPON_ALPHABET,
    LineItem,
    apply_bulk_discount,
    coupon_expiry,
    find_customer_orders,
    make_coupon_code,
    order_total,
    subtotal,
)


def test_subtotal_adds_up_line_items():
    items = [LineItem("MUG", 12.00, 2), LineItem("TEE", 20.00, 1)]
    assert subtotal(items) == 44.00


def test_small_orders_get_no_discount():
    assert apply_bulk_discount(40.00) == 40.00


def test_large_orders_get_ten_percent_off():
    assert apply_bulk_discount(200.00) == 180.00


def test_order_total_includes_tax():
    items = [LineItem("MUG", 20.00, 2)]
    assert order_total(items) == 43.30


def test_coupon_code_has_expected_shape():
    code = make_coupon_code()
    assert len(code) == 8
    assert all(ch in COUPON_ALPHABET for ch in code)


def test_coupon_expires_after_thirty_days():
    assert coupon_expiry(30) - coupon_expiry(0) >= timedelta(days=29, hours=23)


def test_find_customer_orders_returns_their_orders(conn):
    orders = find_customer_orders(conn, "ana@example.com")
    assert [order_id for order_id, _ in orders] == [1, 2]
