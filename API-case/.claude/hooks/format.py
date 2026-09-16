"""PostToolUse hook: auto-format Python files right after Claude edits them.

Claude Code pipes the tool-call payload as JSON via stdin. This script
extracts the edited file path and runs `ruff format` on it, so formatting
is enforced by the harness instead of relying on the model to remember.

Exit code is always 0: a formatting failure must never block the edit.
"""

import json
import subprocess
import sys


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    file_path: str = payload.get("tool_input", {}).get("file_path", "")
    if not file_path.endswith(".py"):
        return

    subprocess.run(
        ["uv", "run", "ruff", "format", file_path],
        capture_output=True,
        check=False,
    )


if __name__ == "__main__":
    main()
