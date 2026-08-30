"""Occurframe conformance oracle - REFERENCE cron matcher.

This is NOT an engine under test. It is an independent, policy-parameterised
reference used to *derive* the expected outcome lists that appear in the
corpus, so that expectations are computed from a declared policy rather than
copied from any incumbent (which would make the oracle circular).

Design: cron is a predicate over local wall-clock instants. We therefore
  1. enumerate candidate local *naive* datetimes that satisfy the field sets,
  2. map each candidate to an absolute instant under a declared DST policy.

Every ambiguity cron has is a named parameter here. Nothing is defaulted
silently.

Policy axes
-----------
dom_dow : how the day-of-month and day-of-week fields combine
    "vixie"   - OR when both restricted; AND when either is a literal '*'
                (the reference implementation's actual predicate, including
                the first-character DOM_STAR/DOW_STAR parser artefact)
    "or"      - OR when both fields denote a proper subset of their range
                (POSIX prose: "specified as an element or list")
    "or_text" - OR whenever neither field is the literal '*' (croner default,
                dragonmantank/cron-expression)
    "and"     - always AND (fcron dayand=true, micron strict, node-cron)
    "nth"     - dcron: "the Nth such weekday of the month", DOM gives N
    "reject"  - Quartz/AWS: both restricted is a parse error ('?' required)
dow_zero_seven :
    "both"    - 0 and 7 both denote Sunday (Vixie)
    "zero"    - 0 only; 7 out of range (POSIX)
    "quartz"  - 1=SUN .. 7=SAT (Quartz/AWS/Cloudflare)
    "monday_zero" - 0=MON .. 6=SUN, 7 rejected (APScheduler
                CronTrigger.from_crontab; NAMED days remain Sunday-based, so
                numeric and named forms disagree inside one engine)
fields : 5 | 6 | 7  and seconds_leading : bool, year_field : bool
dst_gap  : "skip" | "next_valid" | "shift_forward" | "fire_at_gap_start"
dst_fold : "first" | "second" | "both"
"""
from __future__ import annotations
import calendar
import datetime as dt
from dataclasses import dataclass, field as _f
from typing import List, Optional, Set, Tuple

MONTH_NAMES = {n.upper(): i for i, n in enumerate(
    ["", "jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"]) if n}
DOW_NAMES_STD = {"SUN": 0, "MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5, "SAT": 6}
DOW_NAMES_QUARTZ = {"SUN": 1, "MON": 2, "TUE": 3, "WED": 4, "THU": 5, "FRI": 6, "SAT": 7}


class CronRefError(ValueError):
    pass


@dataclass
class Policy:
    dom_dow: str = "vixie"
    dow_zero_seven: str = "both"
    fields: int = 5
    seconds_leading: bool = False
    year_field: bool = False
    dst_gap: str = "next_valid"
    dst_fold: str = "first"
    allow_L: bool = False
    allow_W: bool = False
    allow_hash: bool = False
    allow_qmark: bool = False


@dataclass
class FieldSpec:
    lo: int = 0
    hi: int = 0
    values: Set[int] = _f(default_factory=set)
    star: bool = False           # field text began with '*'
    literal_star: bool = False   # field text was exactly '*'
    qmark: bool = False
    last: bool = False           # 'L' alone (DOM: last day of month)
    last_offset: Optional[int] = None   # 'L-3'
    nearest_weekday: Optional[int] = None  # 'nW'
    last_weekday_of_month: bool = False    # 'LW'
    nth: List[Tuple[int, int]] = _f(default_factory=list)  # DOW '5#3' -> (dow,n)
    last_dow: List[int] = _f(default_factory=list)         # DOW '5L'


def _int(tok: str, names) -> int:
    t = tok.strip().upper()
    if names and t in names:
        return names[t]
    if not t or not (t.lstrip("-").isdigit()):
        raise CronRefError(f"not a number: {tok!r}")
    return int(t)


def parse_field(text: str, lo: int, hi: int, names=None, *, kind="generic",
                pol: Policy = Policy()) -> FieldSpec:
    text = text.strip()
    if text == "":
        raise CronRefError("empty field")
    fs = FieldSpec()
    fs.lo, fs.hi = lo, hi
    fs.star = text[0] == "*"
    fs.literal_star = text == "*"
    if text == "?":
        if not pol.allow_qmark:
            raise CronRefError("'?' not supported in this dialect")
        fs.qmark = True
        fs.star = True
        fs.values = set(range(lo, hi + 1))
        return fs
    for term in text.split(","):
        term = term.strip()
        if term == "":
            raise CronRefError("empty list element")
        step = 1
        if "/" in term:
            base, _, s = term.partition("/")
            if s == "" or not s.isdigit() or int(s) == 0:
                raise CronRefError(f"bad step {s!r}")
            step = int(s)
            term = base
        up = term.upper()
        # --- special tokens ---------------------------------------------
        if kind == "dom":
            if up == "L":
                if not pol.allow_L:
                    raise CronRefError("'L' not supported in this dialect")
                fs.last = True
                continue
            if up == "LW":
                if not (pol.allow_L and pol.allow_W):
                    raise CronRefError("'LW' not supported in this dialect")
                fs.last_weekday_of_month = True
                continue
            if up.startswith("L-"):
                if not pol.allow_L:
                    raise CronRefError("'L' not supported in this dialect")
                fs.last_offset = int(up[2:])
                continue
            if up.endswith("W"):
                if not pol.allow_W:
                    raise CronRefError("'W' not supported in this dialect")
                fs.nearest_weekday = int(up[:-1])
                continue
        if kind == "dow":
            if "#" in up:
                if not pol.allow_hash:
                    raise CronRefError("'#' not supported in this dialect")
                d, _, n = up.partition("#")
                fs.nth.append((_int(d, names), int(n)))
                continue
            if up.endswith("L") and up != "L":
                if not pol.allow_L:
                    raise CronRefError("'L' not supported in this dialect")
                fs.last_dow.append(_int(up[:-1], names))
                continue
            if up == "L":
                if not pol.allow_L:
                    raise CronRefError("'L' not supported in this dialect")
                fs.last_dow.append(names["SAT"] if names is DOW_NAMES_QUARTZ else 6)
                continue
        # --- ranges / steps ---------------------------------------------
        if term == "*":
            a, b = lo, hi
        elif "-" in term[1:]:
            aa, _, bb = term.partition("-") if term[0] != "-" else (term, "", "")
            a, b = _int(aa, names), _int(bb, names)
            if a < lo or b > hi:
                raise CronRefError(f"range {a}-{b} outside [{lo},{hi}]")
            if a > b:
                # wrapping range: Vixie rejects; some dialects wrap
                raise CronRefError(f"reversed range {a}-{b}")
        else:
            a = _int(term, names)
            if a < lo or a > hi:
                raise CronRefError(f"value {a} outside [{lo},{hi}]")
            # bare value with a step means "start at a, to end of field"
            b = hi if step > 1 else a
        for v in range(a, b + 1, step):
            fs.values.add(v)
    return fs


def _norm_dow(v: int, pol: Policy) -> int:
    """Map a field value to python weekday-sunday-0 space (0=Sun..6=Sat)."""
    if pol.dow_zero_seven == "quartz":
        return (v - 1) % 7
    if pol.dow_zero_seven == "monday_zero":
        return (v + 1) % 7          # 0=Mon .. 6=Sun  (APScheduler)
    return v % 7


@dataclass
class ParsedCron:
    sec: Optional[FieldSpec]
    minute: FieldSpec
    hour: FieldSpec
    dom: FieldSpec
    month: FieldSpec
    dow: FieldSpec
    year: Optional[FieldSpec]
    pol: Policy


def parse(expr: str, pol: Policy) -> ParsedCron:
    toks = expr.split()
    n = len(toks)
    if n != pol.fields:
        raise CronRefError(f"expected {pol.fields} fields, got {n}")
    i = 0
    sec = None
    if pol.seconds_leading:
        sec = parse_field(toks[i], 0, 59, pol=pol); i += 1
    minute = parse_field(toks[i], 0, 59, pol=pol); i += 1
    hour = parse_field(toks[i], 0, 23, pol=pol); i += 1
    dom = parse_field(toks[i], 1, 31, kind="dom", pol=pol); i += 1
    month = parse_field(toks[i], 1, 12, names=MONTH_NAMES, pol=pol); i += 1
    dow_hi = 7 if pol.dow_zero_seven in ("both", "quartz") else 6
    dow_lo = 1 if pol.dow_zero_seven == "quartz" else 0
    names = DOW_NAMES_QUARTZ if pol.dow_zero_seven == "quartz" else DOW_NAMES_STD
    dow = parse_field(toks[i], dow_lo, dow_hi, names=names, kind="dow", pol=pol); i += 1
    year = None
    if pol.year_field:
        year = parse_field(toks[i], 1970, 2199, pol=pol); i += 1
    if pol.dom_dow == "reject" and not (dom.star or dow.star):
        raise CronRefError(
            "Support for specifying both a day-of-week AND a day-of-month "
            "parameter is not implemented.")
    return ParsedCron(sec, minute, hour, dom, month, dow, year, pol)


def _dom_matches(fs: FieldSpec, d: dt.date) -> bool:
    ndays = calendar.monthrange(d.year, d.month)[1]
    if fs.last and d.day == ndays:
        return True
    if fs.last_offset is not None and d.day == ndays - fs.last_offset:
        return True
    if fs.last_weekday_of_month:
        last = dt.date(d.year, d.month, ndays)
        while last.weekday() >= 5:
            last -= dt.timedelta(days=1)
        if d == last:
            return True
    if fs.nearest_weekday is not None:
        tgt = min(fs.nearest_weekday, ndays)
        t = dt.date(d.year, d.month, tgt)
        if t.weekday() == 5:      # Sat -> Fri, unless that leaves the month
            cand = t - dt.timedelta(days=1)
            if cand.month != t.month:
                cand = t + dt.timedelta(days=2)
        elif t.weekday() == 6:    # Sun -> Mon, unless that leaves the month
            cand = t + dt.timedelta(days=1)
            if cand.month != t.month:
                cand = t - dt.timedelta(days=2)
        else:
            cand = t
        if d == cand:
            return True
    return d.day in fs.values


def _dow_matches(fs: FieldSpec, d: dt.date, pol: Policy) -> bool:
    wd = (d.weekday() + 1) % 7          # 0=Sun .. 6=Sat
    for (v, n) in fs.nth:
        if _norm_dow(v, pol) == wd and ((d.day - 1) // 7) + 1 == n:
            return True
    for v in fs.last_dow:
        ndays = calendar.monthrange(d.year, d.month)[1]
        if _norm_dow(v, pol) == wd and d.day + 7 > ndays:
            return True
    return wd in {_norm_dow(v, pol) for v in fs.values}


def _day_matches(pc: ParsedCron, d: dt.date) -> bool:
    pol = pc.pol
    if d.month not in pc.month.values:
        return False
    if pc.year is not None and d.year not in pc.year.values:
        return False
    # "restricted" has two readings. Vixie tests the field's FIRST CHARACTER
    # (pc.dom.star); POSIX's prose tests whether the field denotes an element
    # or list, i.e. whether its value set is a proper subset of the field
    # range. The corpus keeps both, because engines ship both.
    def _covers(fs):
        if fs.last or fs.last_offset is not None or fs.nearest_weekday is not None \
                or fs.last_weekday_of_month or fs.nth or fs.last_dow:
            return False
        if fs.hi - fs.lo + 1 == 7 and pol.dow_zero_seven == "both":
            return len(fs.values) >= 7
        return len(fs.values) == fs.hi - fs.lo + 1
    dom_restricted = not _covers(pc.dom)
    dow_restricted = not _covers(pc.dow)
    dm = _dom_matches(pc.dom, d)
    dw = _dow_matches(pc.dow, d, pol)
    mode = pol.dom_dow
    if mode == "reject":
        mode = "vixie"
    if mode == "vixie":
        if pc.dom.literal_star or pc.dow.literal_star or pc.dom.qmark or pc.dow.qmark:
            return dm and dw
        if pc.dom.star or pc.dow.star:   # first-char artefact: '*,10' etc.
            return dm and dw
        return dm or dw
    if mode == "or":
        # POSIX prose: "element or list" == a proper subset of the field range.
        if not dom_restricted or not dow_restricted:
            return dm and dw
        return dm or dw
    if mode == "or_text":
        # Union whenever neither field is the literal '*', regardless of what
        # the fields denote. Observed in croner (legacy mode) and
        # dragonmantank/cron-expression.
        if pc.dom.literal_star or pc.dow.literal_star:
            return dm and dw
        return dm or dw
    if mode == "and":
        return dm and dw
    if mode == "nth":
        # dcron: DOW restricted + DOM restricted -> the Nth such weekday,
        # N taken from the day-of-month values interpreted as ordinals 1..5.
        if dom_restricted and dow_restricted:
            if not dw:
                return False
            n = ((d.day - 1) // 7) + 1
            ndays = calendar.monthrange(d.year, d.month)[1]
            is_last = d.day + 7 > ndays
            return n in pc.dom.values or (is_last and 5 in pc.dom.values)
        return dm and dw
    raise CronRefError(f"unknown dom_dow policy {mode!r}")


def _times_of_day(pc: ParsedCron):
    secs = sorted(pc.sec.values) if pc.sec is not None else [0]
    for h in sorted(pc.hour.values):
        for m in sorted(pc.minute.values):
            for s in secs:
                yield h, m, s


def naive_occurrences(pc: ParsedCron, start: dt.datetime, n: int,
                      inclusive: bool = False, horizon_days: int = 366 * 12):
    """Yield the first n naive local occurrences strictly after `start`."""
    out = []
    d = start.date()
    for _ in range(horizon_days):
        if _day_matches(pc, d):
            for h, m, s in _times_of_day(pc):
                cand = dt.datetime(d.year, d.month, d.day, h, m, s)
                if cand > start or (inclusive and cand == start):
                    out.append(cand)
                    if len(out) >= n:
                        return out
        d += dt.timedelta(days=1)
    return out


# --------------------------------------------------------------- DST mapping
def to_instants(naive_list, tz, pol: Policy):
    """Map naive local wall times to aware instants under the declared policy.

    Returns a list of aware datetimes. A gap-policy of "skip" drops the
    occurrence entirely; "next_valid" fires at the first valid wall time at or
    after the nominal one; "fire_at_gap_start" fires at the instant the gap
    begins. A fold-policy of "both" emits both instants.
    """
    out = []
    for nv in naive_list:
        a = nv.replace(tzinfo=tz)
        exists = a.astimezone(dt.timezone.utc).astimezone(tz).replace(tzinfo=None) == nv
        if not exists:
            if pol.dst_gap == "skip":
                continue
            if pol.dst_gap == "fire_at_gap_start":
                probe = nv
                while True:
                    probe -= dt.timedelta(minutes=1)
                    p = probe.replace(tzinfo=tz)
                    if p.astimezone(dt.timezone.utc).astimezone(tz).replace(tzinfo=None) == probe:
                        break
                out.append((probe + dt.timedelta(minutes=1)).replace(tzinfo=tz)
                           .astimezone(dt.timezone.utc).astimezone(tz))
                continue
            probe = nv
            for _ in range(24 * 60):
                probe += dt.timedelta(minutes=1)
                p = probe.replace(tzinfo=tz)
                if p.astimezone(dt.timezone.utc).astimezone(tz).replace(tzinfo=None) == probe:
                    out.append(p)
                    break
            continue
        f0 = nv.replace(tzinfo=tz, fold=0)
        f1 = nv.replace(tzinfo=tz, fold=1)
        ambiguous = f0.utcoffset() != f1.utcoffset()
        if ambiguous:
            if pol.dst_fold == "first":
                out.append(f0)
            elif pol.dst_fold == "second":
                out.append(f1)
            else:
                out.append(f0); out.append(f1)
        else:
            out.append(f0)
    return out


def fmt(d: dt.datetime) -> str:
    if d.tzinfo is None:
        return d.strftime("%Y-%m-%dT%H:%M:%S")
    loc = d.strftime("%Y-%m-%dT%H:%M:%S") + _off(d)
    utc = d.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{loc}|{utc}"


def _off(d):
    o = d.utcoffset()
    if o is None:
        return ""
    tot = int(o.total_seconds())
    sign = "+" if tot >= 0 else "-"
    tot = abs(tot)
    return f"{sign}{tot//3600:02d}:{(tot%3600)//60:02d}"


def run(expr: str, pol: Policy, start_naive: dt.datetime, n: int, tz=None,
        inclusive: bool = False) -> List[str]:
    pc = parse(expr, pol)
    naive = naive_occurrences(pc, start_naive, n if tz is None else n * 3 + 8,
                              inclusive=inclusive)
    if tz is None:
        return [fmt(x) for x in naive[:n]]
    return [fmt(x) for x in to_instants(naive, tz, pol)[:n]]
