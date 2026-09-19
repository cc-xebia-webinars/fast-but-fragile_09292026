# Reviewing AI-Assisted Changes

The quality gate handles what a machine can check reliably. This checklist covers what it can't, so reviewers can spend their attention where it actually matters instead of re-checking formatting and imports.

## Let the gate do its job first

Don't start a human review until `uv run python tools/gate.py` passes. If a reviewer finds a style or lint issue, that's a sign the gate needs a new rule, not that the reviewer should keep an eye out for it next time.

## Read the requirement, then the code

Assistants write code that matches the shape of a request, and the details are where they drift. Before reading the diff, reread the ticket and note every boundary and rule in it, for example "the 30th day still counts" or "orders of $100 or more". Then find each one in the code and in a test. The refund-window bug in this demo passes every automated check, and the only way to find it is to compare the code against the sentence in the requirement.

## Question anything unfamiliar

If a function, parameter, or flag is new to you, look it up in the documentation for the version we pin. Hallucinated APIs look exactly like real ones, and they're most common on paths that don't get exercised often, like dashboards, admin tools, and error handling.

## Look for silent failure

Blanket `except` blocks, default values that hide missing data, and early returns of empty lists all turn an error into wrong data. Ask what happens when the database is down or the input is malformed, and whether anyone would find out.

## Watch for suppressions

A new `# noqa`, `# type: ignore`, or a relaxed rule in `pyproject.toml` deserves the same scrutiny as new code. When an assistant is asked to "make the gate pass", suppressing the finding is often the shortest route, so ask for a fix instead and check that you got one.

## Check that the tests would fail

Coverage only tells you the code ran. For each new test, ask whether it would fail if the logic were wrong. When in doubt, flip a comparison in the code and rerun the test, which is exactly what the mutation check in Demo 2 automates.

## Keep changes reviewable

Large AI-generated diffs are hard to review well. If a change is too big to reason about in one sitting, ask for it to be split. Reviewers who are overwhelmed tend to approve, and that's where the "looks right" problem comes from.
