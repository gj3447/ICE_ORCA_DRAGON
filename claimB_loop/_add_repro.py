import json
import hashlib

RESULTS = "results_c3_truncation_stability.json"
RESULTS_RUN1 = "results_c3_truncation_stability_run1.json"
SCRIPT = "claimB_truncation_stability.py"

with open(RESULTS, "r", encoding="utf-8") as f:
    r1 = json.load(f)
with open(RESULTS_RUN1, "r", encoding="utf-8") as f:
    r2 = json.load(f)

t1 = r1.pop("timestamp")
t2 = r2.pop("timestamp")
identical = (json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True))
r1["timestamp"] = t1

r1["reproducibility"] = {
    "run2_verdict": r1["verdict"],
    "byte_identical": identical,
    "mismatches": (["timestamp"] if not identical else [])
}

with open(SCRIPT, "rb") as f:
    r1["script_sha256"] = hashlib.sha256(f.read()).hexdigest()

with open(RESULTS, "w", encoding="utf-8") as f:
    json.dump(r1, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Reproducibility added. Byte-identical={identical}")
