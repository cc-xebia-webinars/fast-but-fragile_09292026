"""Order pricing for the demo shop, with the Demo 1 bugs already fixed.

The code here is correct. What Demo 2 questions is whether the tests would notice
if it stopped being correct.
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

# Money stays in Decimal so every rounding decision is explicit and matches finance.
TAX_RATE = Decimal("0.0825")
BULK_DISCOUNT_THRESHOLD = Decimal("100.00")
BULK_DISCOUNT_RATE = Decimal("0.10")
FREE_SHIPPING_THRESHOLD = Decimal("50.00")
FLAT_SHIPPING = Decimal("5.99")
CENT = Decimal("0.01")


@dataclass(frozen=True)
class LineItem:
    """A single product line in a shopping cart."""

    sku: str
    unit_price: Decimal
    quantity: int


def subtotal(items: list[LineItem]) -> Decimal:
    """Return the cart subtotal before discounts, shipping, and tax."""
    return sum((item.unit_price * item.quantity for item in items), Decimal("0"))


def apply_bulk_discount(amount: Decimal) -> Decimal:
    """Take 10% off orders of $100 or more."""
    if amount >= BULK_DISCOUNT_THRESHOLD:
        return amount * (1 - BULK_DISCOUNT_RATE)
    return amount


def shipping_cost(amount: Decimal) -> Decimal:
    """Ship free at $50 or more; otherwise charge a flat rate."""
    if amount >= FREE_SHIPPING_THRESHOLD:
        return Decimal("0.00")
    return FLAT_SHIPPING


def add_tax(amount: Decimal) -> Decimal:
    """Add sales tax and round half a cent up, the way finance reconciles it."""
    return (amount * (1 + TAX_RATE)).quantize(CENT, rounding=ROUND_HALF_UP)


def order_total(items: list[LineItem]) -> Decimal:
    """Return what the customer pays: discounted goods plus shipping, then tax."""
    discounted = apply_bulk_discount(subtotal(items))
    return add_tax(discounted + shipping_cost(discounted))
