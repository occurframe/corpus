"""RRULE vectors for the Occurframe conformance oracle.

Expected outcome lists here are NOT produced by any recurrence engine. They
are either (a) transcribed from RFC 5545 §3.8.5.3's own worked examples, whose
printed instance lists are part of the specification text, or (b) derived by
plain calendar arithmetic (`datetime` + `zoneinfo`) from a rule the RFC states
in prose. Every transcription is re-checked below by structural assertions
(weekday, day-of-month, month, ordinal position) so a typo cannot survive the
build.
"""
from __future__ import annotations
import calendar
import datetime as dt
from zoneinfo import ZoneInfo

from common import V, cite, single, cases, reject, open_, rrule_in

NY = "America/New_York"


def _fmt_zoned(tzid, stamp):
    tz = ZoneInfo(tzid)
    y, mo, d = int(stamp[0:4]), int(stamp[4:6]), int(stamp[6:8])
    h, mi, s = int(stamp[9:11]), int(stamp[11:13]), int(stamp[13:15])
    a = dt.datetime(y, mo, d, h, mi, s, tzinfo=tz)
    off = a.utcoffset()
    tot = int(off.total_seconds())
    sign = "+" if tot >= 0 else "-"
    tot = abs(tot)
    loc = a.strftime("%Y-%m-%dT%H:%M:%S") + f"{sign}{tot//3600:02d}:{(tot%3600)//60:02d}"
    utc = a.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{loc}|{utc}"


def occ(tzid, *stamps):
    """Format iCalendar local stamps (YYYYMMDDTHHMMSS) in a zone."""
    if tzid is None:
        return [f"{s[0:4]}-{s[4:6]}-{s[6:8]}T{s[9:11]}:{s[11:13]}:{s[13:15]}"
                for s in stamps]
    return [_fmt_zoned(tzid, s) for s in stamps]


WD = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}


def assert_weekday(stamps, code):
    for s in stamps:
        d = dt.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
        assert d.weekday() == WD[code], f"{s} is not a {code}"


def assert_dom(stamps, days):
    for s in stamps:
        assert int(s[6:8]) in days, f"{s} day-of-month not in {days}"


def build():
    # =================================================================
    # FAMILY: rrule.core -- DTSTART, COUNT, UNTIL
    # =================================================================
    daily10 = ["199709%02dT090000" % d for d in range(2, 12)]
    V(id="RRULE-CORE-001", family="rrule.core",
      title="RFC 5545 §3.8.5.3 worked example: daily for 10 occurrences",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=10", count=12, zone=NY),
      classification="NORMATIVE",
      context={"tzdb_min": "2025c", "requires": ["tz.zoneinfo"]},
      normative=[cite("rfc5545-3.8.5.3",
                      "Daily for 10 occurrences: ... ==> (1997 9:00 AM EDT) "
                      "September 2-11")],
      expect=single(occ(NY, *daily10),
                    "DTSTART is synchronised with the rule and is the first "
                    "instance; COUNT includes it."),
      rationale="The corpus's control vector: if an engine fails this, nothing "
                "else it reports is interpretable.",
      tags=["count", "control"])

    V(id="RRULE-CORE-002", family="rrule.core",
      title="COUNT includes DTSTART when DTSTART matches the rule",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=1", count=3, zone=NY),
      classification="NORMATIVE",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "The COUNT rule part defines the number of occurrences at "
                      "which to range-bound the recurrence."),
                 cite("rfc8984-4.3.3",
                      "the start date-time ... is always the first occurrence "
                      "in the expansion",
                      note="JSCalendar legislates what RFC 5545 leaves to "
                           "inference")],
      expect=single(occ(NY, "19970902T090000")),
      rationale="Isolates the 'does COUNT count DTSTART' question from every "
                "other variable.",
      tags=["count"])

    V(id="RRULE-CORE-003", family="rrule.core",
      title="DTSTART unsynchronised with the rule (the RFC calls this undefined)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=MONTHLY;BYDAY=FR;BYMONTHDAY=13;COUNT=4",
                     count=5, zone=NY),
      classification="AMBIGUOUS_STANDARD",
      policy_axis="rrule.dtstart_emission",
      context={"tzdb_min": "2025c"},
      normative=[
          cite("rfc5545-3.8.5.3",
               "If the specified recurrence rule does not include the start "
               "date-time, then the recurrence instances ... are undefined."),
          cite("eid5920",
               note="REJECTED, on the ground that 'the original example "
                    "intentionally demonstrates the EXDATE feature by "
                    "excluding the first occurrence' — which presupposes "
                    "DTSTART *is* emitted. The RFC Editor thereby endorsed the "
                    "emit reading inside an errata rejection note, which has "
                    "no normative standing."),
          cite("rfc8984-4.3.3",
               "the start date-time ... is always the first occurrence in the "
               "expansion ... even if it would normally not match the rule"),
      ],
      expect=cases("admissible", [
          ("emit-dtstart", {"rrule.dtstart_emission": "always"},
           occ(NY, "19970902T090000", "19980213T090000", "19980313T090000",
               "19981113T090000"),
           "DTSTART is emitted as instance 1 even though 1997-09-02 is a "
           "Tuesday and not the 13th. This is JSCalendar's legislated "
           "behaviour and the reading the RFC's own Friday-the-13th example "
           "(which EXDATEs DTSTART away) presupposes."),
          ("rule-only", {"rrule.dtstart_emission": "if_matching"},
           occ(NY, "19980213T090000", "19980313T090000", "19981113T090000",
               "19990813T090000"),
           "DTSTART is a seed only; the set contains rule matches at or after "
           "it. python-dateutil, rrule.js and most engines behave this way."),
          ("reject", {"rrule.dtstart_emission": "reject"}, None,
           "Refuse the rule as undefined per the literal text of §3.8.5.3."),
      ], "Three readings, one of which the RFC's own example depends on and "
         "another of which it declares undefined."),
      rationale=("DTSTART's role is the deepest under-specification in RFC "
                 "5545. §3.8.5.3 says the case is undefined; the same section "
                 "prints an example that only works if DTSTART is emitted; "
                 "erratum 5920's rejection entrenches the contradiction; "
                 "RFC 8984 fixes it in the opposite direction to the "
                 "ecosystem. Manufacturing a single answer here would be "
                 "dishonest."),
      tags=["dtstart", "headline"])

    V(id="RRULE-CORE-004", family="rrule.core",
      title="RFC 5545's Friday-the-13th example verbatim, with its EXDATE",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     f"EXDATE;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=MONTHLY;BYDAY=FR;BYMONTHDAY=13", count=5,
                     zone=NY),
      classification="NORMATIVE",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "Every Friday the 13th, forever: ... ==> (1998 9:00 AM "
                      "EST) February 13;March 13;November 13 (1999 9:00 AM "
                      "EDT) August 13 (2000 9:00 AM EDT) October 13"),
                 cite("eid5920", note="a proposal to delete this EXDATE was "
                                      "rejected")],
      expect=single(occ(NY, "19980213T090000", "19980313T090000",
                        "19981113T090000", "19990813T090000",
                        "20001013T090000"),
                    "Under either DTSTART reading the EXDATE removes the "
                    "1997-09-02 seed, so this vector is decidable where "
                    "RRULE-CORE-003 is not."),
      rationale=("Deliberately paired with CORE-003: the same rule becomes "
                 "NORMATIVE once the EXDATE removes the contested instance. "
                 "The pair localises the ambiguity precisely."),
      tags=["dtstart", "exdate", "byday", "bymonthday"])
    assert_weekday(["19980213T090000", "19980313T090000", "19981113T090000",
                    "19990813T090000", "20001013T090000"], "FR")
    assert_dom(["19980213T090000", "19980313T090000", "19981113T090000",
                "19990813T090000", "20001013T090000"], {13})

    V(id="RRULE-CORE-005", family="rrule.core",
      title="UNTIL is inclusive when it names an instance exactly",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=DAILY;UNTIL=19970904T130000Z", count=6,
                     zone=NY),
      classification="NORMATIVE",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "If the value specified by UNTIL is synchronized with the "
                      "specified recurrence, this DATE or DATE-TIME becomes the "
                      "last instance of the recurrence.")],
      expect=single(occ(NY, "19970902T090000", "19970903T090000",
                        "19970904T090000"),
                    "1997-09-04T09:00 EDT is 13:00Z, exactly UNTIL, and is "
                    "therefore included."),
      rationale="Inclusivity is stated normatively and is still implemented as "
                "exclusive by some engines; it is cheap to test and decisive.",
      tags=["until"])

    V(id="RRULE-CORE-006", family="rrule.core",
      title="UNTIL one second before an instance excludes it", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=DAILY;UNTIL=19970904T125959Z", count=6,
                     zone=NY),
      classification="NORMATIVE",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10")],
      expect=single(occ(NY, "19970902T090000", "19970903T090000")),
      rationale="The exclusive half of the UNTIL boundary; the pair pins the "
                "comparison operator exactly.",
      tags=["until"])

    V(id="RRULE-CORE-007", family="rrule.core",
      title="UNTIL must be UTC when DTSTART carries a TZID (erratum 3883's "
            "example, corrected)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=HOURLY;INTERVAL=3;UNTIL=19970902T210000Z",
                     count=8, zone=NY),
      classification="NORMATIVE",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "if the 'DTSTART' property is specified as a date with "
                      "local time and time zone reference, then the UNTIL rule "
                      "part MUST be specified as a date with UTC time"),
                 cite("eid3883",
                      "UNTIL=19970902T170000Z terminates at 1:00 PM EDT, not "
                      "5:00 PM; the correct value is UNTIL=19970902T210000Z")],
      expect=single(occ(NY, "19970902T090000", "19970902T120000",
                        "19970902T150000")),
      rationale=("The RFC's own authors got this wrong in a printed example, "
                 "and two further errata (5872, 6212) are readers getting it "
                 "wrong in the opposite direction. One correct and two "
                 "incorrect errata against UNTIL-in-UTC examples is direct "
                 "evidence that the local-time/UTC boundary is a "
                 "comprehension trap."),
      tags=["until", "utc-coupling", "headline"])

    V(id="RRULE-CORE-008", family="rrule.core",
      title="The uncorrected erratum-3883 example (UNTIL=...T170000Z)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=HOURLY;INTERVAL=3;UNTIL=19970902T170000Z",
                     count=8, zone=NY),
      classification="NORMATIVE",
      context={"tzdb_min": "2025c"},
      normative=[cite("eid3883", note="Verified, Technical")],
      expect=single(occ(NY, "19970902T090000", "19970902T120000"),
                    "17:00Z is 13:00 EDT, so only 09:00 and 12:00 local are "
                    "in range — the behaviour the erratum exists to explain."),
      rationale="Paired with CORE-007 so an engine that silently reads UNTIL "
                "as local time is caught: it would emit five instances here "
                "instead of two.",
      tags=["until", "utc-coupling", "discriminator"])

    V(id="RRULE-CORE-009", family="rrule.core",
      title="UNTIL with a floating DTSTART must be floating", kind="rrule",
      op="rrule.expand",
      input=rrule_in("DTSTART:19970902T090000\n"
                     "RRULE:FREQ=DAILY;UNTIL=19970904T090000", count=6),
      classification="NORMATIVE",
      normative=[cite("rfc5545-3.3.10",
                      "if the 'DTSTART' property is specified as a date with "
                      "local time, then the UNTIL rule part MUST also be "
                      "specified as a date with local time")],
      expect=single(occ(None, "19970902T090000", "19970903T090000",
                        "19970904T090000")),
      rationale="The floating branch of the UNTIL value-type coupling; engines "
                "that normalise everything to UTC internally get this wrong.",
      tags=["until", "floating"])

    V(id="RRULE-CORE-010", family="rrule.core",
      title="UNTIL value type mismatched with DTSTART (Z on a floating start)",
      kind="rrule", op="rrule.parse",
      input=rrule_in("DTSTART:19970902T090000\n"
                     "RRULE:FREQ=DAILY;UNTIL=19970904T130000Z", count=6),
      classification="INVALID",
      normative=[cite("rfc5545-3.3.10",
                      "The value of the UNTIL rule part MUST have the same "
                      "value type as the 'DTSTART' property.")],
      expect=reject("until_value_type_mismatch",
                    "MUST-level requirement. Engines that coerce silently "
                    "produce a set the author did not write."),
      rationale="A MUST that the ABNF cannot enforce, so it is hand-checked or "
                "not checked at all.",
      tags=["until", "invalid"])

    V(id="RRULE-CORE-011", family="rrule.core",
      title="COUNT and UNTIL in the same RRULE (forbidden)", kind="rrule",
      op="rrule.parse",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=10;UNTIL=19970904T130000Z",
                     count=12, zone=NY),
      classification="INVALID",
      normative=[cite("rfc5545-3.3.10",
                      "The UNTIL rule part and the COUNT rule part MUST NOT "
                      "occur in the same 'recur'.",
                      note="stated only in an ABNF comment, which no generated "
                           "parser can enforce"),
                 cite("dateutil-docs",
                      note="python-dateutil deprecated accepting both 'to make "
                           "sure dateutil is fully compliant with RFC-5545'")],
      expect=reject("count_and_until",
                    "MUST NOT. Admissible non-conformant behaviours observed "
                    "in the wild: apply whichever bound is hit first; ignore "
                    "UNTIL; ignore COUNT; emit a deprecation warning and "
                    "proceed. All are failures against this vector."),
      rationale=("The only MUST NOT in §3.3.10 expressed exclusively as an "
                 "ABNF comment. It is the clearest example of a constraint the "
                 "grammar cannot carry, and therefore of why a conformance "
                 "corpus is needed at all."),
      tags=["count", "until", "invalid", "headline"])

    V(id="RRULE-CORE-012", family="rrule.core",
      title="INTERVAL counts periods from DTSTART, not from the calendar",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5", count=6, zone=NY),
      classification="NORMATIVE",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "Every 10 days, 5 occurrences: ... ==> (1997 9:00 AM EDT) "
                      "September 2,12,22;October 2,12")],
      expect=single(occ(NY, "19970902T090000", "19970912T090000",
                        "19970922T090000", "19971002T090000",
                        "19971012T090000")),
      rationale=("The direct counterpart of CRON-ANCH-004: RRULE's INTERVAL is "
                 "anchored to DTSTART and crosses month boundaries; cron's "
                 "step is anchored to the field's low bound and resets. The "
                 "two vectors together define the gap any unified model must "
                 "bridge."),
      tags=["interval", "anchoring", "cross-grammar"])

    V(id="RRULE-CORE-013", family="rrule.core",
      title="Infinite recurrence with no COUNT and no UNTIL", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=DAILY", count=5, zone=NY),
      classification="POLICY_DEPENDENT", policy_axis="rrule.truncation",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "If neither the COUNT nor UNTIL rule parts are present, "
                      "the recurrence rule is considered to repeat forever.")],
      expect=cases("per_policy", [
          ("lazy-iterator", {"rrule.truncation": "lazy"},
           occ(NY, "19970902T090000", "19970903T090000", "19970904T090000",
               "19970905T090000", "19970906T090000"),
           "The engine returns a lazy sequence and the caller takes 5. The "
           "only behaviour that composes with a scheduler."),
          ("caller-bounded", {"rrule.truncation": "caller_window"},
           occ(NY, "19970902T090000", "19970903T090000", "19970904T090000",
               "19970905T090000", "19970906T090000"),
           "The engine requires an explicit window and returns the same "
           "prefix."),
          ("materialise", {"rrule.truncation": "materialise"}, None,
           "Engines whose only API materialises the whole set hang or "
           "exhaust memory. Recorded as a result, not excused."),
      ], "'Repeats forever' is normative; what an API does with it is not."),
      rationale=("RFC 5545 places no bound on expansion cost. Every practical "
                 "engine must therefore add a policy the standard does not "
                 "define, and the corpus records which one."),
      tags=["truncation", "policy"])

    V(id="RRULE-CORE-014", family="rrule.core",
      title="Bounded-range query over an infinite rule (between semantics)",
      kind="rrule", op="rrule.between",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=DAILY", count=10, zone=NY,
                     between=["1997-09-04T09:00:00", "1997-09-06T09:00:00"]),
      classification="POLICY_DEPENDENT", policy_axis="rrule.range_inclusivity",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      note="the RFC defines a recurrence *set*; it defines no "
                           "range query, so endpoint inclusivity is entirely a "
                           "library invention")],
      expect=cases("per_policy", [
          ("closed", {"rrule.range_inclusivity": "[a,b]"},
           occ(NY, "19970904T090000", "19970905T090000", "19970906T090000"),
           "dateutil rruleset.between(inc=True); Luxon Interval "
           "containses."),
          ("half-open", {"rrule.range_inclusivity": "[a,b)"},
           occ(NY, "19970904T090000", "19970905T090000"),
           "The convention most range APIs use elsewhere in the same "
           "codebases."),
          ("open", {"rrule.range_inclusivity": "(a,b)"},
           occ(NY, "19970905T090000"),
           "dateutil rruleset.between(inc=False), the default."),
      ], "Three inclusivity conventions ship, and one library (dateutil) "
         "defaults to the rarest of them."),
      rationale=("Range queries are how every scheduler actually consumes a "
                 "recurrence, and the endpoints are exactly where "
                 "double-firing and missed-firing bugs live. The RFC is "
                 "silent, so this is POLICY_DEPENDENT by construction."),
      tags=["range", "policy", "headline"])

    V(id="RRULE-CORE-015", family="rrule.core",
      title="FREQ missing", kind="rrule", op="rrule.parse",
      input=rrule_in("DTSTART:19970902T090000\nRRULE:COUNT=5", count=5),
      classification="INVALID",
      normative=[cite("rfc5545-3.3.10",
                      "The FREQ rule part ... This rule part MUST be specified "
                      "in the recurrence rule.")],
      expect=reject("missing_freq"),
      rationale="The only unconditionally required rule part.",
      tags=["invalid"])

    V(id="RRULE-CORE-016", family="rrule.core",
      title="INTERVAL=0", kind="rrule", op="rrule.parse",
      input=rrule_in("DTSTART:19970902T090000\n"
                     "RRULE:FREQ=DAILY;INTERVAL=0;COUNT=3", count=3),
      classification="INVALID",
      normative=[cite("rfc5545-3.3.10",
                      "The INTERVAL rule part ... contains a positive integer "
                      "representing at which intervals the recurrence rule "
                      "repeats.")],
      expect=reject("interval_not_positive",
                    "Observed failure modes include an infinite loop and a "
                    "silent coercion to 1."),
      rationale="A crash-class vector on a MUST-shaped word ('positive').",
      tags=["invalid"])

    V(id="RRULE-CORE-017", family="rrule.core",
      title="COUNT=0", kind="rrule", op="rrule.expand",
      input=rrule_in("DTSTART:19970902T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=0", count=3),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.count_zero",
      normative=[cite("rfc5545-3.3.10",
                      "COUNT ... defines the number of occurrences at which to "
                      "range-bound the recurrence",
                      note="the ABNF is 1*DIGIT, which admits 0; the prose "
                           "does not say whether 0 is legal")],
      expect=cases("admissible", [
          ("empty", {"rrule.count_zero": "empty"}, [],
           "Zero occurrences — the literal reading."),
          ("reject", {"rrule.count_zero": "reject"}, None,
           "Treat 0 as out of range."),
          ("dtstart-only", {"rrule.count_zero": "dtstart"},
           occ(None, "19970902T090000"),
           "Engines that always emit DTSTART first and then apply COUNT."),
      ]),
      rationale="The ABNF admits a value the prose never contemplates; three "
                "behaviours ship.",
      tags=["count", "empty-set"])

    V(id="RRULE-CORE-018", family="rrule.core",
      title="UNTIL earlier than DTSTART (empty recurrence set)", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970902T090000\n"
                     "RRULE:FREQ=DAILY;UNTIL=19970901T130000Z", count=3,
                     zone=NY),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.empty_set",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10", note="no statement about an UNTIL that "
                                             "precedes DTSTART")],
      expect=cases("admissible", [
          ("empty", {"rrule.empty_set": "empty"}, [],
           "The set is empty; the caller sees no occurrences."),
          ("dtstart-only", {"rrule.empty_set": "dtstart"},
           occ(NY, "19970902T090000"),
           "Engines that emit DTSTART unconditionally before applying UNTIL."),
          ("reject", {"rrule.empty_set": "reject"}, None,
           "Reject at parse time."),
      ], "The empty recurrence set is under-specified identically in both "
         "grammars; compare CRON-INV-007."),
      rationale=("Paired deliberately with the cron empty-set vectors. A "
                 "product that promises 'never silently empty' has to answer "
                 "this in both grammars with the same policy."),
      tags=["empty-set", "until"])

    # =================================================================
    # FAMILY: rrule.by  -- BY* rule parts
    # =================================================================
    fr1 = ["19970905T090000", "19971003T090000", "19971107T090000",
           "19971205T090000", "19980102T090000", "19980206T090000",
           "19980306T090000", "19980403T090000", "19980501T090000",
           "19980605T090000"]
    assert_weekday(fr1, "FR")
    for s in fr1:
        assert int(s[6:8]) <= 7, s
    V(id="RRULE-BY-001", family="rrule.by",
      title="Monthly on the first Friday for 10 occurrences (RFC example)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970905T090000\n"
                     "RRULE:FREQ=MONTHLY;COUNT=10;BYDAY=1FR", count=12, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "Monthly on the first Friday for 10 occurrences")],
      expect=single(occ(NY, *fr1)),
      rationale="The nth-weekday control vector; also the direct counterpart "
                "of cron '#'.",
      tags=["byday", "nth-weekday", "cross-grammar"])

    mo2last = ["19970922T090000", "19971020T090000", "19971117T090000",
               "19971222T090000"]
    assert_weekday(mo2last, "MO")
    V(id="RRULE-BY-002", family="rrule.by",
      title="Monthly on the second-to-last Monday (RFC example)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970922T090000\n"
                     "RRULE:FREQ=MONTHLY;BYDAY=-2MO;COUNT=4", count=6, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "Monthly on the second-to-last Monday of the month for 6 "
                      "months")],
      expect=single(occ(NY, *mo2last)),
      rationale="Negative ordinals are the construct cron cannot express at "
                "all beyond 'L'; this is where the grammars stop being "
                "translatable.",
      tags=["byday", "negative-ordinal", "cross-grammar"])

    V(id="RRULE-BY-003", family="rrule.by",
      title="BYDAY=5SU in months that have only four Sundays", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260101T090000\n"
                     "RRULE:FREQ=MONTHLY;BYDAY=5SU;COUNT=5", count=6, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "If the BYDAY rule part is specified with a numeric "
                      "value ... it MUST only be used in conjunction with "
                      "either the MONTHLY or YEARLY 'FREQ'",
                      note="a month without a 5th Sunday simply contributes no "
                           "instance; the RFC never clamps"),
               ],
      expect=single(occ(NY, "20260329T090000", "20260531T090000",
                        "20260830T090000", "20261129T090000",
                        "20270131T090000"),
                    "Months without a fifth Sunday are skipped. Silent "
                    "clamping to the last Sunday is a conformance failure and "
                    "is observed."),
      rationale=("Directly paired with CRON-EXT-007 (SUN#5). Both grammars "
                 "specify skip; both have implementations that clamp; a user "
                 "who wanted 'last Sunday' gets a schedule that fires 5 times "
                 "a year in one engine and 12 in another."),
      tags=["byday", "nth-weekday", "cross-grammar", "headline"])
    assert_weekday(["20260329T090000", "20260531T090000", "20260830T090000",
                    "20261129T090000", "20270131T090000"], "SU")
    for s in ["20260329T090000", "20260531T090000", "20260830T090000",
              "20261129T090000", "20270131T090000"]:
        assert (int(s[6:8]) - 1) // 7 + 1 == 5, s

    V(id="RRULE-BY-004", family="rrule.by",
      title="BYDAY=-1SU (last Sunday) never skips a month", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260101T090000\n"
                     "RRULE:FREQ=MONTHLY;BYDAY=-1SU;COUNT=5", count=6, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "-1MO represents the last Monday of the month")],
      expect=single(occ(NY, "20260125T090000", "20260222T090000",
                        "20260329T090000", "20260426T090000",
                        "20260531T090000")),
      rationale="The correct spelling of what most authors of BYDAY=5SU "
                "actually meant; paired with BY-003 it quantifies the cost of "
                "the mistake.",
      tags=["byday", "negative-ordinal"])
    assert_weekday(["20260125T090000", "20260222T090000", "20260329T090000",
                    "20260426T090000", "20260531T090000"], "SU")

    V(id="RRULE-BY-005", family="rrule.by",
      title="BYMONTHDAY=31: months without a 31st are omitted", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260131T090000\n"
                     "RRULE:FREQ=MONTHLY;BYMONTHDAY=31;COUNT=6", count=8,
                     zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "Recurrence instances falling on invalid dates and times "
                      "are ignored and not counted as part of the recurrence "
                      "set."),
                 cite("eid4271",
                      note="splits that sentence: invalid *dates* keep the "
                           "MUST-ignore treatment; nonexistent *local times* "
                           "are routed to §3.3.5 instead")],
      expect=single(occ(NY, "20260131T090000", "20260331T090000",
                        "20260531T090000", "20260731T090000",
                        "20260831T090000", "20261031T090000"),
                    "Seven months a year, not twelve. Contrast Stripe's "
                    "billing anchor, which bills the last day of the month "
                    "instead, and relativedelta/Temporal 'constrain', which "
                    "clamp to the 28th/30th."),
      rationale=("The single most consequential month-end divergence in the "
                 "corpus, because three defensible semantics exist — omit "
                 "(RFC), clamp (Temporal constrain, relativedelta, Stripe), "
                 "drift (naive iterated addition) — and only the first is "
                 "RFC-conformant."),
      tags=["bymonthday", "month-end", "headline"])

    V(id="RRULE-BY-006", family="rrule.by",
      title="BYMONTHDAY=30: February always omitted", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260130T090000\n"
                     "RRULE:FREQ=MONTHLY;BYMONTHDAY=30;COUNT=5", count=7,
                     zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10")],
      expect=single(occ(NY, "20260130T090000", "20260330T090000",
                        "20260430T090000", "20260530T090000",
                        "20260630T090000")),
      rationale="Separates 'omitted in 5 months' (31) from 'omitted in 1 "
                "month' (30); engines with a special case for 31 fail here.",
      tags=["bymonthday", "month-end"])

    V(id="RRULE-BY-007", family="rrule.by",
      title="BYMONTHDAY=29: February appears only in leap years", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20270129T090000\n"
                     "RRULE:FREQ=MONTHLY;BYMONTHDAY=29;COUNT=14", count=16,
                     zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10")],
      expect=single(occ(NY, "20270129T090000", "20270329T090000",
                        "20270429T090000", "20270529T090000",
                        "20270629T090000", "20270729T090000",
                        "20270829T090000", "20270929T090000",
                        "20271029T090000", "20271129T090000",
                        "20271229T090000", "20280129T090000",
                        "20280229T090000", "20280329T090000"),
                    "2027 is not a leap year so February is skipped; 2028 is, "
                    "so 2028-02-29 is included."),
      rationale="The leap-year boundary inside a monthly rule; catches engines "
                "whose month-length table is hard-coded.",
      tags=["bymonthday", "leap-year"])

    V(id="RRULE-BY-008", family="rrule.by",
      title="BYMONTHDAY=-1 (last day of month) never skips", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20270131T090000\n"
                     "RRULE:FREQ=MONTHLY;BYMONTHDAY=-1;COUNT=5", count=6,
                     zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "-10 represents the tenth to the last day of the month")],
      expect=single(occ(NY, "20270131T090000", "20270228T090000",
                        "20270331T090000", "20270430T090000",
                        "20270531T090000")),
      rationale="The correct spelling of 'end of month'; paired with BY-005 it "
                "shows the RFC does have the construct users reach for.",
      tags=["bymonthday", "month-end", "negative-ordinal"])

    V(id="RRULE-BY-009", family="rrule.by",
      title="BYMONTHDAY=1,-1 (first and last day, RFC example)", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970930T090000\n"
                     "RRULE:FREQ=MONTHLY;BYMONTHDAY=1,-1;COUNT=5", count=6,
                     zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "Monthly on the first and last day of the month for 10 "
                      "occurrences")],
      expect=single(occ(NY, "19970930T090000", "19971001T090000",
                        "19971031T090000", "19971101T090000",
                        "19971130T090000"),
                    "Positive and negative day numbers are merged and sorted "
                    "within each month."),
      rationale="Mixed-sign lists are where ordering bugs surface.",
      tags=["bymonthday", "negative-ordinal"])

    V(id="RRULE-BY-010", family="rrule.by",
      title="Yearly on 29 February", kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20240229T090000\n"
                     "RRULE:FREQ=YEARLY;BYMONTH=2;BYMONTHDAY=29;COUNT=3",
                     count=4, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "Recurrence instances falling on invalid dates ... are "
                      "ignored"),
                 cite("rfc7529",
                      note="RFC 7529 adds SKIP=OMIT|BACKWARD|FORWARD precisely "
                           "because RFC 5545 offers only OMIT; eleven years "
                           "on, the flagship JS RRULE library's documentation "
                           "does not mention RSCALE at all")],
      expect=single(occ(NY, "20240229T090000", "20280229T090000",
                        "20320229T090000"),
                    "Four-year gaps. A 'yearly' event that fires every four "
                    "years is correct RFC 5545 and almost never what the "
                    "author meant."),
      rationale=("The canonical leap-day vector, and the entry point to "
                 "RFC 7529: SKIP=BACKWARD would give 28 Feb and SKIP=FORWARD "
                 "1 Mar, but neither is available without RSCALE."),
      tags=["leap-year", "yearly", "rfc7529", "headline"])

    V(id="RRULE-BY-011", family="rrule.by",
      title="Yearly on 29 February with RSCALE and SKIP=BACKWARD (RFC 7529)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20240229T090000\n"
                     "RRULE:RSCALE=GREGORIAN;FREQ=YEARLY;SKIP=BACKWARD;COUNT=3",
                     count=4, zone=NY),
      classification="DIALECT_DEPENDENT", policy_axis="rrule.rscale_support",
      dialect_axis="rrule.profile", context={"tzdb_min": "2025c"},
      normative=[cite("rfc7529",
                      "SKIP=BACKWARD ... the date is set to the closest "
                      "preceding valid date")],
      expect=cases("per_dialect", [
          ("rfc7529", {"rrule.rscale_support": "yes"},
           occ(NY, "20240229T090000", "20250228T090000", "20260228T090000"),
           "Engines implementing RFC 7529."),
          ("ignore-unknown-parts", {"rrule.rscale_support": "ignore"},
           occ(NY, "20240229T090000", "20280229T090000", "20320229T090000"),
           "Engines that silently drop RSCALE and SKIP fall back to OMIT — "
           "the most dangerous outcome, because the rule parses and produces "
           "a plausible but different set."),
          ("reject", {"rrule.rscale_support": "no"}, None,
           "Engines that reject unknown rule parts."),
      ]),
      rationale=("RFC 7529 is eleven years old and effectively unimplemented "
                 "outside CalDAV servers. The 'silently ignore' outcome is the "
                 "reason this vector exists: unknown-rule-part handling is "
                 "itself an unspecified policy."),
      tags=["rfc7529", "leap-year", "unknown-parts"])

    V(id="RRULE-BY-012", family="rrule.by",
      title="BYSETPOS=3 over BYDAY=TU,WE,TH (RFC example)", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970904T090000\n"
                     "RRULE:FREQ=MONTHLY;BYDAY=TU,WE,TH;BYSETPOS=3;COUNT=3",
                     count=4, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "The third instance into the month of one of Tuesday, "
                      "Wednesday, or Thursday, for the next 3 months: ... "
                      "==> (1997 9:00 AM EDT) September 4;October 7;November 6")],
      expect=single(occ(NY, "19970904T090000", "19971007T090000",
                        "19971106T090000")),
      rationale="BYSETPOS is applied last, over the whole period's candidate "
                "set; engines that apply it per-BYDAY-value produce a "
                "different set entirely.",
      tags=["bysetpos"])

    setpos2 = ["19970929T090000", "19971030T090000", "19971127T090000",
               "19971230T090000", "19980129T090000", "19980226T090000",
               "19980330T090000"]
    for s in setpos2:
        d = dt.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
        assert d.weekday() < 5, s
    V(id="RRULE-BY-013", family="rrule.by",
      title="BYSETPOS=-2 (second-to-last weekday of the month, RFC example)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970929T090000\n"
                     "RRULE:FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-2;"
                     "COUNT=7", count=8, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "The second-to-last weekday of the month: ... ==> "
                      "September 29;October 30;November 27;December 30;"
                      "January 29;February 26;March 30")],
      expect=single(occ(NY, *setpos2)),
      rationale="Negative BYSETPOS plus a five-value BYDAY is the standard "
                "business-day idiom and the most common BYSETPOS in the wild.",
      tags=["bysetpos", "business-day"])

    V(id="RRULE-BY-014", family="rrule.by",
      title="BYSETPOS with FREQ=WEEKLY (a period with at most 7 candidates)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;BYSETPOS=-1;COUNT=4",
                     count=5, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "BYSETPOS ... specify the nth occurrence within the set "
                      "of recurrence instances specified by the rule ... "
                      "corresponding to the last day of the week")],
      expect=single(occ(NY, "20260109T090000", "20260116T090000",
                        "20260123T090000", "20260130T090000"),
                    "With WKST defaulting to MO, the weekly period is Mon-Sun "
                    "and the last of {Mon,Wed,Fri} is Friday. DTSTART "
                    "2026-01-05 is a Monday and is NOT in the set, so this "
                    "vector also probes DTSTART emission."),
      rationale="BYSETPOS interacts with WKST through the definition of the "
                "period; few engines test this combination.",
      tags=["bysetpos", "wkst"])
    assert_weekday(["20260109T090000", "20260116T090000", "20260123T090000",
                    "20260130T090000"], "FR")

    V(id="RRULE-BY-015", family="rrule.by",
      title="BYSETPOS=0 (out of range)", kind="rrule", op="rrule.parse",
      input=rrule_in("DTSTART:19970904T090000\n"
                     "RRULE:FREQ=MONTHLY;BYDAY=TU;BYSETPOS=0;COUNT=3", count=3),
      classification="INVALID",
      normative=[cite("rfc5545-3.3.10",
                      "Valid values are 1 to 366 or -366 to -1.")],
      expect=reject("bysetpos_out_of_range"),
      rationale="An explicit numeric range in the RFC that engines routinely "
                "do not enforce.",
      tags=["bysetpos", "invalid"])

    V(id="RRULE-BY-016", family="rrule.by",
      title="BYSETPOS without any other BY* rule part",
      kind="rrule", op="rrule.expand",
      input=rrule_in("DTSTART:19970904T090000\n"
                     "RRULE:FREQ=MONTHLY;BYSETPOS=1;COUNT=3", count=4),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.bysetpos_alone",
      normative=[cite("rfc5545-3.3.10",
                      "BYSETPOS ... MUST only be used in conjunction with "
                      "another BYxxx rule part.")],
      expect=cases("admissible", [
          ("reject", {"rrule.bysetpos_alone": "reject"}, None,
           "The MUST reading."),
          ("degenerate", {"rrule.bysetpos_alone": "degenerate"},
           occ(None, "19970904T090000", "19971004T090000", "19971104T090000"),
           "Engines that treat the single implicit candidate (the DTSTART day) "
           "as the set, making BYSETPOS=1 a no-op."),
      ], "A MUST that the ABNF cannot express; both behaviours ship."),
      rationale="Second example of a prose constraint outside the grammar's "
                "reach, in a different rule part from CORE-011.",
      tags=["bysetpos", "invalid"])

    wk_mo = ["19970805T090000", "19970810T090000", "19970819T090000",
             "19970824T090000"]
    wk_su = ["19970805T090000", "19970817T090000", "19970819T090000",
             "19970831T090000"]
    V(id="RRULE-BY-017", family="rrule.by",
      title="WKST=MO with INTERVAL=2 (RFC's own WKST example)", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970805T090000\n"
                     "RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=4;BYDAY=TU,SU;WKST=MO",
                     count=5, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "An example where the days generated makes a difference "
                      "because of WKST: ... WKST=MO ==> (1997 EDT) August "
                      "5,10,19,24")],
      expect=single(occ(NY, *wk_mo)),
      rationale="Half of the RFC's own demonstration that WKST changes the "
                "occurrence set.",
      tags=["wkst", "interval"])

    V(id="RRULE-BY-018", family="rrule.by",
      title="WKST=SU with INTERVAL=2 (same rule, different week start)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970805T090000\n"
                     "RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=4;BYDAY=TU,SU;WKST=SU",
                     count=5, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "changing only WKST to SU yields ==> (1997 EDT) August "
                      "5,17,19,31")],
      expect=single(occ(NY, *wk_su)),
      rationale=("The RFC prints both answers, so this pair is fully "
                 "normative and is the cleanest available test of whether an "
                 "engine implements WKST at all. Engines that ignore WKST "
                 "return the WKST=MO answer here."),
      tags=["wkst", "interval", "discriminator", "headline"])

    V(id="RRULE-BY-019", family="rrule.by",
      title="WKST default is MO when omitted", kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970805T090000\n"
                     "RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=4;BYDAY=TU,SU",
                     count=5, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "The default value is MO.")],
      expect=single(occ(NY, *wk_mo),
                    "Identical to WKST=MO. Engines that default to the "
                    "locale's first day of week (observed in calendar UIs) "
                    "return the WKST=SU set instead."),
      rationale="A locale-dependent default would make the same rule mean "
                "different things for different users; the RFC forecloses it "
                "and this vector proves conformance.",
      tags=["wkst", "locale"])

    V(id="RRULE-BY-020", family="rrule.by",
      title="BYWEEKNO=20 with BYDAY=MO (RFC example)", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19970512T090000\n"
                     "RRULE:FREQ=YEARLY;BYWEEKNO=20;BYDAY=MO;COUNT=3", count=4,
                     zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "Monday of week number 20 (where the default start of "
                      "the week is Monday), forever: ==> (1997 9:00 AM EDT) "
                      "May 12;(1998 9:00 AM EDT) May 11;(1999 9:00 AM EDT) "
                      "May 17")],
      expect=single(occ(NY, "19970512T090000", "19980511T090000",
                        "19990517T090000")),
      rationale="The RFC prints three years of results, which is enough to "
                "detect an off-by-one in the ISO week algorithm.",
      tags=["byweekno", "iso-week"])

    V(id="RRULE-BY-021", family="rrule.by",
      title="BYWEEKNO=1 across a year boundary (ISO 8601 week 1)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260101T090000\n"
                     "RRULE:FREQ=YEARLY;BYWEEKNO=1;BYDAY=MO;COUNT=4", count=5,
                     zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "This rule part MUST NOT be used when the FREQ rule part "
                      "is set to anything other than YEARLY. ... a week is "
                      "defined as a seven day period, starting on the weekday "
                      "defined by the WKST rule part. Week number one of the "
                      "calendar year is the first week that contains at least "
                      "four (4) days in that calendar year.")],
      expect=single(occ(NY, "20270104T090000", "20280103T090000",
                        "20290101T090000", "20291231T090000"),
                    "Two boundary effects in one set. (a) The candidate for "
                    "year 2026 is 2025-12-29 — ISO week 1 of 2026 starts in "
                    "calendar 2025 — and is dropped because it precedes "
                    "DTSTART, so the first emitted instance is for 2027. "
                    "(b) The candidate for year 2030 is 2029-12-31, which "
                    "lies in calendar year 2029. An engine that filters "
                    "candidates by calendar year loses the second."),
      rationale=("The year-boundary case is the whole reason BYWEEKNO is hard: "
                 "the instance generated 'for' a year can lie in the adjacent "
                 "calendar year, and the RFC's four-day rule is the only thing "
                 "that decides it."),
      tags=["byweekno", "iso-week", "year-boundary", "headline"])
    for s, iso in [("20270104T090000", (2027, 1, 1)), ("20280103T090000", (2028, 1, 1)),
                   ("20290101T090000", (2029, 1, 1)), ("20291231T090000", (2030, 1, 1))]:
        d = dt.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
        assert d.isocalendar()[:3] == iso, (s, d.isocalendar())

    V(id="RRULE-BY-022", family="rrule.by",
      title="BYWEEKNO=53 in a year that has no week 53", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20261228T090000\n"
                     "RRULE:FREQ=YEARLY;BYWEEKNO=53;BYDAY=MO;COUNT=3", count=4,
                     zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10")],
      expect=single(occ(NY, "20261228T090000", "20321227T090000",
                        "20371228T090000"),
                    "Only ISO long years have a week 53; short years "
                    "contribute nothing."),
      rationale="Extends BY-021 to the rarest ISO case; catches engines that "
                "clamp 53 to 52.",
      tags=["byweekno", "iso-week"])
    for s in ["20261228T090000", "20321227T090000", "20371228T090000"]:
        d = dt.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
        assert d.isocalendar()[1] == 53 and d.weekday() == 0, (s, d.isocalendar())

    V(id="RRULE-BY-023", family="rrule.by",
      title="BYWEEKNO with WKST=SU (weeks are not ISO weeks any more)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260101T090000\n"
                     "RRULE:FREQ=YEARLY;BYWEEKNO=1;BYDAY=SU;WKST=SU;COUNT=3",
                     count=4, zone=NY),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.byweekno_wkst",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "a week is defined as a seven day period, starting on the "
                      "weekday defined by the WKST rule part",
                      note="the four-day rule is stated without reference to "
                           "WKST, so whether 'week 1' is recomputed under a "
                           "non-Monday WKST is not determined"),
                 cite("eid3779", note="Verified; edits the same BYDAY sentence "
                                      "as erratum 1913 to a different and "
                                      "non-nested wording"),
                 cite("eid1913", note="Verified; the other edit of that "
                                      "sentence")],
      expect=open_("Recorded, not scored. The RFC defines week numbering "
                   "relative to WKST but states the four-day rule in ISO "
                   "terms; engines variously (a) recompute week 1 under the "
                   "declared WKST, (b) use ISO weeks regardless of WKST, or "
                   "(c) ignore BYWEEKNO when WKST is not MO. No source "
                   "arbitrates, and two Verified errata edit the neighbouring "
                   "sentence irreconcilably."),
      rationale=("An honest 'open' vector. Its value is the measurement: the "
                 "differential matrix shows how many distinct answers exist, "
                 "which is the falsifiable claim, rather than a fabricated "
                 "expected list."),
      tags=["byweekno", "wkst", "errata", "open"])

    V(id="RRULE-BY-024", family="rrule.by",
      title="BYWEEKNO with FREQ=MONTHLY (forbidden)", kind="rrule",
      op="rrule.parse",
      input=rrule_in("DTSTART:20260101T090000\n"
                     "RRULE:FREQ=MONTHLY;BYWEEKNO=1;COUNT=3", count=3),
      classification="INVALID",
      normative=[cite("rfc5545-3.3.10",
                      "This rule part MUST NOT be used when the FREQ rule part "
                      "is set to anything other than YEARLY.")],
      expect=reject("byweekno_freq_mismatch"),
      rationale="An explicit MUST NOT tied to FREQ; the expand/limit table's "
                "only outright prohibition.",
      tags=["byweekno", "invalid"])

    V(id="RRULE-BY-025", family="rrule.by",
      title="Numeric BYDAY with FREQ=WEEKLY (forbidden)", kind="rrule",
      op="rrule.parse",
      input=rrule_in("DTSTART:20260105T090000\n"
                     "RRULE:FREQ=WEEKLY;BYDAY=2MO;COUNT=3", count=3),
      classification="INVALID",
      normative=[cite("rfc5545-3.3.10",
                      "The numeric value in a BYDAY rule part with the FREQ "
                      "rule part set to YEARLY corresponds to an offset within "
                      "the month when the BYMONTH rule part is present ... "
                      "It MUST NOT be specified when the FREQ rule part is set "
                      "to anything other than MONTHLY or YEARLY.")],
      expect=reject("byday_ordinal_freq_mismatch"),
      rationale="Frequently accepted and silently reinterpreted as plain MO.",
      tags=["byday", "invalid"])

    V(id="RRULE-BY-026", family="rrule.by",
      title="Numeric BYDAY with FREQ=YEARLY and BYWEEKNO present "
            "(errata 1913 vs 3779)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260101T090000\n"
                     "RRULE:FREQ=YEARLY;BYWEEKNO=20;BYDAY=2MO;COUNT=3",
                     count=4, zone=NY),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.byday_ordinal_scope",
      context={"tzdb_min": "2025c"},
      normative=[cite("eid1913",
                      note="Verified/Technical: corrects the sentence to read "
                           "'when the BYWEEKNO or BYMONTH rule parts are not "
                           "present'"),
                 cite("eid3779",
                      note="Verified/Technical: edits the SAME sentence to "
                           "'when the BYMONTH rule part is not present'. The "
                           "two corrected texts are not nested and cannot both "
                           "be applied."),
                 cite("rfc5545-3.3.10")],
      expect=open_("Recorded, not scored. Under erratum 1913 the numeric "
                   "prefix is invalid here (BYWEEKNO is present); under "
                   "erratum 3779 it is valid and means the second Monday of "
                   "the year. Both errata are Verified. There is no "
                   "consolidated text of RFC 5545 §3.3.10."),
      rationale=("The strongest single argument in the corpus that 'RFC 5545 "
                 "compliant' is unfalsifiable without a corpus: two Verified "
                 "errata edit one sentence into two incompatible sentences, "
                 "and an engine can conform to either."),
      tags=["byday", "errata", "open", "headline"])

    V(id="RRULE-BY-027", family="rrule.by",
      title="FREQ=YEARLY with BYMONTHDAY only (erratum 3747's Note 2)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260315T090000\n"
                     "RRULE:FREQ=YEARLY;BYMONTHDAY=15;COUNT=4", count=5,
                     zone=NY),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.note2",
      context={"tzdb_min": "2025c"},
      normative=[cite("eid3747",
                      "Note 2: Limit if BYYEARDAY or BYMONTHDAY is present; "
                      "otherwise, special expand for YEARLY.",
                      note="Verified, classified Editorial, but it changes "
                           "expansion semantics"),
                 cite("rfc5545-3.3.10", note="the published Note 2 differs")],
      expect=cases("admissible", [
          ("limit", {"rrule.note2": "post_errata"},
           occ(NY, "20260315T090000", "20270315T090000", "20280315T090000",
               "20290315T090000"),
           "Post-errata reading: BYMONTHDAY limits, so only the month of "
           "DTSTART survives."),
          ("expand", {"rrule.note2": "pre_errata"},
           occ(NY, "20260315T090000", "20260415T090000", "20260515T090000",
               "20260615T090000"),
           "Pre-errata reading: BYMONTHDAY expands across all twelve months. "
           "python-dateutil implements the pre-errata text."),
      ], "A Verified erratum against the canonical expansion table describes "
         "behaviour the most widely deployed reference implementation does "
         "not exhibit."),
      rationale=("'Conform to RFC 5545 plus verified errata' and 'match the "
                 "ecosystem' are mutually exclusive goals, and this vector is "
                 "where that becomes measurable. The most-linked HTML mirror "
                 "of §3.3.10 still serves the pre-errata text, so implementers "
                 "reading the ordinary web copy never see the correction."),
      tags=["errata", "expand-limit", "headline"])

    V(id="RRULE-BY-028", family="rrule.by",
      title="BYMONTH with FREQ=MONTHLY (limit, not expand)", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260115T090000\n"
                     "RRULE:FREQ=MONTHLY;BYMONTH=3,6,9,12;COUNT=4", count=5,
                     zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      note="the expand/limit table gives Limit for BYMONTH "
                           "under FREQ=MONTHLY")],
      expect=single(occ(NY, "20260315T090000", "20260615T090000",
                        "20260915T090000", "20261215T090000")),
      rationale="A quarterly schedule written the way most users write it; the "
                "expand/limit table's most common practical application.",
      tags=["bymonth", "expand-limit"])

    V(id="RRULE-BY-029", family="rrule.by",
      title="BYHOUR expands under FREQ=DAILY", kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260101T090000\n"
                     "RRULE:FREQ=DAILY;BYHOUR=9,17;COUNT=4", count=5, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      note="expand/limit table: BYHOUR expands under DAILY")],
      expect=single(occ(NY, "20260101T090000", "20260101T170000",
                        "20260102T090000", "20260102T170000")),
      rationale="Time-of-day expansion is the half of the table that DST "
                "interacts with; a prerequisite for the rrule.dst family.",
      tags=["byhour", "expand-limit"])

    V(id="RRULE-BY-030", family="rrule.by",
      title="US presidential election day (RFC example: BYDAY+BYMONTHDAY "
            "intersection)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:19961105T090000\n"
                     "RRULE:FREQ=YEARLY;INTERVAL=4;BYMONTH=11;BYDAY=TU;"
                     "BYMONTHDAY=2,3,4,5,6,7,8;COUNT=3", count=4, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "Every 4 years, the first Tuesday after a Monday in "
                      "November, forever (U.S. Presidential Election day): "
                      "==> (1996 9:00 AM EST) November 5;(2000 9:00 AM EST) "
                      "November 7;(2004 9:00 AM EST) November 2")],
      expect=single(occ(NY, "19961105T090000", "20001107T090000",
                        "20041102T090000"),
                    "BYDAY and BYMONTHDAY INTERSECT in RRULE. In cron the same "
                    "two fields are UNIONed under the Vixie rule — the single "
                    "clearest semantic incompatibility between the grammars."),
      rationale=("The definitive cross-grammar vector: '0 9 2-8 11 2' in cron "
                 "means the 2nd-8th OR every Tuesday; the same intent in RRULE "
                 "requires an intersection. A translator that maps fields "
                 "positionally is wrong by construction."),
      tags=["byday", "bymonthday", "cross-grammar", "headline"])
    assert_weekday(["19961105T090000", "20001107T090000", "20041102T090000"], "TU")

    V(id="RRULE-BY-031", family="rrule.by",
      title="Invalid dates are ignored, not clamped (RFC example)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20070115T090000\n"
                     "RRULE:FREQ=MONTHLY;BYMONTHDAY=15,30;COUNT=5", count=6,
                     zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "An example where an invalid date (i.e., February 30) is "
                      "ignored. ==> (2007 EST) January 15,30 (2007 EST) "
                      "February 15 (2007 EDT) March 15,30")],
      expect=single(occ(NY, "20070115T090000", "20070130T090000",
                        "20070215T090000", "20070315T090000",
                        "20070330T090000")),
      rationale="The RFC's own demonstration that COUNT counts emitted "
                "instances, not attempted ones.",
      tags=["bymonthday", "count", "invalid-date"])

    V(id="RRULE-BY-032", family="rrule.by",
      title="BYMONTHDAY=32", kind="rrule", op="rrule.parse",
      input=rrule_in("DTSTART:20260101T090000\n"
                     "RRULE:FREQ=MONTHLY;BYMONTHDAY=32;COUNT=1", count=1),
      classification="INVALID",
      normative=[cite("rfc5545-3.3.10",
                      "Valid values are 1 to 31 or -31 to -1.")],
      expect=reject("bymonthday_out_of_range"),
      rationale="Range enforcement on the most-used BY part.",
      tags=["bymonthday", "invalid"])

    # =================================================================
    # FAMILY: rrule.dst
    # =================================================================
    V(id="RRULE-DST-001", family="rrule.dst",
      title="Daily 02:30 across the US spring-forward gap", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260306T023000\n"
                     "RRULE:FREQ=DAILY;COUNT=4", count=5, zone=NY),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.gap",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      "Recurrence instances falling on invalid dates and times "
                      "are ignored and not counted",
                      note="the published text"),
                 cite("eid4271",
                      "invalid dates keep MUST-ignore; nonexistent local times "
                      "are 'handled as specified in Section 3.3.5'"),
                 cite("rfc5545-3.3.5",
                      "If the local time described does not occur ... the "
                      "DATE-TIME value is interpreted using the UTC offset "
                      "before the gap.")],
      expect=cases("admissible", [
          ("drop", {"rrule.gap": "omit"},
           occ(NY, "20260306T023000", "20260307T023000") +
           [_fmt_zoned(NY, "20260309T023000")],
           "Published RFC text: the nonexistent instance is ignored and not "
           "counted, so COUNT=4 reaches 2026-03-10."),
          ("pre-gap-offset", {"rrule.gap": "pre_gap_offset"},
           occ(NY, "20260306T023000", "20260307T023000") +
           ["2026-03-08T02:30:00-05:00|2026-03-08T07:30:00Z"] +
           occ(NY, "20260309T023000"),
           "Erratum 4271 routed through §3.3.5: 02:30 EST = 07:30Z, which is "
           "03:30 EDT in wall-clock terms."),
          ("imaginary-local", {"rrule.gap": "imaginary"},
           ["2026-03-08T02:30:00-04:00|2026-03-08T06:30:00Z"], None),
      ], "python-dateutil emits 2026-03-08T02:30:00-04:00, a datetime for "
         "which dateutil.tz.datetime_exists() returns False: it neither drops "
         "the instance nor resolves it via the pre-gap offset."),
      rationale=("Three positions on nonexistent local times — published RFC, "
                 "Verified erratum, and the most-used reference "
                 "implementation — and none is what a user would predict. "
                 "This is the vector that most directly falsifies 'RFC 5545 "
                 "compliant' as a claim."),
      tags=["gap", "errata", "headline"])

    V(id="RRULE-DST-002", family="rrule.dst",
      title="Daily 01:30 across the US autumn fold", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20261030T013000\n"
                     "RRULE:FREQ=DAILY;COUNT=4", count=6, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.5",
                      "If the local time described occurs more than once ... "
                      "the DATE-TIME value refers to the first occurrence."),
                 cite("eid4271")],
      expect=single(occ(NY, "20261030T013000", "20261031T013000") +
                    ["2026-11-01T01:30:00-04:00|2026-11-01T05:30:00Z"] +
                    occ(NY, "20261102T013000"),
                    "The fold case IS settled by §3.3.5: first occurrence, "
                    "i.e. the pre-transition offset. Emitting both instants, "
                    "or only the second, is a conformance failure."),
      rationale=("Deliberately classified NORMATIVE while its gap counterpart "
                 "is AMBIGUOUS_STANDARD: §3.3.5 resolves the fold and leaves "
                 "the gap to erratum 4271. Engines usually get the fold right "
                 "and the gap wrong, and the asymmetry is only visible when "
                 "the two are tested as a pair."),
      tags=["fold", "headline"])

    V(id="RRULE-DST-003", family="rrule.dst",
      title="A recurrence whose local time is stable but whose UTC offset "
            "changes (the DST-safe property)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260301T090000\n"
                     "RRULE:FREQ=WEEKLY;COUNT=3", count=4, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.5",
                      note="a DATE-TIME with a TZID is a local time; the UTC "
                           "instant is derived, not stored")],
      expect=single(occ(NY, "20260301T090000", "20260308T090000",
                        "20260315T090000"),
                    "09:00 local on all three dates; the UTC instants are "
                    "14:00Z, 13:00Z, 13:00Z. An engine that expands in UTC and "
                    "converts back produces 08:00 or 10:00 local after the "
                    "transition."),
      rationale=("The defining property of zoned recurrence, and the one most "
                 "often broken by engines that normalise to UTC on parse. "
                 "Cheap to test, decisive, and the reason the corpus's output "
                 "encoding carries both local and UTC forms."),
      tags=["offset-change", "control"])

    V(id="RRULE-DST-004", family="rrule.dst",
      title="Weekly 02:15 in Lord Howe (30-minute transition)", kind="rrule",
      op="rrule.expand",
      input=rrule_in("DTSTART;TZID=Australia/Lord_Howe:20260919T021500\n"
                     "RRULE:FREQ=WEEKLY;COUNT=4", count=5,
                     zone="Australia/Lord_Howe"),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.gap",
      context={"tzdb_min": "2025c"},
      normative=[cite("eid4271"), cite("rfc5545-3.3.5")],
      expect=open_("Recorded, not scored. 2026-10-04T02:15 does not exist in "
                   "Lord Howe (the gap is 02:00-02:30). Engines that resolve a "
                   "gap by adding one hour land at 03:15, which is 45 minutes "
                   "later than the pre-gap-offset answer of 02:30."),
      rationale=("The half-hour transition is where a hard-coded one-hour "
                 "correction becomes visibly wrong rather than merely "
                 "arbitrary."),
      tags=["gap", "half-hour", "open"])

    V(id="RRULE-DST-005", family="rrule.dst",
      title="Daily 01:30 in Antarctica/Troll (two-hour transition)",
      kind="rrule", op="rrule.expand",
      input=rrule_in("DTSTART;TZID=Antarctica/Troll:20260327T013000\n"
                     "RRULE:FREQ=DAILY;COUNT=4", count=5,
                     zone="Antarctica/Troll"),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.gap",
      context={"tzdb_min": "2025c"},
      normative=[cite("eid4271"), cite("rfc5545-3.3.5")],
      expect=open_("Recorded, not scored. Troll's 2026-03-29 transition is "
                   "+00 to +02, so 01:30 and 02:30 both fail to exist. A "
                   "one-hour correction lands inside the gap."),
      rationale="The widest gap in the tzdb; a correctness test for the gap "
                "resolution algorithm rather than for its policy.",
      tags=["gap", "two-hour", "open"])

    V(id="RRULE-DST-006", family="rrule.dst",
      title="A monthly recurrence across the Apia date-line jump",
      kind="rrule", op="rrule.expand",
      input=rrule_in("DTSTART;TZID=Pacific/Apia:20111030T120000\n"
                     "RRULE:FREQ=MONTHLY;BYMONTHDAY=30;COUNT=4", count=5,
                     zone="Pacific/Apia"),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.gap",
      context={"tzdb_min": "2025c"},
      normative=[cite("eid4271"), cite("rfc5545-3.3.5"), cite("tz-theory")],
      expect=open_("Recorded, not scored. 2011-12-30 did not exist in Samoa: "
                   "the zone jumped from 2011-12-29T23:59:59-10:00 to "
                   "2011-12-31T00:00:00+14:00. The 'interpret using the offset "
                   "before the gap' rule of §3.3.5 yields "
                   "2011-12-30T12:00:00-10:00 = 2011-12-30T22:00:00Z, which "
                   "lands on 2011-12-31T12:00 local — a full calendar day "
                   "later in local terms."),
      rationale=("The pathological case for every gap policy: the 'gap' is 24 "
                 "hours wide and the pre-gap-offset rule produces a wall time "
                 "on a different date. Any product claiming a DST policy must "
                 "state what it does here."),
      tags=["gap", "skipped-day", "open", "headline"])

    V(id="RRULE-DST-007", family="rrule.dst",
      title="UTC DTSTART is immune to DST by construction", kind="rrule",
      op="rrule.expand",
      input=rrule_in("DTSTART:20260306T073000Z\nRRULE:FREQ=DAILY;COUNT=4",
                     count=5, zone="UTC"),
      classification="NORMATIVE",
      normative=[cite("rfc5545-3.3.5")],
      expect=single(["2026-03-06T07:30:00+00:00|2026-03-06T07:30:00Z",
                     "2026-03-07T07:30:00+00:00|2026-03-07T07:30:00Z",
                     "2026-03-08T07:30:00+00:00|2026-03-08T07:30:00Z",
                     "2026-03-09T07:30:00+00:00|2026-03-09T07:30:00Z"],
                    "The control for the DST family: a UTC anchor has no gap "
                    "and no fold, and the local wall time in New York drifts "
                    "by an hour instead."),
      rationale=("Every hosted scheduler's documented workaround ('use UTC') "
                 "is this vector. It is correct and it is also the vector that "
                 "shows what the workaround costs: the wall time moves."),
      tags=["utc", "control"])

    V(id="RRULE-DST-008", family="rrule.dst",
      title="Floating DTSTART (no TZID, no Z) has no instants at all",
      kind="rrule", op="rrule.expand",
      input=rrule_in("DTSTART:20260306T023000\nRRULE:FREQ=DAILY;COUNT=4",
                     count=5),
      classification="NORMATIVE",
      normative=[cite("rfc5545-3.3.5",
                      "Date-time values of this type are said to be 'floating' "
                      "and are not bound to any time zone in particular. They "
                      "are used to represent the same hour, minute, and second "
                      "value regardless of which time zone is currently being "
                      "observed.")],
      expect=single(occ(None, "20260306T023000", "20260307T023000",
                        "20260308T023000", "20260309T023000"),
                    "Including 2026-03-08T02:30, which is not a valid local "
                    "time in New York. Floating times are correct here "
                    "precisely because they are not bound to a zone."),
      rationale=("The third DTSTART value type, and the one that makes the "
                 "gap/fold question disappear entirely. A model that has no "
                 "floating type cannot express this vector; a model that has "
                 "one must decide when the binding to a zone happens."),
      tags=["floating", "gap"])

    V(id="RRULE-DST-009", family="rrule.dst",
      title="Hourly recurrence across the fold: 25-hour day", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20261101T000000\n"
                     "RRULE:FREQ=HOURLY;COUNT=5", count=6, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10",
                      note="FREQ=HOURLY advances by absolute hours, so the "
                           "repeated wall hour is traversed once in each "
                           "offset")],
      expect=single(["2026-11-01T00:00:00-04:00|2026-11-01T04:00:00Z",
                     "2026-11-01T01:00:00-04:00|2026-11-01T05:00:00Z",
                     "2026-11-01T01:00:00-05:00|2026-11-01T06:00:00Z",
                     "2026-11-01T02:00:00-05:00|2026-11-01T07:00:00Z",
                     "2026-11-01T03:00:00-05:00|2026-11-01T08:00:00Z"],
                    "01:00 appears twice with different offsets. This is the "
                    "only construct in RFC 5545 that produces two instances "
                    "with the same wall time, and it is the reason occurrence "
                    "identity cannot be a wall-clock string."),
      rationale=("Decisive for occurrence identity: any product that keys "
                 "occurrences by local date-time collapses these two rows and "
                 "silently drops a run. Paired with CRON-DST-016, which asks "
                 "the same question of an hourly cron."),
      tags=["fold", "hourly", "identity", "headline"])

    V(id="RRULE-DST-010", family="rrule.dst",
      title="Hourly recurrence across the gap: 23-hour day", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260308T000000\n"
                     "RRULE:FREQ=HOURLY;COUNT=5", count=6, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.3.10")],
      expect=single(["2026-03-08T00:00:00-05:00|2026-03-08T05:00:00Z",
                     "2026-03-08T01:00:00-05:00|2026-03-08T06:00:00Z",
                     "2026-03-08T03:00:00-04:00|2026-03-08T07:00:00Z",
                     "2026-03-08T04:00:00-04:00|2026-03-08T08:00:00Z",
                     "2026-03-08T05:00:00-04:00|2026-03-08T09:00:00Z"],
                    "02:00 local never appears; the hours are contiguous in "
                    "UTC and discontinuous in wall time."),
      rationale="The gap counterpart of DST-009, and the case where a "
                "wall-clock scheduler emits a run that has no instant.",
      tags=["gap", "hourly"])

    V(id="RRULE-DST-011", family="rrule.dst",
      title="Zero-offset transition: Asia/Amman abolishes DST (2022)",
      kind="rrule", op="rrule.expand",
      input=rrule_in("DTSTART;TZID=Asia/Amman:20221027T003000\n"
                     "RRULE:FREQ=DAILY;COUNT=4", count=5, zone="Asia/Amman"),
      classification="NORMATIVE", context={"tzdb_min": "2022e"},
      normative=[cite("tzdb-news",
                      note="Jordan and Syria made +03 permanent in October "
                           "2022; the transition changes the abbreviation and "
                           "the isdst flag but not the offset")],
      expect=single(["2022-10-27T00:30:00+03:00|2022-10-26T21:30:00Z",
                     "2022-10-28T00:30:00+03:00|2022-10-27T21:30:00Z",
                     "2022-10-29T00:30:00+03:00|2022-10-28T21:30:00Z",
                     "2022-10-30T00:30:00+03:00|2022-10-29T21:30:00Z"],
                    "No wall time is skipped or repeated; an engine that keys "
                    "gap/fold detection on the isdst flag reports a "
                    "transition here and mis-resolves the instant."),
      rationale=("The zero-offset transition separates two implementation "
                 "strategies that are otherwise indistinguishable: comparing "
                 "utcoffset() (correct) versus comparing dst() or the "
                 "abbreviation (incorrect)."),
      tags=["zero-offset", "discriminator"])

    V(id="RRULE-DST-012", family="rrule.dst",
      title="Zero-offset transition: Asia/Damascus abolishes DST (2022)",
      kind="rrule", op="rrule.expand",
      input=rrule_in("DTSTART;TZID=Asia/Damascus:20221027T003000\n"
                     "RRULE:FREQ=DAILY;COUNT=4", count=5, zone="Asia/Damascus"),
      classification="NORMATIVE", context={"tzdb_min": "2022e"},
      normative=[cite("tzdb-news")],
      expect=single(["2022-10-27T00:30:00+03:00|2022-10-26T21:30:00Z",
                     "2022-10-28T00:30:00+03:00|2022-10-27T21:30:00Z",
                     "2022-10-29T00:30:00+03:00|2022-10-28T21:30:00Z",
                     "2022-10-30T00:30:00+03:00|2022-10-29T21:30:00Z"]),
      rationale="Paired with DST-011 so a single zone's data cannot explain a "
                "failure.",
      tags=["zero-offset", "discriminator"])

    # =================================================================
    # FAMILY: rrule.sets  -- RDATE / EXDATE / recurrence sets
    # =================================================================
    V(id="RRULE-SET-001", family="rrule.sets",
      title="EXDATE removes an instance the RRULE generates", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=5\n"
                     f"EXDATE;TZID={NY}:20260107T090000", count=6, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "the 'EXDATE' property ... take precedence over those "
                      "specified by inclusion properties (i.e., RDATE and "
                      "RRULE)")],
      expect=single(occ(NY, "20260105T090000", "20260106T090000",
                        "20260108T090000", "20260109T090000"),
                    "COUNT=5 generates five candidates; EXDATE removes one, so "
                    "four remain. COUNT bounds generation, not the final set."),
      rationale=("The COUNT-versus-EXDATE interaction is the corpus's cheapest "
                 "test of whether an engine composes the set correctly or "
                 "applies EXDATE before COUNT."),
      tags=["exdate", "count"])

    V(id="RRULE-SET-002", family="rrule.sets",
      title="RDATE adds an instance outside the RRULE", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=WEEKLY;COUNT=3\n"
                     f"RDATE;TZID={NY}:20260107T140000", count=5, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.2",
                      "This property can be specified in recurring 'VEVENT' "
                      "... to define a set of instances")],
      expect=single(occ(NY, "20260105T090000", "20260107T140000",
                        "20260112T090000", "20260119T090000"),
                    "The RDATE instance is merged in date order, not appended."),
      rationale="Ordering of merged RDATEs is a common bug and is directly "
                "observable.",
      tags=["rdate"])

    V(id="RRULE-SET-003", family="rrule.sets",
      title="EXDATE takes precedence over RDATE for the same instant",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=WEEKLY;COUNT=2\n"
                     f"RDATE;TZID={NY}:20260107T140000\n"
                     f"EXDATE;TZID={NY}:20260107T140000", count=4, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "the 'EXDATE' property ... take precedence over those "
                      "specified by inclusion properties (i.e., RDATE and "
                      "RRULE)")],
      expect=single(occ(NY, "20260105T090000", "20260112T090000"),
                    "The explicitly added instance is explicitly removed; "
                    "EXDATE wins."),
      rationale="The precedence rule is normative and unambiguous, which makes "
                "it a useful control against the genuinely ambiguous "
                "precedence vector SET-004.",
      tags=["exdate", "rdate", "precedence"])

    V(id="RRULE-SET-004", family="rrule.sets",
      title="EXDATE with VALUE=DATE against a DATE-TIME DTSTART "
            "(erratum 6316, open since 2020)",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=HOURLY;INTERVAL=6;COUNT=8\n"
                     "EXDATE;VALUE=DATE:20260106", count=9, zone=NY),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.exdate_value_type",
      context={"tzdb_min": "2025c"},
      normative=[cite("eid6316",
                      note="REPORTED 2020-10-22, still not Verified six years "
                           "on: asks whether a DATE-only EXDATE excludes all "
                           "instances occurring on that date"),
                 cite("rfc5545-3.8.5.1",
                      note="the property definition permits VALUE=DATE but "
                           "does not say how it matches DATE-TIME instances")],
      expect=cases("admissible", [
          ("exclude-whole-day", {"rrule.exdate_value_type": "date_matches_day"},
           occ(NY, "20260105T090000", "20260105T150000", "20260105T210000",
               "20260107T030000", "20260107T090000", "20260107T150000"),
           "The reading erratum 6316 proposes: a DATE-valued EXDATE removes "
           "every instance on that date."),
          ("exclude-midnight-only",
           {"rrule.exdate_value_type": "date_is_midnight"},
           occ(NY, "20260105T090000", "20260105T150000", "20260105T210000",
               "20260106T030000", "20260106T090000", "20260106T150000",
               "20260106T210000", "20260107T030000"),
           "The literal reading: DATE 20260106 is 20260106T000000, which no "
           "instance equals, so nothing is excluded."),
          ("reject", {"rrule.exdate_value_type": "must_match_dtstart"}, None,
           "Engines requiring EXDATE's value type to equal DTSTART's — the "
           "position erratum 6316 asks the RFC to take."),
      ], "Six years as a Reported erratum with no resolution."),
      rationale=("A live, unresolved specification question in the most "
                 "safety-relevant direction: an EXDATE that fails to exclude "
                 "is a job that runs when someone said it must not. Three "
                 "shipped behaviours, no arbiter."),
      tags=["exdate", "value-type", "errata", "headline"])

    V(id="RRULE-SET-005", family="rrule.sets",
      title="EXDATE naming an instant the rule never generates", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=3\n"
                     f"EXDATE;TZID={NY}:20260106T100000", count=4, zone=NY),
      classification="POLICY_DEPENDENT", policy_axis="rrule.exdate_unmatched",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.1", note="no statement about an EXDATE "
                                              "that matches nothing")],
      expect=cases("per_policy", [
          ("silent", {"rrule.exdate_unmatched": "ignore"},
           occ(NY, "20260105T090000", "20260106T090000", "20260107T090000"),
           "The overwhelmingly common behaviour."),
          ("warn", {"rrule.exdate_unmatched": "warn"},
           occ(NY, "20260105T090000", "20260106T090000", "20260107T090000"),
           "Same set, plus a diagnostic. Distinguishable only via the runner's "
           "diagnostics channel."),
          ("reject", {"rrule.exdate_unmatched": "reject"}, None,
           "Treat a no-op EXDATE as an authoring error."),
      ]),
      rationale=("A typo in an EXDATE — the wrong minute, the wrong zone — is "
                 "silently a no-op in every mainstream engine, and the "
                 "consequence is a job that runs on a day someone explicitly "
                 "excluded. Worth a policy axis in any new product."),
      tags=["exdate", "policy"])

    V(id="RRULE-SET-006", family="rrule.sets",
      title="EXDATE in a different zone naming the same instant", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=3\n"
                     "EXDATE;TZID=Europe/London:20260106T140000", count=4,
                     zone=NY),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.exdate_matching",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.1", note="no statement about whether "
                                              "EXDATE matching is by instant "
                                              "or by (zone, wall time) pair")],
      expect=cases("admissible", [
          ("instant-match", {"rrule.exdate_matching": "instant"},
           occ(NY, "20260105T090000", "20260107T090000"),
           "2026-01-06T14:00 London is 2026-01-06T09:00 New York — the same "
           "instant, so the instance is removed."),
          ("wall-time-match", {"rrule.exdate_matching": "wall"},
           occ(NY, "20260105T090000", "20260106T090000", "20260107T090000"),
           "Engines comparing (zone, wall time) pairs find no match and remove "
           "nothing."),
      ]),
      rationale=("Occurrence identity in one vector. If instances are "
                 "instants, the first answer is right; if they are "
                 "zone-qualified wall times, the second is. RFC 5545 never "
                 "says, and the choice propagates into every deduplication "
                 "and cancellation feature built on top."),
      tags=["exdate", "identity", "headline"])

    V(id="RRULE-SET-007", family="rrule.sets",
      title="Duplicate instants from RRULE and RDATE are coalesced",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=3\n"
                     f"RDATE;TZID={NY}:20260106T090000", count=5, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "Where duplicate instances are generated by the 'RRULE' "
                      "and 'RDATE' properties, only one recurrence is "
                      "considered.")],
      expect=single(occ(NY, "20260105T090000", "20260106T090000",
                        "20260107T090000"),
                    "Three instances, not four."),
      rationale="An explicit normative de-duplication requirement that is "
                "trivially testable and not universally implemented.",
      tags=["rdate", "dedup"])

    V(id="RRULE-SET-008", family="rrule.sets",
      title="Two RRULEs in one component", kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=2\n"
                     "RRULE:FREQ=WEEKLY;BYDAY=WE;COUNT=2", count=6, zone=NY),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.multiple_rrule",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      note="the property may appear more than once per the "
                           "component grammar, but the specification "
                           "deprecates it without forbidding it and does not "
                           "define the combination")],
      expect=cases("admissible", [
          ("union", {"rrule.multiple_rrule": "union"},
           occ(NY, "20260105T090000", "20260107T090000", "20260112T090000",
               "20260114T090000"),
           "Set union, each rule bounded by its own COUNT."),
          ("first-only", {"rrule.multiple_rrule": "first"},
           occ(NY, "20260105T090000", "20260112T090000"),
           "Engines that keep only the first RRULE — the most common "
           "behaviour, and a silent data loss."),
          ("reject", {"rrule.multiple_rrule": "reject"}, None, None),
      ]),
      rationale=("Multiple RRULEs are legal syntax, deprecated prose, and "
                 "undefined semantics. Silently dropping the second rule is "
                 "the modal behaviour and is invisible to the author."),
      tags=["multiple-rrule", "silent-drop"])

    V(id="RRULE-SET-009", family="rrule.sets",
      title="Every instance excluded: an empty recurrence set", kind="rrule",
      op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=2\n"
                     f"EXDATE;TZID={NY}:20260105T090000,20260106T090000",
                     count=3, zone=NY),
      classification="POLICY_DEPENDENT", policy_axis="rrule.empty_set",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3", note="no statement about a fully "
                                              "excluded set")],
      expect=cases("per_policy", [
          ("empty", {"rrule.empty_set": "empty"}, [],
           "Return an empty set — the reading consistent with EXDATE "
           "precedence."),
          ("reject", {"rrule.empty_set": "reject"}, None,
           "Treat a component with no instances as invalid."),
      ]),
      rationale=("Empty is a legitimate answer that many APIs cannot express "
                 "(an iterator that raises StopIteration on the first call is "
                 "indistinguishable from an error to some callers). Paired "
                 "with CRON-INV-007 and RRULE-CORE-018."),
      tags=["empty-set", "exdate"])

    V(id="RRULE-SET-010", family="rrule.sets",
      title="EXRULE (removed from RFC 5545, present in RFC 2445)",
      kind="rrule", op="rrule.parse",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=10\n"
                     "EXRULE:FREQ=WEEKLY;BYDAY=SA,SU", count=11, zone=NY),
      classification="DIALECT_DEPENDENT", policy_axis="rrule.exrule",
      dialect_axis="rrule.profile", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      note="RFC 5545 removed EXRULE, which RFC 2445 defined; "
                           "the property is therefore legal iCalendar under "
                           "one standard and unknown under its successor")],
      expect=cases("per_dialect", [
          ("rfc2445", {"rrule.exrule": "supported"},
           occ(NY, "20260105T090000", "20260106T090000", "20260107T090000",
               "20260108T090000", "20260109T090000", "20260112T090000",
               "20260113T090000", "20260114T090000"),
           "Engines retaining RFC 2445 support (dateutil's rruleset has "
           "exrule) exclude the weekend days."),
          ("ignore", {"rrule.exrule": "ignore"},
           occ(NY, "20260105T090000", "20260106T090000", "20260107T090000",
               "20260108T090000", "20260109T090000", "20260110T090000"),
           "Engines that ignore unknown properties emit the full daily set — "
           "including the weekend the author excluded."),
          ("reject", {"rrule.exrule": "reject"}, None, None),
      ]),
      rationale=("A property whose removal from a standard silently changes "
                 "the meaning of existing data. The 'ignore' outcome runs jobs "
                 "on days that were explicitly excluded, which is the same "
                 "failure class as SET-004."),
      tags=["exrule", "legacy", "silent-drop"])

    V(id="RRULE-SET-011", family="rrule.sets",
      title="RDATE with a PERIOD value", kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=WEEKLY;COUNT=2\n"
                     "RDATE;VALUE=PERIOD:20260107T140000Z/PT1H", count=4,
                     zone=NY),
      classification="DIALECT_DEPENDENT", policy_axis="rrule.rdate_period",
      dialect_axis="rrule.profile", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.2",
                      "Value Type: The default value type for this property is "
                      "DATE-TIME. The value type can be set to DATE or PERIOD.")],
      expect=cases("per_dialect", [
          ("supported", {"rrule.rdate_period": "supported"},
           occ(NY, "20260105T090000") +
           ["2026-01-07T09:00:00-05:00|2026-01-07T14:00:00Z"] +
           occ(NY, "20260112T090000"),
           "The period's start becomes the instance; its duration overrides "
           "the component's."),
          ("reject", {"rrule.rdate_period": "unsupported"}, None,
           "Most recurrence-only libraries have no duration concept and "
           "cannot represent this at all."),
      ]),
      rationale=("PERIOD-valued RDATE is the only place RFC 5545 lets a single "
                 "occurrence carry a different *magnitude* from its siblings — "
                 "the construct Stripe's prorated stub period needs and that "
                 "no pure recurrence library models."),
      tags=["rdate", "period", "scope-boundary"])

    V(id="RRULE-SET-012", family="rrule.sets",
      title="RDATE before DTSTART", kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=WEEKLY;COUNT=2\n"
                     f"RDATE;TZID={NY}:20251229T090000", count=4, zone=NY),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.rdate_before_dtstart",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.2", note="no statement that RDATE values "
                                              "must be at or after DTSTART")],
      expect=cases("admissible", [
          ("include", {"rrule.rdate_before_dtstart": "include"},
           occ(NY, "20251229T090000", "20260105T090000", "20260112T090000"),
           "The recurrence set now starts before its own DTSTART."),
          ("drop", {"rrule.rdate_before_dtstart": "drop"},
           occ(NY, "20260105T090000", "20260112T090000"),
           "Engines that clamp the set to [DTSTART, ...)."),
          ("reject", {"rrule.rdate_before_dtstart": "reject"}, None, None),
      ]),
      rationale=("Breaks the widely assumed invariant 'DTSTART is the minimum "
                 "of the recurrence set'. Any product that uses DTSTART as a "
                 "query lower bound is wrong under the 'include' reading."),
      tags=["rdate", "dtstart", "invariant"])

    V(id="RRULE-SET-013", family="rrule.sets",
      title="EXDATE alone with no RRULE", kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     f"EXDATE;TZID={NY}:20260105T090000", count=3, zone=NY),
      classification="AMBIGUOUS_STANDARD", policy_axis="rrule.dtstart_emission",
      context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3"), cite("eid5920")],
      expect=cases("admissible", [
          ("empty", {"rrule.dtstart_emission": "always"}, [],
           "DTSTART is an instance and the EXDATE removes it: an event that "
           "exists and never occurs."),
          ("dtstart-survives", {"rrule.dtstart_emission": "seed_only"},
           occ(NY, "20260105T090000"),
           "Engines where DTSTART is a seed outside the set and therefore not "
           "excludable."),
      ]),
      rationale="The minimal probe of DTSTART's membership in the set; one "
                "line of input distinguishes the two models.",
      tags=["dtstart", "exdate", "discriminator"])

    V(id="RRULE-SET-014", family="rrule.sets",
      title="RDATE and RRULE producing instants one second apart",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={NY}:20260105T090000\n"
                     "RRULE:FREQ=DAILY;COUNT=3\n"
                     f"RDATE;TZID={NY}:20260106T090001", count=5, zone=NY),
      classification="NORMATIVE", context={"tzdb_min": "2025c"},
      normative=[cite("rfc5545-3.8.5.3",
                      "Where duplicate instances are generated ... only one "
                      "recurrence is considered.",
                      note="these are not duplicates")],
      expect=single(occ(NY, "20260105T090000", "20260106T090000",
                        "20260106T090001", "20260107T090000"),
                    "Four instances. Engines that de-duplicate at date "
                    "granularity, or that compare with a tolerance, collapse "
                    "these to three."),
      rationale="Pins the granularity of the de-duplication rule that SET-007 "
                "establishes.",
      tags=["rdate", "dedup", "identity"])
