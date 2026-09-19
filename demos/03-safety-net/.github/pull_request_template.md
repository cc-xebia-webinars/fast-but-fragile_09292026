## What changed and why

<!-- A sentence or two in your own words. If you can't explain it, it isn't ready to merge. -->

## How much of this was AI-assisted?

- [ ] None
- [ ] Some (suggestions or snippets I reworked)
- [ ] Most (generated code I reviewed and adjusted)

## Reviewer checklist for AI-assisted changes

- [ ] `uv run python tools/gate.py` passes locally and in CI
- [ ] No rules were disabled, and no `# noqa` or `# type: ignore` comments were added to get there
- [ ] Every new library call exists in the version we pin (check the docs, not the suggestion)
- [ ] Boundaries in the requirement (inclusive vs. exclusive, empty input, zero) have tests
- [ ] Money uses `Decimal`, times are timezone-aware, SQL is parameterized, secrets use `secrets`
- [ ] New tests would fail if the code were wrong, not just run it
- [ ] Any new dependency is intentional and shows up in `uv.lock`

See `REVIEW_CHECKLIST.md` for the reasoning behind each item.
