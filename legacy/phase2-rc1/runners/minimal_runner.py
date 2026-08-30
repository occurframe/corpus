#!/usr/bin/env python3
# Proof of the format's adoption cost: a COMPLETE, conforming runner in 50
# lines of code, using only a JSON parser and the engine under test. This is
# the whole reason the corpus is JSON Lines rather than libical's bespoke
# `RRULE:/DTSTART:/INSTANCES:` text format, which needs a hand-written lexer
# in every language before a single vector can be executed.
#
#   source /home/claude/calendar-probe/env.sh
#   python3 runners/minimal_runner.py < vectors/cron-day-fields.jsonl
import datetime as dt, json, sys
from croniter import croniter                      # the engine under test

ENGINE, VERSION = "croniter", "6.3.0.dev0"

def fmt(d):
    if d.tzinfo is None:
        return d.strftime("%Y-%m-%dT%H:%M:%S")
    o = int(d.utcoffset().total_seconds())
    sign, o = ("+" if o >= 0 else "-"), abs(o)
    return (d.strftime("%Y-%m-%dT%H:%M:%S") + f"{sign}{o//3600:02d}:{(o%3600)//60:02d}"
            + "|" + d.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

def tzdb():
    try:
        return open("/usr/share/zoneinfo/tzdata.zi").readline().split()[-1]
    except OSError:
        return "unknown"

for line in sys.stdin:
    if not line.strip():
        continue
    v = json.loads(line)
    rec = {"vector_id": v["id"], "corpus_version": v["corpus_version"],
           "runner": "minimal_runner.py", "engine": ENGINE,
           "engine_version": VERSION, "language": "python",
           "tzdb": tzdb(), "tzdb_source": "/usr/share/zoneinfo"}
    if v["op"] not in ("cron.next", "cron.parse"):
        rec |= {"status": "unsupported_op", "occurrences": [], "error": None}
    else:
        i = v["input"]
        start = dt.datetime.fromisoformat(i["start"])
        if i.get("zone"):
            from zoneinfo import ZoneInfo
            start = start.replace(tzinfo=ZoneInfo(i["zone"]))
        try:
            it = croniter(i["expr"], start)
            occ = [fmt(it.get_next(dt.datetime)) for _ in range(i["count"])]
            rec |= {"status": "ok" if occ else "empty", "occurrences": occ,
                    "error": None}
        except Exception as e:                      # errors are results
            rec |= {"status": "error", "occurrences": [],
                    "error": f"{type(e).__name__}: {e}"[:500]}
    print(json.dumps(rec))
