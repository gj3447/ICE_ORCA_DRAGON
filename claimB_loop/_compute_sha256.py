import hashlib, json

path = str(__import__("pathlib").Path(__file__).resolve().parent / "prereg_claimB_loop_20260724.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Canonical JSON serialization for hash: sorted keys, no extra whitespace, no ASCII escape
s = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
h = hashlib.sha256(s).hexdigest()
print(h)

sha_path = path + ".sha256"
with open(sha_path, "w", encoding="utf-8") as f:
    f.write(f"{h}  prereg_claimB_loop_20260724.json")
