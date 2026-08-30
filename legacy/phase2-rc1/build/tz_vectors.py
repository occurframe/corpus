"""Timezone-database provenance vectors.

These vectors have no single correct answer independent of a tzdb version.
Their purpose is to make the *data dependency* falsifiable: an engine that
reports a result without declaring which tzdb produced it has told you
nothing, and two engines that disagree here may both be correct.

The corpus therefore pins an expected answer PER TZDB RELEASE, and the runner
is required to report the tzdb version it actually used.
"""
from __future__ import annotations

from common import V, cite, cases, single, open_, cron_in, rrule_in

VAN = "America/Vancouver"
EDM = "America/Edmonton"
CAS = "Africa/Casablanca"


def build():
    V(id="TZDB-001", family="tzdb.provenance",
      title="America/Vancouver noon daily across 2026-11-01 "
            "(BC abolished DST in tzdb 2026b)",
      kind="cron", op="cron.next",
      input=cron_in("0 12 * * *", "2026-10-30T00:00:00", 4, zone=VAN),
      classification="POLICY_DEPENDENT", policy_axis="tz.tzdb_version",
      context={"tzdb_min": None, "tzdb_pin": "per-case",
               "requires": ["tz.zoneinfo"]},
      normative=[cite("tzdb-2026b",
                      "British Columbia's 2026-03-08 spring forward was its "
                      "last foreseeable clock change, as it moved to permanent "
                      "-07 thereafter.",
                      note="tzdb models the change at 2026-11-01 02:00 to work "
                           "around a CLDR limitation, although it legally took "
                           "place on 2026-03-09"),
                 cite("tzdb-news")],
      expect=cases("per_policy", [
          ("tzdb<=2026a", {"tz.tzdb_version": "2026a"},
           ["2026-10-30T12:00:00-07:00|2026-10-30T19:00:00Z",
            "2026-10-31T12:00:00-07:00|2026-10-31T19:00:00Z",
            "2026-11-01T12:00:00-08:00|2026-11-01T20:00:00Z",
            "2026-11-02T12:00:00-08:00|2026-11-02T20:00:00Z"],
           "Ordinary PDT->PST fall back on 2026-11-01."),
          ("tzdb>=2026b", {"tz.tzdb_version": "2026b"},
           ["2026-10-30T12:00:00-07:00|2026-10-30T19:00:00Z",
            "2026-10-31T12:00:00-07:00|2026-10-31T19:00:00Z",
            "2026-11-01T12:00:00-07:00|2026-11-01T19:00:00Z",
            "2026-11-02T12:00:00-07:00|2026-11-02T19:00:00Z"],
           "Permanent -07; the abbreviation becomes MST and the clock never "
           "goes back."),
      ], "A one-hour difference in the absolute firing time of a daily job, "
         "caused entirely by which tzdb the process loaded."),
      rationale=("The corpus's proof that engine version is not sufficient "
                 "provenance. Two runs of the identical library on the "
                 "identical expression differ by an hour because one process "
                 "read /usr/share/zoneinfo and the other read a bundled copy. "
                 "Any conformance claim that does not name a tzdb release is "
                 "unfalsifiable."),
      tags=["tzdb", "provenance", "headline"])

    V(id="TZDB-002", family="tzdb.provenance",
      title="America/Edmonton noon daily across 2026-11-01 "
            "(Alberta abolished DST in tzdb 2026c)",
      kind="cron", op="cron.next",
      input=cron_in("0 12 * * *", "2026-10-30T00:00:00", 4, zone=EDM),
      classification="POLICY_DEPENDENT", policy_axis="tz.tzdb_version",
      context={"tzdb_min": None, "tzdb_pin": "per-case"},
      normative=[cite("tzdb-2026c",
                      "Alberta's 2026-03-08 spring forward was its last "
                      "foreseeable clock change, as it moved to permanent -06 "
                      "thereafter."),
                 cite("tzdb-news")],
      expect=cases("per_policy", [
          ("tzdb<=2026b", {"tz.tzdb_version": "2026b"},
           ["2026-10-30T12:00:00-06:00|2026-10-30T18:00:00Z",
            "2026-10-31T12:00:00-06:00|2026-10-31T18:00:00Z",
            "2026-11-01T12:00:00-07:00|2026-11-01T19:00:00Z",
            "2026-11-02T12:00:00-07:00|2026-11-02T19:00:00Z"],
           "Ordinary MDT->MST fall back."),
          ("tzdb>=2026c", {"tz.tzdb_version": "2026c"},
           ["2026-10-30T12:00:00-06:00|2026-10-30T18:00:00Z",
            "2026-10-31T12:00:00-06:00|2026-10-31T18:00:00Z",
            "2026-11-01T12:00:00-06:00|2026-11-01T18:00:00Z",
            "2026-11-02T12:00:00-06:00|2026-11-02T18:00:00Z"],
           "Permanent -06, reported with the abbreviation CST."),
      ], "Deliberately paired with TZDB-001: the two provinces changed in "
         "DIFFERENT tzdb releases, so a process on 2026b is correct for "
         "Vancouver and wrong for Edmonton."),
      rationale=("The pair is a three-way discriminator: a run that gets "
                 "TZDB-001 right and TZDB-002 wrong is on 2026b exactly; both "
                 "wrong is <=2026a; both right is >=2026c. The corpus can "
                 "therefore *infer* an engine's tzdb release from its output, "
                 "which is what makes tzdb provenance auditable rather than "
                 "self-reported."),
      tags=["tzdb", "provenance", "discriminator", "headline"])

    V(id="TZDB-003", family="tzdb.provenance",
      title="Africa/Casablanca: Morocco moves to permanent UTC on 2026-09-20",
      kind="cron", op="cron.next",
      input=cron_in("0 12 * * *", "2026-09-18T00:00:00", 4, zone=CAS),
      classification="POLICY_DEPENDENT", policy_axis="tz.tzdb_version",
      context={"tzdb_min": None, "tzdb_pin": "per-case"},
      normative=[cite("tzdb-2026c",
                      "Morocco plans to move back to permanent UTC, without "
                      "daylight saving time transitions, on 2026-09-20 at "
                      "02:00.")],
      expect=cases("per_policy", [
          ("tzdb<=2026b", {"tz.tzdb_version": "2026b"},
           ["2026-09-18T12:00:00+01:00|2026-09-18T11:00:00Z",
            "2026-09-19T12:00:00+01:00|2026-09-19T11:00:00Z",
            "2026-09-20T12:00:00+01:00|2026-09-20T11:00:00Z",
            "2026-09-21T12:00:00+01:00|2026-09-21T11:00:00Z"],
           "Morocco's pre-2026c model keeps +01 outside Ramadan."),
          ("tzdb>=2026c", {"tz.tzdb_version": "2026c"},
           ["2026-09-18T12:00:00+01:00|2026-09-18T11:00:00Z",
            "2026-09-19T12:00:00+01:00|2026-09-19T11:00:00Z",
            "2026-09-20T12:00:00+00:00|2026-09-20T12:00:00Z",
            "2026-09-21T12:00:00+00:00|2026-09-21T12:00:00Z"],
           "Permanent UTC from 2026-09-20 02:00."),
      ], "A third province of the same problem, on a different continent and "
         "in a zone whose rules are also Ramadan-dependent."),
      rationale=("Chosen because Morocco's rule is *predictive*: the tzdb "
                 "entry encodes a plan, not a fait accompli. A schedule "
                 "computed today for 2027 can change meaning when the plan "
                 "does, which is the strongest argument that occurrence "
                 "materialisation must record its tzdb."),
      tags=["tzdb", "provenance", "predictive"])

    V(id="TZDB-004", family="tzdb.provenance",
      title="RRULE weekly at 12:00 in America/Vancouver across the same boundary",
      kind="rrule", op="rrule.expand",
      input=rrule_in(f"DTSTART;TZID={VAN}:20261018T120000\n"
                     "RRULE:FREQ=WEEKLY;COUNT=4", count=5, zone=VAN),
      classification="POLICY_DEPENDENT", policy_axis="tz.tzdb_version",
      context={"tzdb_pin": "per-case"},
      normative=[cite("tzdb-2026b")],
      expect=cases("per_policy", [
          ("tzdb<=2026a", {"tz.tzdb_version": "2026a"},
           ["2026-10-18T12:00:00-07:00|2026-10-18T19:00:00Z",
            "2026-10-25T12:00:00-07:00|2026-10-25T19:00:00Z",
            "2026-11-01T12:00:00-08:00|2026-11-01T20:00:00Z",
            "2026-11-08T12:00:00-08:00|2026-11-08T20:00:00Z"], None),
          ("tzdb>=2026b", {"tz.tzdb_version": "2026b"},
           ["2026-10-18T12:00:00-07:00|2026-10-18T19:00:00Z",
            "2026-10-25T12:00:00-07:00|2026-10-25T19:00:00Z",
            "2026-11-01T12:00:00-07:00|2026-11-01T19:00:00Z",
            "2026-11-08T12:00:00-07:00|2026-11-08T19:00:00Z"], None),
      ]),
      rationale="Shows the provenance dependency is a property of the zone "
                "data, not of the expression grammar: the RRULE and cron "
                "vectors diverge identically.",
      tags=["tzdb", "provenance", "cross-grammar"])

    V(id="TZDB-005", family="tzdb.provenance",
      title="A gap that exists under one tzdb and not another "
            "(America/Vancouver 2027-03-14 02:30)",
      kind="cron", op="cron.next",
      input=cron_in("30 2 * * *", "2027-03-12T00:00:00", 4, zone=VAN),
      classification="POLICY_DEPENDENT",
      policy_axis="tz.tzdb_version|cron.dst_gap",
      context={"tzdb_pin": "per-case"},
      normative=[cite("tzdb-2026b")],
      expect=cases("per_policy", [
          ("tzdb<=2026a/gap-skip", {"tz.tzdb_version": "2026a",
                                    "cron.dst_gap": "skip"},
           ["2027-03-12T02:30:00-08:00|2027-03-12T10:30:00Z",
            "2027-03-13T02:30:00-08:00|2027-03-13T10:30:00Z",
            "2027-03-15T02:30:00-07:00|2027-03-15T09:30:00Z",
            "2027-03-16T02:30:00-07:00|2027-03-16T09:30:00Z"],
           "2027-03-14T02:30 is inside the spring-forward gap and is skipped."),
          ("tzdb<=2026a/next-valid", {"tz.tzdb_version": "2026a",
                                      "cron.dst_gap": "next_valid"},
           ["2027-03-12T02:30:00-08:00|2027-03-12T10:30:00Z",
            "2027-03-13T02:30:00-08:00|2027-03-13T10:30:00Z",
            "2027-03-14T03:00:00-07:00|2027-03-14T10:00:00Z",
            "2027-03-15T02:30:00-07:00|2027-03-15T09:30:00Z"], None),
          ("tzdb>=2026b", {"tz.tzdb_version": "2026b"},
           ["2027-03-12T02:30:00-07:00|2027-03-12T09:30:00Z",
            "2027-03-13T02:30:00-07:00|2027-03-13T09:30:00Z",
            "2027-03-14T02:30:00-07:00|2027-03-14T09:30:00Z",
            "2027-03-15T02:30:00-07:00|2027-03-15T09:30:00Z"],
           "No transition exists at all, so the DST policy is not even "
           "reached and every day fires."),
      ], "Two policy axes compose: the DST-gap policy is only observable under "
         "one of the two tzdb releases."),
      rationale=("The most subtle failure this corpus can express. A test "
                 "suite that pins the DST policy but not the tzdb will pass "
                 "or fail depending on when the container image was built, "
                 "and the failure will look like a scheduling bug."),
      tags=["tzdb", "provenance", "gap", "headline"])

    V(id="TZDB-006", family="tzdb.provenance",
      title="Zone abbreviation is not a stable identifier "
            "(Edmonton reports CST at -06:00)",
      kind="cron", op="cron.next",
      input=cron_in("0 12 * * *", "2027-01-14T00:00:00", 2, zone=EDM),
      classification="POLICY_DEPENDENT", policy_axis="tz.tzdb_version",
      context={"tzdb_pin": "per-case"},
      normative=[cite("tz-theory",
                      note="tzdb abbreviations are advisory and are neither "
                           "unique nor stable across releases"),
                 cite("tzdb-2026c")],
      expect=cases("per_policy", [
          ("tzdb<=2026b", {"tz.tzdb_version": "2026b"},
           ["2027-01-14T12:00:00-07:00|2027-01-14T19:00:00Z",
            "2027-01-15T12:00:00-07:00|2027-01-15T19:00:00Z"],
           "MST."),
          ("tzdb>=2026c", {"tz.tzdb_version": "2026c"},
           ["2027-01-14T12:00:00-06:00|2027-01-14T18:00:00Z",
            "2027-01-15T12:00:00-06:00|2027-01-15T18:00:00Z"],
           "Reported as CST — the abbreviation of a zone 1,200 km to the east. "
           "Any system that persists 'MST' rather than 'America/Edmonton' is "
           "now storing a wrong answer."),
      ]),
      rationale=("Included to close a specific product question: whether an "
                 "occurrence record may store an offset or an abbreviation "
                 "instead of an IANA zone id. It may not, and this vector is "
                 "the proof."),
      tags=["tzdb", "provenance", "identity"])

    V(id="TZDB-007", family="tzdb.provenance",
      title="A zone whose historical data changed: Europe/Lisbon 1992",
      kind="cron", op="cron.next",
      input=cron_in("0 12 * * *", "1992-09-25T00:00:00", 4,
                    zone="Europe/Lisbon"),
      classification="NORMATIVE",
      context={"tzdb_min": "2020a"},
      normative=[cite("tz-theory",
                      note="historical data is revised between releases; the "
                           "1992 Portugal change is stable in modern tzdb")],
      expect=single(["1992-09-25T12:00:00+01:00|1992-09-25T11:00:00Z",
                     "1992-09-26T12:00:00+01:00|1992-09-26T11:00:00Z",
                     "1992-09-27T12:00:00+01:00|1992-09-27T11:00:00Z",
                     "1992-09-28T12:00:00+01:00|1992-09-28T11:00:00Z"],
                    "Portugal moved from WET to CET on 1992-09-27 at 01:00 "
                    "UTC, changing the STANDARD offset rather than a DST rule. "
                    "Noon local stays noon local; the UTC instant moves."),
      rationale=("Distinguishes 'the zone's DST rule changed' from 'the zone's "
                 "standard offset changed'. Engines that cache a single "
                 "standard offset per zone fail only on the second kind, and "
                 "only for historical dates."),
      tags=["tzdb", "historical"])

    V(id="TZDB-008", family="tzdb.provenance",
      title="Unknown zone identifier", kind="cron", op="cron.parse",
      input=cron_in("0 12 * * *", "2026-01-01T00:00:00", 1,
                    zone="America/Not_A_Real_Zone"),
      classification="INVALID",
      normative=[cite("tz-theory")],
      expect=cases("admissible", [
          ("reject", {}, None,
           "Raise a zone-not-found error. Required."),
      ], "Engines that silently fall back to UTC or to the process's local "
         "zone produce a schedule that is off by the local offset and gives no "
         "diagnostic. That is the failure this vector detects."),
      rationale="A silent UTC fallback is the single easiest way to ship a "
                "scheduler that is wrong by hours in production and correct in "
                "CI, because CI runs in UTC.",
      tags=["tzdb", "invalid"])

    V(id="TZDB-009", family="tzdb.provenance",
      title="Deprecated zone alias (US/Pacific)", kind="cron", op="cron.next",
      input=cron_in("0 12 * * *", "2026-01-14T00:00:00", 2, zone="US/Pacific"),
      classification="DIALECT_DEPENDENT", policy_axis="tz.link_handling",
      dialect_axis="tz.database_profile",
      normative=[cite("tz-theory",
                      note="backward-compatibility Links are shipped in the "
                           "'backward' file and are omitted from some "
                           "slim/vanguard builds and from some ICU "
                           "configurations")],
      expect=cases("per_dialect", [
          ("links-present", {"tz.link_handling": "resolve"},
           ["2026-01-14T12:00:00-08:00|2026-01-14T20:00:00Z",
            "2026-01-15T12:00:00-08:00|2026-01-15T20:00:00Z"],
           "Resolves to America/Los_Angeles."),
          ("links-absent", {"tz.link_handling": "reject"}, None,
           "Builds without the 'backward' file reject the identifier."),
      ]),
      rationale=("Zone identifiers stored years ago may not resolve in a "
                 "modern slim tzdb build. This is a migration hazard for any "
                 "product that persists a zone string, and it is a property of "
                 "the *build* rather than of the release number."),
      tags=["tzdb", "aliases", "migration"])

    V(id="TZDB-010", family="tzdb.provenance",
      title="Etc/GMT+5 has a NEGATIVE offset (POSIX sign inversion)",
      kind="cron", op="cron.next",
      input=cron_in("0 12 * * *", "2026-01-14T00:00:00", 2, zone="Etc/GMT+5"),
      classification="NORMATIVE",
      normative=[cite("tz-theory",
                      note="the Etc/GMT[+-]N zones follow the POSIX TZ sign "
                           "convention, which is the opposite of ISO 8601")],
      expect=single(["2026-01-14T12:00:00-05:00|2026-01-14T17:00:00Z",
                     "2026-01-15T12:00:00-05:00|2026-01-15T17:00:00Z"],
                    "Etc/GMT+5 is UTC-05:00. An engine that maps the "
                    "identifier to +05:00 is ten hours wrong."),
      rationale="A documented, normative sign inversion that is nonetheless "
                "one of the most common zone-handling defects.",
      tags=["tzdb", "sign-convention"])
