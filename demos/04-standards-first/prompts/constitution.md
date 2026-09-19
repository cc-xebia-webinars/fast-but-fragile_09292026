Paste everything below the line after `/speckit-constitution` in Copilot Chat.

---

Create the constitution for the shop project, a small Python 3.14 codebase managed with uv. Use these principles.

1. Correctness before speed. Money is always Decimal and rounds half up to the cent. Datetimes are timezone-aware UTC. Every boundary stated in a specification (inclusive or exclusive, zero, empty input) must appear in an acceptance scenario and in a test.
2. Secure by default. SQL is always parameterized. Values a customer could guess to gain money, such as codes, tokens, and reference numbers, come from the secrets module. Errors are never silently swallowed.
3. Tests prove behavior. Tests assert exact values and would fail if the logic were wrong. Boundaries are tested just below, at, and just above the threshold. Coverage is a floor of 90%, not a goal, and tests written only to raise coverage aren't accepted.
4. The quality gate is the definition of done. `uv run python tools/gate.py` (ruff, mypy in strict mode, and pytest with coverage) must pass. Suppressing a finding with noqa, type: ignore, or a relaxed rule is not an acceptable fix.
5. Simple and reviewable. Prefer the standard library. New dependencies need a stated reason. Keep each change small enough for a human to review in one sitting, and only use APIs that exist in the pinned versions.

Governance: amendments require a pull request that explains the reason and updates any affected templates. The plan for every feature must include a constitution check against these five principles.
