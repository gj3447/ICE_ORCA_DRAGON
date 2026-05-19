"""Normalize 3 legacy prose verdicts to taxonomy {CONFIRMED, REFUTED, ...}.

Preserves original prose as verdict_reasoning.

# KG: ICE_ORCA_DRAGON L3 verdict taxonomy normalization
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).parent
DATE = "2026-05-17"

LEGACY = {
    "derive_Lstar_results.json": {
        "verdict": "REFUTED",
        "self_refutation": True,
        "verdict_source": "self-refutation prose preserved 2026-05-17",
    },
    "derive_dimensionless_results.json": {
        "verdict": "NUMEROLOGY_HOLD",
        "self_refutation": False,
        "verdict_source": "self-flagged postdiction prose preserved 2026-05-17",
    },
    "derive_mass_ratios_results.json": {
        "verdict": "REFUTED",
        "self_refutation": True,
        "verdict_source": "self-refutation prose preserved 2026-05-17 (STATUS.md ledger 2026-05-14)",
    },
}


def normalize(path: pathlib.Path, entry: dict) -> None:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} root is not dict")
    legacy_prose = data.get("verdict")
    if legacy_prose in {"REFUTED", "CONFIRMED", "CONFIRMATION_LOCAL",
                       "NUMEROLOGY_HOLD", "INCONCLUSIVE", "DISCOVERY"}:
        print(f"  skip (already taxonomy): {path.name}")
        return
    new_data = {
        "verdict": entry["verdict"],
        "verdict_reasoning": legacy_prose,
        "verdict_source": entry["verdict_source"],
        "verdict_date": DATE,
        "self_refutation": entry["self_refutation"],
        **{k: v for k, v in data.items() if k != "verdict"},
    }
    path.write_text(json.dumps(new_data, indent=2, ensure_ascii=False) + "\n")
    print(f"  normalized: {path.name} -> {entry['verdict']} (legacy prose preserved)")


def main() -> None:
    for name, entry in LEGACY.items():
        p = ROOT / name
        if not p.exists():
            print(f"  MISSING: {name}")
            continue
        normalize(p, entry)


if __name__ == "__main__":
    main()
