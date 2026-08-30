"""Cron vectors for the Occurframe conformance oracle."""
from __future__ import annotations
import datetime as dt
from zoneinfo import ZoneInfo

from common import V, cite, single, cases, reject, open_, cron_in
import cron_ref as R

D = dt.datetime.fromisoformat

VIXIE = R.Policy(dom_dow="vixie", dow_zero_seven="both", allow_L=False)
POSIX = R.Policy(dom_dow="or", dow_zero_seven="zero")
ANDP = R.Policy(dom_dow="and", dow_zero_seven="both")
NTH = R.Policy(dom_dow="nth", dow_zero_seven="both")
QUARTZ = R.Policy(dom_dow="reject", dow_zero_seven="quartz", fields=6,
                  seconds_leading=True, allow_L=True, allow_W=True,
                  allow_hash=True, allow_qmark=True)
QUARTZ7 = R.Policy(dom_dow="reject", dow_zero_seven="quartz", fields=7,
                   seconds_leading=True, year_field=True, allow_L=True,
                   allow_W=True, allow_hash=True, allow_qmark=True)
EXT5 = R.Policy(dom_dow="vixie", allow_L=True, allow_W=True, allow_hash=True,
                allow_qmark=True)
SEC6 = R.Policy(fields=6, seconds_leading=True)


def ref(expr, pol, start, n, zone=None, inclusive=False):
    tz = ZoneInfo(zone) if zone else None
    return R.run(expr, pol, D(start), n, tz=tz, inclusive=inclusive)


def build():
    # =================================================================
    # FAMILY: cron.day-fields  -- the five production resolutions
    # =================================================================
    NOTE_FIVE = ("Five distinct resolutions of the DOM/DOW ambiguity exist in "
                 "production: OR (Vixie lineage / POSIX / robfig / GCP), AND "
                 "(fcron dayand, GNU micron strict, node-cron, Cronos), "
                 "Nth-weekday (dcron / micron dillon), parse error with a "
                 "mandatory '?' (Quartz, AWS EventBridge, Cloudflare), and "
                 "mutual exclusion by requiring one field to be '*' (Vercel).")

    POLICY_TABLE = [
        ("or/vixie", R.Policy(dom_dow="vixie"),
         "Vixie / cronie / POSIX prose: OR when both day fields are "
         "restricted, AND when either is a literal '*'."),
        ("or-any-nonstar", R.Policy(dom_dow="or_text"),
         "OR whenever neither field is the literal '*', regardless of what "
         "the fields denote (croner legacy mode, dragonmantank/"
         "cron-expression). Differs from Vixie only for day fields that "
         "cover their whole range without being written '*'."),
        ("or-set-semantics", R.Policy(dom_dow="or"),
         "POSIX read literally: 'element or list' means a proper subset of "
         "the field range, so a fully covering range is NOT restricted."),
        ("and", R.Policy(dom_dow="and"),
         "fcron dayand=true, GNU micron strict, node-cron, Cronos, "
         "APScheduler."),
        ("and+monday-zero", R.Policy(dom_dow="and",
                                     dow_zero_seven="monday_zero"),
         "APScheduler 3.x CronTrigger.from_crontab(): AND, and numeric "
         "day-of-week is 0=MONDAY, so every numeric weekday in a copied "
         "crontab shifts by one day."),
        ("nth", R.Policy(dom_dow="nth"),
         "dcron / GNU micron 'dillon': day-of-month values are read as "
         "ordinals 1..5 selecting the Nth such weekday; an empty set is the "
         "honest result when the DOM values fall outside 1..5."),
    ]

    def five_way(id_, expr, start, n, title, extra_rationale="", tags=()):
        cs = []
        for lab, pol, note in POLICY_TABLE:
            try:
                occ = ref(expr, pol, start, n)
            except R.CronRefError:
                occ = None
            cs.append((lab, {"cron.dom_dow": lab}, occ, note))
        cs.append(("reject", {"cron.dom_dow": "reject"}, None,
                   "Quartz / AWS EventBridge / Cloudflare: ParseException — "
                   "'Support for specifying both a day-of-week AND a "
                   "day-of-month parameter is not implemented.'"))
        cs.append(("exclusive", {"cron.dom_dow": "exclusive"}, None,
                   "Vercel: rejected at deploy time; one of the two day fields "
                   "must be '*'."))
        V(id=id_, family="cron.day-fields", title=title, kind="cron",
          op="cron.next", input=cron_in(expr, start, n),
          classification="DIALECT_DEPENDENT",
          policy_axis="cron.dom_dow", dialect_axis="cron.dialect",
          context={"dialect": "declared", "policy": {"cron.dom_dow": "declared"},
                   "requires": ["cron.5field"]},
          normative=[
              cite("crontab5", "If both fields are restricted (i.e., are not *), "
                               "the command will be run when either field matches "
                               "the current time."),
              cite("posix-crontab", "If either the month or day of month is "
                                    "specified as an element or list, and the day "
                                    "of week is also specified as an element or "
                                    "list, then any day matching either ... shall "
                                    "be matched."),
              cite("vixie-cron.c", "the dom/dow situation is odd. '* * 1,15 * Sun' "
                                   "will run on the first and fifteenth AND every "
                                   "Sunday; ... yes, it's bizarre. like many "
                                   "bizarre things, it's the standard."),
              cite("micron", note="three mutually incompatible interpretations of "
                                  "the same five fields, selectable per job"),
              cite("fcron5", note="dayand is (boolean, default true)"),
              cite("dcron", note="0 11 1,5 * mon-wed means the first and last "
                                 "Mon/Tue/Wed"),
              cite("quartz"),
          ],
          expect=cases("per_dialect", cs, NOTE_FIVE),
          rationale=("The single most consequential divergence in the cron "
                     "family. No source arbitrates between the five: POSIX and "
                     "crontab(5) state OR, fcron and micron ship AND as the "
                     "default, dcron ships a third reading, and Quartz makes the "
                     "input illegal. Classified DIALECT_DEPENDENT rather than "
                     "KNOWN_DIVERGENCE because each behaviour is documented by "
                     "its own dialect; the corpus therefore demands a declared "
                     "dialect, not a universal answer. " + extra_rationale),
          tags=list(tags) + ["dom_dow", "five-way"])

    five_way("CRON-DAYF-001", "0 12 13 * FRI", "2026-01-01T00:00:00", 6,
             "Friday the 13th: the canonical DOM/DOW collision",
             "0 0 13 * 5 denotes three different things and one parse error "
             "across four widely deployed dialects.", tags=["headline"])
    five_way("CRON-DAYF-002", "30 4 1,15 * 5", "2026-01-01T00:00:00", 8,
             "crontab(5)'s own worked example (1st and 15th, plus every Friday)")
    five_way("CRON-DAYF-003", "0 11 1,5 * mon-wed", "2026-01-01T00:00:00", 8,
             "dcron's own worked example, read by four dialects")
    five_way("CRON-DAYF-004", "0 0 1 * SUN", "2026-01-01T00:00:00", 6,
             "Single DOM element with a single DOW element")
    five_way("CRON-DAYF-005", "0 0 29-31 * MON", "2026-01-01T00:00:00", 8,
             "Range DOM with a single DOW: month-end or Monday")
    five_way("CRON-DAYF-006", "0 6 1-7 * 1", "2026-01-01T00:00:00", 8,
             "The 'first Monday' idiom written naively (a DOM/DOW trap)")

    # ---- the DOM_STAR parser artefact ------------------------------
    for n_, expr, note in [
        ("CRON-DAYF-010", "0 12 *,10 * 2",
         "DOM text begins with '*' so Vixie sets DOM_STAR before parsing and "
         "the predicate becomes AND, even though the field denotes {1..31,10}."),
        ("CRON-DAYF-011", "0 12 10,* * 2",
         "The same set written in the other order does NOT set DOM_STAR, so "
         "the predicate is OR. Two spellings of one set, two answers."),
        ("CRON-DAYF-012", "0 12 1-31 * 2",
         "A fully-covering range does not set DOM_STAR, so the predicate is "
         "OR and the job runs every day rather than only on Tuesdays."),
    ]:
        occ = ref(expr, VIXIE, "2026-01-01T00:00:00", 6)
        V(id=n_, family="cron.day-fields",
          title="DOM_STAR first-character artefact: " + expr, kind="cron",
          op="cron.next", input=cron_in(expr, "2026-01-01T00:00:00", 6),
          classification="KNOWN_DIVERGENCE",
          policy_axis="cron.dom_dow", dialect_axis="cron.dialect",
          context={"dialect": "vixie", "policy": {"cron.dom_dow": "vixie"}},
          normative=[cite("vixie-entry.c",
                          "if (ch == '*') e->flags |= DOM_STAR;"),
                     cite("crontab-guru-bug",
                          "cron inspects the very first character of the day fields")],
          expect=cases("admissible", [
              ("vixie-artefact", {"cron.dom_dow": "vixie"}, occ,
               "Reference matcher reproducing the first-character flagging."),
              ("or-set-semantics", {"cron.dom_dow": "or"},
               ref(expr, R.Policy(dom_dow="or"), "2026-01-01T00:00:00", 6),
               "Engines that decide OR/AND from the parsed value set rather "
               "than the literal text."),
              ("or-any-nonstar", {"cron.dom_dow": "or_text"},
               ref(expr, R.Policy(dom_dow="or_text"), "2026-01-01T00:00:00", 6),
               "Engines that OR whenever neither field is the literal '*'."),
              ("and+monday-zero", {"cron.dom_dow": "and+monday-zero"},
               ref(expr, R.Policy(dom_dow="and",
                                  dow_zero_seven="monday_zero"),
                   "2026-01-01T00:00:00", 6),
               "APScheduler: AND, with numeric day-of-week 0=Monday."),
              ("reject", {"cron.dom_dow": "reject"}, None,
               "Engines that reject a step or list form appearing here."),
          ], note),
          rationale=("The rule that governs a quarter of all cron expressions "
                     "is an artefact of reading one character before parsing. "
                     "No specification describes it; crontab(5) and POSIX both "
                     "describe the set-semantics reading. Classified "
                     "KNOWN_DIVERGENCE: the reference implementation and the "
                     "reference documentation disagree and neither arbitrates."),
          tags=["dom_dow", "parser-artefact"])

    occ = ref("0 0 */100,1-7 * MON", VIXIE, "2026-01-01T00:00:00", 6)
    V(id="CRON-DAYF-013", family="cron.day-fields",
      title="The '*/100,1-7 * MON' first-Monday idiom weaponising the artefact",
      kind="cron", op="cron.next",
      input=cron_in("0 0 */100,1-7 * MON", "2026-01-01T00:00:00", 6),
      classification="KNOWN_DIVERGENCE",
      policy_axis="cron.dom_dow", dialect_axis="cron.dialect",
      context={"dialect": "vixie", "policy": {"cron.dom_dow": "vixie"}},
      normative=[cite("healthchecks-funky",
                      "0 0 */100,1-7 * MON yields 'first Monday of the month'")],
      expect=cases("admissible", [
          ("vixie-artefact", {"cron.dom_dow": "vixie"}, occ,
           "Leading '*' sets DOM_STAR, forcing AND; '*/100' contributes only "
           "day 1; '1-7' bounds the window to the first week."),
          ("reject-step", {"cron.step_gt_field": "reject"}, None,
           "Dialects that reject a step larger than the field range."),
      ], "The community's canonical workaround depends on a parser bug in the "
         "rule's own reference implementation."),
      rationale=("Strongest single piece of evidence that cron's day semantics "
                 "are an implementation artefact rather than a rule: the "
                 "idiom is only correct if the bug is present."),
      tags=["dom_dow", "parser-artefact", "headline"])

    # =================================================================
    # FAMILY: cron.dow-numbering
    # =================================================================
    for id_, expr, title in [
        ("CRON-DOW-001", "0 12 * * 0", "Day-of-week 0"),
        ("CRON-DOW-002", "0 12 * * 7", "Day-of-week 7"),
        ("CRON-DOW-003", "0 12 * * 0,7", "Day-of-week 0 and 7 in one list"),
    ]:
        vix = ref(expr, VIXIE, "2026-01-01T00:00:00", 4)
        try:
            px = ref(expr, POSIX, "2026-01-01T00:00:00", 4)
            px_err = None
        except R.CronRefError as e:
            px, px_err = None, str(e)
        try:
            qz = ref("0 " + expr + " *", QUARTZ7, "2026-01-01T00:00:00", 4)
        except R.CronRefError:
            qz = None
        try:
            mz = ref(expr, R.Policy(dow_zero_seven="monday_zero"),
                     "2026-01-01T00:00:00", 4)
        except R.CronRefError as e:
            mz = None
        cs = [("vixie-both", {"cron.dow_numbering": "both"}, vix,
               "0 and 7 both denote Sunday."),
              ("monday-zero", {"cron.dow_numbering": "monday_zero"}, mz,
               "APScheduler 3.x from_crontab(): 0=MON..6=SUN and 7 is out of "
               "range. Named days (SUN, MON) stay Sunday-based in the same "
               "engine, so numeric and named spellings of one weekday "
               "disagree."),
              ("posix-zero-only", {"cron.dow_numbering": "zero"}, px,
               px_err or "POSIX fixes day-of-week at [0,6] with 0=Sunday and "
                         "admits no 7."),
              ("quartz-1-7", {"cron.dow_numbering": "quartz"}, qz,
               "Quartz/AWS/Cloudflare: 1=SUN..7=SAT, so this literal names a "
               "different weekday.")]
        V(id=id_, family="cron.dow-numbering", title=title, kind="cron",
          op="cron.next", input=cron_in(expr, "2026-01-01T00:00:00", 4),
          classification="DIALECT_DEPENDENT",
          policy_axis="cron.dow_numbering", dialect_axis="cron.dialect",
          context={"dialect": "declared",
                   "policy": {"cron.dow_numbering": "declared"}},
          normative=[
              cite("posix-crontab", "day of the week (0 - 6 with 0=Sunday)"),
              cite("crontab5", "day of week (0 - 7) (0 or 7 is Sunday, or use "
                               "names)"),
              cite("quartz", "dayMap.put(\"SUN\", 1)"),
          ],
          expect=cases("per_dialect", cs,
                       "A numeral copied from a Vixie crontab into a Quartz "
                       "scheduler fires on the wrong day every week, forever, "
                       "with no error at any layer."),
          rationale=("Two incompatible numbering bases with overlapping legal "
                     "ranges, so the same literal is valid in both dialects and "
                     "silently means a different weekday. This is the highest-"
                     "severity silent-mistranslation vector in the corpus."),
          tags=["dow", "silent-mistranslation"])

    V(id="CRON-DOW-013", family="cron.dow-numbering",
      title="Numeric and named spellings of the same weekday must agree "
            "(0 vs SUN)",
      kind="cron", op="cron.next",
      input=cron_in("0 12 * * 0", "2026-01-01T00:00:00", 3),
      classification="NORMATIVE",
      normative=[cite("posix-crontab",
                      "day of the week (0 - 6 with 0=Sunday)"),
                 cite("crontab5",
                      "Names can also be used for the 'month' and 'day of "
                      "week' fields.",
                      note="crontab(5) presents names as an alternative "
                           "spelling of the numbers, not a second numbering")],
      expect=single(ref("0 12 * * 0", VIXIE, "2026-01-01T00:00:00", 3),
                    "Must equal the result of '0 12 * * SUN' in the same "
                    "engine. An engine whose numeric and named day-of-week "
                    "fields use different bases fails this vector while "
                    "passing every named-day vector."),
      rationale=("Measured, not hypothetical: APScheduler 3.11.3's "
                 "from_crontab() maps numeric 0 to Monday while mapping the "
                 "name SUN to Sunday, so the two spellings of 'Sunday' in one "
                 "engine denote different days. Because the corpus scores "
                 "numeric and named vectors separately, this vector is what "
                 "makes the inconsistency visible as a single failure."),
      tags=["dow", "silent-mistranslation", "discriminator", "headline"])

    V(id="CRON-DOW-004", family="cron.dow-numbering",
      title="Day-of-week 8 (out of range in every dialect)", kind="cron",
      op="cron.parse", input=cron_in("0 12 * * 8", "2026-01-01T00:00:00", 1),
      classification="INVALID", policy_axis=None,
      normative=[cite("posix-crontab"), cite("crontab5"), cite("quartz")],
      expect=reject("field_value_out_of_range",
                    "Engines MUST reject; a silent clamp to 7 or 1 is a "
                    "conformance failure."),
      rationale="Range enforcement is the cheapest observable conformance "
                "property and is not universal.",
      tags=["dow", "invalid"])

    for id_, expr, title, cls in [
        ("CRON-DOW-005", "0 12 * * FRI-MON",
         "Wrapping named day range FRI-MON", "DIALECT_DEPENDENT"),
        ("CRON-DOW-006", "0 12 * * 5-1",
         "Wrapping numeric day range 5-1", "DIALECT_DEPENDENT"),
        ("CRON-DOW-007", "0 12 * * SAT-SUN",
         "Non-wrapping named day range SAT-SUN", "NORMATIVE"),
    ]:
        try:
            vix = ref(expr, VIXIE, "2026-01-01T00:00:00", 6)
            err = None
        except R.CronRefError as e:
            vix, err = None, str(e)
        wrapped = None
        if err:
            # compute what a wrap-permitting dialect would produce
            lo, hi = expr.split()[-1].split("-")
            names = R.DOW_NAMES_STD
            a = names.get(lo.upper(), None)
            b = names.get(hi.upper(), None)
            if a is None:
                a, b = int(lo), int(hi)
            vals = []
            i = a
            while True:
                vals.append(i % 7)
                if i % 7 == b % 7:
                    break
                i += 1
            e2 = " ".join(expr.split()[:-1] + [",".join(str(v) for v in sorted(set(vals)))])
            wrapped = ref(e2, VIXIE, "2026-01-01T00:00:00", 6)
        cs = [("reject-reversed", {"cron.range_wrap": "reject"}, None,
               err or "n/a — this range does not wrap"),
              ("wrap-modulo", {"cron.range_wrap": "wrap"}, wrapped or vix,
               "Dialects that wrap a reversed range around the field bounds "
               "(croner, some Quartz ports, cron_descriptor).")]
        if not err:
            cs = [("normative", {}, vix, "Ascending range; no dialect variance.")]
        V(id=id_, family="cron.dow-numbering", title=title, kind="cron",
          op="cron.next", input=cron_in(expr, "2026-01-01T00:00:00", 6),
          classification=cls,
          policy_axis="cron.range_wrap" if err else None,
          dialect_axis="cron.dialect" if err else None,
          normative=[cite("posix-crontab",
                          "Ranges of numbers are allowed. ... two numbers "
                          "separated with a hyphen"),
                     cite("crontab5")],
          expect=cases("per_dialect", cs) if err else single(vix),
          rationale=("Neither POSIX nor crontab(5) says what a reversed range "
                     "means. Vixie's parser rejects it; several dialects wrap "
                     "modulo the field. 'Friday through Monday' is a phrase "
                     "users write; the corpus must record that it is not "
                     "portable." if err else
                     "An ascending range within the field bounds is the one "
                     "unambiguous case and anchors the family."),
          tags=["dow", "range-wrap"])

    for id_, expr, title in [
        ("CRON-DOW-008", "0 12 * * sun", "Lowercase day name"),
        ("CRON-DOW-009", "0 12 * jan,dec mon", "Lowercase month and day names"),
        ("CRON-DOW-010", "0 12 * * Wednesday",
         "Full weekday name (not in any published grammar)"),
    ]:
        if "Wednesday" in expr:
            V(id=id_, family="cron.names", title=title, kind="cron",
              op="cron.parse", input=cron_in(expr, "2026-01-01T00:00:00", 3),
              classification="DIALECT_DEPENDENT",
              policy_axis="cron.long_names", dialect_axis="cron.dialect",
              normative=[cite("crontab5", "Names can also be used for the "
                                          "'month' and 'day of week' fields. "
                                          "Use the first three letters of the "
                                          "particular day or month (case does "
                                          "not matter).")],
              expect=cases("per_dialect", [
                  ("three-letter-only", {"cron.long_names": "reject"}, None,
                   "crontab(5) specifies exactly three letters; longer names "
                   "are a parse error."),
                  ("prefix-tolerant", {"cron.long_names": "accept"},
                   ref("0 12 * * WED", VIXIE, "2026-01-01T00:00:00", 3),
                   "Engines that match on a case-insensitive prefix accept the "
                   "full name."),
              ]),
              rationale="Tolerance beyond the grammar is itself a divergence: "
                        "an expression that parses in one engine is a "
                        "deployment failure in another.",
              tags=["names"])
        else:
            V(id=id_, family="cron.names", title=title, kind="cron",
              op="cron.next", input=cron_in(expr, "2026-01-01T00:00:00", 4),
              classification="NORMATIVE",
              normative=[cite("crontab5", "Use the first three letters of the "
                                          "particular day or month (case does "
                                          "not matter).")],
              expect=single(ref(expr, VIXIE, "2026-01-01T00:00:00", 4)),
              rationale="Case-insensitive three-letter names are explicitly "
                        "normative in crontab(5) and unambiguous.",
              tags=["names"])

    V(id="CRON-DOW-011", family="cron.names",
      title="Named range with a step: MON-FRI/2", kind="cron", op="cron.next",
      input=cron_in("0 12 * * MON-FRI/2", "2026-01-01T00:00:00", 6),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.step_on_named_range", dialect_axis="cron.dialect",
      normative=[cite("crontab5", "Step values can be used in conjunction with "
                                  "ranges."),
                 cite("posix-crontab", note="POSIX defines no step operator at "
                                            "all; '/' is a Vixie extension.")],
      expect=cases("per_dialect", [
          ("accept", {"cron.step_on_named_range": "accept"},
           ref("0 12 * * MON-FRI/2", VIXIE, "2026-01-01T00:00:00", 6),
           "Mon, Wed, Fri."),
          ("reject", {"cron.step_on_named_range": "reject"}, None,
           "Dialects that forbid steps on name-valued ranges."),
      ]),
      rationale="POSIX has no '/' operator; every step vector in this corpus "
                "is therefore an extension test, not a standards test.",
      tags=["names", "steps"])

    V(id="CRON-DOW-012", family="cron.names",
      title="Named month range wrapping the year boundary: NOV-FEB",
      kind="cron", op="cron.next",
      input=cron_in("0 12 1 NOV-FEB *", "2026-01-01T00:00:00", 5),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.range_wrap", dialect_axis="cron.dialect",
      normative=[cite("crontab5"), cite("posix-crontab")],
      expect=cases("per_dialect", [
          ("reject-reversed", {"cron.range_wrap": "reject"}, None,
           "Vixie's parser rejects a reversed range."),
          ("wrap-modulo", {"cron.range_wrap": "wrap"},
           ref("0 12 1 1,2,11,12 *", VIXIE, "2026-01-01T00:00:00", 5),
           "Wrapping dialects read NOV-FEB as {11,12,1,2}."),
      ]),
      rationale="The wrap question is asked once per field; the month field "
                "is where users hit it (winter seasons cross the year).",
      tags=["names", "range-wrap"])

    # =================================================================
    # FAMILY: cron.field-count
    # =================================================================
    V(id="CRON-FIELDS-001", family="cron.field-count",
      title="Five-field form (POSIX / Vixie baseline)", kind="cron",
      op="cron.next", input=cron_in("15 10 * * *", "2026-01-01T00:00:00", 4),
      classification="NORMATIVE",
      context={"dialect": "any", "requires": ["cron.5field"]},
      normative=[cite("posix-crontab", "The cron command shall ... minute, "
                                       "hour, day of the month, month, and day "
                                       "of the week")],
      expect=single(ref("15 10 * * *", VIXIE, "2026-01-01T00:00:00", 4)),
      rationale="The one field-count every dialect accepts; the control vector "
                "for the family.",
      tags=["fields"])

    V(id="CRON-FIELDS-002", family="cron.field-count",
      title="Six-field form: is the extra field seconds or year?", kind="cron",
      op="cron.next", input=cron_in("0 15 10 * * *", "2026-01-01T00:00:00", 4,
                                    fields=6),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.sixth_field", dialect_axis="cron.dialect",
      normative=[cite("quartz", note="Quartz's six-field form is "
                                     "sec min hour dom month dow"),
                 cite("aws-eventbridge",
                      note="EventBridge's six-field form is "
                           "min hour dom month dow year")],
      expect=cases("per_dialect", [
          ("seconds-leading", {"cron.sixth_field": "seconds"},
           ref("0 15 10 * * *", R.Policy(fields=6, seconds_leading=True),
               "2026-01-01T00:00:00", 4),
           "Quartz, croner, cron-parser (6-field), robfig with "
           "WithSeconds(): the leading field is seconds."),
          ("year-trailing", {"cron.sixth_field": "year"},
           ref("0 15 10 * * 2026", R.Policy(fields=6, year_field=True),
               "2026-01-01T00:00:00", 4),
           "AWS EventBridge, Spring: the trailing field is the year. Here the "
           "trailing token is '*', so the year is unrestricted and the "
           "expression means 10:15 daily."),
          ("reject", {"cron.sixth_field": "reject"}, None,
           "Strict five-field engines (POSIX crontab, cronsim default)."),
      ], "The same six tokens denote 10:15:00 daily under one reading and "
         "10:15 daily under another; both are silently accepted."),
      rationale=("The six-field form is the worst kind of ambiguity: both "
                 "readings parse, both produce plausible schedules, and the "
                 "difference is only visible in the seconds field of the "
                 "output. No document arbitrates between Quartz's and "
                 "EventBridge's placement of the extra field."),
      tags=["fields", "headline", "silent-mistranslation"])

    V(id="CRON-FIELDS-003", family="cron.field-count",
      title="Seven-field Quartz form with an explicit year", kind="cron",
      op="cron.next",
      input=cron_in("0 0 12 ? * MON 2027", "2026-01-01T00:00:00", 4, fields=7),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.field_count", dialect_axis="cron.dialect",
      normative=[cite("quartz", "Seconds Minutes Hours Day-of-Month Month "
                                "Day-of-Week Year (optional field)")],
      expect=cases("per_dialect", [
          ("quartz7", {"cron.field_count": 7},
           ref("0 0 12 ? * MON 2027", QUARTZ7, "2026-01-01T00:00:00", 4),
           "Quartz/Quartz.NET: Mondays at noon, restricted to 2027."),
          ("reject", {"cron.field_count": "5-or-6"}, None,
           "Everything in the Vixie lineage."),
      ]),
      rationale="The year field is the only cron construct that can make a "
                "recurrence finite; it is also the least portable.",
      tags=["fields", "year"])

    V(id="CRON-FIELDS-004", family="cron.field-count",
      title="Seconds granularity: every 15 seconds", kind="cron",
      op="cron.next",
      input=cron_in("*/15 * * * * *", "2026-01-01T00:00:00", 6, fields=6),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.seconds", dialect_axis="cron.dialect",
      normative=[cite("posix-crontab", note="POSIX cron has one-minute "
                                            "resolution and no seconds field"),
                 cite("quartz")],
      expect=cases("per_dialect", [
          ("seconds", {"cron.seconds": "supported"},
           ref("*/15 * * * * *", SEC6, "2026-01-01T00:00:00", 6),
           "Quartz, croner, cron-parser, robfig-with-seconds."),
          ("reject", {"cron.seconds": "unsupported"}, None,
           "Five-field engines."),
      ]),
      rationale="Sub-minute scheduling is the most common reason to leave the "
                "five-field form, and the point at which cron expressions stop "
                "being portable at all.",
      tags=["fields", "seconds"])

    V(id="CRON-FIELDS-005", family="cron.field-count",
      title="Four fields (too few)", kind="cron", op="cron.parse",
      input=cron_in("0 12 * *", "2026-01-01T00:00:00", 1),
      classification="INVALID",
      normative=[cite("posix-crontab"), cite("crontab5")],
      expect=reject("field_count",
                    "Must be rejected. Engines that pad a missing field with "
                    "'*' produce a schedule the author never wrote."),
      rationale="Silent padding is observed in the wild; this vector makes it "
                "falsifiable.",
      tags=["fields", "invalid"])

    V(id="CRON-FIELDS-006", family="cron.field-count",
      title="Eight fields (too many in every dialect)", kind="cron",
      op="cron.parse",
      input=cron_in("0 0 0 1 1 * 2026 extra", "2026-01-01T00:00:00", 1),
      classification="INVALID",
      normative=[cite("quartz", note="seven fields is the documented maximum")],
      expect=reject("field_count"),
      rationale="Upper bound of the field-count axis.",
      tags=["fields", "invalid"])

    V(id="CRON-FIELDS-007", family="cron.field-count",
      title="Six-field form with an unambiguous year token (2027)",
      kind="cron", op="cron.next",
      input=cron_in("0 12 1 1 * 2027", "2026-01-01T00:00:00", 3, fields=6),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.sixth_field", dialect_axis="cron.dialect",
      normative=[cite("aws-eventbridge")],
      expect=cases("per_dialect", [
          ("year-trailing", {"cron.sixth_field": "year"},
           ref("0 12 1 1 * 2027", R.Policy(fields=6, year_field=True),
               "2026-01-01T00:00:00", 3),
           "Reads 2027 as a year; the schedule is finite and has exactly one "
           "occurrence."),
          ("seconds-leading", {"cron.sixth_field": "seconds"}, None,
           "Reads the leading '0' as seconds and then finds '2027' in the "
           "day-of-week field: out of range, so a parse error."),
      ], "This vector disambiguates the two six-field readings by construction: "
         "one accepts, the other must reject."),
      rationale="A discriminating vector — it identifies which six-field "
                "dialect an engine implements without needing its docs.",
      tags=["fields", "year", "discriminator"])

    for id_, expr, title, occ_pol in [
        ("CRON-FIELDS-008", "@daily", "Macro @daily", VIXIE),
        ("CRON-FIELDS-009", "@yearly", "Macro @yearly", VIXIE),
        ("CRON-FIELDS-010", "@monthly", "Macro @monthly", VIXIE),
        ("CRON-FIELDS-011", "@weekly", "Macro @weekly", VIXIE),
        ("CRON-FIELDS-012", "@hourly", "Macro @hourly", VIXIE),
    ]:
        equiv = {"@daily": "0 0 * * *", "@yearly": "0 0 1 1 *",
                 "@monthly": "0 0 1 * *", "@weekly": "0 0 * * 0",
                 "@hourly": "0 * * * *"}[expr]
        V(id=id_, family="cron.field-count", title=title, kind="cron",
          op="cron.next", input=cron_in(expr, "2026-01-01T00:00:00", 4),
          classification="NORMATIVE",
          normative=[cite("crontab5",
                          f"{expr}\tRun once a ... (equivalent to \"{equiv}\")")],
          expect=single(ref(equiv, occ_pol, "2026-01-01T00:00:00", 4),
                        f"Documented as exactly equivalent to '{equiv}'."),
          rationale="crontab(5) gives the exact five-field expansion, so the "
                    "answer is normative and every engine that accepts the "
                    "macro can be scored against it.",
          tags=["macros"])

    V(id="CRON-FIELDS-013", family="cron.field-count",
      title="@reboot (an event, not a recurrence)", kind="cron",
      op="cron.parse", input=cron_in("@reboot", "2026-01-01T00:00:00", 1),
      classification="AMBIGUOUS_STANDARD",
      normative=[cite("crontab5", "@reboot : Run once, at startup.")],
      expect=cases("admissible", [
          ("reject", {}, None,
           "A recurrence library has no startup event and should reject."),
          ("empty", {}, [],
           "Parse successfully and yield no occurrences."),
          ("error-at-iteration", {}, None,
           "Parse successfully, raise on first iteration."),
      ], "crontab(5) defines @reboot only in terms of the daemon's lifecycle, "
         "so a pure recurrence engine has no correct answer."),
      rationale=("@reboot is the clearest case in the corpus where the "
                 "expression language names something outside the recurrence "
                 "model. Recording three admissible answers is more useful "
                 "than legislating one."),
      tags=["macros", "execution-boundary"])

    # =================================================================
    # FAMILY: cron.steps
    # =================================================================
    V(id="CRON-STEP-001", family="cron.steps",
      title="*/35 in the minute field: step does not mean interval",
      kind="cron", op="cron.next",
      input=cron_in("*/35 * * * *", "2026-01-01T00:00:00", 6),
      classification="NORMATIVE",
      normative=[cite("crontab5",
                      "steps are evaluated just within the field they are "
                      "applied to")],
      expect=single(ref("*/35 * * * *", VIXIE, "2026-01-01T00:00:00", 6),
                    "Fires at :00 and :35 of every hour — NOT every 35 minutes."),
      rationale=("The most-reported cron misunderstanding, and one the man page "
                 "actually settles. It is NORMATIVE, and it is also the vector "
                 "that proves cron cannot express 'every N minutes' for N not "
                 "dividing 60."),
      tags=["steps", "headline"])

    V(id="CRON-STEP-002", family="cron.steps",
      title="5/20: bare value with a step (start-at semantics)", kind="cron",
      op="cron.next", input=cron_in("5/20 * * * *", "2026-01-01T00:00:00", 6),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.bare_start_step", dialect_axis="cron.dialect",
      normative=[cite("posix-crontab", note="no '/' operator at all"),
                 cite("crontab5",
                      note="documents 'range/step', not 'value/step'"),
                 cite("quartz", "'5/20' in the minutes field means every 20th "
                                "minute of the hour starting at minute 5")],
      expect=cases("per_dialect", [
          ("start-at", {"cron.bare_start_step": "start_at"},
           ref("5/20 * * * *", VIXIE, "2026-01-01T00:00:00", 6),
           "Quartz semantics: 5, 25, 45 — the bare value is a lower bound and "
           "the range runs to the field maximum."),
          ("reject", {"cron.bare_start_step": "reject"}, None,
           "Engines implementing only the documented 'range/step' form."),
          ("single-value", {"cron.bare_start_step": "ignore_step"},
           ref("5 * * * *", VIXIE, "2026-01-01T00:00:00", 6),
           "Engines that parse the value and silently drop the step."),
      ]),
      rationale=("'N/step' appears in no POSIX or crontab(5) grammar but is "
                 "accepted by most modern engines with Quartz's meaning. The "
                 "silent-drop behaviour is the dangerous one and is why this "
                 "vector exists."),
      tags=["steps", "start-at"])

    V(id="CRON-STEP-003", family="cron.steps",
      title="0/1 vs * — Quartz idiom in the seconds field", kind="cron",
      op="cron.next", input=cron_in("0/1 * * * * *", "2026-01-01T00:00:00", 3,
                                    fields=6),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.bare_start_step", dialect_axis="cron.dialect",
      normative=[cite("quartz")],
      expect=cases("per_dialect", [
          ("start-at", {"cron.bare_start_step": "start_at"},
           ref("0/1 * * * * *", SEC6, "2026-01-01T00:00:00", 3),
           "Equivalent to '*' in the seconds field."),
          ("reject", {"cron.bare_start_step": "reject"}, None, None),
      ]),
      rationale="The idiom is ubiquitous in copied Quartz expressions and is a "
                "hard parse error in strict engines.",
      tags=["steps", "start-at"])

    V(id="CRON-STEP-004", family="cron.steps",
      title="Step larger than the field range: */90 in minutes", kind="cron",
      op="cron.next", input=cron_in("*/90 * * * *", "2026-01-01T00:00:00", 4),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.step_gt_field", dialect_axis="cron.dialect",
      normative=[cite("crontab5",
                      "steps are evaluated just within the field they are "
                      "applied to")],
      expect=cases("per_dialect", [
          ("collapse-to-first", {"cron.step_gt_field": "accept"},
           ref("*/90 * * * *", VIXIE, "2026-01-01T00:00:00", 4),
           "The step exceeds the range so only the range start survives: "
           "minute 0 of every hour."),
          ("reject", {"cron.step_gt_field": "reject"}, None,
           "Engines that validate step <= (hi - lo)."),
      ]),
      rationale=("The user intent ('every 90 minutes') is inexpressible; both "
                 "behaviours are defensible and both are shipped. Neither the "
                 "man page nor POSIX addresses an oversized step."),
      tags=["steps"])

    V(id="CRON-STEP-005", family="cron.steps",
      title="Step of zero", kind="cron", op="cron.parse",
      input=cron_in("*/0 * * * *", "2026-01-01T00:00:00", 1),
      classification="INVALID",
      normative=[cite("crontab5")],
      expect=reject("step_zero",
                    "Division by zero or an infinite loop are both observed; "
                    "the required behaviour is a parse error."),
      rationale="A crash-class vector: engines that do not validate this hang.",
      tags=["steps", "invalid"])

    V(id="CRON-STEP-006", family="cron.steps",
      title="Range with a step: 10-16/2 (documented form)", kind="cron",
      op="cron.next", input=cron_in("0 10-16/2 * * *", "2026-01-01T00:00:00", 5),
      classification="NORMATIVE",
      normative=[cite("crontab5",
                      "Step values can be used in conjunction with ranges. "
                      "Following a range with \"/<number>\" specifies skips of "
                      "the number's value through the range.")],
      expect=single(ref("0 10-16/2 * * *", VIXIE, "2026-01-01T00:00:00", 5)),
      rationale="The one step form crontab(5) documents by example; the "
                "family's control vector.",
      tags=["steps"])

    V(id="CRON-STEP-007", family="cron.steps",
      title="Step on a wrapping range: 22-2/2 in hours", kind="cron",
      op="cron.next", input=cron_in("0 22-2/2 * * *", "2026-01-01T00:00:00", 5),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.range_wrap", dialect_axis="cron.dialect",
      normative=[cite("crontab5")],
      expect=cases("per_dialect", [
          ("reject-reversed", {"cron.range_wrap": "reject"}, None,
           "Vixie's parser rejects the reversed range before the step matters."),
          ("wrap-modulo", {"cron.range_wrap": "wrap"},
           ref("0 22,0,2 * * *", VIXIE, "2026-01-01T00:00:00", 5),
           "Wrapping dialects enumerate 22,0,2 — but the step's phase across "
           "the wrap point is itself undefined."),
      ], "Two undefined behaviours compose here: range wrap and step phase."),
      rationale="Overnight windows are a real user need and the least "
                "portable construct in the field grammar.",
      tags=["steps", "range-wrap"])

    V(id="CRON-STEP-008", family="cron.steps",
      title="*/1 (identity step)", kind="cron", op="cron.next",
      input=cron_in("*/1 * * * *", "2026-01-01T00:00:00", 3),
      classification="NORMATIVE",
      normative=[cite("crontab5")],
      expect=single(ref("*/1 * * * *", VIXIE, "2026-01-01T00:00:00", 3)),
      rationale="Identity control for the step machinery.",
      tags=["steps"])

    V(id="CRON-STEP-009", family="cron.steps",
      title="Step in the day-of-month field: */10 does not mean every 10 days",
      kind="cron", op="cron.next",
      input=cron_in("0 0 */10 * *", "2026-01-01T00:00:00", 8),
      classification="NORMATIVE",
      normative=[cite("crontab5",
                      "steps are evaluated just within the field they are "
                      "applied to")],
      expect=single(ref("0 0 */10 * *", VIXIE, "2026-01-01T00:00:00", 8),
                    "Days 1, 11, 21, 31 of each month; the phase resets every "
                    "month, so the gap from the 31st to the 1st is one day."),
      rationale=("The clearest demonstration that cron is a predicate over "
                 "instants and not an interval generator: the '10-day period' "
                 "the user asked for never exists."),
      tags=["steps", "headline"])

    V(id="CRON-STEP-010", family="cron.steps",
      title="Comma list mixing a range-step and a literal", kind="cron",
      op="cron.next",
      input=cron_in("0 0-6/2,23 * * *", "2026-01-01T00:00:00", 6),
      classification="NORMATIVE",
      normative=[cite("crontab5", "Lists are allowed. ... ranges or numbers")],
      expect=single(ref("0 0-6/2,23 * * *", VIXIE, "2026-01-01T00:00:00", 6)),
      rationale="Composition of the documented forms; catches engines whose "
                "list parser and step parser do not compose.",
      tags=["steps"])

    V(id="CRON-STEP-011", family="cron.steps",
      title="Negative step", kind="cron", op="cron.parse",
      input=cron_in("*/-5 * * * *", "2026-01-01T00:00:00", 1),
      classification="INVALID",
      normative=[cite("crontab5")],
      expect=reject("step_negative"),
      rationale="Boundary of the step grammar.",
      tags=["steps", "invalid"])

    V(id="CRON-STEP-012", family="cron.steps",
      title="Step applied to a single '*' in the month field", kind="cron",
      op="cron.next", input=cron_in("0 0 1 */3 *", "2026-01-01T00:00:00", 6),
      classification="NORMATIVE",
      normative=[cite("crontab5")],
      expect=single(ref("0 0 1 */3 *", VIXIE, "2026-01-01T00:00:00", 6),
                    "Quarterly anchored to January, because the month field's "
                    "range starts at 1 — not 'every three months from now'."),
      rationale="Anchoring of a step is always to the field's low bound, never "
                "to the current instant; this is the cron/RRULE INTERVAL "
                "distinction in its cheapest observable form.",
      tags=["steps", "anchoring", "headline"])

    # =================================================================
    # FAMILY: cron.extensions (L / W / #)
    # =================================================================
    V(id="CRON-EXT-001", family="cron.extensions",
      title="L in the day-of-month field (last day of month)", kind="cron",
      op="cron.next", input=cron_in("0 9 L * *", "2027-01-01T00:00:00", 5),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.L", dialect_axis="cron.dialect",
      normative=[cite("quartz", "'L' ... has different meaning in each of the "
                                "two fields in which it is allowed")],
      expect=cases("per_dialect", [
          ("supported", {"cron.L": "supported"},
           ref("0 9 L * *", EXT5, "2027-01-01T00:00:00", 5),
           "31 Jan, 28 Feb, 31 Mar, 30 Apr, 31 May."),
          ("reject", {"cron.L": "unsupported"}, None,
           "POSIX/Vixie: 'L' is not in the grammar."),
      ]),
      rationale="'Last day of month' is the single most requested construct "
                "cron cannot express in its standard grammar; the extension is "
                "widespread but not universal.",
      tags=["extensions", "L"])

    V(id="CRON-EXT-002", family="cron.extensions",
      title="L-3 (third-to-last day of month)", kind="cron", op="cron.next",
      input=cron_in("0 9 L-3 * *", "2027-01-01T00:00:00", 4),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.L", dialect_axis="cron.dialect",
      normative=[cite("quartz", "\"L-3\" would mean the third-to-last day of "
                                "the calendar month")],
      expect=cases("per_dialect", [
          ("supported", {"cron.L": "supported"},
           ref("0 9 L-3 * *", EXT5, "2027-01-01T00:00:00", 4), None),
          ("reject", {"cron.L": "unsupported"}, None, None),
      ]),
      rationale="Offset-from-last is the cron analogue of RRULE "
                "BYMONTHDAY=-4 and lets the two grammars be cross-checked.",
      tags=["extensions", "L"])

    V(id="CRON-EXT-003", family="cron.extensions",
      title="15W: nearest weekday to the 15th", kind="cron", op="cron.next",
      input=cron_in("0 9 15W * *", "2026-01-01T00:00:00", 8),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.W", dialect_axis="cron.dialect",
      normative=[cite("quartz",
                      "the 'nearest' weekday to the 15th of the month ... "
                      "the 'W' character ... will not 'jump' over the boundary "
                      "of a month's days")],
      expect=cases("per_dialect", [
          ("supported", {"cron.W": "supported"},
           ref("0 9 15W * *", EXT5, "2026-01-01T00:00:00", 8), None),
          ("reject", {"cron.W": "unsupported"}, None, None),
      ]),
      rationale=("'W' is exactly the finance industry's Modified Following "
                 "roll convention over a weekends-only calendar; it is the one "
                 "business-day construct that reached the cron grammar."),
      tags=["extensions", "W", "business-day"])

    V(id="CRON-EXT-004", family="cron.extensions",
      title="1W when the 1st is a Saturday (must not jump into last month)",
      kind="cron", op="cron.next",
      input=cron_in("0 9 1W * *", "2026-07-01T00:00:00", 4),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.W", dialect_axis="cron.dialect",
      normative=[cite("quartz", "will not 'jump' over the boundary of a "
                                "month's days")],
      expect=cases("per_dialect", [
          ("supported", {"cron.W": "supported"},
           ref("0 9 1W * *", EXT5, "2026-07-01T00:00:00", 4),
           "1 Aug 2026 is a Saturday; the documented behaviour rolls forward "
           "to Monday 3 Aug, not back to Friday 31 Jul."),
          ("reject", {"cron.W": "unsupported"}, None, None),
      ]),
      rationale="The month-boundary clause is the part of 'W' implementations "
                "most often get wrong; it is separately testable.",
      tags=["extensions", "W", "business-day"])

    V(id="CRON-EXT-005", family="cron.extensions",
      title="LW: last weekday of the month", kind="cron", op="cron.next",
      input=cron_in("0 9 LW * *", "2026-01-01T00:00:00", 6),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.W", dialect_axis="cron.dialect",
      normative=[cite("quartz", "specify \"LW\" ... which translates to "
                                "\"last weekday of the month\"")],
      expect=cases("per_dialect", [
          ("supported", {"cron.W": "supported"},
           ref("0 9 LW * *", EXT5, "2026-01-01T00:00:00", 6), None),
          ("reject", {"cron.W": "unsupported"}, None, None),
      ]),
      rationale="Combines two extensions; catches engines that support each "
                "separately but not together.",
      tags=["extensions", "W", "L"])

    V(id="CRON-EXT-006", family="cron.extensions",
      title="FRI#3: third Friday of the month", kind="cron", op="cron.next",
      input=cron_in("0 0 9 ? * FRI#3 *", "2026-01-01T00:00:00", 5, fields=7),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.hash", dialect_axis="cron.dialect",
      normative=[cite("quartz", "\"6#3\" ... the third Friday of the month")],
      expect=cases("per_dialect", [
          ("supported", {"cron.hash": "supported"},
           ref("0 0 9 ? * FRI#3 *", QUARTZ7, "2026-01-01T00:00:00", 5), None),
          ("reject", {"cron.hash": "unsupported"}, None, None),
      ]),
      rationale="Direct counterpart of RRULE BYDAY=3FR; the pair lets a "
                "cron→RRULE translator be tested for equivalence.",
      tags=["extensions", "hash", "cross-grammar"])

    V(id="CRON-EXT-007", family="cron.extensions",
      title="SUN#5 in a month with only four Sundays", kind="cron",
      op="cron.next",
      input=cron_in("0 0 9 ? * SUN#5 *", "2026-01-01T00:00:00", 4, fields=7),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.hash", dialect_axis="cron.dialect",
      normative=[cite("quartz", "if there is not (for example) a 5th Friday in "
                                "the month, then no firing will occur that "
                                "month")],
      expect=cases("per_dialect", [
          ("skip-month", {"cron.hash": "supported"},
           ref("0 0 9 ? * SUN#5 *", QUARTZ7, "2026-01-01T00:00:00", 4),
           "Months without a fifth Sunday are skipped entirely — the "
           "documented behaviour, and the exact analogue of RRULE BYDAY=5SU."),
          ("reject", {"cron.hash": "unsupported"}, None, None),
          ("clamp-to-last", {"cron.hash": "clamp"},
           ref("0 0 9 ? * SUNL *", QUARTZ7, "2026-01-01T00:00:00", 4),
           "Engines that silently treat #5 as 'last' — observed, and a "
           "different occurrence set."),
      ]),
      rationale="The skip-vs-clamp choice is where cron '#' and RRULE 'nth' "
                "diverge from user intent identically; a paired vector with "
                "RRULE-BY-013.",
      tags=["extensions", "hash", "cross-grammar", "headline"])

    V(id="CRON-EXT-008", family="cron.extensions",
      title="FRIL / 6L: last Friday of the month", kind="cron", op="cron.next",
      input=cron_in("0 0 9 ? * FRIL *", "2026-01-01T00:00:00", 5, fields=7),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.L", dialect_axis="cron.dialect",
      normative=[cite("quartz", "\"6L\" ... means \"the last friday of the "
                                "month\"")],
      expect=cases("per_dialect", [
          ("supported", {"cron.L": "supported"},
           ref("0 0 9 ? * FRIL *", QUARTZ7, "2026-01-01T00:00:00", 5), None),
          ("reject", {"cron.L": "unsupported"}, None, None),
      ]),
      rationale="Counterpart of RRULE BYDAY=-1FR.",
      tags=["extensions", "L", "cross-grammar"])

    V(id="CRON-EXT-009", family="cron.extensions",
      title="'?' in the day-of-month field with a restricted day-of-week",
      kind="cron", op="cron.next",
      input=cron_in("0 0 12 ? * MON *", "2026-01-01T00:00:00", 4, fields=7),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.qmark", dialect_axis="cron.dialect",
      normative=[cite("quartz", "'?' ... means 'no specific value'"),
                 cite("aws-eventbridge", note="EventBridge requires '?' in one "
                                              "of the two day fields")],
      expect=cases("per_dialect", [
          ("supported", {"cron.qmark": "supported"},
           ref("0 0 12 ? * MON *", QUARTZ7, "2026-01-01T00:00:00", 4),
           "'?' is equivalent to '*' for matching purposes but suppresses the "
           "both-restricted error."),
          ("reject", {"cron.qmark": "unsupported"}, None,
           "Vixie lineage: '?' is not in the grammar."),
      ]),
      rationale="'?' is the only construct in any cron dialect whose purpose "
                "is to disambiguate the DOM/DOW rule; it belongs beside the "
                "five-way family.",
      tags=["extensions", "qmark", "dom_dow"])

    V(id="CRON-EXT-010", family="cron.extensions",
      title="'?' in both day fields", kind="cron", op="cron.next",
      input=cron_in("0 0 12 ? * ? *", "2026-01-01T00:00:00", 3, fields=7),
      classification="AMBIGUOUS_STANDARD",
      policy_axis="cron.qmark", dialect_axis="cron.dialect",
      normative=[cite("quartz", note="the documentation states '?' is allowed "
                                     "in one of the two fields but does not "
                                     "define both")],
      expect=cases("admissible", [
          ("accept-as-star", {"cron.qmark": "supported"},
           ref("0 0 12 ? * ? *", QUARTZ7, "2026-01-01T00:00:00", 3),
           "Both treated as '*': fires daily."),
          ("reject", {"cron.qmark": "one_only"}, None,
           "Engines enforcing 'exactly one ?'."),
      ], "Quartz's own documentation does not say what two '?' means; both "
         "behaviours ship."),
      rationale="A genuine gap in the second-most-copied cron dialect's "
                "documentation.",
      tags=["extensions", "qmark"])

    V(id="CRON-EXT-011", family="cron.extensions",
      title="'H' (Jenkins hash) in the minute field", kind="cron",
      op="cron.parse", input=cron_in("H * * * *", "2026-01-01T00:00:00", 1),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.hash_H", dialect_axis="cron.dialect",
      normative=[cite("crontab5", note="'H' is not in the Vixie grammar"),
                 cite("micron", note="not in micron either; 'H' is a Jenkins "
                                     "extension whose value depends on the "
                                     "job's name, i.e. on data outside the "
                                     "expression")],
      expect=cases("per_dialect", [
          ("reject", {"cron.hash_H": "unsupported"}, None,
           "Every engine outside Jenkins."),
          ("job-dependent", {"cron.hash_H": "supported"}, None,
           "Jenkins: the occurrence set is a function of the job name, so the "
           "expression alone does not denote a set. Not scoreable by this "
           "corpus; recorded to mark the boundary."),
      ]),
      rationale=("Included deliberately as the boundary marker: an expression "
                 "whose meaning depends on data outside the expression cannot "
                 "have a conformance vector, and saying so is part of "
                 "specifying the oracle's scope."),
      tags=["extensions", "scope-boundary"])

    V(id="CRON-EXT-012", family="cron.extensions",
      title="cronie's '~' random operator", kind="cron", op="cron.parse",
      input=cron_in("~ * * * *", "2026-01-01T00:00:00", 1),
      classification="DIALECT_DEPENDENT",
      policy_axis="cron.random", dialect_axis="cron.dialect",
      normative=[cite("crontab5", note="cronie adds a '~' random operator")],
      expect=cases("per_dialect", [
          ("reject", {"cron.random": "unsupported"}, None, None),
          ("nondeterministic", {"cron.random": "supported"}, None,
           "cronie: the occurrence set is drawn at parse time and is not "
           "reproducible. Out of scope for conformance scoring."),
      ]),
      rationale="Second scope-boundary marker: non-determinism, like Jenkins "
                "'H', removes the expression from the oracle's domain.",
      tags=["extensions", "scope-boundary"])

    V(id="CRON-EXT-013", family="cron.extensions",
      title="L in the day-of-week field with no preceding number", kind="cron",
      op="cron.next", input=cron_in("0 0 9 ? * L *", "2026-01-01T00:00:00", 4,
                                    fields=7),
      classification="AMBIGUOUS_STANDARD",
      policy_axis="cron.L", dialect_axis="cron.dialect",
      normative=[cite("quartz", "'L' ... in the day-of-week field ... simply "
                                "means \"7\" or \"SAT\"")],
      expect=cases("admissible", [
          ("saturday", {"cron.L": "quartz"},
           ref("0 0 9 ? * L *", QUARTZ7, "2026-01-01T00:00:00", 4),
           "Quartz: bare 'L' in the DOW field means Saturday (day 7)."),
          ("last-day-of-week-of-month", {"cron.L": "last"}, None,
           "Engines that read it as 'the last <something> of the month'."),
          ("reject", {"cron.L": "unsupported"}, None, None),
      ], "Quartz's definition is surprising enough that ports have "
         "reimplemented it differently."),
      rationale="A one-character expression with three shipped meanings.",
      tags=["extensions", "L"])

    V(id="CRON-EXT-014", family="cron.extensions",
      title="32W (nearest weekday to a day that never exists)", kind="cron",
      op="cron.parse", input=cron_in("0 9 32W * *", "2026-01-01T00:00:00", 1),
      classification="INVALID",
      normative=[cite("quartz", note="day-of-month range is 1-31")],
      expect=reject("field_value_out_of_range"),
      rationale="Extension grammars must still enforce the base field range.",
      tags=["extensions", "invalid"])

    # =================================================================
    # FAMILY: cron.invalid
    # =================================================================
    for id_, expr, err, title in [
        ("CRON-INV-001", "60 * * * *", "field_value_out_of_range",
         "Minute 60"),
        ("CRON-INV-002", "* 24 * * *", "field_value_out_of_range", "Hour 24"),
        ("CRON-INV-003", "0 0 0 * *", "field_value_out_of_range",
         "Day-of-month 0"),
        ("CRON-INV-004", "0 0 32 * *", "field_value_out_of_range",
         "Day-of-month 32"),
        ("CRON-INV-005", "0 0 * 13 *", "field_value_out_of_range", "Month 13"),
        ("CRON-INV-006", "0 0 * 0 *", "field_value_out_of_range", "Month 0"),
        ("CRON-INV-007", "0 0 30 2 *", "empty_recurrence_set",
         "30 February — syntactically valid, semantically empty"),
        ("CRON-INV-008", "a b c d e", "syntax", "Non-numeric garbage"),
        ("CRON-INV-009", "", "syntax", "Empty expression"),
        ("CRON-INV-010", "0 0 1-  * *", "syntax", "Truncated range"),
    ]:
        if err == "empty_recurrence_set":
            V(id=id_, family="cron.invalid", title=title, kind="cron",
              op="cron.next", input=cron_in(expr, "2026-01-01T00:00:00", 1),
              classification="AMBIGUOUS_STANDARD",
              policy_axis="cron.empty_set",
              normative=[cite("crontab5", note="no statement about "
                                               "unsatisfiable field "
                                               "combinations"),
                         cite("posix-crontab")],
              expect=cases("admissible", [
                  ("empty", {"cron.empty_set": "empty"}, [],
                   "Return no occurrences."),
                  ("error-at-parse", {"cron.empty_set": "reject"}, None,
                   "Reject at parse time as unsatisfiable."),
                  ("error-at-iteration", {"cron.empty_set": "raise"}, None,
                   "Parse, then raise on iteration (croniter raises "
                   "CroniterBadDateError after exhausting its search window)."),
                  ("hang", {"cron.empty_set": "unbounded"}, None,
                   "Search forever. Observed; a denial-of-service class bug."),
              ], "The empty recurrence set is the single most under-specified "
                 "state in both grammars."),
              rationale=("'0 0 30 2 *' parses under every dialect's field rules "
                         "and denotes nothing. No cron document says what an "
                         "engine must do, and all four behaviours ship, "
                         "including the unbounded search."),
              tags=["invalid", "empty-set", "headline"])
        else:
            V(id=id_, family="cron.invalid", title=title, kind="cron",
              op="cron.parse", input=cron_in(expr, "2026-01-01T00:00:00", 1),
              classification="INVALID",
              normative=[cite("posix-crontab"), cite("crontab5")],
              expect=reject(err),
              rationale="Field-range and grammar enforcement; the cheapest "
                        "conformance signal an engine emits.",
              tags=["invalid"])

    V(id="CRON-INV-011", family="cron.invalid",
      title="Day-of-month 31 in a month that never has 31 days", kind="cron",
      op="cron.next", input=cron_in("0 0 31 4 *", "2026-01-01T00:00:00", 1),
      classification="AMBIGUOUS_STANDARD", policy_axis="cron.empty_set",
      normative=[cite("crontab5"), cite("posix-crontab")],
      expect=cases("admissible", [
          ("empty", {"cron.empty_set": "empty"}, [], None),
          ("error-at-parse", {"cron.empty_set": "reject"}, None, None),
          ("error-at-iteration", {"cron.empty_set": "raise"}, None, None),
          ("hang", {"cron.empty_set": "unbounded"}, None, None),
      ]),
      rationale="Second empty-set vector, chosen so that an engine with a "
                "leap-year special case still fails to find an occurrence.",
      tags=["invalid", "empty-set"])

    V(id="CRON-INV-012", family="cron.invalid",
      title="Whitespace-tolerant parsing (tabs and multiple spaces)",
      kind="cron", op="cron.next",
      input=cron_in("0\t12  *   *  *", "2026-01-01T00:00:00", 3),
      classification="NORMATIVE",
      normative=[cite("crontab5",
                      "fields ... separated by blanks or tabs")],
      expect=single(ref("0 12 * * *", VIXIE, "2026-01-01T00:00:00", 3)),
      rationale="Explicitly normative in crontab(5) and frequently broken by "
                "engines that split on a single space.",
      tags=["invalid", "lexical"])

    # =================================================================
    # FAMILY: cron.anchoring
    # =================================================================
    V(id="CRON-ANCH-001", family="cron.anchoring",
      title="Start instant exactly on an occurrence: inclusive or exclusive?",
      kind="cron", op="cron.next",
      input=cron_in("0 12 * * *", "2026-01-01T12:00:00", 3),
      classification="POLICY_DEPENDENT", policy_axis="cron.start_inclusivity",
      normative=[cite("crontab5", note="crontab(5) describes a daemon matching "
                                       "the current minute; it says nothing "
                                       "about a 'next occurrence after T' API, "
                                       "which is a library invention")],
      expect=cases("per_policy", [
          ("exclusive", {"cron.start_inclusivity": "exclusive"},
           ref("0 12 * * *", VIXIE, "2026-01-01T12:00:00", 3, inclusive=False),
           "Strictly after the start instant. croniter get_next, cron-parser, "
           "croner default."),
          ("inclusive", {"cron.start_inclusivity": "inclusive"},
           ref("0 12 * * *", VIXIE, "2026-01-01T12:00:00", 3, inclusive=True),
           "At or after. APScheduler's get_next_fire_time(None, now) and "
           "several schedulers' catch-up paths."),
      ], "An off-by-one that duplicates or drops exactly one run, always at a "
         "boundary, and only when the caller's clock lands exactly on the "
         "schedule."),
      rationale=("No cron document defines a 'next after T' function, so its "
                 "inclusivity is a library policy. It is the most common "
                 "source of duplicate-fire bugs in catch-up logic, and the "
                 "corpus makes the axis explicit rather than picking a "
                 "winner."),
      tags=["anchoring", "policy", "headline"])

    V(id="CRON-ANCH-002", family="cron.anchoring",
      title="Sub-minute start instant (seconds and micros in the anchor)",
      kind="cron", op="cron.next",
      input=cron_in("0 12 * * *", "2026-01-01T12:00:30", 2),
      classification="POLICY_DEPENDENT", policy_axis="cron.start_truncation",
      normative=[cite("crontab5")],
      expect=cases("per_policy", [
          ("truncate-to-minute", {"cron.start_truncation": "truncate"},
           ref("0 12 * * *", VIXIE, "2026-01-01T12:00:00", 2, inclusive=False),
           "Engines that floor the anchor to the minute then step; the 12:00 "
           "occurrence of the same day is already past."),
          ("exact", {"cron.start_truncation": "exact"},
           ref("0 12 * * *", VIXIE, "2026-01-01T12:00:30", 2),
           "Engines comparing exact instants — same answer here, but see "
           "CRON-ANCH-003 where they differ."),
      ]),
      rationale="Truncation policy is invisible until it is not; pairing this "
                "with ANCH-003 isolates it.",
      tags=["anchoring", "policy"])

    V(id="CRON-ANCH-003", family="cron.anchoring",
      title="Sub-minute start instant, seconds-granularity expression",
      kind="cron", op="cron.next",
      input=cron_in("30 * * * * *", "2026-01-01T12:00:15", 3, fields=6),
      classification="POLICY_DEPENDENT", policy_axis="cron.start_truncation",
      normative=[cite("quartz")],
      expect=cases("per_policy", [
          ("exact", {"cron.start_truncation": "exact"},
           ref("30 * * * * *", SEC6, "2026-01-01T12:00:15", 3),
           "12:00:30 is still ahead of the anchor and must be emitted."),
          ("truncate-to-minute", {"cron.start_truncation": "truncate"},
           ref("30 * * * * *", SEC6, "2026-01-01T12:01:00", 3),
           "Engines that floor to the minute lose the 12:00:30 firing."),
      ]),
      rationale="Directly measurable divergence caused by an undocumented "
                "internal truncation.",
      tags=["anchoring", "policy", "seconds"])

    V(id="CRON-ANCH-004", family="cron.anchoring",
      title="Cron has no anchor: '*/7' in the day field restarts each month",
      kind="cron", op="cron.next",
      input=cron_in("0 0 */7 * *", "2026-01-01T00:00:00", 10),
      classification="NORMATIVE",
      normative=[cite("crontab5", "steps are evaluated just within the field "
                                  "they are applied to"),
                 cite("rfc5545-3.3.10",
                      "The DTSTART ... are used as the seed values, and then "
                      "the RRULE is applied to the seed values",
                      note="contrast: RRULE's INTERVAL counts periods from "
                           "DTSTART; cron has no seed at all")],
      expect=single(ref("0 0 */7 * *", VIXIE, "2026-01-01T00:00:00", 10),
                    "Days 1,8,15,22,29 of every month; the 29→1 gap is 3, 2 or "
                    "4 days depending on month length."),
      rationale=("The structural difference between the two grammars, stated "
                 "as one executable vector: cron is a predicate over instants "
                 "with no origin, RRULE is a generator from an anchor. Any "
                 "unified model must reproduce both columns."),
      tags=["anchoring", "cross-grammar", "headline"])

    # =================================================================
    # FAMILY: cron.dst
    # =================================================================
    def dst_vec(id_, expr, zone, start, n, title, rationale, tags=(),
                fields=5, pol=None):
        pol = pol or VIXIE
        cs = []
        for lab, gap, fold, note in [
            ("skip", "skip", "first",
             "crontab(5): jobs in the missing hour never run; jobs in the "
             "repeated hour run twice — but the second half of that sentence "
             "is a *daemon* behaviour, so a library that returns a set must "
             "still choose."),
            ("next_valid", "next_valid", "first",
             "Fire at the first valid wall time at or after the nominal one "
             "(croniter's default; APScheduler; most cloud schedulers)."),
            ("fire_at_gap_start", "fire_at_gap_start", "first",
             "Fire at the instant the gap opens (i.e. the pre-gap offset "
             "applied to the wall time) — RFC 5545 §3.3.5 as routed by "
             "erratum 4271."),
            ("fold_both", "next_valid", "both",
             "Emit both instants of an ambiguous wall time (Vixie daemon "
             "behaviour for repeated hours, and cronsim's option)."),
            ("fold_second", "next_valid", "second",
             "Emit only the second (post-transition) instant."),
        ]:
            p = R.Policy(dom_dow=pol.dom_dow, dow_zero_seven=pol.dow_zero_seven,
                         fields=fields, seconds_leading=(fields == 6),
                         dst_gap=gap, dst_fold=fold,
                         allow_L=pol.allow_L, allow_W=pol.allow_W,
                         allow_hash=pol.allow_hash, allow_qmark=pol.allow_qmark)
            try:
                occ = ref(expr, p, start, n, zone=zone)
            except R.CronRefError:
                occ = None
            cs.append((lab, {"cron.dst_gap": gap, "cron.dst_fold": fold}, occ,
                       note))
        V(id=id_, family="cron.dst", title=title, kind="cron", op="cron.next",
          input=cron_in(expr, start, n, zone=zone, fields=fields),
          classification="POLICY_DEPENDENT",
          policy_axis="cron.dst_gap|cron.dst_fold",
          context={"tzdb_min": "2025c", "policy": {"cron.dst_gap": "declared",
                                                   "cron.dst_fold": "declared"},
                   "requires": ["tz.zoneinfo"]},
          normative=[
              cite("crontab5",
                   "Jobs ... which are scheduled during the 'missing times' "
                   "will never be run. ... times which occur more than once ... "
                   "will cause matching jobs to be run twice."),
              cite("rfc5545-3.3.5",
                   "If the local time described occurs more than once ... the "
                   "DATE-TIME value refers to the first occurrence ... If the "
                   "local time ... does not occur ... the DATE-TIME value is "
                   "interpreted using the UTC offset before the gap."),
              cite("eid4271"),
          ],
          expect=cases("per_policy", cs,
                       "Five policies, five different occurrence sets. No "
                       "source arbitrates for a *library*; crontab(5) speaks "
                       "only about a daemon."),
          rationale=rationale, tags=list(tags) + ["dst"])

    dst_vec("CRON-DST-001", "30 2 * * *", "America/New_York",
            "2026-03-07T00:00:00", 4,
            "Spring-forward gap: 02:30 daily across the US DST start",
            "The canonical DST vector. crontab(5) says the job never runs; "
            "every hosted scheduler and most libraries run it anyway, at four "
            "different instants. This is the vector that makes 'DST-safe' "
            "falsifiable.", tags=["gap", "headline"])
    dst_vec("CRON-DST-002", "30 1 * * *", "America/New_York",
            "2026-10-30T00:00:00", 4,
            "Autumn fold: 01:30 daily across the US DST end",
            "The repeated wall time. A daemon fires twice; a library returning "
            "a set must decide whether the set contains one instant or two, "
            "and the choice changes occurrence identity, not just timing.",
            tags=["fold", "headline"])
    dst_vec("CRON-DST-003", "15 2 * * *", "Australia/Lord_Howe",
            "2026-10-02T00:00:00", 4,
            "30-minute DST transition (Lord Howe Island): 02:15 daily",
            "Lord Howe shifts by 00:30, so the gap is 02:00-02:30 and the "
            "'shift by one hour' assumption baked into many engines produces "
            "an instant inside the gap or an hour late.",
            tags=["gap", "half-hour"])
    dst_vec("CRON-DST-004", "45 1 * * *", "Australia/Lord_Howe",
            "2026-04-03T00:00:00", 4,
            "30-minute fold (Lord Howe Island): 01:45 daily",
            "The ambiguous window is only 30 minutes wide; engines that "
            "hard-code a 60-minute fold either miss it or over-apply it.",
            tags=["fold", "half-hour"])
    dst_vec("CRON-DST-005", "30 1 * * *", "Antarctica/Troll",
            "2026-03-27T00:00:00", 4,
            "Two-hour DST transition (Antarctica/Troll): 01:30 daily",
            "Troll jumps +00 to +02 in one step. Any engine that resolves a "
            "gap by adding one hour lands *inside* the gap and either loops or "
            "emits an impossible instant.", tags=["gap", "two-hour", "headline"])
    dst_vec("CRON-DST-006", "30 1 * * *", "Antarctica/Troll",
            "2026-10-24T00:00:00", 4,
            "Two-hour fold (Antarctica/Troll): 01:30 daily",
            "The two-hour ambiguous window is the widest in the tzdb and the "
            "most likely to break fold handling.", tags=["fold", "two-hour"])
    dst_vec("CRON-DST-007", "0 12 30 * *", "Pacific/Apia",
            "2011-11-01T00:00:00", 3,
            "A whole calendar day that does not exist (Pacific/Apia 2011-12-30)",
            "Apia crossed the date line: 2011-12-30 never existed in local "
            "time. A monthly 'the 30th at noon' schedule has an occurrence "
            "with no instant. Gap policies that search forward by minutes "
            "must search across a 24-hour discontinuity.",
            tags=["gap", "skipped-day", "headline"])
    dst_vec("CRON-DST-008", "30 0 * * *", "Asia/Amman",
            "2022-10-27T00:00:00", 4,
            "Zero-offset-change transition (Asia/Amman, October 2022)",
            "Jordan abolished DST by making +03 permanent; the 2022-10-28 "
            "transition changes the abbreviation and the DST flag but not the "
            "offset. Engines keyed on isdst rather than on utcoffset report a "
            "transition where there is no discontinuity.",
            tags=["zero-offset"])
    dst_vec("CRON-DST-009", "30 0 * * *", "Asia/Damascus",
            "2022-10-27T00:00:00", 4,
            "Zero-offset-change transition (Asia/Damascus, October 2022)",
            "Syria made +03 permanent in the same season; paired with Amman it "
            "isolates the isdst-vs-offset bug from any single zone's data.",
            tags=["zero-offset"])
    dst_vec("CRON-DST-010", "30 0 * * *", "Asia/Kathmandu",
            "2026-01-01T00:00:00", 3,
            "Non-hour standard offset (+05:45, Asia/Kathmandu)",
            "No transition here — the vector exists to catch engines that "
            "assume offsets are whole hours when formatting or when computing "
            "'midnight'.", tags=["non-hour-offset"])
    dst_vec("CRON-DST-011", "30 0 * * *", "Australia/Eucla",
            "2026-01-01T00:00:00", 3,
            "Non-hour standard offset (+08:45, Australia/Eucla)",
            "Second non-hour offset, chosen because the quarter-hour component "
            "differs from Kathmandu's.", tags=["non-hour-offset"])
    dst_vec("CRON-DST-012", "0 12 * * *", "Europe/Lisbon",
            "1992-09-25T00:00:00", 4,
            "Historical standard-offset change (Europe/Lisbon, 1992-09-27)",
            "Lisbon moved from WET to CET in 1992 — a change to the *standard* "
            "offset, not a DST rule. Engines that cache a zone's standard "
            "offset once produce a one-hour error for all historical "
            "occurrences.", tags=["historical"])
    dst_vec("CRON-DST-013", "0 12 * * *", "America/New_York",
            "2007-03-09T00:00:00", 4,
            "Historical DST rule change (US Energy Policy Act, 2007)",
            "The US moved DST start from April to March in 2007. A vector "
            "before and after the rule change catches engines that apply the "
            "current rule to historical dates.", tags=["historical"])
    dst_vec("CRON-DST-014", "30 2 * * *", "America/Santiago",
            "2026-09-05T00:00:00", 4,
            "Southern-hemisphere spring forward (America/Santiago)",
            "Reverses the sign convention of the northern-hemisphere vectors "
            "so that a hard-coded 'March is spring forward' assumption fails.",
            tags=["gap", "southern"])
    dst_vec("CRON-DST-015", "30 23 * * *", "America/St_Johns",
            "2026-03-07T00:00:00", 4,
            "Half-hour standard offset with DST (America/St_Johns, -03:30)",
            "Newfoundland combines a non-hour offset with an ordinary DST "
            "rule; the gap is 00:01-01:00 local, not 02:00-03:00.",
            tags=["gap", "non-hour-offset"])
    dst_vec("CRON-DST-016", "0 * * * *", "America/New_York",
            "2026-11-01T00:00:00", 6,
            "Hourly schedule across the fold: how many 01:00s?",
            "An hourly cron is the case where the fold policy is directly "
            "observable as a count: five or six firings between 00:00 and "
            "04:00 depending on the policy.", tags=["fold", "headline"])
    dst_vec("CRON-DST-017", "*/30 * * * *", "America/New_York",
            "2026-03-08T00:00:00", 8,
            "Half-hourly schedule across the gap: how many firings?",
            "The count-based counterpart to DST-016 on the gap side.",
            tags=["gap"])
    dst_vec("CRON-DST-018", "0 0 * * *", "Pacific/Kiritimati",
            "2026-01-01T00:00:00", 3,
            "Extreme positive offset (+14:00, Pacific/Kiritimati)",
            "The largest offset in the tzdb; catches engines that assume "
            "offsets fit in [-12,+12] or that normalise through a 32-bit "
            "minute count.", tags=["extreme-offset"])
    dst_vec("CRON-DST-019", "0 0 * * *", "Pacific/Niue",
            "2026-01-01T00:00:00", 3,
            "Extreme negative offset (-11:00, Pacific/Niue)",
            "Lower bound counterpart to DST-018.", tags=["extreme-offset"])
    dst_vec("CRON-DST-020", "30 2 * * SUN", "Europe/London",
            "2026-03-01T00:00:00", 4,
            "Weekly schedule landing exactly on the transition Sunday",
            "The gap and the DOW restriction interact: a weekly job at 02:30 "
            "on Sundays hits the gap on exactly one Sunday a year, so the "
            "'skip' policy silently drops a whole week rather than a day.",
            tags=["gap", "weekly"])
