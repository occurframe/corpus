# Vector format v1 — grammar

One vector per line of a `.jsonl` file. No comments, no folding, no
continuation lines: a line is a complete JSON object, so any language with a
JSON parser can consume the corpus without writing a lexer.

```
corpus-file   = *( vector LF )
vector        = <a JSON object matching the schema below>
```

## Schema

```jsonc
{
  "corpus_version": "1.0.0-rc1",     // string, semver-ish; see VERSIONING
  "id":        "CRON-DAYF-001",      // STABLE case ID; never reused, never renumbered
  "family":    "cron.day-fields",    // semantic family, dotted
  "title":     "Friday the 13th: the canonical DOM/DOW collision",
  "kind":      "cron" | "rrule",
  "op":        "cron.next" | "cron.parse" | "rrule.expand"
             | "rrule.parse" | "rrule.between",

  "input": {                          // the expression plus its anchor and zone
    "kind":   "cron",
    "expr":   "0 12 13 * FRI",
    "start":  "2026-01-01T00:00:00",  // naive local time, interpreted in `zone`
    "count":  6,
    "zone":   null | "America/New_York",
    "fields": 5 | 6 | 7,
    "inclusive": false
  },
  // ... or, for kind == "rrule":
  // "input": { "kind":"rrule", "ics":"DTSTART;TZID=...:...\nRRULE:...",
  //            "count":6, "zone":"America/New_York",
  //            "between":["1997-09-04T09:00:00","1997-09-06T09:00:00"] }

  "context": {                        // REQUIRED CONTEXTUAL DATA
    "tzdb_min":  null | "2025c",      // oldest tzdb release that yields the expectation
    "tzdb_pin":  null | "per-case",   // "per-case" => expect.cases are keyed by tzdb
    "dialect":   null | "vixie" | "declared",
    "policy":    { "cron.dom_dow": "declared" },
    "requires":  ["cron.5field", "tz.zoneinfo"]
  },

  "classification": "NORMATIVE" | "POLICY_DEPENDENT" | "DIALECT_DEPENDENT"
                  | "AMBIGUOUS_STANDARD" | "KNOWN_DIVERGENCE" | "INVALID",
  "policy_axis":  null | "cron.dom_dow" | "cron.dst_gap|cron.dst_fold",
  "dialect_axis": null | "cron.dialect" | "rrule.profile",

  "normative": [                      // NORMATIVE SOURCE, where one exists
    { "key": "crontab5",
      "title": "crontab(5), Vixie/cronie lineage",
      "url":   "https://man7.org/linux/man-pages/man5/crontab.5.html",
      "quote": "If both fields are restricted ...",   // optional, verbatim
      "note":  "…" }                                  // optional, editorial
  ],

  "expect": { ... },                  // EXPECTED OR ADMISSIBLE OUTCOMES; see below

  "incumbents": {                     // KNOWN INCUMBENT OUTPUTS + ENGINE VERSIONS
    "croniter@tz2026a": {             //   + TZDB PROVENANCE, frozen from a run
      "engine": "croniter",
      "engine_version": "6.3.0.dev0 (git kiorky/croniter @3dd4d14 2026-08-14)",
      "language": "python 3.11.15",
      "tzdb": "2026a", "tzdb_source": "/usr/share/zoneinfo",
      "status": "ok", "occurrences": ["2026-01-02T12:00:00", "..."]
    }
  },

  "rationale": "…",                   // CLASSIFICATION RATIONALE: why this class,
                                      // and why the vector is worth its weight
  "tags": ["dom_dow", "headline"]
}
```

## `expect`

Five modes. The mode determines how a runner's output is graded.

```jsonc
{"mode": "single",  "occurrences": ["…"], "note": "…"}
{"mode": "reject",  "error_class": "field_value_out_of_range", "note": "…"}
{"mode": "per_policy"   | "per_dialect" | "admissible",
 "cases": [ {"label": "or/vixie",
             "when":  {"cron.dom_dow": "or/vixie"},
             "occurrences": ["…"] | null,      // null == "must reject"
             "note":  "…"} ],
 "note": "…"}
{"mode": "open", "note": "why this is measured but not scored"}
```

* `single` — byte equality with the whole array. Used only where a source
  supplies one answer.
* `reject` — the engine must fail. `error_class` names the required failure,
  for reporting; the corpus does not require a particular exception type,
  because no two languages agree on one.
* `per_policy` / `per_dialect` / `admissible` — the output must equal exactly
  one case. The matching case's `label` is recorded, so the matrix reports
  *which* policy an engine implements rather than only whether it passed. A
  case with `"occurrences": null` matches a rejection.
* `open` — recorded, never scored. Reserved for `AMBIGUOUS_STANDARD` and
  `KNOWN_DIVERGENCE` vectors whose admissible space cannot be honestly
  enumerated.

`when` is the machine-readable statement of the policy axis: a conforming
product declares its policy as a `{axis: value}` map, and the corpus can then
select the single case that product must satisfy.

## Classification, normatively

| class | meaning | `expect.mode` normally used |
|---|---|---|
| `NORMATIVE` | a standard or authoritative document supplies one right answer | `single` |
| `POLICY_DEPENDENT` | the answer depends on a declared policy the standards do not fix | `per_policy` |
| `DIALECT_DEPENDENT` | the answer depends on the declared cron dialect or RRULE profile | `per_dialect` |
| `AMBIGUOUS_STANDARD` | the standard genuinely does not say; cite the ambiguity | `admissible` or `open` |
| `KNOWN_DIVERGENCE` | implementations differ and no source arbitrates | `admissible` or `open` |
| `INVALID` | the input must be rejected; `error_class` states the required error | `reject` |

## Identifier grammar

```
id      = FAMILY "-" SUBFAMILY "-" 3DIGIT
FAMILY  = "CRON" / "RRULE" / "TZDB"
```

IDs are permanent. A vector whose expectation is found to be wrong is
**corrected in place** if the input is unchanged, and **retired** (kept, with
`"status": "retired"` and a pointer to its replacement) if the input must
change. Numbers are never reused.
