---
name: handoff
description: Write or refresh .claude/HANDOFF.md (work log, pre-commit checkpoints, and a commit recommendation - what, why now, type choice, one-line message) for the current uncommitted changes. Use when the user asks for a commit message, a summary of what changed, or what to check before committing.
---

# Handoff Generator

1. If `.claude/HANDOFF.md` already exists, read it first. Any text that is
   not Claude's own (user notes, comments, edits) is feedback — apply it or
   answer it before overwriting.
2. Inspect the working tree: `git status`, `git diff`, and `git diff --cached`
   if anything is staged. Do NOT run `git commit`, `git push`, or `git add`.
3. If the verification commands have not been run in this session, run them
   now (`uv run pytest`, `uv run ruff check .`, `uv run mypy .`) and record
   the actual result. Never guess.
4. **Overwrite** `.claude/HANDOFF.md` using the exact format in
   `.claude/rules/handoff.md`. Fill the header with the current branch and
   timestamp. Put anything long (reasoning, alternatives, TODOs, questions)
   in the 상세 기록 section, not in the top sections.
5. Fill the 💬 커밋 추천 section with all four items: 무엇을 (the unit of
   change), 왜 지금 (why this is a good commit boundary — or 보류 권고 with
   the reason and the condition to become committable), 타입 선택 (TYPE and
   why), 추천 메시지 (one line). If the diff spans unrelated concerns, give a
   split plan instead: 2–3 commits in order, each with 무엇을 / 왜 지금 /
   files to `git add` / one-line message.
6. In chat, report: the file path, a one-line status of the checks, and the
   💬 커밋 추천 section verbatim. Nothing else from the file.
