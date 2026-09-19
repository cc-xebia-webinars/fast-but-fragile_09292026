"""The local quality gate: the same checks CI runs, in one command.

    uv run python tools/gate.py

Every check runs even when an earlier one fails. With AI-generated code you want
the whole list of findings in one pass, so you can hand all of it back to the
assistant at once instead of fixing one tool's complaints at a time.
"""

import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

# Each check targets a failure mode that AI-generated code is prone to.
CHECKS: list[tuple[str, str, list[str]]] = [
    (
        "Lint and security rules",
        "outdated patterns, risky calls, SQL built from strings",
        ["ruff", "check", "src", "tests"],
    ),
    (
        "Strict type check",
        "hallucinated APIs, missing types, wrong return values",
        ["mypy"],
    ),
    (
        "Tests, deprecations, coverage",
        "behavior, deprecated calls, untested code",
        ["pytest", "--cov=shop", "--cov-report=term-missing", "--cov-fail-under=90"],
    ),
]


def main() -> int:
    results: list[tuple[str, bool]] = []
    for title, catches, command in CHECKS:
        print(f"\n=== {title}  (catches: {catches})")
        print(f"$ {' '.join(command)}", flush=True)
        # Running each tool through the current interpreter guarantees it's the
        # version pinned in uv.lock, not whatever happens to be on the PATH.
        completed = subprocess.run([sys.executable, "-m", *command], cwd=PROJECT)
        results.append((title, completed.returncode == 0))

    print("\n=== Quality gate summary")
    for title, passed in results:
        print(f"  {'PASS' if passed else 'FAIL'}  {title}")

    all_passed = all(passed for _, passed in results)
    print("\nGate passed." if all_passed else "\nGate failed. Fix the findings; don't suppress them.")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
