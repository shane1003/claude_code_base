# Project Guidelines

<!-- ================================================================== -->
<!-- SECTION A: PER-REPO — replace everything in this section when      -->
<!-- copying this template into another repository.                     -->
<!-- ================================================================== -->

ML research / experiment repository (PyTorch) managed with `uv`.
The goal is **reproducible experiments**: every result must be traceable to
a config, a seed, a data version, and a git commit.

## 1. Build, Run & Test Commands
- **Environment Sync**: `uv sync`
- **Manage Dependencies**: `uv add <pkg>` or `uv remove <pkg>` (Do NOT edit pyproject.toml manually)
- **Train**: `uv run python -m src.train --config configs/<exp>.yaml`
- **Evaluate**: `uv run python -m src.eval --config configs/<exp>.yaml --ckpt <path>`
- **Smoke Run (tiny subset, CPU)**: `uv run python -m src.train --config configs/<exp>.yaml --debug`
- **Run Tests (fast, CPU-only)**: `uv run pytest`
- **Run Single Test**: `uv run pytest tests/test_metrics.py -k "test_auc"`
- **Lint & Format**: `uv run ruff check --fix .` && `uv run ruff format .`
- **Type Checking**: `uv run mypy src/`
- **GPU Check**: `nvidia-smi`

## 2. Architecture Rules (Research)
- **Directory Layout**:
  - `configs/`: One YAML per experiment. Every hyperparameter lives here, never in code.
  - `src/data/`: Datasets, transforms, loaders. Deterministic given a seed.
  - `src/models/`: Model definitions only. No training loops, no I/O.
  - `src/train/`: Training loop, optimizer/scheduler setup, checkpointing.
  - `src/eval/`: Metrics and evaluation scripts. Pure functions, unit-tested.
  - `src/utils/`: Seeding, logging, device selection, config loading.
  - `scripts/`: One-off entry points (data prep, export). Thin wrappers over `src/`.
  - `notebooks/`: Exploration only. Never imported by `src/`. Promote reusable code to `src/`.
  - `tests/`: Fast CPU tests with tiny synthetic tensors. Never trains a real model.
  - `data/`, `weights/`, `outputs/`: Git-ignored. Referenced by path + hash/version in configs.
- **Config-Driven**: No magic numbers. Every knob (lr, batch size, threshold, paths) comes from the config.
- **Experiment Isolation**: Never edit a baseline config in place. Copy it to a new file (`configs/<date>_<name>.yaml`) and change only what the experiment tests.
- **Run Artifacts**: Each run writes to `outputs/<date>_<name>/` containing the resolved config, git hash, seed, metrics, and logs. Never overwrite a previous run.
- **Device Handling**: Select device from config/CLI via `src/utils`. Never hardcode `cuda:0`.

<!-- ================================================================== -->
<!-- SECTION B: UNIVERSAL — copy as-is to any repository.               -->
<!-- ================================================================== -->

## 3. Core Behavioral Guidelines (Karpathy Principles)
1. **Think Before Coding**: Explicitly state assumptions. Ask questions on ambiguity instead of guessing.
2. **Simplicity First**: Write minimum required code. No overengineering or speculative abstractions.
3. **Surgical Changes**: Touch ONLY code required for the task. Do NOT refactor/clean adjacent code without permission.
4. **Goal-Driven Execution**: Validate changes with the test and lint commands in Section 1 before marking complete.

## 4. Never Do
- Never edit dependency manifests by hand (use the package manager CLI).
- Never skip, delete, or weaken a failing test to make the suite pass — fix the cause or report it.
- Never commit secrets, credentials, or large binary files.
- Never run `git commit` or `git push`. The user commits and pushes manually. Instead, finish every task by overwriting `.claude/HANDOFF.md` (see `.claude/rules/handoff.md`).
- Never use `--no-verify`, `--force` push, or amend published commits unless explicitly asked.
- Never write a commit message body: commits are a single subject line only (`git commit -m "TYPE: one sentence"`, see `.claude/rules/commit.md`). No multi-line messages, no extra `-m` flags, no trailers.

<!-- Research-specific "Never Do" — these belong to Section A when porting to another case -->
- Never delete or overwrite files under `outputs/`, `data/`, or `weights/`. Experiment results cannot be regenerated for free.
- Never change a metric or evaluation function without adding/updating a known-answer test in `tests/`. A silently changed metric invalidates every past comparison.
- Never commit notebook outputs, datasets, or checkpoints. Reference them by path and hash.
- Never hardcode absolute local paths (home directories, drive letters). Paths come from config or env.
- Never start a full training run without an explicit request. Use the `--debug` smoke run to validate code changes.

## 5. Code Style & Documentation
- **Readability First**: Clear, simple, self-documenting code over clever/compact syntax.
- **Detailed Style Rules**: Read `.claude/rules/code-style.md`.
- **Type Annotations**: Mandatory explicit type hints for parameters and return types.
- **Google Docstring Style**: Apply Google-style docstrings (`Args`, `Returns`, `Raises`) for all public functions/classes/modules.
- **Comments**: Focus on explaining *WHY* a non-obvious logic was used, not *WHAT*.

## 6. Workflows
- **Task Handoff**: End every code change by overwriting `.claude/HANDOFF.md` per `.claude/rules/handoff.md` (work log, checkpoints, experiment info, commit recommendation: what / why now / type / message, detailed notes). Read user feedback left in that file before starting the next task. Use `/handoff` to refresh it on demand.
- **New Experiment**: Use the `/experiment` skill (`.claude/skills/experiment/SKILL.md`): hypothesis, config copy, smoke run, log entry.
- **Git Commit messages**: Follow `.claude/rules/commit.md` when recommending a message.
- **Refactoring**: Use the `/refactor` skill (`.claude/skills/refactor/SKILL.md`).
- **Merge Requests**: Use the `/mr` skill (`.claude/skills/mr/SKILL.md`).
- **Code Review**: The `code-reviewer` agent reviews diffs before commit.
