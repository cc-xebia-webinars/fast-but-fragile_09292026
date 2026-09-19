# Demo 1: The "Looks Right" Problem

AI-generated code is usually tidy, well named, and documented, which makes it easy to trust. In this demo we'll look at a pricing module that an assistant wrote from a reasonable prompt. Its tests pass and its coverage is 97%, yet it has six real defects, one for each way AI code tends to break. We'll use GitHub Copilot to review it and then run a set of edge-case probes to see what a quick read-through missed.

**Time:** about 15 minutes  
**Agenda topics:** why AI shifts the quality conversation, and where AI code tends to break

## Before You Start

Install these tools first:

- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.5 or later. uv downloads Python 3.14 for you, so a separate Python install isn't required.
- [Visual Studio Code](https://code.visualstudio.com/) with [GitHub Copilot set up](https://code.visualstudio.com/docs/copilot/setup): select the Copilot icon in the Status Bar, choose **Use AI Features**, and sign in with GitHub. Copilot Free is enough for this demo.

Open this folder as its own VS Code window, so Copilot only sees this demo's files:

```
code demos/01-looks-right
```

Then install the dependencies. Do this before the session, while you're online. After that the demo runs offline, apart from Copilot itself.

```
uv sync
```

## What's in the Folder

| Path | Purpose |
|------|---------|
| `src/shop/pricing.py` | The AI-generated module, with the prompt that produced it in the docstring |
| `tests/test_pricing.py` | The happy-path tests that came with it |
| `probes/test_probes.py` | Edge-case probes, one or more per failure mode |
| `reference/pricing.py` | A corrected version, with each fix marked `FIX:` |
| `conftest.py` | Adds a `--impl` switch so the probes can run against either version |

## Presentation Trail

### Step 1: Read the requirement, then the code

Open `src/shop/pricing.py`. Start with the docstring, which holds the prompt the assistant was given. Point out the details that matter: "orders of $100 **or more**", "8.25% tax", "expire in 30 days", "look up a customer's past orders by email", and "95th percentile".

Then scroll through the code. It reads well: there's a dataclass for line items, constants at the top, type hints, and a docstring on every function. Ask the audience whether they'd approve this in a pull request. Most people would, and that's the "looks right" problem. The code is plausible enough that reviewers relax.

### Step 2: Run the tests the assistant wrote

Open `tests/test_pricing.py`. The tests check a normal subtotal, a small order with no discount, a $200 order with a discount, tax on a $40 order, the coupon code format, the expiry window, and an order lookup. Each one is reasonable. Now run them with coverage:

```
uv run pytest --cov=shop --cov-report=term-missing
```

All seven tests pass with 97% coverage. The only line that never ran is line 70, inside `p95_order_value`. Keep that line number in mind for later.

### Step 3: Ask Copilot to review it

In the Chat view, choose the **Ask** role, make sure `pricing.py` is attached as context (it's attached automatically when the file is open in the editor), and send:

```
Review this module against the requirement in its docstring. List any
correctness, security, or maintainability problems, most serious first.
```

Copilot will usually catch several issues, often the SQL built from an f-string and the float money, and sometimes the others. Its answer varies from run to run, and that's the teaching point: an AI reviewer is a helpful extra pair of eyes, but it isn't a guarantee. Note which issues it found, so you can compare against the probes in the next step.

You can also highlight `apply_bulk_discount`, right-click, and choose **Generate Code > Review** to see inline review comments in the editor. Menu labels move between VS Code releases, so check this one in your installed version before the session.

### Step 4: Run the probes

Open `probes/test_probes.py`. Each probe asks one question the happy-path tests skipped, and each is labeled with the failure mode it targets. Run them against the generated module:

```
uv run pytest probes
```

All seven probes fail. Walk through each failure using the fixes in `reference/pricing.py`:

| Probe | Failure mode | What went wrong |
|-------|--------------|-----------------|
| `test_exactly_100_dollars_gets_the_bulk_discount` | Subtle logic error | `>` instead of `>=`, so a $100.00 order misses the discount the requirement promised |
| `test_half_cent_totals_round_up` | Subtle logic error | Floats can't store 10.825 exactly, and `round()` uses banker's rounding, so the customer is charged $10.82 instead of $10.83 |
| `test_coupon_expiry_is_timezone_aware` | Outdated pattern | `datetime.utcnow()` is deprecated in Python 3.12 and later, and it returns a naive datetime that's easy to compare against local time by mistake |
| `test_p95_order_value_works` | Hallucinated API | `statistics.quantile` doesn't exist (the real function is `quantiles`). This is line 70, the one coverage told us never ran |
| `test_email_lookup_resists_sql_injection` | Silent security gap | The email is pasted into SQL, so `nobody' OR '1'='1` returns every customer's orders |
| `test_coupon_codes_are_not_reproducible_from_a_seed` (x2) | Silent security gap | `random` is predictable, and anyone who can reproduce its state can generate valid coupons |

Draw attention to how quiet these failures are. None of them crash the happy path. The hallucinated API only breaks on the dashboard path nobody tested, and the security gaps behave perfectly for honest input.

### Step 5: Confirm the fixes

Open `reference/pricing.py` and compare it with the generated version. Each change is marked with a `FIX:` comment explaining why. Then run the same probes against it:

```
uv run pytest probes --impl reference
```

All seven pass. Close by pointing out that every one of these issues is findable, just not by the tests the assistant wrote for its own code. The rest of the webinar covers how to catch them systematically.

## Reset

Nothing in this demo modifies the tracked files. If you edited anything during the session, restore it with:

```
git restore .
```
