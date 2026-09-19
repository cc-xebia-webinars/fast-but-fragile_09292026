"""Edge-case probes that ask the questions the happy-path tests skipped.

Run them against the AI-generated module first, then with --impl reference:

    uv run pytest probes
    uv run pytest probes --impl reference
"""

import random
from decimal import Decimal

import pytest


def money(pricing, amount: str):
    # The generated module works in floats and the reference works in Decimal,
    # so each probe builds its inputs in whatever type the module expects.
    return Decimal(amount) if pricing.__name__.startswith("reference") else float(amount)


def as_cents(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"))


# Subtle logic error: the requirement says "$100 or more".
def test_exactly_100_dollars_gets_the_bulk_discount(pricing):
    items = [pricing.LineItem("DESK-LAMP", money(pricing, "100.00"), 1)]
    assert as_cents(pricing.order_total(items)) == Decimal("97.43")


# Subtle logic error: float money plus banker's rounding lands on the wrong cent.
def test_half_cent_totals_round_up(pricing):
    items = [pricing.LineItem("NOTEBOOK", money(pricing, "10.00"), 1)]
    assert as_cents(pricing.order_total(items)) == Decimal("10.83")


# Outdated pattern: naive datetimes from the deprecated utcnow().
def test_coupon_expiry_is_timezone_aware(pricing):
    assert pricing.coupon_expiry().tzinfo is not None


# Hallucinated API: the rarely used dashboard path has never actually run.
def test_p95_order_value_works(pricing):
    totals = [money(pricing, str(n)) for n in range(1, 101)]
    assert 94 <= float(pricing.p95_order_value(totals)) <= 97


# Silent security gap: user input is pasted straight into SQL.
def test_email_lookup_resists_sql_injection(pricing, conn):
    assert pricing.find_customer_orders(conn, "nobody' OR '1'='1") == []


# Silent security gap: coupons worth money come from a predictable generator.
@pytest.mark.parametrize("seed", [7, 42])
def test_coupon_codes_are_not_reproducible_from_a_seed(pricing, seed):
    random.seed(seed)
    first = pricing.make_coupon_code()
    random.seed(seed)
    second = pricing.make_coupon_code()
    assert first != second
