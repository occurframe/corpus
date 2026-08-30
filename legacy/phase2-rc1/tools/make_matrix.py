#!/usr/bin/env python3
"""Score raw runner output against the corpus and emit the differential matrix.

  python3 tools/make_matrix.py --vectors vectors --raw raw --out matrix

Produces
  matrix/matrix.json       machine-readable: per (vector, engine) verdict
  matrix/matrix.md         the differential matrix, divergences highlighted
  matrix/divergences.md    every vector with >1 distinct engine answer
  matrix/conformance-<engine>.md  a per-engine conformance report

Verdicts
  PASS        output equals the single expected list
  PASS[label] output equals one admissible case; the label names the policy
              or dialect the engine implements
  FAIL        output is well-formed but matches nothing the corpus admits
  NOVEL       same as FAIL, but on an AMBIGUOUS_STANDARD / KNOWN_DIVERGENCE
              vector: a behaviour no source and no case predicted
  REJECT-OK   engine rejected an INVALID input (required)
  REJECT-BAD  engine accepted an INVALID input (conformance failure)
  HANG        engine did not terminate inside the runner's per-vector budget
  RECORD      expect.mode == "open": measured, deliberately not scored
  N/A         engine does not implement this operation
"""
from __future__ import annotations
import argparse
import collections
import json
import os

PASS_KINDS = {"PASS", "REJECT-OK"}


def load_jsonl(p):
    with open(p) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def load_vectors(d):
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith(".jsonl"):
            for v in load_jsonl(os.path.join(d, f)):
                out[v["id"]] = v
    return out


def is_descriptive(occ):
    return bool(occ) and isinstance(occ[0], str) and occ[0].startswith("DESCRIPTION:")


def grade(v, r):
    exp = v["expect"]
    mode = exp["mode"]
    st = r["status"]
    occ = r.get("occurrences") or []
    if st == "unsupported_op":
        return "N/A", None
    if st == "timeout":
        return "HANG", None
    if st == "unsupported":
        return "N/A", None
    rejected = st in ("error", "crash")
    if is_descriptive(occ):
        # a describe-only engine: only its accept/reject decision is scoreable
        if mode == "reject":
            return "REJECT-BAD", None
        return "RECORD", "accepted"
    if mode == "single":
        if rejected:
            return "FAIL", "rejected"
        return ("PASS", None) if occ == exp["occurrences"] else ("FAIL", None)
    if mode == "reject":
        return ("REJECT-OK", None) if rejected else ("REJECT-BAD", None)
    if mode == "open":
        return "RECORD", ("rejected" if rejected else None)
    # per_policy | per_dialect | admissible
    for c in exp["cases"]:
        want = c["occurrences"]
        if want is None:
            if rejected or st == "empty" and False:
                return "PASS", c["label"]
        elif not rejected and occ == want:
            return "PASS", c["label"]
    novel = v["classification"] in ("AMBIGUOUS_STANDARD", "KNOWN_DIVERGENCE")
    return ("NOVEL" if novel else "FAIL"), ("rejected" if rejected else None)


def signature(r):
    if r["status"] == "unsupported_op":
        return None
    if r["status"] in ("error", "crash"):
        return "ERROR"
    if r["status"] == "timeout":
        return "HANG"
    if r["status"] == "empty":
        return "EMPTY"
    occ = r.get("occurrences") or []
    if is_descriptive(occ):
        return None
    return "|".join(occ)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vectors", default="vectors")
    ap.add_argument("--raw", default="raw")
    ap.add_argument("--out", default="matrix")
    a = ap.parse_args()

    vecs = load_vectors(a.vectors)
    results = []
    for f in sorted(os.listdir(a.raw)):
        if f.endswith(".jsonl"):
            for r in load_jsonl(os.path.join(a.raw, f)):
                r["_file"] = f
                results.append(r)

    # engine key includes the tzdb, because the same engine on two tzdbs is
    # two different oracles and the corpus refuses to conflate them.
    def ekey(r):
        return f"{r['engine']}@tz{r['tzdb']}"

    engines = {}
    for r in results:
        engines.setdefault(ekey(r), {
            "engine": r["engine"], "engine_version": r["engine_version"],
            "language": r["language"], "tzdb": r["tzdb"],
            "tzdb_source": r["tzdb_source"], "runner": r["runner"]})
    ekeys = sorted(engines)

    cell = {}
    for r in results:
        g, label = grade(vecs[r["vector_id"]], r)
        cell[(r["vector_id"], ekey(r))] = {
            "verdict": g, "label": label, "status": r["status"],
            "occurrences": r.get("occurrences") or [], "error": r.get("error"),
            "signature": signature(r)}

    os.makedirs(a.out, exist_ok=True)

    # ---- divergence analysis ---------------------------------------
    diverge = {}
    for vid in vecs:
        sigs = collections.defaultdict(list)
        for ek in ekeys:
            c = cell.get((vid, ek))
            if not c or c["signature"] is None:
                continue
            sigs[c["signature"]].append(ek)
        if len(sigs) > 1:
            diverge[vid] = sigs

    summary = {
        "engines": engines,
        "vector_count": len(vecs),
        "engine_count": len(ekeys),
        "cells": len(cell),
        "divergent_vectors": len(diverge),
        "verdict_counts": collections.Counter(
            c["verdict"] for c in cell.values()),
        "per_engine": {},
    }
    for ek in ekeys:
        cnt = collections.Counter()
        labels = collections.Counter()
        for vid in vecs:
            c = cell.get((vid, ek))
            if c:
                cnt[c["verdict"]] += 1
                if c["label"]:
                    labels[c["label"]] += 1
        scored = sum(v for k, v in cnt.items()
                     if k in ("PASS", "FAIL", "REJECT-OK", "REJECT-BAD", "NOVEL", "HANG"))
        passed = cnt["PASS"] + cnt["REJECT-OK"]
        summary["per_engine"][ek] = {
            "verdicts": dict(cnt), "policy_labels": dict(labels),
            "scored": scored, "passed": passed,
            "rate": round(100.0 * passed / scored, 1) if scored else None}

    with open(os.path.join(a.out, "matrix.json"), "w") as fh:
        json.dump({"summary": {**summary,
                               "verdict_counts": dict(summary["verdict_counts"])},
                   "cells": {f"{k[0]}||{k[1]}": v for k, v in cell.items()},
                   "divergences": {k: {s: e for s, e in v.items()}
                                   for k, v in diverge.items()}},
                  fh, indent=1)

    # ---- matrix.md --------------------------------------------------
    SYM = {"PASS": "P", "FAIL": "F", "NOVEL": "N", "REJECT-OK": "R",
           "REJECT-BAD": "x", "HANG": "H", "RECORD": ".", "N/A": "-"}
    lines = []
    lines.append("# Differential conformance matrix\n")
    lines.append(f"Corpus {next(iter(vecs.values()))['corpus_version']} · "
                 f"{len(vecs)} vectors × {len(ekeys)} engine builds = "
                 f"{len(cell)} measured cells · "
                 f"{len(diverge)} vectors show >1 distinct answer.\n")
    lines.append("Legend: `P` pass · `R` correctly rejected an invalid input · "
                 "`F` fail · `N` novel behaviour on an already-ambiguous "
                 "vector · `x` accepted an input that must be rejected · "
                 "`H` did not terminate · `.` recorded, not scored · "
                 "`-` operation not implemented.\n")
    lines.append("## Engine builds\n")
    lines.append("| key | engine | version | runtime | tzdb | tzdb source |")
    lines.append("|---|---|---|---|---|---|")
    for ek in ekeys:
        e = engines[ek]
        lines.append(f"| `{ek}` | {e['engine']} | {e['engine_version']} | "
                     f"{e['language']} | **{e['tzdb']}** | {e['tzdb_source']} |")
    lines.append("\n## Scoreboard\n")
    lines.append("| engine build | scored | passed | rate | P | R | F | N | x | H | . | - |")
    lines.append("|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    for ek in ekeys:
        s = summary["per_engine"][ek]
        v = s["verdicts"]
        lines.append("| `%s` | %d | %d | %s | %d | %d | %d | %d | %d | %d | %d | %d |" % (
            ek, s["scored"], s["passed"],
            f"{s['rate']}%" if s["rate"] is not None else "n/a",
            v.get("PASS", 0), v.get("REJECT-OK", 0), v.get("FAIL", 0),
            v.get("NOVEL", 0), v.get("REJECT-BAD", 0), v.get("HANG", 0),
            v.get("RECORD", 0), v.get("N/A", 0)))

    lines.append("\n## Matrix\n")
    short = {ek: str(i + 1) for i, ek in enumerate(ekeys)}
    lines.append("Columns, in order: " + " · ".join(
        f"**{short[ek]}**=`{ek}`" for ek in ekeys) + "\n")
    hdr = "| vector | class | " + " | ".join(short[ek] for ek in ekeys) + " | dist |"
    lines.append(hdr)
    lines.append("|---|---|" + "---|" * (len(ekeys) + 1))
    for vid in sorted(vecs):
        v = vecs[vid]
        row = []
        for ek in ekeys:
            c = cell.get((vid, ek))
            row.append(SYM.get(c["verdict"], "?") if c else "-")
        nd = len(diverge.get(vid, {}))
        mark = f"**{nd}**" if nd > 1 else str(nd)
        lines.append(f"| `{vid}` | {v['classification'][:4]} | " +
                     " | ".join(row) + f" | {mark} |")

    with open(os.path.join(a.out, "matrix.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")

    # ---- divergences.md ---------------------------------------------
    dl = ["# Measured divergences\n",
          "Every vector on which two engine builds produced different "
          "output. `ERROR` means the engine rejected the input, `HANG` that "
          "it did not terminate, `EMPTY` that it returned no occurrences.\n"]
    order = sorted(diverge, key=lambda k: (-len(diverge[k]), k))
    for vid in order:
        v = vecs[vid]
        dl.append(f"\n## `{vid}` — {v['title']}\n")
        dl.append(f"*{v['classification']}* · family `{v['family']}` · "
                  f"policy axis `{v['policy_axis']}`\n")
        if v["kind"] == "cron":
            dl.append(f"input: `{v['input']['expr']}` from "
                      f"`{v['input']['start']}` "
                      f"zone `{v['input'].get('zone')}` × {v['input']['count']}\n")
        else:
            dl.append("input:\n```\n" + v["input"]["ics"] + "\n```\n")
        dl.append(f"**{len(diverge[vid])} distinct answers:**\n")
        for sig, eks in sorted(diverge[vid].items(),
                               key=lambda kv: (-len(kv[1]), kv[0])):
            pretty = sig if sig in ("ERROR", "HANG", "EMPTY") else \
                "<br>".join(sig.split("|")[:8]) if len(sig) < 900 else sig[:900]
            labels = set()
            for ek in eks:
                c = cell[(vid, ek)]
                if c["label"]:
                    labels.add(c["label"])
            dl.append(f"- **{', '.join(eks)}**"
                      + (f" → admissible case `{'/'.join(sorted(labels))}`"
                         if labels else "")
                      + f"\n  <br>`{pretty}`\n")
    with open(os.path.join(a.out, "divergences.md"), "w") as fh:
        fh.write("\n".join(dl) + "\n")

    # ---- per-engine conformance reports ------------------------------
    for ek in ekeys:
        s = summary["per_engine"][ek]
        e = engines[ek]
        rl = [f"# Conformance report — `{ek}`\n",
              f"- engine: **{e['engine']}** {e['engine_version']}",
              f"- runtime: {e['language']}",
              f"- tzdb: **{e['tzdb']}** (from {e['tzdb_source']})",
              f"- runner: {e['runner']}",
              f"- corpus: {next(iter(vecs.values()))['corpus_version']}",
              "",
              f"**Scored {s['scored']} of {len(vecs)} vectors; "
              f"{s['passed']} pass ({s['rate']}%).** The remainder are "
              "operations this engine does not implement, or vectors the "
              "corpus records without scoring.", ""]
        if s["policy_labels"]:
            rl.append("## Policies and dialects this engine implements\n")
            rl.append("| axis value observed | vectors |")
            rl.append("|---|--:|")
            for k, n in sorted(s["policy_labels"].items(), key=lambda x: -x[1]):
                rl.append(f"| `{k}` | {n} |")
            rl.append("")
        for want in ("FAIL", "REJECT-BAD", "HANG", "NOVEL"):
            rows = [vid for vid in sorted(vecs)
                    if cell.get((vid, ek), {}).get("verdict") == want]
            if not rows:
                continue
            rl.append(f"## {want} ({len(rows)})\n")
            for vid in rows:
                c = cell[(vid, ek)]
                rl.append(f"- `{vid}` {vecs[vid]['title']}")
                if c["error"]:
                    rl.append(f"  - engine said: `{c['error'][:200]}`")
                elif c["occurrences"]:
                    rl.append(f"  - engine gave: `{', '.join(c['occurrences'][:4])}`")
                exp = vecs[vid]["expect"]
                if exp["mode"] == "single":
                    rl.append(f"  - corpus expects: "
                              f"`{', '.join(exp['occurrences'][:4])}`")
            rl.append("")
        with open(os.path.join(a.out, f"conformance-{ek.replace('/', '_')}.md"),
                  "w") as fh:
            fh.write("\n".join(rl) + "\n")

    print(json.dumps({"engines": len(ekeys), "vectors": len(vecs),
                      "cells": len(cell), "divergent_vectors": len(diverge),
                      "verdicts": dict(summary["verdict_counts"])}, indent=2))


if __name__ == "__main__":
    main()
