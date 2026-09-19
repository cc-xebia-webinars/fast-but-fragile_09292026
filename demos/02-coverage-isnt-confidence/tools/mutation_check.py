"""A small mutation tester for the demo.

Coverage tells you which lines ran. Mutation testing tells you whether the tests
would notice if those lines were wrong. This script makes one small change at a
time to src/shop/pricing.py (a "mutant"), runs the tests, and reports whether the
tests failed (the mutant was killed) or still passed (the mutant survived).

It's deliberately tiny so it can be read on stage. For real projects, look at
mutmut or cosmic-ray. mutmut relies on fork(), so it won't run on Windows.

Usage:
    uv run python tools/mutation_check.py
    uv run python tools/mutation_check.py --tests reference/test_pricing_strong.py
"""

import argparse
import ast
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
TARGET = Path("src/shop/pricing.py")

# Each swap is a mistake a person or an assistant could plausibly make.
COMPARE_SWAPS: dict[type[ast.cmpop], type[ast.cmpop]] = {
    ast.GtE: ast.Gt,
    ast.Gt: ast.GtE,
    ast.LtE: ast.Lt,
    ast.Lt: ast.LtE,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
}
BINOP_SWAPS: dict[type[ast.operator], type[ast.operator]] = {
    ast.Add: ast.Sub,
    ast.Sub: ast.Add,
    ast.Mult: ast.Div,
    ast.Div: ast.Mult,
}
NAME_SWAPS = {"ROUND_HALF_UP": "ROUND_HALF_EVEN"}


@dataclass
class Mutant:
    line: int
    description: str
    source: str


def nudge(text: str) -> str | None:
    """Shift a numeric string literal by one unit in its last decimal place."""
    try:
        value = Decimal(text)
    except InvalidOperation:
        return None
    step = Decimal(1).scaleb(value.as_tuple().exponent)
    return str(value + step)


def find_mutants(source: str) -> list[Mutant]:
    tree = ast.parse(source)
    mutants: list[Mutant] = []

    # Every candidate node is re-located by position in a fresh tree, so each
    # mutant carries exactly one change.
    for index, node in enumerate(ast.walk(tree)):
        change: str | None = None
        fresh = ast.parse(source)
        twin = list(ast.walk(fresh))[index]

        if isinstance(node, ast.Compare) and type(node.ops[0]) in COMPARE_SWAPS:
            new_op = COMPARE_SWAPS[type(node.ops[0])]
            twin.ops[0] = new_op()
            change = f"{type(node.ops[0]).__name__} -> {new_op.__name__}"
        elif isinstance(node, ast.BinOp) and type(node.op) in BINOP_SWAPS:
            new_op = BINOP_SWAPS[type(node.op)]
            twin.op = new_op()
            change = f"{type(node.op).__name__} -> {new_op.__name__}"
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and nudge(node.value):
            new_value = nudge(node.value)
            twin.value = new_value
            change = f'"{node.value}" -> "{new_value}"'
        elif isinstance(node, ast.Name) and node.id in NAME_SWAPS:
            # decimal's rounding modes are plain strings, so a string constant stands in
            # for the other mode without having to add an import to the mutant.
            replacement = NAME_SWAPS[node.id]
            twin.__class__ = ast.Constant
            twin.value = replacement
            twin.kind = None
            change = f"{node.id} -> {replacement}"

        if change:
            mutants.append(Mutant(node.lineno, change, ast.unparse(fresh)))
    return mutants


def run_tests(workdir: Path, tests: str) -> bool:
    """Return True when the test run passes, which means the mutant survived."""
    # Mutants are often the same size as the original and written within the same
    # second, so a cached .pyc from the previous mutant could be reused. Turning off
    # bytecode caching guarantees every run imports the mutant actually on disk.
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", "--no-cov", tests],
        cwd=workdir,
        env=env,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tests", default="tests", help="Test file or folder to run against each mutant.")
    args = parser.parse_args()

    source = (PROJECT / TARGET).read_text(encoding="utf-8")
    mutants = find_mutants(source)

    with tempfile.TemporaryDirectory() as tmp:
        # Work on a copy so a crash or Ctrl+C can never leave a mutant in the real source.
        workdir = Path(tmp) / "project"
        shutil.copytree(PROJECT, workdir, ignore=shutil.ignore_patterns(".venv", ".git", "__pycache__"))

        if not run_tests(workdir, args.tests):
            print("The tests fail on the unmodified code, so there's nothing to measure yet.")
            return 1

        survivors: list[Mutant] = []
        for mutant in mutants:
            (workdir / TARGET).write_text(mutant.source, encoding="utf-8")
            survived = run_tests(workdir, args.tests)
            status = "SURVIVED" if survived else "killed"
            print(f"  line {mutant.line:>3}  {mutant.description:<40} {status}")
            if survived:
                survivors.append(mutant)

    killed = len(mutants) - len(survivors)
    score = 100 * killed / len(mutants) if mutants else 100.0
    print(f"\nMutation score: {killed}/{len(mutants)} killed ({score:.0f}%)")
    if survivors:
        print("Each surviving mutant is a bug your tests would have let through.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
