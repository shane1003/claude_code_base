---
name: refactor
description: Safe refactoring procedure - verify test coverage first, change in small atomic steps, validate after every step. Use when asked to refactor, restructure, or clean up existing code.
---

# Refactoring Procedure

When assigned a refactoring task, strictly follow this procedure:

## Step 1: Verify Test Coverage
- Run the project test command (see CLAUDE.md, e.g. `uv run pytest`) BEFORE changing any code.
- If tests fail or do not exist for the target module, write/fix tests FIRST before refactoring.

## Step 2: Incremental Steps
- Perform refactoring in small, atomic steps.
- Do NOT change external interfaces, API response structures, or business logic behavior unless explicitly requested.
- Touch ONLY the code required for the task. No opportunistic cleanup of adjacent code.

## Step 3: Verification
- Run the test and type-check commands (e.g. `uv run pytest` and `uv run mypy .`) after every incremental change.
- If a test breaks, revert to the last working state and re-evaluate before continuing.

## Completion Criteria
- All tests pass, type check passes, and lint passes.
- Report what changed and what stayed intentionally untouched.
