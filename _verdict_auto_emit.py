"""Auto-emit verdict JSON for ICE_ORCA_DRAGON scripts (zero body modification).

PROM 16 A3-S1 design (prom16-ice-residual-2026-05-17, R3 of ActionPlan).

Three layers:
  1. atexit hook  — normal exit + sys.exit(N) + SystemExit
  2. excepthook   — unhandled exception → verdict='ERROR' + traceback tail
  3. signal hook  — SIGTERM (best-effort; NOT SIGKILL / os._exit)

Idempotent: merges into existing <script>_results.json via setdefault().
NEVER overwrites pre-existing verdict / verdict_reasoning (preserves 18+ explicit-verdict scripts).
NEVER auto-sets CONFIRMED (MT_RubberStampVerdict guard) — only structural COMPLETED|ERROR.

Usage:
  Option A (per-script):   add `import _verdict_auto_emit` at the top of any script.
  Option B (global retrofit): copy to PYTHONUSERBASE/usercustomize.py to auto-import
                              for every Python invocation. Requires env-var opt-in:
                                  export SYMPOSIUM_VERDICT_AUTO_EMIT=1
                              to avoid polluting unrelated tooling.
  Optional API: `from _verdict_auto_emit import set_verdict`
                `set_verdict("CONFIRMED", "reasoning here")`
                will populate verdict/verdict_reasoning before atexit fires.

# KG: R3 of prom16-ice-residual ActionPlan, MT_RubberStampVerdict guard, MT_SuccessBias guard
"""

from __future__ import annotations

import atexit
import json
import os
import pathlib
import platform
import signal
import sys
import time
import traceback

_START = time.time()
_SCRIPT_PATH = pathlib.Path(sys.argv[0]).resolve() if sys.argv and sys.argv[0] else None
_OUT_FILE = (
    _SCRIPT_PATH.with_name(_SCRIPT_PATH.stem + "_results.json")
    if _SCRIPT_PATH and _SCRIPT_PATH.suffix == ".py"
    else None
)

_STATE: dict = {
    "verdict_user": None,
    "verdict_reasoning_user": None,
    "exception": None,
}

_AGENT_STACK = {
    "agent_id": os.environ.get("CLAUDE_AGENT_ID", "manual"),
    "session_id": os.environ.get("CLAUDE_SESSION_ID", ""),
    "python_version": platform.python_version(),
    "platform": platform.platform(),
    "cwd": os.getcwd(),
    "argv": list(sys.argv),
    "hook_version": "verdict_auto_emit/1.0",
}


def set_verdict(verdict: str, reasoning: str = "") -> None:
    """Optional API: caller-supplied verdict/reasoning. Beats structural defaults."""
    _STATE["verdict_user"] = verdict
    _STATE["verdict_reasoning_user"] = reasoning


def _merge_and_write(extra: dict) -> None:
    if _OUT_FILE is None:
        return
    existing: dict = {}
    if _OUT_FILE.exists():
        try:
            loaded = json.loads(_OUT_FILE.read_text(encoding="utf-8"))
            existing = loaded if isinstance(loaded, dict) else {"_legacy_payload": loaded}
        except Exception:
            existing = {"_unreadable_existing": True}

    # setdefault preserves any human-supplied verdict already in the file
    for key, value in extra.items():
        existing.setdefault(key, value)
    existing.setdefault("agent_stack", _AGENT_STACK)

    try:
        _OUT_FILE.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
    except Exception as e:
        sys.stderr.write(f"[verdict_auto_emit] write failed: {e}\n")


@atexit.register
def _on_exit() -> None:
    walltime = round(time.time() - _START, 6)

    if _STATE["exception"] is not None:
        verdict = "ERROR"
        reasoning = (
            f"unhandled {_STATE['exception']['type']}: {_STATE['exception']['msg']}"
        )
    elif _STATE["verdict_user"] is not None:
        verdict = _STATE["verdict_user"]
        reasoning = _STATE["verdict_reasoning_user"] or "set via set_verdict()"
    else:
        verdict = "COMPLETED"
        reasoning = (
            "AUTO_EMIT_PLACEHOLDER (no exception, no explicit set_verdict). "
            "MT_RubberStampVerdict guard: structural only — does not assert "
            "CONFIRMED/REFUTED/NUMEROLOGY classification."
        )

    _merge_and_write(
        {
            "verdict": verdict,
            "verdict_reasoning": reasoning,
            "verdict_source": "verdict_auto_emit/1.0",
            "verdict_date": time.strftime("%Y-%m-%d"),
            "walltime_sec": walltime,
            "exit_path": "exception" if _STATE["exception"] else "normal",
        }
    )


_orig_excepthook = sys.excepthook


def _hook_excepthook(exc_type, exc_value, tb):
    _STATE["exception"] = {
        "type": exc_type.__name__,
        "msg": str(exc_value),
        "traceback_tail": "".join(
            traceback.format_exception(exc_type, exc_value, tb)
        )[-4000:],
    }
    _orig_excepthook(exc_type, exc_value, tb)


sys.excepthook = _hook_excepthook


def _sigterm_handler(signum, frame):
    _STATE["exception"] = {
        "type": "SIGTERM",
        "msg": f"received signal {signum}",
        "traceback_tail": "",
    }
    sys.exit(143)


try:
    signal.signal(signal.SIGTERM, _sigterm_handler)
except (ValueError, OSError):
    # non-main thread or platform without SIGTERM — skip silently
    pass
