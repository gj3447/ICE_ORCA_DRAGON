#!/usr/bin/env python3
"""ice — ICE_ORCA_DRAGON 실험 스크립트 단일 진입 CLI (single-file, stdlib only).

~41개 runnable 스크립트(queue_*, prove_s*, derive_*, numerology_*, claimB_loop/*,
dated test dirs)를 하나의 명령으로 묶는다. discovery 는 매 실행시
`if __name__ == "__main__"` guard 스캔 (캐시 없음 — repro_check.py 관례대로 저렴).

usage:
  ice list [--json]         runnable 스크립트 열거 (relpath + 한 줄 설명)
  ice run <name|relpath> [-- args...]   스크립트를 *자기 디렉토리*에서 python3 실행,
                                        출력 스트리밍, exit code 그대로 전파
  ice repro [args...]       repro_check.py 얇은 pass-through (`ice repro --list` 등)
  ice info <name>           경로/독스트링/산출 result JSON 표시

name 은 stem(queue_01_orbit_analysis) 또는 relpath(claimB_loop/claimB_zd_nullity_spectrum).
unique-prefix 매칭 허용, 모호하면 매치 목록과 함께 에러.
"""
import argparse
import ast
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent

GUARD = re.compile(r"if\s+__name__\s*==\s*['\"]__main__['\"]\s*:")
# helper/모듈 디렉토리 — runnable 대상 아님 (repro_check.py discovery 관례와 동일 기준)
SKIP_DIRS = {"_archive", "_findings", "papers", "docs", "__pycache__"}
# harness 자체는 `ice repro` 로 노출 — run 대상 목록에서는 제외
SELF_EXCLUDE = {"repro_check.py", pathlib.Path(__file__).name}


def _doc_line(path):
    """모듈 독스트링 첫 줄, 없으면 첫 주석 줄."""
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    try:
        doc = ast.get_docstring(ast.parse(src))
        if doc:
            return doc.strip().splitlines()[0].strip()
    except SyntaxError:
        pass
    for line in src.splitlines():
        line = line.strip()
        if line.startswith("#!"):
            continue
        if line.startswith("#"):
            return line.lstrip("#").strip()
        if line and not line.startswith(('"', "'")):
            break
    return ""


def discover():
    """main-guard 를 가진 runnable 스크립트를 스캔. [{name, relpath, path, doc}] sorted."""
    out = []
    for p in ROOT.rglob("*.py"):
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts[:-1]):
            continue
        if p.name.startswith("_") or p.name in SELF_EXCLUDE:
            continue
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if GUARD.search(src):
            out.append({
                "name": p.stem,
                "relpath": rel.with_suffix("").as_posix(),
                "path": p,
                "doc": _doc_line(p),
            })
    out.sort(key=lambda e: e["relpath"])
    return out


def resolve(entries, query):
    """exact > unique-prefix (stem 또는 relpath). (entry, err) 반환."""
    q = query[:-3] if query.endswith(".py") else query
    exact = [e for e in entries if q in (e["name"], e["relpath"])]
    if len(exact) == 1:
        return exact[0], None
    pref = [e for e in entries
            if e["name"].startswith(q) or e["relpath"].startswith(q)]
    if len(pref) == 1:
        return pref[0], None
    if not pref:
        return None, f"ice: no runnable script matches '{query}' (see `ice list`)"
    lines = "\n".join(f"  {e['relpath']}" for e in pref)
    return None, f"ice: ambiguous prefix '{query}' matches {len(pref)} scripts:\n{lines}"


def repro_map():
    """repro_check.py 의 script->output JSON 매핑 (없으면 {})."""
    try:
        sys.path.insert(0, str(ROOT))
        import repro_check
        return dict(repro_check.SCRIPTS)
    except Exception:
        return {}
    finally:
        try:
            sys.path.remove(str(ROOT))
        except ValueError:
            pass


def cmd_list(ns):
    entries = discover()
    if ns.json:
        print(json.dumps(
            [{"name": e["name"], "path": e["relpath"] + ".py", "doc": e["doc"]}
             for e in entries],
            ensure_ascii=False, indent=2))
    else:
        for e in entries:
            doc = f" — {e['doc']}" if e["doc"] else ""
            print(f"{e['relpath']}{doc}")
        print(f"\n{len(entries)} runnable scripts", file=sys.stderr)
    return 0


def cmd_run(ns):
    entries = discover()
    entry, err = resolve(entries, ns.name)
    if err:
        print(err, file=sys.stderr)
        return 2
    args = list(ns.script_args)
    if args and args[0] == "--":
        args = args[1:]
    r = subprocess.run([sys.executable, entry["path"].name, *args],
                       cwd=entry["path"].parent)
    return r.returncode


def cmd_repro(argv):
    """repro_check.py 얇은 pass-through (exit code 그대로)."""
    r = subprocess.run([sys.executable, "repro_check.py", *argv], cwd=ROOT)
    return r.returncode


def cmd_info(ns):
    entries = discover()
    entry, err = resolve(entries, ns.name)
    if err:
        print(err, file=sys.stderr)
        return 2
    print(f"name:    {entry['name']}")
    print(f"path:    {entry['relpath']}.py")
    print(f"run:     ice run {entry['relpath']}")
    doc = _doc_line(entry["path"])
    try:
        full = ast.get_docstring(ast.parse(
            entry["path"].read_text(encoding="utf-8", errors="replace"))) or ""
    except SyntaxError:
        full = ""
    if full:
        print(f"doc:     {full.strip().splitlines()[0].strip()}")
        for line in full.strip().splitlines()[1:]:
            print(f"         {line.rstrip()}")
    elif doc:
        print(f"doc:     {doc}")
    # result JSON: repro_check 매핑 우선, 없으면 소스 내 *.json 리터럴 휴리스틱
    mapping = repro_map()
    out = mapping.get(entry["name"])
    if out:
        print(f"results: {out}  (from repro_check.py SCRIPTS)")
    else:
        src = entry["path"].read_text(encoding="utf-8", errors="replace")
        found = sorted(set(re.findall(r"[\w\-./]+\.json", src)))
        found = [f for f in found if not f.startswith(("http", "//"))]
        if found:
            print(f"results: {', '.join(found)}  (guessed from source literals; "
                  f"no repro_check.py mapping)")
        else:
            print("results: (none detected; no repro_check.py mapping)")
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    # `ice repro ...` 는 argparse 가 repro 측 옵션(--list 등)을 먹지 않도록 선제 가로챔
    if argv and argv[0] == "repro":
        return cmd_repro(argv[1:])

    ap = argparse.ArgumentParser(
        prog="ice",
        description="ICE_ORCA_DRAGON 실험 스크립트 단일 진입 CLI",
        epilog="extra subcommand: ice repro [args...] — repro_check.py pass-through")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="runnable 스크립트 열거")
    p.add_argument("--json", action="store_true", help="JSON 배열로 출력")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("run", help="스크립트를 자기 디렉토리에서 실행")
    p.add_argument("name", help="stem, relpath, 또는 unique prefix")
    p.add_argument("script_args", nargs=argparse.REMAINDER,
                   help="`--` 뒤 인자는 스크립트로 그대로 전달")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("info", help="경로/독스트링/result JSON 표시")
    p.add_argument("name", help="stem, relpath, 또는 unique prefix")
    p.set_defaults(func=cmd_info)

    ns = ap.parse_args(argv)
    return ns.func(ns)


if __name__ == "__main__":
    sys.exit(main())
