# Project Guidelines

<!-- ================================================================== -->
<!-- SECTION A: PER-REPO — replace everything in this section when      -->
<!-- copying this template into another repository.                     -->
<!-- ================================================================== -->

FastAPI backend application managed with `uv`.

## 1. Build, Run & Test Commands
- **Environment Sync**: `uv sync`
- **Manage Dependencies**: `uv add <pkg>` or `uv remove <pkg>` (Do NOT edit pyproject.toml manually)
- **Dev Server**: `uv run uvicorn app.main:app --reload`
- **Run All Tests**: `uv run pytest`
- **Run Single Test**: `uv run pytest tests/test_users.py -k "test_login"`
- **Lint & Format**: `uv run ruff check --fix .` && `uv run ruff format .`
- **Type Checking**: `uv run mypy .`

## 2. Architecture Rules (FastAPI)
- **Directory Layout**:
  - `app/api/`: Endpoint routing (`APIRouter`)
  - `app/schemas/`: Pydantic v2 Request/Response schemas (DTOs)
  - `app/models/`: Database ORM models
  - `app/services/`: Pure business logic
  - `app/core/`: App configuration, DB session, security
- **Strict Separation**: Never return ORM models directly in API responses. Always use Pydantic schemas.
- **Dependency Injection**: Always use `Depends()` for DB session management and authentication.

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

## 5. Code Style & Documentation
- **Readability First**: Clear, simple, self-documenting code over clever/compact syntax.
- **Detailed Style Rules**: Read `.claude/rules/code-style.md`.
- **Type Annotations**: Mandatory explicit type hints for parameters and return types.
- **Google Docstring Style**: Apply Google-style docstrings (`Args`, `Returns`, `Raises`) for all public functions/classes/modules.
- **Comments**: Focus on explaining *WHY* a non-obvious logic was used, not *WHAT*.

## 6. Workflows
- **Task Handoff**: End every code change by overwriting `.claude/HANDOFF.md` per `.claude/rules/handoff.md` (work log, checkpoints, commit recommendation: what / why now / type / message, detailed notes). Read user feedback left in that file before starting the next task. Use `/handoff` to refresh it on demand.
- **Git Commit messages**: Follow `.claude/rules/commit.md` when recommending a message.
- **Refactoring**: Use the `/refactor` skill (`.claude/skills/refactor/SKILL.md`).
- **Merge Requests**: Use the `/mr` skill (`.claude/skills/mr/SKILL.md`).
- **Code Review**: The `code-reviewer` agent reviews diffs before commit.
