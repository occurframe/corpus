#!/usr/bin/env python3
"""Freeze measured engine outputs into the corpus as `incumbents`.

Pipeline:  build_all.py  ->  runners/*  ->  freeze_incumbents.py  ->  build_all.py

Every vector MUST carry known incumbent outputs, engine versions and tzdb
provenance. Those are *measurements*, not authored data, so they are produced
by this step and re-injected at the next build. Keeping them out of the
authoring source is what stops the corpus becoming circular: an expected
value is never derived from an incumbent, but every incumbent's answer is
recorded beside it.
"""
import argparse, json, os

ap = argparse.ArgumentParser()
ap.add_argument("--raw", default="raw")
ap.add_argument("--out", default="vectors/incumbents.json")
a = ap.parse_args()

inc = {}
for f in sorted(os.listdir(a.raw)):
    if not f.endswith(".jsonl"):
        continue
    for line in open(os.path.join(a.raw, f)):
        if not line.strip():
            continue
        r = json.loads(line)
        if r["status"] == "unsupported_op":
            continue
        key = f"{r['engine']}@tz{r['tzdb']}"
        e = {"engine": r["engine"], "engine_version": r["engine_version"],
             "language": r["language"], "tzdb": r["tzdb"],
             "tzdb_source": r["tzdb_source"], "status": r["status"]}
        if r["status"] in ("ok", "empty"):
            e["occurrences"] = r["occurrences"]
        else:
            e["error"] = r.get("error")
        inc.setdefault(r["vector_id"], {})[key] = e

os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
json.dump(inc, open(a.out, "w"), indent=1, sort_keys=True)
print(f"froze incumbents for {len(inc)} vectors "
      f"({sum(len(v) for v in inc.values())} engine observations) -> {a.out}")
