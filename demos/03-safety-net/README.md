# Demo 3: Automated Gates and the Copilot Review Loop

Human reviewers can't keep up with the volume of code an assistant produces, and they shouldn't have to check things a tool can check. In this demo, an assistant has just written a refunds module. We'll run a single-command quality gate that combines linting, security rules, strict typing, deprecation checks, and coverage, and map each finding to the failure modes from Demo 1. Then we'll hand the findings back to GitHub Copilot, rerun the gate, and use Copilot's code review to find the one bug no tool could see.

**Time:** about 20 minutes  
**Agenda topic:** building a review and testing safety net

## Before You Start

Install these tools first:

- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.5 or later. uv downloads Python 3.14 for you.
- [Visual Studio Code](https://code.visualstudio.com/) with [GitHub Copilot set up](https://code.visualstudio.com/docs/copilot/setup): select the Copilot icon in the Status Bar, choose **Use AI Features**, and sign in with GitHub.

Open this folder as its own VS Code window and install the dependencies before the session:

```
code demos/03-safety-net
uv sync
```

## What's in the Folder

| Path | Purpose |
|------|---------|
| `src/shop/refunds.py` | The newly generated refunds module, with the prompt in its docstring |
| `src/shop/pricing.py` | Pricing code that already passes the gate |
| `tests/` | Tests for both modules, including the ones the assistant wrote for refunds |
| `tools/gate.py` | The quality gate: ruff, mypy in strict mode, and pytest with coverage |
| `pyproject.toml` | Where the gate's rules live, with a comment explaining each rule family |
| `.github/workflows/quality-gate.yml` | The same gate in GitHub Actions, ready to copy into a real repository |
| `.github/pull_request_template.md` | A pull request checklist for AI-assisted changes |
| `REVIEW_CHECKLIST.md` | What human reviewers should focus on once the gate passes |
| `reference/refunds.py` | The fixed module, as a fallback for the live fix |

## Presentation Trail

### Step 1: Read the new code the way a busy reviewer would

Open `src/shop/refunds.py`. Read the requirement in the docstring and skim the functions: a refund window, a restocking fee, a reference number, a lookup, and a median for a dashboard. It looks like the pricing module from Demo 1 did at first glance: tidy and plausible.

### Step 2: Show how the gate is configured

Open `pyproject.toml` and scroll to `[tool.ruff.lint]`. Each rule family is there for a reason, and the comment ties it to a failure mode: `UP` and `DTZ` for outdated patterns, `S` for security, `BLE` for errors that get swallowed. Then point out `strict = true` under `[tool.mypy]` and `filterwarnings = ["error::DeprecationWarning"]` under pytest. These three settings do most of the work against AI-specific mistakes.

Open `tools/gate.py`. It runs each check even when an earlier one fails, so the whole list of findings arrives in one pass, which is exactly what you want to hand back to an assistant.

### Step 3: Run the gate

```
uv run python tools/gate.py
```

The gate fails on all three checks. Walk through the findings and match each one to its failure mode:

| Tool | Finding | Failure mode |
|------|---------|--------------|
| ruff `DTZ003` | `datetime.utcnow()` used | Outdated pattern |
| ruff `S311` | `random` used for reference numbers | Silent security gap |
| ruff `S608` | SQL built from an f-string | Silent security gap |
| ruff `BLE001` | `except Exception` returns an empty list | Silent failure |
| mypy `attr-defined` | `Module has no attribute "quantile"; maybe "quantiles"?` | Hallucinated API |
| mypy `no-untyped-def` | Three functions missing type hints | Maintainability |
| mypy `no-any-return` | `median_refund` returns an unchecked value | Hallucinated API (a side effect of the missing function) |
| pytest | `DeprecationWarning` from `utcnow()` becomes a test failure | Outdated pattern |
| pytest | `AttributeError` in `median_refund` | Hallucinated API |

Point out that mypy caught the hallucinated API without running a single line of code. In Demo 1, we only found it with a hand-written probe. The `attr-defined` check is on by default, so why strict mode? By default, mypy doesn't check the body of a function that has no type hints, and generated code often arrives without them. Strict mode requires the hints, so every function gets checked.

### Step 4: Hand the findings back to Copilot

Select all of the gate output in the terminal. In the Chat view, choose the **Agent** role, attach the terminal selection (or paste it), and send:

```
The quality gate failed on src/shop/refunds.py. Fix every finding in the
output above. Don't add noqa or type: ignore comments, and don't change
pyproject.toml. Fix the underlying code. Then run
uv run python tools/gate.py and keep going until it passes.
```

While Copilot works, talk about the instruction "don't suppress". Assistants that are asked to make a check pass will sometimes silence it instead, which is why the pull request template in `.github/pull_request_template.md` asks reviewers to look for new suppressions.

When Copilot finishes, rerun the gate yourself:

```
uv run python tools/gate.py
```

If the live fix doesn't converge in a few minutes, use the prepared version:

```
Copy-Item reference/refunds.py src/shop/refunds.py     # PowerShell
cp reference/refunds.py src/shop/refunds.py            # macOS / Linux
```

### Step 5: Find the bug the gate can't see

The gate is green, but one bug remains. Reread the requirement: "the 30th day still counts". Open `src/shop/refunds.py`, highlight `is_refundable`, right-click, and choose **Generate Code > Review**. To review every uncommitted change instead, open Source Control and select **Copilot Code Review - Uncommitted Changes** from the Changes header. Menu labels move between VS Code releases, so check them in your installed version. Alternatively, ask in chat:

```
Review is_refundable against the requirement in the module docstring.
Is the boundary on day 30 handled correctly?
```

In the original code, `now - purchased_at < REFUND_WINDOW` rejects a refund on day 30. The fix is `<=`, which `reference/refunds.py` uses. No linter or type checker can know what the business meant, so this is the part of review that still needs a person, or a reviewer with the requirement in hand. Open `REVIEW_CHECKLIST.md` and show the section "Read the requirement, then the code".

### Step 6: Put the gate in CI

Open `.github/workflows/quality-gate.yml`. It installs uv, runs `uv sync --locked`, and runs the same `tools/gate.py`, so local results and CI results always agree. Explain that `--locked` fails the build if an assistant added a dependency without updating the lock file. The file doesn't run from inside the demos folder, because GitHub only reads workflows at the repository root, so it's there to copy.

This is also a good place to mention that on a paid Copilot plan you can request Copilot as a reviewer on a pull request. (Copilot Free only includes selection review in VS Code.) It follows the repository's `.github/copilot-instructions.md`, which we'll write in Demo 4, along with any matching `.instructions.md` files, read from the pull request's head branch.

## Reset

Restore the generated module, and anything else Copilot changed in this folder, so the demo can be run again:

```
git restore .
```
