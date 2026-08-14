#!/usr/bin/env python3
"""Compatibility entry point for the TypeScript + Effect reproduction command.

The reproduction implementation lives in ``src/repro``. New automation should
invoke ``./ice repro`` or ``npm run ice -- repro`` directly.
"""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


if __name__ == "__main__":
    raise SystemExit(
        subprocess.run([str(ROOT / "ice"), "repro", *sys.argv[1:]], cwd=ROOT).returncode
    )
