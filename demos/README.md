# Demos

These four demos follow one small codebase, a shop's pricing and refunds code, from AI-generated and fragile to guarded by automated gates and steered by team standards. Each demo is self-contained, with its own `uv` project and a pinned Python 3.14, so you can run any of them on its own. GitHub Copilot in Visual Studio Code is the AI coding tool throughout.

| # | Demo | Description | Time |
|---|------|-------------|------|
| 1 | [The "Looks Right" Problem](./01-looks-right/README.md) | A tidy, fully tested pricing module that an assistant wrote, and the six defects a quick review missed: a logic error, float money, a deprecated call, a hallucinated API, SQL injection, and predictable coupon codes. | 15 min |
| 2 | [Coverage Isn't Confidence](./02-coverage-isnt-confidence/README.md) | Tests with 100% coverage that kill only 2 of 17 mutants, and how Copilot, prompted for boundaries instead of coverage, writes tests that protect the code. | 15 min |
| 3 | [Automated Gates and the Copilot Review Loop](./03-safety-net/README.md) | A one-command quality gate (ruff, strict mypy, pytest with deprecations as errors and a coverage floor) that catches the Demo 1 failure modes, the loop of feeding its findings back to Copilot, and a CI workflow to match. | 20 min |
| 4 | [Standards First with Spec Kit and Copilot](./04-standards-first/README.md) | Copilot custom instructions, scoped instructions, and prompt files, followed by a Spec Kit workflow from constitution to spec, plan, tasks, implementation, and convergence. | 20 min |

## Getting Ready

Every demo needs these tools:

- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.5 or later
- [Visual Studio Code](https://code.visualstudio.com/) with [GitHub Copilot set up](https://code.visualstudio.com/docs/copilot/setup): select the Copilot icon in the Status Bar, choose **Use AI Features**, and sign in with GitHub.

Demo 4 also needs [Spec Kit](https://github.com/github/spec-kit):

```
uv tool install specify-cli
```

Run `uv sync` in each demo folder while you're online. After that, everything except Copilot itself runs offline.

In the Chat view, use the **Local** session target, and pick the **Ask** or **Agent** role as each demo says. Demo 4 uses a prompt file, and prompt files only load in Local sessions.

Open each demo as its own VS Code window, for example `code demos/03-safety-net`. Copilot reads custom instructions from the root of the workspace, and opening the demo folder directly keeps it focused on that demo's files.

On Windows, clone the repository to a short path such as `C:\src`. mypy ships compiled extensions whose file paths are long, and inside a deeply nested folder they can exceed the Windows path limit, which shows up as `DLL load failed ... The filename or extension is too long`. Enabling [long path support](https://learn.microsoft.com/windows/win32/fileio/maximum-file-path-limitation) also fixes it.
