#!/usr/bin/env python3
"""Occurframe conformance-oracle runner: Python engines.

RUNNER CONTRACT (identical in every language)
---------------------------------------------
  input   : JSONL vectors on stdin, or --vectors <file-or-dir>
  output  : JSONL results on stdout, one record per (vector, engine)
  exit 0  : the run completed; per-vector failures are RESULTS, not exit codes
  exit 1  : fatal harness error (could not read vectors, could not import)
  exit 2  : usage error

Result record fields are documented in ../docs/RUNNER-CONTRACT.md.

Engines: python-dateutil, croniter, cronsim, APScheduler 3, pandas.
Run twice to vary tzdb provenance:
    python3 run_python.py --tzdata system      # /usr/share/zoneinfo
    python3 run_python.py --tzdata vendored    # PyPI tzdata package
"""
from __future__ import annotations
import argparse
import datetime as dt
import importlib.metadata as md
import json
import os
import signal
import sys
import traceback

UTC = dt.timezone.utc
TIMEOUT_S = 8


class VectorTimeout(Exception):
    pass


def _alarm(sig, frm):
    raise VectorTimeout(f"exceeded {TIMEOUT_S}s")


signal.signal(signal.SIGALRM, _alarm)


# ------------------------------------------------------------------ formatting
def off_str(d):
    o = d.utcoffset()
    tot = int(o.total_seconds())
    s = "+" if tot >= 0 else "-"
    tot = abs(tot)
    return f"{s}{tot//3600:02d}:{(tot%3600)//60:02d}"


def fmt(d):
    if d is None:
        return "null"
    if isinstance(d, str):
        return d
    if getattr(d, "tzinfo", None) is None:
        return d.strftime("%Y-%m-%dT%H:%M:%S")
    return (d.strftime("%Y-%m-%dT%H:%M:%S") + off_str(d) + "|" +
            d.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"))


# ------------------------------------------------------------------ tz setup
def setup_tz(mode):
    import zoneinfo
    if mode == "vendored":
        sys.path.insert(0, "/home/claude/calendar-probe/vendor/tzdata/src")
        import tzdata
        zoneinfo.reset_tzpath([])
        return tzdata.IANA_VERSION, "PyPI tzdata " + tzdata.__version__
    src = None
    for p in zoneinfo.TZPATH:
        f = os.path.join(p, "tzdata.zi")
        if os.path.exists(f):
            with open(f) as fh:
                first = fh.readline().strip()
            src = p
            return first.replace("# version ", ""), src
    return "unknown", src or str(zoneinfo.TZPATH)


# ------------------------------------------------------------------ ics parse
def parse_ics(ics):
    """Split a corpus `ics` block into its properties."""
    out = {"dtstart": None, "tzid": None, "rrule": [], "exrule": [],
           "rdate": [], "exdate": [], "raw": ics}
    for line in ics.split("\n"):
        name, _, value = line.partition(":")
        params = name.split(";")
        key = params[0].upper()
        pd = {}
        for p in params[1:]:
            k, _, v = p.partition("=")
            pd[k.upper()] = v
        if key == "DTSTART":
            out["dtstart"] = value
            out["tzid"] = pd.get("TZID")
        elif key == "RRULE":
            out["rrule"].append(value)
        elif key == "EXRULE":
            out["exrule"].append(value)
        elif key == "RDATE":
            out["rdate"].append((pd, value))
        elif key == "EXDATE":
            out["exdate"].append((pd, value))
    return out


# ------------------------------------------------------------------ engines
class Engine:
    name = "?"
    version = "?"
    ops = ()

    def run(self, v):
        raise NotImplementedError


def _start_dt(v):
    s = v["input"]["start"]
    naive = dt.datetime.fromisoformat(s)
    z = v["input"].get("zone")
    if z:
        from zoneinfo import ZoneInfo
        return naive.replace(tzinfo=ZoneInfo(z))
    return naive


class Croniter(Engine):
    name = "croniter"
    ops = ("cron.next", "cron.parse")

    def __init__(self, day_or=True):
        from croniter import croniter  # noqa
        self.day_or = day_or
        self.name = "croniter" if day_or else "croniter[day_or=False]"
        self.version = "6.3.0.dev0 (git kiorky/croniter @3dd4d14 2026-08-14)"

    def run(self, v):
        from croniter import croniter
        i = v["input"]
        n = i["count"]
        it = croniter(i["expr"], _start_dt(v), day_or=self.day_or)
        return [fmt(it.get_next(dt.datetime)) for _ in range(n)]


class Cronsim(Engine):
    name = "cronsim"
    ops = ("cron.next", "cron.parse")
    version = "2.7 (git cuu508/cronsim @fd2e617, tag 2.7)"

    def run(self, v):
        from cronsim import CronSim
        i = v["input"]
        it = CronSim(i["expr"], _start_dt(v))
        out = []
        for _ in range(i["count"]):
            try:
                out.append(fmt(next(it)))
            except StopIteration:
                break
        return out


class APScheduler(Engine):
    name = "apscheduler3"
    ops = ("cron.next", "cron.parse")
    version = "3.11.3 (git agronholm/apscheduler @4308ec9, tag 3.11.3)"

    def run(self, v):
        from apscheduler.triggers.cron import CronTrigger
        from zoneinfo import ZoneInfo
        i = v["input"]
        z = i.get("zone")
        tz = ZoneInfo(z) if z else UTC
        trig = CronTrigger.from_crontab(i["expr"], timezone=tz)
        start = _start_dt(v)
        if start.tzinfo is None:
            start = start.replace(tzinfo=tz)
        out, prev = [], None
        cur = start
        for _ in range(i["count"]):
            nxt = trig.get_next_fire_time(prev, cur)
            if nxt is None:
                break
            out.append(fmt(nxt if z else nxt.replace(tzinfo=None)))
            prev, cur = nxt, nxt + dt.timedelta(seconds=1)
        return out


class DateutilRRule(Engine):
    name = "python-dateutil"
    ops = ("rrule.expand", "rrule.parse", "rrule.between")

    def __init__(self):
        self.version = md.version("python-dateutil")

    def run(self, v):
        from dateutil.rrule import rrulestr
        from dateutil.tz import gettz
        i = v["input"]
        ics = i["ics"]
        p = parse_ics(ics)
        tzids = {}
        if p["tzid"]:
            tzids[p["tzid"]] = gettz(p["tzid"])
        for pd, _ in p["exdate"] + p["rdate"]:
            if "TZID" in pd:
                tzids[pd["TZID"]] = gettz(pd["TZID"])
        rs = rrulestr(ics, forceset=True, unfold=True,
                      tzids=(lambda name: gettz(name)))
        if v["op"] == "rrule.between":
            a, b = i["between"]
            from zoneinfo import ZoneInfo
            z = i.get("zone")
            da = dt.datetime.fromisoformat(a)
            db = dt.datetime.fromisoformat(b)
            if z:
                da = da.replace(tzinfo=gettz(z))
                db = db.replace(tzinfo=gettz(z))
            return [fmt(x) for x in rs.between(da, db, inc=False)]
        out = []
        for x in rs:
            out.append(fmt(x))
            if len(out) >= i["count"]:
                break
        return out


class Pandas(Engine):
    name = "pandas"
    ops = ("rrule.expand",)

    def __init__(self):
        import pandas as pd
        self.version = pd.__version__

    def run(self, v):
        """pandas has no RRULE engine. It is included to record the exact
        boundary of what a general date-range library can express: only
        BY-part-free rules with a COUNT map onto date_range."""
        import pandas as pd
        i = v["input"]
        p = parse_ics(i["ics"])
        if len(p["rrule"]) != 1 or p["rdate"] or p["exdate"] or p["exrule"]:
            raise NotImplementedError("pandas: recurrence sets unsupported")
        parts = dict(kv.split("=", 1) for kv in p["rrule"][0].split(";"))
        if set(parts) - {"FREQ", "COUNT", "INTERVAL"}:
            raise NotImplementedError(
                "pandas: BY* / UNTIL / WKST unsupported (" +
                ",".join(sorted(set(parts) - {"FREQ", "COUNT", "INTERVAL"})) + ")")
        if "COUNT" not in parts:
            raise NotImplementedError("pandas: unbounded rules unsupported")
        freq = {"DAILY": "D", "WEEKLY": "W", "MONTHLY": "MS", "YEARLY": "YS",
                "HOURLY": "h", "MINUTELY": "min", "SECONDLY": "s"}.get(parts["FREQ"])
        if freq is None:
            raise NotImplementedError("pandas: FREQ=" + parts["FREQ"])
        iv = int(parts.get("INTERVAL", 1))
        ds = p["dtstart"]
        start = dt.datetime(int(ds[0:4]), int(ds[4:6]), int(ds[6:8]),
                            int(ds[9:11]), int(ds[11:13]), int(ds[13:15]))
        tzid = p["tzid"]
        idx = pd.date_range(start=start, periods=int(parts["COUNT"]),
                            freq=f"{iv}{freq}", tz=tzid)
        return [fmt(x.to_pydatetime()) for x in idx][:i["count"]]


# ------------------------------------------------------------------ driver
def load_vectors(path):
    files = []
    if path is None:
        return [json.loads(l) for l in sys.stdin if l.strip()]
    if os.path.isdir(path):
        files = sorted(os.path.join(path, f) for f in os.listdir(path)
                       if f.endswith(".jsonl"))
    else:
        files = [path]
    out = []
    for f in files:
        with open(f) as fh:
            for line in fh:
                if line.strip():
                    out.append(json.loads(line))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vectors")
    ap.add_argument("--out")
    ap.add_argument("--tzdata", default="system", choices=("system", "vendored"))
    ap.add_argument("--engine", action="append")
    a = ap.parse_args()

    tzdb, tzsrc = setup_tz(a.tzdata)
    try:
        vectors = load_vectors(a.vectors)
    except Exception as e:
        print(f"fatal: cannot read vectors: {e}", file=sys.stderr)
        return 1

    engines = []
    for cls, args in ((Croniter, (True,)), (Croniter, (False,)), (Cronsim, ()),
                      (APScheduler, ()), (DateutilRRule, ()), (Pandas, ())):
        try:
            e = cls(*args)
            if a.engine and e.name not in a.engine:
                continue
            engines.append(e)
        except Exception as e2:
            print(f"warn: engine {cls.__name__} unavailable: {e2}",
                  file=sys.stderr)

    out = open(a.out, "w") if a.out else sys.stdout
    lang = f"python {sys.version.split()[0]}"
    for v in vectors:
        for e in engines:
            base_op = v["op"]
            probe_op = base_op
            if base_op in ("cron.parse",):
                probe_op = "cron.next"
            if base_op in ("rrule.parse",):
                probe_op = "rrule.expand"
            if base_op not in e.ops and probe_op not in e.ops:
                rec = dict(status="unsupported_op", occurrences=[],
                           error=f"engine does not implement {base_op}")
            else:
                t0 = dt.datetime.now()
                try:
                    signal.setitimer(signal.ITIMER_REAL, TIMEOUT_S)
                    occ = e.run(v)
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    rec = dict(status="ok", occurrences=occ, error=None)
                    if occ == []:
                        rec["status"] = "empty"
                except VectorTimeout as ex:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    rec = dict(status="timeout", occurrences=[], error=str(ex))
                except NotImplementedError as ex:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    rec = dict(status="unsupported", occurrences=[],
                               error=f"{type(ex).__name__}: {ex}")
                except RecursionError as ex:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    rec = dict(status="crash", occurrences=[],
                               error=f"{type(ex).__name__}: {ex}")
                except BaseException as ex:  # engine errors are results
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    rec = dict(status="error", occurrences=[],
                               error=f"{type(ex).__name__}: {ex}".strip()[:500])
                rec["elapsed_ms"] = round(
                    (dt.datetime.now() - t0).total_seconds() * 1000, 2)
            rec.update(vector_id=v["id"], corpus_version=v["corpus_version"],
                       runner="run_python.py", engine=e.name,
                       engine_version=e.version, language=lang,
                       tzdb=tzdb, tzdb_source=str(tzsrc))
            out.write(json.dumps(rec) + "\n")
    if a.out:
        out.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
