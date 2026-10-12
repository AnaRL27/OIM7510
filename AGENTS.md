# Rules for my agent

I am a graduate business student learning Python and SQL for analytics. Treat me as a careful beginner who has never worked as a developer.

## How to help me

- Write the simplest code that works. Prefer plain `for` loops, `if`, lists and dicts. Use a comprehension, a lambda or a class only when I ask for one.
- Explain, without being asked, any line I could not have written myself, in one sentence.
- If your code skips rows, converts values or changes a type, tell me how many rows it affected.
- When my request is ambiguous, ask me one question before you write anything.
- Keep answers short. Leave out the preamble, the emoji headings and the summary of what you just did.

## Notebooks

- My notebooks are marimo files. A name can be defined in only one cell. A cell shows its last expression, so end a chart cell with the chart and never call `plt.show()`.
- I start marimo from the repository folder with `uv run marimo edit`.

## Environment

- This repository is a uv project, and uv manages everything in it: `uv add` and `uv remove` for packages, `uv run` to run anything, `uv sync` to rebuild the environment on another computer. Never use `pip`, `conda`, `python -m venv` or `uv pip install`, because none of them records the change in `pyproject.toml`.
- Every copy of this repository has a `pyproject.toml` in its root folder. If you cannot find it, I have opened the wrong folder: stop and tell me. Do not create one, and do not install anywhere else.
- My repository is public. Never put an API key, a password or personal data into a committed file. Keys go in `.env`.

## Checking work

- Before you tell me something works, run it and show me what it printed. A marimo notebook runs top to bottom with `uv run python <notebook>.py`.

## Commits

- Write a short summary line (50 characters or fewer, imperative mood, e.g. "Add gain calculation to notebook 3"), a blank line, then a body explaining what changed and why.
- List notable changes as bullet points when a commit touches more than one thing.
- Never mention an AI tool or assistant in the commit message.
