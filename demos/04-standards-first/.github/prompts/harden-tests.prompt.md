---
description: Strengthen the tests for a module until they would catch real bugs.
agent: agent
argument-hint: Path to the module, for example src/shop/pricing.py
---

Strengthen the tests for the module I name (default to the file that's open in the editor).

1. Read the module and list every rule it enforces: thresholds, rounding, time windows, error cases.
2. For each rule, check the existing tests in `tests/` and tell me which rules aren't pinned by an exact assertion.
3. Add tests for the gaps. Use `pytest.mark.parametrize` with values just below, at, and just above every boundary, and assert exact `Decimal` values.
4. Where a rule should hold for every input, add one Hypothesis property test.
5. Don't change the module under test. If a new test fails, stop and show me the failure, because it may be a real bug.
6. Run `uv run python tools/gate.py` and report the result.
