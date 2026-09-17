"""PostToolUse hook: format the file Claude just edited.

Claude Code pipes the tool-call payload as JSON via stdin. This script reads
the edited file path and formats *only that one file*, so hygiene is enforced
by the harness instead of relying on the model to remember.

Two rules keep this safe:

1. Only ever hand the formatter a single explicit file path. Never a directory
   and never ``.`` -- a repo-wide run rewrites files that have nothing to do
   with the current task.
2. Only extensions listed in ``FORMATTABLE`` reach ruff. Since ruff 0.14,
   ``ruff format`` also rewrites Python code blocks inside Markdown, so adding
   ``.md`` here would let this hook silently edit the rule documents under
   ``.claude/rules/``. Do not add it.

The hook must never fail an edit, so every error is swallowed and the exit
code is always 0.
"""

import json
import shutil
import subprocess
import sys

# Extensions this hook is allowed to format. See rule 2 above before adding to
# this tuple. Markdown is deliberately absent.
FORMATTABLE = (".py", ".pyi")

# A formatter that has not finished in this many seconds is not worth blocking
# the edit for.
TIMEOUT_SECONDS = 30


def _format(file_path: str) -> None:
    """Runs ruff on one file, preferring a directly installed executable.

    Falling back to ``uv run`` only when ruff is not on PATH keeps the hook
    working in a checkout where ``uv sync`` has not been run yet.

    Args:
        file_path: Absolute or repo-relative path of the single file to format.
    """
    ruff = shutil.which("ruff")
    command = (
        [ruff, "format", file_path]
        if ruff
        else ["uv", "run", "ruff", "format", file_path]
    )
    subprocess.run(command, capture_output=True, check=False, timeout=TIMEOUT_SECONDS)


def main() -> None:
    """Reads the hook payload from stdin and formats the edited file."""
    # lstrip the BOM: on Windows some shells prepend one when piping, and
    # json.loads rejects it. Without this the hook would silently do nothing.
    payload = json.loads(sys.stdin.read().lstrip("\ufeff") or "{}")
    file_path = payload.get("tool_input", {}).get("file_path") or ""

    if file_path.endswith(FORMATTABLE):
        _format(file_path)


if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001 - a hook must never break the edit
        pass
    sys.exit(0)
