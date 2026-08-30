"""Shared authoring helpers for the Occurframe conformance corpus.

The corpus artefact is `vectors/*.jsonl`. This package is the *authoring
source*: it lets a vector's expected outcomes be **computed from a declared
policy** by the independent reference matcher in `reference/cron_ref.py`,
rather than copied out of an engine under test. Copying from an engine would
make the oracle circular; that is the single most important property of this
build step.
"""
from __future__ import annotations
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "reference"))

CORPUS_VERSION = "1.0.0-rc1"

# --------------------------------------------------------------- sources
# Every entry is a citation that was read directly during Phase I or Phase II.
S = {
    # --- RFC 5545 and its errata -------------------------------------
    "rfc5545-3.3.10": ("RFC 5545 §3.3.10 (RECUR value type)",
                       "https://www.rfc-editor.org/rfc/rfc5545#section-3.3.10"),
    "rfc5545-3.8.5.3": ("RFC 5545 §3.8.5.3 (Recurrence Rule)",
                        "https://www.rfc-editor.org/rfc/rfc5545#section-3.8.5.3"),
    "rfc5545-3.8.5.1": ("RFC 5545 §3.8.5.1 (Exception Date-Times)",
                        "https://www.rfc-editor.org/rfc/rfc5545#section-3.8.5.1"),
    "rfc5545-3.8.5.2": ("RFC 5545 §3.8.5.2 (Recurrence Date-Times)",
                        "https://www.rfc-editor.org/rfc/rfc5545#section-3.8.5.2"),
    "rfc5545-3.3.5": ("RFC 5545 §3.3.5 (DATE-TIME)",
                      "https://www.rfc-editor.org/rfc/rfc5545#section-3.3.5"),
    "eid1913": ("RFC 5545 erratum 1913 (Verified, Technical, §3.3.10)",
                "https://www.rfc-editor.org/errata/eid1913"),
    "eid3747": ("RFC 5545 erratum 3747 (Verified, Editorial, §3.3.10 Note 2)",
                "https://www.rfc-editor.org/errata/eid3747"),
    "eid3779": ("RFC 5545 erratum 3779 (Verified, Technical, §3.3.10)",
                "https://www.rfc-editor.org/errata/eid3779"),
    "eid3883": ("RFC 5545 erratum 3883 (Verified, Technical, §3.8.5.3 UNTIL example)",
                "https://www.rfc-editor.org/errata/eid3883"),
    "eid4271": ("RFC 5545 erratum 4271 (Verified, Technical, §3.3.10 nonexistent local times)",
                "https://www.rfc-editor.org/errata/eid4271"),
    "eid5920": ("RFC 5545 erratum 5920 (REJECTED, §3.8.5.3 Friday-the-13th example)",
                "https://www.rfc-editor.org/errata/eid5920"),
    "eid6316": ("RFC 5545 erratum 6316 (REPORTED since 2020-10-22, §3.8.5.1 EXDATE value type)",
                "https://www.rfc-editor.org/errata/eid6316"),
    "rfc7529": ("RFC 7529 (Non-Gregorian Recurrence Rules, RSCALE/SKIP)",
                "https://www.rfc-editor.org/rfc/rfc7529"),
    "rfc8984-4.3.3": ("RFC 8984 §4.3.3 (JSCalendar RecurrenceRule)",
                      "https://www.rfc-editor.org/rfc/rfc8984#section-4.3.3"),
    # --- cron --------------------------------------------------------
    "posix-crontab": ("POSIX.1-2017 crontab",
                      "https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html"),
    "crontab5": ("crontab(5), Vixie/cronie lineage",
                 "https://man7.org/linux/man-pages/man5/crontab.5.html"),
    "vixie-cron.c": ("vixie/cron cron.c find_jobs() dom/dow predicate",
                     "https://github.com/vixie/cron/blob/master/cron.c"),
    "vixie-entry.c": ("vixie/cron entry.c DOM_STAR/DOW_STAR first-character flagging",
                      "https://github.com/vixie/cron/blob/master/entry.c"),
    "crontab-guru-bug": ("crontab.guru, 'the cron bug'",
                         "https://crontab.guru/cron-bug.html"),
    "fcron5": ("fcrontab(5), dayand option",
               "https://man.archlinux.org/man/fcrontab.5.en"),
    "dcron": ("dcron crontab.markdown (Nth-weekday day-field semantics)",
              "https://github.com/dubiousjim/dcron/blob/master/crontab.markdown"),
    "micron": ("GNU micron manual, Cronjob Definition (strict/vixie/dillon)",
               "https://www.gnu.org.ua/software/micron/manual/Cronjob-Definition.html"),
    "quartz": ("Quartz CronExpression (1=SUN..7=SAT, '?' requirement, L/W/#)",
               "https://www.quartz-scheduler.org/api/2.3.0/org/quartz/CronExpression.html"),
    "aws-eventbridge": ("AWS EventBridge schedule expressions (6 fields, '?' required)",
                        "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-cron-expressions.html"),
    "healthchecks-funky": ("healthchecks.io, 'Schedule a cron job the funky way' (*/100,1-7 idiom)",
                           "https://blog.healthchecks.io/2022/09/schedule-cron-job-the-funky-way/"),
    # --- tzdb --------------------------------------------------------
    "tzdb-news": ("IANA tz database NEWS",
                  "https://data.iana.org/time-zones/tzdb/NEWS"),
    "tzdb-2026b": ("tzdb 2026b (2026-04-22): British Columbia permanent -07",
                   "https://www.iana.org/time-zones/releases/2026b"),
    "tzdb-2026c": ("tzdb 2026c (2026-07-08): Alberta permanent -06; Morocco permanent UTC 2026-09-20",
                   "https://www.iana.org/time-zones/releases/2026c"),
    "tz-theory": ("IANA tz theory.html (zone naming and stability guarantees)",
                  "https://data.iana.org/time-zones/theory.html"),
    # --- other -------------------------------------------------------
    "libical-recur-test": ("libical src/test/icalrecur_test.txt (format precedent)",
                           "https://github.com/libical/libical/blob/master/src/test/icalrecur_test.txt"),
    "dateutil-docs": ("python-dateutil rrule documentation (until+count deprecation)",
                      "https://dateutil.readthedocs.io/en/stable/rrule.html"),
    "iso8601-2": ("ISO 8601-2:2019 clause 5 repeat rules (EDTF working draft)",
                  "https://www.loc.gov/standards/datetime/"),
}

CLASSES = {"NORMATIVE", "POLICY_DEPENDENT", "DIALECT_DEPENDENT",
           "AMBIGUOUS_STANDARD", "KNOWN_DIVERGENCE", "INVALID"}

_seen_ids = set()
_vectors = []


def cite(key, quote=None, note=None):
    title, url = S[key]
    d = {"key": key, "title": title, "url": url}
    if quote:
        d["quote"] = quote
    if note:
        d["note"] = note
    return d


def V(*, id, family, title, kind, op, input, classification, expect,
      rationale, normative=(), context=None, policy_axis=None,
      dialect_axis=None, tags=(), incumbents=None):
    assert classification in CLASSES, classification
    assert id not in _seen_ids, f"duplicate id {id}"
    _seen_ids.add(id)
    ctx = {
        "tzdb_min": None,
        "tzdb_pin": None,
        "dialect": None,
        "policy": {},
        "requires": [],
    }
    if context:
        ctx.update(context)
    v = {
        "corpus_version": CORPUS_VERSION,
        "id": id,
        "family": family,
        "title": title,
        "kind": kind,
        "op": op,
        "input": input,
        "context": ctx,
        "classification": classification,
        "policy_axis": policy_axis,
        "dialect_axis": dialect_axis,
        "normative": list(normative),
        "expect": expect,
        "incumbents": incumbents or {},
        "rationale": rationale,
        "tags": list(tags),
    }
    _vectors.append(v)
    return v


# ---------------------------------------------------------------- expect
def single(occ, note=None):
    d = {"mode": "single", "occurrences": occ}
    if note:
        d["note"] = note
    return d


def cases(mode, cs, note=None):
    """cs: list of (label, when-dict, occurrences, note)."""
    d = {"mode": mode, "cases": [
        {"label": lab, "when": when, "occurrences": occ, "note": n}
        for (lab, when, occ, n) in cs]}
    if note:
        d["note"] = note
    return d


def reject(error_class, note=None):
    d = {"mode": "reject", "error_class": error_class}
    if note:
        d["note"] = note
    return d


def open_(note):
    return {"mode": "open", "note": note}


# ---------------------------------------------------------------- inputs
def cron_in(expr, start, count=5, zone=None, fields=5, inclusive=False):
    return {"kind": "cron", "expr": expr, "start": start, "count": count,
            "zone": zone, "fields": fields, "inclusive": inclusive}


def rrule_in(ics, count=6, zone=None, between=None):
    d = {"kind": "rrule", "ics": ics, "count": count, "zone": zone}
    if between:
        d["between"] = between
    return d


# ---------------------------------------------------------------- output
def write(path_dir):
    os.makedirs(path_dir, exist_ok=True)
    # Re-inject frozen incumbent measurements, if a previous run produced them.
    inc_path = os.path.join(path_dir, "incumbents.json")
    if os.path.exists(inc_path):
        with open(inc_path) as fh:
            frozen = json.load(fh)
        for v in _vectors:
            if v["id"] in frozen:
                v["incumbents"] = frozen[v["id"]]
    byfam = {}
    for v in _vectors:
        byfam.setdefault(v["family"].replace(".", "-"), []).append(v)
    manifest = {
        "corpus": "occurframe-conformance-oracle",
        "corpus_version": CORPUS_VERSION,
        "generated_utc": dt.datetime.now(dt.timezone.utc)
                           .replace(microsecond=0).isoformat(),
        "vector_count": len(_vectors),
        "files": {},
        "classification_counts": {},
        "family_counts": {},
        "sources": {k: {"title": t, "url": u} for k, (t, u) in S.items()},
    }
    for fam, vs in sorted(byfam.items()):
        fn = f"{fam}.jsonl"
        with open(os.path.join(path_dir, fn), "w") as fh:
            for v in sorted(vs, key=lambda x: x["id"]):
                fh.write(json.dumps(v, sort_keys=False, ensure_ascii=False) + "\n")
        manifest["files"][fn] = len(vs)
    for v in _vectors:
        manifest["classification_counts"][v["classification"]] = \
            manifest["classification_counts"].get(v["classification"], 0) + 1
        manifest["family_counts"][v["family"]] = \
            manifest["family_counts"].get(v["family"], 0) + 1
    with open(os.path.join(path_dir, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    return manifest
