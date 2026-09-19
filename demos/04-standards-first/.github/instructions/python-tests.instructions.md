---
description: Conventions for writing and changing pytest tests in the shop project.
applyTo: "tests/**/*.py"
---

# Test Conventions

- Name tests after the behavior they check, for example `test_refund_window_includes_the_30th_day`.
- Build money values from strings, `Decimal("10.00")`, so the test data is exact.
- Pin "now" with a fixed, timezone-aware `datetime` instead of calling the clock, so tests don't depend on when they run.
- Use fixtures for shared setup such as SQLite connections, and close what you open.
- Each test should fail for exactly one reason. If a test needs a paragraph to explain, split it.
- Don't write tests whose only purpose is raising coverage. A test that can't fail isn't doing any work.
