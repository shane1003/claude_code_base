# Project Guidelines

<!-- ================================================================== -->
<!-- SECTION A: PER-REPO — replace everything in this section when      -->
<!-- copying this template into another repository.                     -->
<!-- ================================================================== -->

ML research / experiment repository (PyTorch) managed with `uv`.
The goal is **reproducible experiments**: every result must be traceable to
a config, a seed, a data version, and a git commit.

## 1. Build, Run & Test Commands

### Validation — read-only, Claude runs these
These report problems without editing anything and without consuming GPU time.
They are the commands meant by "validate" in Section 3.
- **Run Tests (fast, CPU-only)**: `uv run pytest`
- **Run Single Test**: `uv run pytest tests/test_metrics.py -k "test_auc"`
- **Lint Check**: `uv run ruff check .`
- **Format Check**: `uv run ruff format --check .`
- **Type Checking**: `uv run mypy src/`
- **GPU Check**: `nvidia-smi`

### Smoke Run — cheap, Claude may run to validate a code path
- **Smoke Run (tiny subset, CPU)**: `uv run python -m src.train --config configs/<exp>.yaml --debug`

### Mutating or expensive — the user runs these, Claude must not
Claude proposes the exact command and lets the user launch it.
- **Train**: `uv run python -m src.train --config configs/<exp>.yaml` (GPU hours, writes `outputs/`)
- **Evaluate**: `uv run python -m src.eval --config configs/<exp>.yaml --ckpt <path>` (writes `outputs/`)
- **Auto-fix lint**: `uv run ruff check --fix .` (rewrites files repo-wide)
- **Reformat**: `uv run ruff format .` (rewrites files repo-wide)

The two ruff commands above rewrite every matching file in the repository, not
just the ones in the current task. Claude never needs them: the PostToolUse
hook already formats each file it edits, one file at a time.

### Environment
- **Environment Sync**: `uv sync`
- **Manage Dependencies**: `uv add <pkg>` or `uv remove <pkg>` (Do NOT edit pyproject.toml manually)

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
  - `experiments/LOG.md`: Committed experiment ledger, one row per run (hypothesis, config, seed, git hash, metric). Written by `/experiment`.
  - `data/`, `weights/`, `outputs/`: Git-ignored. Referenced by path + hash/version in configs.
- **Config-Driven**: No magic numbers. Every knob (lr, batch size, threshold, paths) comes from the config.
- **Experiment Isolation**: Never edit a baseline config in place. Copy it to a new file (`configs/<date>_<name>.yaml`) and change only what the experiment tests.
- **Run Artifacts**: Each run writes to `outputs/<date>_<name>/` containing the resolved config, git hash, seed, metrics, and logs. Never overwrite a previous run.
- **Device Handling**: Select device from config/CLI via `src/utils`. Never hardcode `cuda:0`.

### Never Do (Research-specific)
These extend the universal list in Section 4 and travel with Section A.
- Never delete or overwrite files under `outputs/`, `data/`, or `weights/`. Experiment results cannot be regenerated for free. `settings.json` denies `rm` and `Remove-Item` outright; the hook skips these paths too.
- Never change a metric or evaluation function without adding/updating a known-answer test in `tests/`. A silently changed metric invalidates every past comparison.
- Never commit notebook outputs, datasets, or checkpoints. Reference them by path and hash.
- Never hardcode absolute local paths (home directories, drive letters). Paths come from config or env.
- Never start a full training run without an explicit request. Use the `--debug` smoke run to validate code changes.

<!-- ================================================================== -->
<!-- SECTION B: UNIVERSAL — copy as-is to any repository.               -->
<!-- ================================================================== -->

## 3. Core Behavioral Guidelines (Karpathy Principles)
1. **Think Before Coding**: Explicitly state assumptions. Ask questions on ambiguity instead of guessing.
2. **Simplicity First**: Write minimum required code. No overengineering or speculative abstractions.
3. **Surgical Changes**: Touch ONLY code required for the task. Do NOT refactor/clean adjacent code without permission.
4. **Goal-Driven Execution**: Validate changes with the **Validation** commands in Section 1 before marking complete. Validation reports; it never rewrites files and never spends GPU time.

## 4. Never Do
- Never edit dependency manifests by hand (use the package manager CLI).
- Never skip, delete, or weaken a failing test to make the suite pass — fix the cause or report it.
- Never commit secrets, credentials, or large binary files.
- Never run `git commit` or `git push`. The user commits and pushes manually. Instead, finish every task by overwriting `.claude/HANDOFF.md` (see `.claude/rules/handoff.md`).
- Never run a repo-wide mutating command as a validation step. `ruff format .` and `ruff check --fix .` rewrite every matching file in the repo, and since ruff 0.16.0 that includes Python code blocks inside Markdown. Use the read-only Validation commands in Section 1 instead.
- Never use `--no-verify`, `--force` push, or amend published commits unless explicitly asked.
- Never write a commit message body: commits are a single subject line only (`git commit -m "TYPE: one sentence"`, see `.claude/rules/commit.md`). No multi-line messages, no extra `-m` flags, no trailers.

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
