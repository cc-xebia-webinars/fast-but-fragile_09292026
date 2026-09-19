# Demo 2: Coverage Isn't Confidence

When a team starts leaning on AI assistants, test coverage is often the first number management asks about. Assistants are very good at raising it, and that's the problem. In this demo, the pricing code is correct and the coverage is 100%, yet the tests would miss nearly every bug we could introduce. We'll measure test strength with mutation testing, then use GitHub Copilot to write tests that actually protect the code.

**Time:** about 15 minutes  
**Agenda topics:** the quality dimensions that matter, and metrics worth tracking vs. vanity metrics

## Before You Start

Install these tools first:

- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.5 or later. uv downloads Python 3.14 for you.
- [Visual Studio Code](https://code.visualstudio.com/) with [GitHub Copilot set up](https://code.visualstudio.com/docs/copilot/setup): select the Copilot icon in the Status Bar, choose **Use AI Features**, and sign in with GitHub. The demo uses the **Agent** role. Copilot Free includes it, but with a limited monthly allowance of GitHub AI Credits, so a paid plan is more comfortable for a live session.

Open this folder as its own VS Code window and install the dependencies before the session:

```
code demos/02-coverage-isnt-confidence
uv sync
```

## What's in the Folder

| Path | Purpose |
|------|---------|
| `src/shop/pricing.py` | Correct pricing code: bulk discount, free-shipping threshold, tax with half-up rounding |
| `tests/test_pricing.py` | Tests that run every line and check almost nothing |
| `tools/mutation_check.py` | A small mutation tester written for this demo |
| `reference/test_pricing_strong.py` | A strong suite to fall back on if the live Copilot run goes sideways |

## Presentation Trail

### Step 1: Look at the code under test

Open `src/shop/pricing.py`. This is the Demo 1 module with the bugs fixed, plus a shipping rule. Money is `Decimal`, the discount starts at exactly $100.00, shipping is free from $50.00, and `add_tax` rounds half a cent up. Point out that there are three thresholds and one rounding rule. Those four details are where a real bug would hide.

### Step 2: Show the vanity metric

Open `tests/test_pricing.py`. Every function gets called, and both branches of each `if` run. Read a few assertions out loud: `is not None`, `>= 0`, `> 0`, `isinstance`. These are the tests you tend to get when you ask an assistant to "get coverage to 100%". Now run them:

```
uv run pytest --cov=shop --cov-report=term-missing
```

Coverage is 100%. On a dashboard, this module looks finished.

### Step 3: Measure test strength with mutation testing

Open `tools/mutation_check.py` and walk through the idea rather than every line. The script makes one small, plausible mistake at a time in `pricing.py`: it flips `>=` to `>`, swaps `+` and `-`, nudges a constant like `"100.00"` to `"100.01"`, or changes the rounding mode. For each mistake (a *mutant*) it runs the tests. If the tests fail, the mutant is *killed*. If they still pass, the mutant *survived*, which means that bug could ship without anyone noticing. The script works on a temporary copy, so the real source is never changed.

```
uv run python tools/mutation_check.py
```

Expect 2 of 17 mutants killed, about 12%. The only two caught are the tax mutants, because `add_tax(...) > Decimal("10.00")` is the one assertion that notices when tax goes the wrong way. Walk through a few survivors. `GtE -> Gt` on the discount line is the exact bug from Demo 1, and these tests with 100% coverage would let it straight back in.

### Step 4: Ask Copilot for tests that matter

In the Chat view, choose the **Agent** role and send this prompt. Notice that it names the rules and asks for boundaries, instead of asking for coverage:

```
Rewrite tests/test_pricing.py so the tests would catch real bugs in
src/shop/pricing.py. For every threshold, test values just below, at, and
just above it with pytest.mark.parametrize, and assert exact Decimal values.
Check that tax rounds half up (10.00 should become 10.83). Add one Hypothesis
property test for a rule that holds for every cart. Don't change pricing.py.
Run the tests with uv run pytest when you're done.
```

Hypothesis is already a dev dependency, so Copilot doesn't need to install anything. While Copilot works, talk about what makes a test strong: it pins exact values, it tests boundaries, and it fails for exactly one reason.

### Step 5: Measure again

```
uv run python tools/mutation_check.py
```

The score should jump. If Copilot's tests leave survivors, that's a useful moment: paste the surviving lines back into chat and ask Copilot to add a test that kills each one. If the live run doesn't go well, use the prepared suite instead:

```
uv run python tools/mutation_check.py --tests reference/test_pricing_strong.py
```

That suite kills 16 of 17 mutants. The one survivor changes `CENT = Decimal("0.01")` to `Decimal("0.02")`, and it survives because `quantize()` only uses the exponent of its argument, so the program behaves exactly the same. That's called an *equivalent mutant*. It's a good reminder that mutation score, like any metric, needs a human to interpret it, and 100% isn't always achievable or meaningful.

### Step 6: Tie it back to metrics

Summarize what the two numbers told us. Coverage answered "did this line run?", and it was 100% both times. Mutation score answered "would the tests notice a bug?", and it went from 12% to over 90%. That's the difference between a vanity metric and a metric worth tracking.

## Reset

Restore the weak tests so the demo can be run again:

```
git restore tests/test_pricing.py
```
