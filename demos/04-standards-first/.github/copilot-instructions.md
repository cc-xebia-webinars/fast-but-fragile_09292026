# Team Standards for the Shop Codebase

These instructions apply to every Copilot chat, agent session, and code review in this repository. They record the decisions our team has already made, so Copilot doesn't have to guess them and reviewers don't have to repeat them.

## Project context

- Python 3.14, managed with `uv`. Run anything with `uv run ...`, and add dependencies with `uv add`, never `pip install`.
- Source lives in `src/shop`, tests live in `tests`, and the quality gate lives in `tools/gate.py`.
- The standard library is preferred. Ask before adding a third-party dependency.

## Correctness rules that aren't negotiable

- Money is always `decimal.Decimal`, never `float`. Round to the cent with `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`, not `round()`.
- Datetimes are timezone-aware UTC: `datetime.now(UTC)`. Never use `datetime.utcnow()` or naive datetimes.
- SQL uses parameter placeholders (`?`). Never build SQL with f-strings, `%`, `+`, or `.format()`.
- Anything a customer could guess to gain value, such as coupon codes, reference numbers, or tokens, comes from the `secrets` module, not `random`.
- Don't catch `Exception` broadly. Let unexpected errors surface instead of returning empty results.
- Only call library functions you're certain exist in Python 3.14. If you're unsure, say so instead of guessing.

## Requirements and tests

- Before writing code, restate every boundary in the requirement (inclusive or exclusive, empty input, zero) and cover each one with a test.
- Write tests that would fail if the logic were wrong. Assert exact values, not just types or "not None".
- Put boundary cases in `pytest.mark.parametrize` tables with values just below, at, and just above each threshold.
- Consider a Hypothesis property test when a rule should hold for every input.

## Definition of done

- `uv run python tools/gate.py` passes: ruff, mypy in strict mode, and pytest with coverage of 90% or higher.
- Never make the gate pass by adding `# noqa`, `# type: ignore`, or relaxing a rule in `pyproject.toml`. Fix the underlying issue, or explain why you can't.
- Keep changes small and focused so a human can review them in one sitting.
- Every public function has type hints and a one-line docstring. Comments explain why, not what.
