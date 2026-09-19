Paste everything below the line after `/speckit-plan` in Copilot Chat.

---

Implement loyalty points as a new module, src/shop/loyalty.py, using only the standard library. Keep the points ledger in memory as a list of dataclass entries (customer ID, points, earned-at timestamp), so no database changes are needed. Reuse apply_bulk_discount from src/shop/pricing.py to compute the discounted goods amount. Add tests in tests/test_loyalty.py. The quality gate in tools/gate.py must pass at the end.
