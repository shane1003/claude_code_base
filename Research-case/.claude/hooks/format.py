"""PostToolUse hook: format the file Claude just edited.

Claude Code pipes the tool-call payload as JSON via stdin. This script reads
the edited file path and handles *only that one file*, so hygiene is enforced
by the harness instead of relying on the model to remember.

- ``*.py`` / ``*.pyi`` -> ``ruff format`` (code style)
- ``*.ipynb``          -> ``nbstripout`` (drop outputs so notebooks diff
  cleanly and no large result blobs get committed)

Three rules keep this safe:

1. Only ever hand a tool a single explicit file path. Never a directory and
   never ``.`` -- a repo-wide run rewrites files that have nothing to do with
   the current task.
2. Only extensions listed below reach a formatter. Since ruff 0.16.0,
   ``ruff format`` also rewrites Python code blocks inside Markdown, so adding
   ``.md`` would let this hook silently edit the rule documents under
   ``.claude/rules/``. Do not add it.
3. Nothing under ``outputs/``, ``data/``, or ``weights/`` is ever touched.
   A finished run is not reproducible for free, so it is off limits even to a
   formatter.

The hook must never fail an edit, so every error is swallowed and the exit
code is always 0.
"""

import json
import shutil
import subprocess
import sys
from pathlib import PurePath

# Extensions this hook is allowed to format. See rule 2 above before adding to
# this tuple. Markdown is deliberately absent.
FORMATTABLE = (".py", ".pyi")
NOTEBOOK = ".ipynb"

# Directories holding experiment artifacts. Never rewritten. See rule 3.
PROTECTED_DIRS = frozenset({"outputs", "data", "weights", "runs", "checkpoints"})

# A tool that has not finished in this many seconds is not worth blocking the
# edit for.
TIMEOUT_SECONDS = 30


def _is_protected(file_path: str) -> bool:
    """Reports whether a path lies inside an experiment artifact directory.

    Args:
        file_path: Absolute or repo-relative path of the edited file.

    Returns:
        True when any path segment names a protected directory.
    """
    return bool(PROTECTED_DIRS.intersection(PurePath(file_path).parts))


def _run(tool: str, args: list[str]) -> None:
    """Runs a formatting tool, preferring a directly installed executable.

    Falling back to ``uv run`` only when the tool is not on PATH keeps the hook
    working in a checkout where ``uv sync`` has not been run yet.

    Args:
        tool: Executable name, for example ``ruff`` or ``nbstripout``.
        args: Arguments following the executable name.
    """
    resolved = shutil.which(tool)
    command = [resolved, *args] if resolved else ["uv", "run", tool, *args]
    subprocess.run(command, capture_output=True, check=False, timeout=TIMEOUT_SECONDS)


def main() -> None:
    """Reads the hook payload from stdin and processes the edited file."""
    # lstrip the BOM: on Windows some shells prepend one when piping, and
    # json.loads rejects it. Without this the hook would silently do nothing.
    payload = json.loads(sys.stdin.read().lstrip("\ufeff") or "{}")
    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""

    if not file_path or _is_protected(file_path):
        return

    if file_path.endswith(FORMATTABLE):
        _run("ruff", ["format", file_path])
    elif file_path.endswith(NOTEBOOK):
        _run("nbstripout", [file_path])


if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001 - a hook must never break the edit
        pass
    sys.exit(0)
