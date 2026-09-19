# Demo 4: Standards First with Spec Kit and Copilot

The first three demos caught problems after the code was written. This one moves quality to the start. We'll write the team's standards down where GitHub Copilot actually reads them, then use GitHub's Spec Kit to take a new feature from constitution to specification, plan, tasks, and implementation, and finish by running the same quality gate from Demo 3.

**Time:** about 20 minutes, most of it waiting on Copilot, which is a good time for questions  
**Agenda topic:** establishing team standards and prompts that bias AI toward quality from the start

## Before You Start

Install these tools first:

- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.5 or later. uv downloads Python 3.14 for you.
- [Visual Studio Code](https://code.visualstudio.com/) with [GitHub Copilot set up](https://code.visualstudio.com/docs/copilot/setup): select the Copilot icon in the Status Bar, choose **Use AI Features**, and sign in with GitHub.
- [Spec Kit](https://github.com/github/spec-kit), GitHub's toolkit for spec-driven development. Install its `specify` command with uv:

  ```
  uv tool install specify-cli
  specify version
  ```

  To pin a release, use `uv tool install specify-cli==<version>`, or install from a Git tag with `--from git+https://github.com/github/spec-kit.git@vX.Y.Z`.

  `specify init` scaffolds from templates bundled inside the CLI, so after it's installed it works offline.

Open this folder as its own VS Code window and install the dependencies before the session:

```
code demos/04-standards-first
uv sync
```

Opening the demo folder on its own matters here. Copilot reads `.github/copilot-instructions.md` from the root of the workspace, so this folder has to be the workspace root.

## What's in the Folder

| Path | Purpose |
|------|---------|
| `.github/copilot-instructions.md` | Team standards that Copilot applies to every chat, agent session, and code review |
| `.github/instructions/python-tests.instructions.md` | Extra rules that apply only to files under `tests/` |
| `.github/prompts/harden-tests.prompt.md` | A reusable prompt file, run in chat as `/harden-tests` |
| `prompts/constitution.md` | The input for `/speckit-constitution` |
| `prompts/feature-loyalty-points.md` | The input for `/speckit-specify` |
| `prompts/plan.md` | The input for `/speckit-plan` |
| `src/shop/`, `tests/`, `tools/gate.py` | The codebase from the end of Demo 3, passing the gate |

## Presentation Trail

### Step 1: Write the standards down where Copilot reads them

Open `.github/copilot-instructions.md`. This is plain Markdown that Copilot adds to every request in this workspace. Walk through the sections. The correctness rules are the fixes from Demos 1 and 3 turned into standing instructions: `Decimal` for money, aware UTC datetimes, parameterized SQL, `secrets`, no blanket excepts, and no guessing at APIs. The definition of done names the gate and forbids suppressions. Point out that none of this is new policy. It's what the team already agreed in reviews, written down once so Copilot doesn't have to rediscover it.

Open `.github/instructions/python-tests.instructions.md`. The `applyTo: "tests/**/*.py"` front matter means these rules are only added when Copilot works on test files. Scoped instructions keep the main file short.

Open `.github/prompts/harden-tests.prompt.md`. A prompt file turns a good prompt, like the one we typed by hand in Demo 2, into a team asset. In Copilot Chat, type `/harden-tests` to show that it appears as a command. You don't need to run it now. Prompt files load in sessions that use the **Local** session target. Sessions that run in the Agent Host, such as the **Copilot** and **Claude** targets, don't load prompt files, and VS Code recommends agent skills for anything that has to work everywhere. Spec Kit's commands, which we'll add in a moment, are agent skills.

To prove Copilot is using the instructions, choose the **Ask** role and ask:

```
What rules should I follow when adding a new function that handles money in this project?
```

The answer should cite `Decimal`, half-up rounding, and the gate. Expand **References** under the response to show that `copilot-instructions.md` was used.

### Step 2: Initialize Spec Kit

In the VS Code terminal, from this folder:

```
specify init --here --force --integration copilot --script ps
```

Use `--script sh` instead of `--script ps` on macOS or Linux. The `--force` flag is needed because the folder isn't empty. Spec Kit only adds files and doesn't touch the ones already here.

Show what it created:

- `.specify/memory/constitution.md` is a template for the project's principles.
- `.specify/templates/` holds the templates for specs, plans, and tasks.
- `.github/skills/speckit-*` holds the commands Copilot now offers: `/speckit-constitution`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`, and `/speckit-converge`, plus optional ones such as `/speckit-clarify`, `/speckit-analyze`, and `/speckit-checklist`.

Agent skills are enabled by default (`chat.useAgentSkills`). If the new commands don't show up in chat, reload the window with **Developer: Reload Window**.

### Step 3: Establish the constitution

Open `prompts/constitution.md` and read the five principles aloud. They match the Copilot instructions, but they play a different role. The instructions shape every individual response, while the constitution governs the whole spec-driven workflow, and every plan must check itself against it.

In the Chat view, with the **Local** session target and the **Agent** role, type `/speckit-constitution` followed by everything below the line in `prompts/constitution.md`, and send it. When it finishes, open `.specify/memory/constitution.md` to show the filled-in principles.

### Step 4: Specify the feature

Open `prompts/feature-loyalty-points.md`. The requirement is deliberately full of boundaries: whole dollars only, blocks of 100, a 50% cap, not applying to shipping or tax, and an inclusive 365-day expiry. These are the details an assistant working from a one-line prompt tends to get wrong.

Type `/speckit-specify` followed by the text below the line, and send it. Spec Kit creates `specs/001-.../spec.md`. Open it and show the user scenarios and acceptance criteria. Look for the boundaries: because the constitution requires every boundary to appear in an acceptance scenario, they should be written out explicitly. If anything is marked `[NEEDS CLARIFICATION]`, that's Spec Kit refusing to guess, which is exactly the behavior we want. You can resolve it with `/speckit-clarify`.

### Step 5: Plan and break into tasks

Type `/speckit-plan` followed by the text below the line in `prompts/plan.md`, and send it. Open the generated `plan.md` and find the constitution check, where the plan confirms it follows each principle. Then run:

```
/speckit-tasks
```

Open `tasks.md`. The tasks are small, ordered, and usually test-first, which makes the implementation easy to review in pieces.

### Step 6: Implement, converge, and run the gate

```
/speckit-implement
```

This step takes the longest, so it's a good time to take questions. When it finishes, run:

```
/speckit-converge
```

Converge compares the code with the spec and plan and appends any remaining work to `tasks.md`. Spec Kit's recommended loop is to repeat implement and converge until converge reports that the feature has converged. If you're short on time, one pass is enough to show the idea. Then run the gate yourself rather than trusting the summary:

```
uv run python tools/gate.py
```

Open the new `src/shop/loyalty.py` and `tests/test_loyalty.py`. Check for the standards: `Decimal` money, aware datetimes, parametrized boundary tests for 99, 100, and 101 points and for the 365th day. Compare this with Demo 1, where a one-line prompt produced code with six defects. The model is the same. What changed is the context we gave it.

If the gate fails, paste the output back into chat as in Demo 3. Point out that the standards didn't remove the need for the safety net. They made it catch less.

## Reset

Spec Kit and Copilot add files to this folder. To return it to its starting state, run these from this folder:

```
git clean -fd .
git restore .
```

`git clean -fd` removes untracked files and folders such as `.specify/`, `.github/skills/`, `specs/`, and the new loyalty files. It keeps `.venv`, because ignored files are only removed with `-x`.
