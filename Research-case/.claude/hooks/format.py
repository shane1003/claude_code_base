"""PostToolUse hook: auto-format files right after Claude edits them.

Claude Code pipes the tool-call payload as JSON via stdin. This script
extracts the edited file path and runs the matching formatter, so hygiene
is enforced by the harness instead of relying on the model to remember.

- ``*.py``    -> ``ruff format`` (code style)
- ``*.ipynb`` -> ``nbstripout`` (strip outputs so notebooks diff cleanly and
                 no large result blobs get committed)

Exit code is always 0: a formatting failure must never block the edit.
"""

import json
import subprocess
import sys


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, capture_output=True, check=False)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    tool_input = payload.get("tool_input", {})
    file_path: str = (
        tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    )

    if file_path.endswith(".py"):
        _run(["uv", "run", "ruff", "format", file_path])
    elif file_path.endswith(".ipynb"):
        _run(["uv", "run", "nbstripout", file_path])


if __name__ == "__main__":
    main()
