"""Run an ICE script with _verdict_auto_emit hook pre-loaded (ZERO source mod).

Usage:
  python3 _verdict_runner.py <script.py> [args...]

PROM 16 A3-S1 zero-mod retrofit (R3 of prom16-ice-residual).
"""

from __future__ import annotations

import pathlib
import runpy
import sys

ROOT = pathlib.Path(__file__).parent

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 _verdict_runner.py <script.py> [args...]", file=sys.stderr)
        sys.exit(2)

    script = (ROOT / sys.argv[1]).resolve()
    if not script.exists():
        print(f"Error: {script} does not exist", file=sys.stderr)
        sys.exit(2)

    # Rewrite sys.argv so the hook detects <script>_results.json
    sys.argv = [str(script)] + sys.argv[2:]

    # Ensure ICE_ORCA_DRAGON on sys.path so script-local imports (cd_embedding etc.) work
    sys.path.insert(0, str(ROOT))

    # Load the hook FIRST so atexit/excepthook are registered before script runs
    import _verdict_auto_emit  # noqa: F401

    # Run the script with __main__ semantics
    runpy.run_path(str(script), run_name="__main__")
