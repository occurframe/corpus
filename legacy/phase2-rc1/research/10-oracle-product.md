# The oracle as a product

This section specifies the conformance corpus as a shipped artefact, written so an implementer can build, operate, govern and distribute it without further design decisions. It formalises `oracle/docs/FORMAT.md`, `oracle/docs/RUNNER-CONTRACT.md` and `oracle/docs/VERSIONING.md`, and adds the parts a document inside the repository cannot argue: licensing, neutrality, adoption.

**Epistemic key.** `[SPEC]` normative standards text · `[DOC]` vendor or project documentation · `[CODE]` read from source · `[FACT]` a checkable state of the world · `[MEASURED]` produced by running this corpus · `[INFER]` derivation from the labelled evidence.

---

## 1. What the oracle is, and what it is not

**It is** a versioned, language-neutral set of executable test vectors for cron expressions and RFC 5545 recurrence rules, each carrying its input, its required context, its classification, its normative citation, and — where the answer depends on a choice no standard makes — an enumeration of the admissible answers, each labelled by the policy that produces it. It ships with a runner contract, reference runners in five languages, a scorer, and frozen measurements of every engine it has been run against.

**It is a translation table before it is a scoreboard.** Its most useful output is not a percentage but a **policy profile**. `[MEASURED]` `matrix/conformance-croniter@tz2026a.md` says croniter implements `cron.dom_dow = or/vixie`, `cron.dow_numbering = both`, `cron.sixth_field = seconds_trailing`, `cron.dst_gap = next_valid`, `cron.start_inclusivity = exclusive`. `[INFER]` That is a migration document — it tells a team moving from croniter to cron-parser which of their expressions change meaning — and no library's documentation answers that today.

**It is not a specification.** Where two shipped resolutions of an ambiguity exist it names both, labels both, and records which engine implements which. `[INFER]` A document picking one would be the N+1th standard; a corpus enumerating them is useful to every incumbent immediately and costs nobody a dependency.

**It is not a quality scoreboard.** `[MEASURED]` `cron-parser[strict]` scores 60.7% because `strict: true` makes six fields mandatory, so it rejects every five-field POSIX expression — a configuration, not a defect.

**It is not an execution-layer test suite.** Missed runs, catch-up, overlap, idempotency and occurrence identity across restarts are outside it; `CRON-FIELDS-013` (`@reboot`) and `RRULE-SET-011` (a PERIOD-valued `RDATE`) mark the boundaries and are recorded as unscoreable.

**It is not an engine, and must never become one.** `reference/cron_ref.py` exists solely to derive expected values from a declared policy, and lives outside `runners/` so nobody can register it as an engine and score the corpus against itself.

---

## 2. The vector format

### 2.1 The precedent and its six failures

`[CODE]` The nearest existing artefact is libical's `src/test/icalrecur_test.txt` — roughly 180 cases in a bespoke `RRULE:` / `DTSTART:` / `INSTANCES:` format. As a *cross-language* artefact it fails on six counts, and each failure is a required field in the replacement: no stable identifier (cases are positional, so none can be cited); no classification (every case asserts one right answer, so the hard cases are unrepresentable); no timezone provenance; no source citation; no policy declaration (it encodes libical's resolutions, making it a description of libical rather than of RFC 5545); and a bespoke syntax costing a hand-written lexer per language.

### 2.2 Requirements, and why JSON Lines

Four requirements, in priority order: **parseable by a fifty-line script in any language** (cross-language adoption is the entire point); **one vector per line**, so a corpus can be sharded, filtered and diffed with line-oriented tools and a partial file is still valid; **self-describing**, because a reader meets one vector in a bug report, not the whole corpus; **extensible without breaking parsers**, because policy axes will be discovered after v1 — `[MEASURED]` three were discovered during this run.

JSON Lines satisfies all four; every language in the study has a JSON parser in its standard library. Two costs are accepted: JSONL is not hand-editable, so the corpus is generated from `build/` and the `.jsonl` files are the artefact; and a vector averages ~12 KB with its citations, rationale and frozen measurements. `[INFER]` That verbosity is the point — the metadata is what distinguishes a conformance corpus from a regression suite.

### 2.3 The grammar

```
corpus-file = *( vector LF )
vector      = <a single-line JSON object matching the schema below>
id          = FAMILY "-" SUBFAMILY "-" 3DIGIT
FAMILY      = "CRON" / "RRULE" / "TZDB"
```

```jsonc
{
  "corpus_version": "1.0.0-rc1",
  "id":        "CRON-DAYF-001",       // STABLE; never reused, never renumbered
  "family":    "cron.day-fields",     // dotted semantic family
  "title":     "Friday the 13th: the canonical DOM/DOW collision",
  "kind":      "cron" | "rrule",
  "op":        "cron.next" | "cron.parse" | "rrule.expand"
             | "rrule.parse" | "rrule.between",

  "input": { "kind":"cron", "expr":"0 12 13 * FRI",
             "start":"2026-01-01T00:00:00",   // naive local time, read in `zone`
             "count":6, "zone":null|"America/New_York",
             "fields":5|6|7, "inclusive":false },
  //  or:   { "kind":"rrule", "ics":"DTSTART;TZID=…:…\nRRULE:…",
  //          "count":6, "zone":"America/New_York", "between":["…","…"] }

  "context": { "tzdb_min": null|"2025c",     // oldest release the expectation holds for
               "tzdb_pin": null|"per-case",  // expectation keyed by release
               "dialect":  null|"vixie"|"declared",
               "policy":   {"cron.dom_dow":"declared"},
               "requires": ["cron.5field","tz.zoneinfo"] },

  "classification": "NORMATIVE" | "POLICY_DEPENDENT" | "DIALECT_DEPENDENT"
                  | "AMBIGUOUS_STANDARD" | "KNOWN_DIVERGENCE" | "INVALID",
  "policy_axis":  null | "cron.dom_dow" | "cron.dst_gap|cron.dst_fold",
  "dialect_axis": null | "cron.dialect" | "rrule.profile",

  "normative": [ {"key":"crontab5","title":"…","url":"…","quote":"…","note":"…"} ],
  "expect":    { … },                 // five modes; see §2.5
  "incumbents": { "croniter@tz2026a": {
      "engine":"croniter", "engine_version":"6.3.0.dev0 (git … @3dd4d14)",
      "language":"python 3.11.15", "tzdb":"2026a",
      "tzdb_source":"/usr/share/zoneinfo",
      "status":"ok", "occurrences":["…"] } },
  "rationale": "why this classification and why this vector earns its weight",
  "tags": ["dom_dow","headline"]
}
```

### 2.4 Why each required field earns its place

**`id`** lets a divergence be *cited*: "cron-parser fails `CRON-DST-003`" means something checkable. Without stable IDs a corpus is a test suite; with them it is a vocabulary.

**`family`** is how coverage is argued about and how a partial adopter selects a subset; filenames derive from families, so the layout is a projection of the taxonomy rather than a second thing to keep in sync.

**`input`** carries the anchor and the zone because a cron expression alone denotes nothing computable: `[SPEC]` crontab(5) describes a daemon matching the current minute, and every library's "next occurrence after T" is an invention with its own inclusivity semantics. `count` bounds an infinite set — a bound no standard supplies and every consumer must.

**`context`** closes three holes that make results incomparable. `tzdb_min` / `tzdb_pin` state which zone data the expectation assumes; a runner on older data is scored `N/A`, never `FAIL`, because a correct engine with stale zone data is not a non-conforming engine, and conflating the two is how tzdb-dependent suites become flaky. `dialect: "declared"` means the vector is unanswerable until the consumer states its dialect. `policy` is a machine-readable "tell me your policy before I grade you".

**`normative`** is a list of `{key, title, url, quote?, note?}`. The `quote` is verbatim standards text, so a reader can check the expectation without leaving the vector and a maintainer who disagrees has something to argue with; `key` indexes a shared registry — `[MEASURED]` `manifest.json` carries all 32 sources — so a citation is spelled identically everywhere and can be counted. **Vectors with an empty `normative` list are exactly the vectors that must not be classified `NORMATIVE`.**

**`incumbents`** is measured, never authored: produced by a separate freeze step (`tools/freeze_incumbents.py`) and re-injected at the next build. `[MEASURED]` 2,432 frozen observations ship with the corpus. Keeping it out of the authoring source is what stops the oracle becoming circular.

**`rationale`** says why this classification, why the vector earns its weight, and what a failure means — the field that makes the corpus reviewable by someone who was not present when it was written.

### 2.5 `expect`: five modes

```jsonc
{"mode":"single",  "occurrences":["…"], "note":"…"}
{"mode":"reject",  "error_class":"field_value_out_of_range", "note":"…"}
{"mode":"per_policy" | "per_dialect" | "admissible",
 "cases":[{"label":"or/vixie", "when":{"cron.dom_dow":"or/vixie"},
           "occurrences":["…"] | null,      // null == "must reject"
           "note":"…"}], "note":"…"}
{"mode":"open", "note":"why this is measured but not scored"}
```

`single` is byte equality with the whole array, used only where a source supplies one answer. `reject` requires failure; `error_class` names it *for reporting* — no particular exception type is required, because no two languages agree on one. The three multi-case modes require the output to equal exactly one case, and the matching `label` is recorded, so the matrix reports *which* policy an engine implements rather than only whether it passed. `open` is recorded and never scored.

### 2.6 One worked example per classification

**`NORMATIVE` — `RRULE-CORE-001`.** Op `rrule.expand`; `DTSTART;TZID=America/New_York:19970902T090000\nRRULE:FREQ=DAILY;COUNT=10`. Citation: `[SPEC]` RFC 5545 §3.8.5.3, quoted — "Daily for 10 occurrences: … ==> (1997 9:00 AM EDT) September 2-11". `mode: "single"`, ten occurrences from `1997-09-02T09:00:00-04:00|1997-09-02T13:00:00Z`. Rationale: "the control vector: if an engine fails this, nothing else it reports is interpretable."

**`POLICY_DEPENDENT` — `CRON-DST-001`.** `30 2 * * *` in `America/New_York` from 2026-03-07, count 4; `policy_axis = "cron.dst_gap|cron.dst_fold"`. Citations: `[DOC]` crontab(5) ("Jobs … scheduled during the 'missing times' will never be run") *and* `[SPEC]` RFC 5545 §3.3.5 with erratum 4271 (a nonexistent local time "is interpreted using the UTC offset before the gap"). `mode: "per_policy"` with five cases — `skip`, `next_valid`, `fire_at_gap_start`, `fold_both`, `fold_second` — each with a `when` map and its own occurrence list.

**`DIALECT_DEPENDENT` — `CRON-FIELDS-002`.** `0 15 10 * * *`, `fields: 6`, `policy_axis = "cron.sixth_field"`. Citations: `[DOC]` Quartz (`sec min hour dom month dow`) and `[DOC]` AWS EventBridge (`min hour dom month dow year`). `mode: "per_dialect"`: `seconds-leading` → `2026-01-01T10:15:00` daily; `year-trailing` → `2026-01-10T15:00:00` monthly; `reject` → `null`. Rationale: "both readings parse, both produce plausible schedules, and the difference is visible only in the seconds field."

**`AMBIGUOUS_STANDARD` — `RRULE-BY-026`.** `FREQ=YEARLY;BYWEEKNO=20;BYDAY=2MO`. Citations: `[SPEC]` errata **1913** and **3779**, both Verified and Technical, editing one sentence of §3.3.10 into two non-nested wordings. `mode: "open"`, noting that under 1913 the numeric prefix is invalid here and under 3779 it means the second Monday of the year, and that no consolidated text exists. Nothing is graded.

**`KNOWN_DIVERGENCE` — `CRON-DAYF-010`.** `0 12 *,10 * 2`. Citations: `[CODE]` vixie `entry.c` (`if (ch == '*') e->flags |= DOM_STAR;`) and `[DOC]` crontab.guru's "cron inspects the very first character of the day fields". `mode: "admissible"` with five cases (`vixie-artefact`, `or-set-semantics`, `or-any-nonstar`, `and+monday-zero`, `reject`). The rationale states why it is not `DIALECT_DEPENDENT`: reference implementation and reference documentation disagree, so no dialect can be declared.

**`INVALID` — `CRON-INV-005`.** `0 0 * 13 *`, op `cron.parse`. Citations: `[SPEC]` POSIX, `[DOC]` crontab(5). `mode: "reject"`, `error_class = "field_value_out_of_range"`. Rationale: "field-range and grammar enforcement; the cheapest conformance signal an engine emits."

### 2.7 The non-circularity rule

**No expected value in the corpus is copied from an engine.** Expectations come from three places only: a verbatim quotation from a normative source (including RFC 5545's own printed instance lists, which are specification text); calendar arithmetic from a rule the standard states in prose, with a structural assertion beside it — `[CODE]` `build/rrule_vectors.py` asserts weekday, day-of-month and ISO-week properties on every transcribed list and caught two authoring errors that way; or `reference/cron_ref.py`, parameterised by a declared policy, so admissible cases are *computed from a policy name* rather than typed. `[INFER]` An oracle that learns its answers from the systems it grades is not an oracle; the property is enforced structurally, not by discipline.

---

## 3. The classification taxonomy, normatively

### 3.1 The six labels

| class | admits a vector when | usual mode |
|---|---|---|
| `NORMATIVE` | a standard supplies exactly one right answer **and the vector quotes it verbatim** | `single` |
| `POLICY_DEPENDENT` | the answer depends on a runtime choice no standard fixes (gap, fold, inclusivity, truncation, tzdb release) | `per_policy` |
| `DIALECT_DEPENDENT` | the answer depends on a declared *syntax family* — cron dialect or RRULE profile | `per_dialect` |
| `AMBIGUOUS_STANDARD` | the standard does not say, or says two incompatible things, and the vector cites the specific silence, erratum or contradiction | `admissible` / `open` |
| `KNOWN_DIVERGENCE` | implementations differ and **no source arbitrates** — including where a reference implementation contradicts its own documentation | `admissible` / `open` |
| `INVALID` | the input must be rejected; `error_class` names the required failure | `reject` |

Two boundaries are load-bearing and often got wrong. A **policy** is something a *deployment* chooses and can change without touching the expression; a **dialect** is what the expression is *written in*. A product can offer a policy as configuration; it cannot offer a dialect as configuration without also demanding the user declare which dialect their stored strings were written in. And `AMBIGUOUS_STANDARD` says *the source is silent or self-contradictory*, while `KNOWN_DIVERGENCE` says *there is no relevant source at all*. `[MEASURED]` The corpus has four `KNOWN_DIVERGENCE` vectors, all in `cron.day-fields`, all because Vixie's code and Vixie's manual page describe different predicates.

### 3.2 The decision procedure

Applied in order; the first rule that fires wins.

1. **Must this input be rejected by a stated rule?** → `INVALID`, with `error_class`. Not merely because most engines reject it.
2. **Does a normative source supply one answer, and can you quote it?** → `NORMATIVE`, `single`, quotation in `normative[].quote`. If you can name the source but cannot quote a sentence settling *this* input, you do not have a `NORMATIVE` vector.
3. **Do two Verified errata, or two sections of one standard, give incompatible answers?** → `AMBIGUOUS_STANDARD`, citing both; use `open` unless the admissible space is finite and enumerable.
4. **Does the answer change with a declared runtime choice?** → `POLICY_DEPENDENT`. Name the axes in `policy_axis`; give every shipped value a case with a `when` map.
5. **Does the answer change with the syntax family?** → `DIALECT_DEPENDENT`, same enumeration discipline.
6. **Do implementations differ with no source to appeal to?** → `KNOWN_DIVERGENCE`. The `rationale` must state *why* none arbitrates; "I could not find one" is insufficient and the search must be recorded.
7. **Otherwise the vector is not ready.** It embodies an unresolved question about the domain, not about an engine, and belongs in an issue.

### 3.3 The no-manufactured-answer rule

**Where the source standard supplies no answer, none may be manufactured.** A contributor may not promote a vector to `NORMATIVE` on the strength of "most engines do X", "the obvious reading is X", or "our engine does X". `[MEASURED]` The corpus has five `open` vectors and 122 `RECORD` cells that are measured, reported and never graded. `[INFER]` An honest `open` is worth more than a fabricated single answer, because a fabricated answer converts a finding about the standard into a finding about an engine — precisely the error the corpus exists to prevent. The rule cuts the other way too: `open` requires a note saying why the space cannot be enumerated, not merely that enumerating it would be work.

`[MEASURED]` Two vectors define the corpus's outer edge rather than testing an engine: `CRON-EXT-011` (Jenkins `H`) and `CRON-EXT-012` (cronie `~`), whose occurrence sets depend on data outside the expression. Both are recorded and marked unscoreable. `[INFER]` A corpus must be able to say where its domain ends, and doing it with vectors makes the boundary machine-readable.

---

## 4. The runner contract

A **runner** executes corpus vectors against one or more engines and reports what happened. It is the only thing a third party must write to join the corpus.

### 4.1 Invocation, exit codes

```
runner [--vectors PATH] [--out PATH] [--engine NAME] [<engine-specific flags>]
```

`--vectors` takes a `.jsonl` file or a directory; **absent, the runner MUST read JSON Lines from stdin.** `--out` names an output file; **absent, the runner MUST write to stdout, and nothing else may go to stdout.** Diagnostics go to stderr. A runner MUST NOT require network access and MUST NOT mutate the vectors. Exit `0` = ran and emitted results; `1` = fatal harness error (vectors unreadable, engine could not be imported); `2` = usage error.

**A vector that fails, errors, crashes or hangs is a RESULT, not an exit code.** The contract's most violated-by-instinct rule and its most important one: a runner that exits non-zero because an engine raised has destroyed the measurement. `[MEASURED]` The corpus's 31 `REJECT-BAD` and 2 `HANG` verdicts exist only because errors are data.

### 4.2 Output record

One JSON object per line, one line per `(vector, engine)` pair, any order.

| field | required | meaning |
|---|---|---|
| `vector_id`, `corpus_version` | yes | copied from the vector |
| `runner` | yes | identifies this runner program |
| `engine` | yes | name; bracketed suffix for a non-default configuration, e.g. `croniter[day_or=False]` |
| `engine_version` | yes | version **and** provenance — a release number, or VCS host, repo and commit |
| `language` | yes | runtime and its version |
| `tzdb`, `tzdb_source` | yes | the IANA release actually in use, and where it came from |
| `status` | yes | `ok` · `empty` · `error` · `crash` · `timeout` · `unsupported` · `unsupported_op` |
| `occurrences` | yes | canonical occurrence strings; `[]` when none |
| `error` | yes | verbatim exception class and message, truncated to 500 bytes |
| `elapsed_ms` | no | wall time for the engine call |

`unsupported` and `unsupported_op` are excluded from scoring; `error` is **scored**, because it is the correct answer for every `INVALID` vector. A runner MUST bound each engine call and report `timeout` rather than aborting; the reference runners use 8 s.

### 4.3 Occurrence encoding

Two forms only. **Zoned**: `YYYY-MM-DDTHH:MM:SS±HH:MM|YYYY-MM-DDTHH:MM:SSZ` — local wall time with offset, a pipe, then the same instant in UTC, both halves required. **Floating**: `YYYY-MM-DDTHH:MM:SS`. Seconds always present; no fractional seconds, no locale formatting; comparison is byte equality of the whole array. `[INFER]` Both halves are what make gaps, folds and tzdb divergence visible under plain string equality: `…01:30:00-04:00|…05:30:00Z` and `…01:30:00-05:00|…06:30:00Z` differ only in the second half, so an engine returning only UTC or only wall time cannot hide the difference. A description-only engine emits one element prefixed `DESCRIPTION:`, scored as accept/reject evidence only.

### 4.4 Operations

| `op` | required behaviour |
|---|---|
| `cron.next` | the first `count` occurrences strictly after `start` (at or after when `inclusive`), with `start` read in `zone` |
| `cron.parse` | parse only; MAY be implemented by calling `cron.next` |
| `rrule.expand` | the first `count` members of the recurrence set defined by `ics` |
| `rrule.parse` | parse only; MAY be implemented via `rrule.expand` |
| `rrule.between` | members between two local timestamps, **in the engine's own inclusivity convention**, which the vector is measuring |

`input.ics` is a `\n`-separated block of content lines — `DTSTART` (optionally `;TZID=`), zero or more `RRULE`, `EXRULE`, `RDATE`, `EXDATE`. No folding, no `BEGIN:VEVENT`, no CRLF.

### 4.5 Provenance is mandatory and audited

Every record must carry `engine`, `engine_version`, `language`, `tzdb` and `tzdb_source`. Where the runtime does not expose a tzdb version the runner MUST fingerprint it: `TZDB-001`, `TZDB-002` and `TZDB-003` were chosen so the offsets of `America/Vancouver`, `America/Edmonton` and `Africa/Casablanca` at three fixed instants identify the release band (`≤2026a` / `2026b` / `≥2026c`) without asking the runtime. `[MEASURED]` `runners/run_js.ts` does this because neither Bun nor Node exposes a reliable value.

### 4.6 The fifty-line constraint, and its proof

**A minimal conforming runner must be implementable in about fifty lines using only a JSON parser and the engine under test.** This is a hard product requirement, not an aspiration: it is what makes the corpus adoptable in a language whose maintainers will not take a dependency.

`[CODE]` `runners/minimal_runner.py` is the proof — a complete conforming runner in 40 lines. It reads JSONL from stdin, formats occurrences including the `wall|UTC` pipe form, detects the tzdb from the first line of `/usr/share/zoneinfo/tzdata.zi`, emits `unsupported_op` for operations it does not implement, wraps the engine call in `try/except` so **errors become results**, and prints one JSON object per line — no argument parser, no configuration, no dependencies beyond the engine. `[INFER]` Any contract change that makes this file materially longer should be rejected.

---

## 5. The conformance report, and what a claim may say

### 5.1 Scoring

`tools/make_matrix.py` assigns one verdict per cell: `PASS`, `PASS[label]`, `FAIL`, `NOVEL`, `REJECT-OK`, `REJECT-BAD`, `HANG`, `RECORD`, `N/A`. The `FAIL`/`NOVEL` distinction is deliberate: on an `AMBIGUOUS_STANDARD` or `KNOWN_DIVERGENCE` vector, output matching no enumerated case is a newly discovered behaviour, and the correct response is to add a case in the next MINOR release. `[MEASURED]` That happened three times during this run.

### 5.2 Report layout

Per engine build, in order: engine and provenance; runtime; **tzdb release and source**; corpus version; pass rate **over scored vectors only**; the **policy profile** with the vector count supporting each axis value; then the individual `FAIL`, `REJECT-BAD`, `HANG` and `NOVEL` vectors with the engine's own output beside the corpus's expectation.

Two presentation rules. A report MUST NOT compute a percentage over unscored cells — `[MEASURED]` 2,284 of 4,600 cells are `N/A`, and including them would make every rate meaningless. And it MUST print the `error` string beside any verdict derived from a rejection, because `[MEASURED]` a `PASS` can be earned by an accidental crash: python-dateutil's `TypeError: can't compare offset-naive and offset-aware datetimes` scores `PASS` on `RRULE-SET-004`, which admits rejection as a case.

### 5.3 What a conformance claim is permitted to say

**A claim MUST name three things: the corpus version, the engine version, and the tzdb release. Any two are insufficient.** The result record makes all three mandatory so a claim cannot be assembled without them.

Permitted:

> *"Engine X 2.1.0 (git … @abc1234) conforms to Occurframe conformance corpus **v1.2.0** under policy profile `{cron.dom_dow: or/vixie, cron.dst_gap: skip, cron.dst_fold: first, cron.start_inclusivity: exclusive}` on **tzdb 2026c**: 104 of 107 scored vectors pass; 3 fail (`CRON-ANCH-003`, `CRON-STEP-003`, `CRON-FIELDS-004`); 77 not applicable; 0 pathologies."*

Not permitted, and a defect in any report that produces it: **"RFC 5545 compliant"**, **"POSIX cron compatible"**, **"DST-safe"**, **"100% conformant"**, or any rate quoted without the policy profile beside it. `[INFER]` Phase I's central finding was that the first three are unfalsifiable; the corpus exists to replace them with a sentence that can be checked and can be wrong.

Three further constraints. A claim may not aggregate across engine configurations — `[MEASURED]` croner's `legacyMode` flips five vectors' verdicts in both directions, so "croner conforms" is not well formed without the flag. A claim may not cite a corpus MAJOR other than the one the run used, because verdicts are not comparable across that boundary. And a claim about a `POLICY_DEPENDENT` vector is a claim about the *declared* policy: passing under `cron.dst_gap = skip` says nothing about behaviour under any other value.

---

## 6. Governance and versioning

### 6.1 `corpus_version`

Stamped into every vector and echoed by every result, so a result is never orphaned from the corpus that produced it.

* **PATCH** — `rationale`, `title`, citations, `incumbents` or `tags` changed; no `input`, no `expect`. Every previously passing result stays valid; no re-run required.
* **MINOR** — vectors **added**, or an `expect` **gained** an admissible case. Verdicts cannot flip pass → fail; they may flip `NOVEL` → `PASS[label]`.
* **MAJOR** — an `input` changed, an `expect` narrowed, a classification moved, or the runner contract changed. Verdicts may flip either way, and reports across the boundary are not comparable.

### 6.2 Adding a vector

Write it in `build/{cron,rrule,tz}_vectors.py` next to its family; take the next free number in its subfamily (numbers are permanent, never reused, including after retirement); supply, in order of preference, a quoted normative source, an enumeration of cases each with a `when` map, or an honest `open` with a note; derive mechanical values from `reference/cron_ref.py` under a named policy rather than typing them, and assert structural properties on any transcribed list; then rebuild → run every runner → re-freeze incumbents → regenerate the matrix. A vector whose `when` maps do not select exactly one case per engine is malformed and is not merged.

### 6.3 Correcting an expectation without invalidating past reports

This turns entirely on ID permanence.

* **The expectation was wrong, the input is right** → **correct in place**, bump **MAJOR**, record the correction in the vector's `rationale`. The ID does not change, so a three-year-old report saying "fails `RRULE-BY-027`" stays interpretable: the reader looks up `RRULE-BY-027` at the corpus version the report names, sees the expectation in force then, and reads the rationale for why it changed. **A past report is never retroactively re-scored** — it is a statement about a corpus version, and that version's vectors are immutable once published.
* **The input itself must change** → the vector is **retired**: it keeps its ID and gains `"status": "retired"` and `"superseded_by": "<new id>"`, and a new vector takes a new number.

`[INFER]` This is the only discipline under which a result set from an older corpus version can still be read years later, and exactly what libical's positional format cannot offer.

### 6.4 Deprecation policy

A retired vector stays in the distributed corpus for **at least two MINOR releases or twelve months, whichever is longer**, so consumers pinned to an older version see the retirement rather than a missing file, and it is never removed from the ID registry. Runners MUST skip `status: "retired"` vectors and MUST NOT treat their absence as an error; scorers MUST list them separately so a reader sees that coverage moved rather than vanished. A MAJOR may relocate them to `vectors/retired/`; it may not renumber them.

Axis governance has the same shape: names are namespaced (`cron.dom_dow`, `rrule.dtstart_emission`, `tz.tzdb_version`) and **append-only within a MAJOR** — adding a *value* is MINOR, renaming or removing one is MAJOR. `[MEASURED]` Twenty-three axes are enumerated in `docs/VERSIONING.md`; three values were added because this run measured them.

### 6.5 tzdb-dependent vectors

Two mechanisms, the author's choice. `context.tzdb_min` names the oldest release for which the expectation holds; older data scores `N/A`, not `FAIL`. `context.tzdb_pin: "per-case"` keys the expectation *by release*, each case carrying `when: {"tz.tzdb_version": "2026a"}`; `[MEASURED]` all ten `tzdb.provenance` vectors use it. `[SPEC]` Roughly four tzdb releases a year change future timestamps, and 2026 alone produced two that changed North American offsets. `[INFER]` Pinning one release would make the corpus wrong within months; ignoring the release would make it untestable. Keying by release is the only stable option, and it forces every report to state its zone data.

### 6.6 Neutrality when the same project also ships an engine

The objection, in its strongest form: *a conformance corpus published by a party that also sells an engine is a marketing instrument. Classification is the lever — call a behaviour `NORMATIVE` when your engine implements it and `POLICY_DEPENDENT` when it does not, and the corpus produces the scoreboard you wanted while looking like a measurement.* The pattern is not hypothetical: `[FACT]` OCPS lives in the same GitHub organisation as croner, whose author also authors OCPS; croner shipped two breaking changes to conform to OCPS 1.4; and Phase I recorded that this materially affects how much weight OCPS's matrix can bear.

Four properties already in the artefact are the partial answer, and each is checkable by a hostile reader. **Non-circularity is enforced by layout** — expectations come from quoted sources or `reference/cron_ref.py`, engine outputs live in `incumbents` and `raw/`, and `reference/` sits outside `runners/`. **Every engine's own words ship**, exception messages included, so a reader who thinks an expectation is wrong can check it without re-running anything. **The corpus mostly declines to say who is right**: `[MEASURED]` 35% `NORMATIVE`, 58 vectors with no single answer by construction, five `open`, 122 cells recorded and never graded — a marketing instrument would not have those numbers. And **verdicts carry labels**: `PASS[or/vixie]` says what an engine does, not that it is good.

None of that makes the corpus neutral. It makes it **auditable**, which is weaker and defensible. Four governance commitments close the remaining gap and should be written into the repository at v1:

* **Classification changes require a MAJOR bump, a written rationale in the vector, and a review window.** Moving a vector between `NORMATIVE` and `POLICY_DEPENDENT` is the exact lever the objection names, so it carries the highest procedural cost.
* **A maintainer whose own engine's verdict changes may not be the sole approver of that change.** With one maintainer, the change waits for an outside reviewer or is not made.
* **The project's own engine is reported in the same format, in the same directory, with no special-casing.**
* **Ship, at v1, at least one vector on which the project's own engine fails, and say so in the README.** This is the only commitment falsifiable at a glance, and therefore the one that carries the trust.

`[INFER]` Beyond commitments, the strongest structural answer is separation: a distinct repository, licence and release cadence, and — if obtainable — commit rights for a maintainer of an incumbent engine. The strongest *available* answer is §8's: give the measurement to a body that already publishes an unmeasured matrix, and let the corpus's credibility rest on someone else's masthead.

---

## 7. Distribution

### 7.1 Repository shape

```
oracle/
├── vectors/     manifest.json · incumbents.json · 14 family .jsonl files
├── docs/        FORMAT.md · RUNNER-CONTRACT.md · VERSIONING.md
├── runners/     run_python.py · run_js.ts · go/main.go · run_php.php
│                run_ruby.rb · minimal_runner.py (40 lines, complete)
├── reference/   cron_ref.py — policy-parameterised matcher, NOT an engine
├── build/       authoring source; regenerates vectors/
├── tools/       make_matrix.py · freeze_incumbents.py
├── raw/         verbatim runner output, one file per runner × tzdb
└── matrix/      matrix.md · divergences.md · matrix.json · conformance-<engine>.md
```

Three decisions are load-bearing. **`vectors/` is generated**, so citations, policy labels and assertions are written once and applied uniformly — hand-maintaining 184 objects with up to eight cases each is not viable. **`raw/` is preserved verbatim**, because a divergence is credible only if the reader can see the engine's own words. **`reference/` is physically separate from `runners/`**, so it can never be scored as an engine. `[INFER]` One change from the research layout: the vendored `engines/` tree should not ship — third-party source belongs in a reproduction script.

### 7.2 Licence

**Recommendation: `CC0-1.0` for `vectors/` and `docs/`; `Apache-2.0` for `runners/`, `reference/`, `tools/` and `build/`.**

The argument turns on how the corpus is actually adopted. `[FACT]` The projects that would benefit most have written policies against dependencies: node-cron's `CONTRIBUTING.md` — "**Zero runtime dependencies.** This is part of node-cron's identity. PRs that add a runtime dependency will not be accepted"; croner's `AGENTS.md` — "Zero dependencies - do not add external dependencies". `[MEASURED]` The Phase II maintainer study classified five of fourteen surveyed projects `CORPUS_ONLY`: corpus adoption is the *only* adoption available from them. `[INFER]` For those projects the adoption unit is not a package but a copy of `vectors/*.jsonl` checked into their own test tree.

That fixes the requirements. The data must survive being copied into MIT, BSD, Apache, GPL and proprietary repositories without adding an obligation the receiving project must reason about, and without an attribution notice inside a fixture directory. A copyleft or share-alike licence forks the corpus the first time someone vendors a subset; even CC-BY attaches an attribution term to files designed to be copied, sharded and regenerated. `CC0-1.0` raises the fewest questions for a reviewer looking at a test fixture. The code is different — `runners/` and `reference/` will be imported and extended — so `Apache-2.0`, for its explicit patent grant. `[INFER]` Where policy blocks CC0, `MIT` for the vectors is an acceptable fallback and should be pre-approved in `LICENSING.md` rather than negotiated per adopter. What must not happen is a bespoke licence: a conformance corpus works only if it is the *same* corpus everywhere, and every non-standard term is a reason to keep a divergent copy.

### 7.3 How a project vendors it

```
vendor/occurframe-oracle/
├── CORPUS_VERSION          # e.g. 1.2.0 — the single pinned string
├── LICENSE                 # CC0-1.0
├── manifest.json
└── vectors/*.jsonl         # all 14, or the subset the project's families need
```

Plus one runner in the project's own language (the 40-line pattern), one CI job, one committed report. Three practices make it durable: pin `CORPUS_VERSION` and fail CI when the vendored files disagree with it; **commit the generated report** so a behaviour change shows up as a diff rather than a red build — that is what makes the corpus a *description* of the engine rather than a gate on it; and run against at least two tzdb releases, because `[MEASURED]` a single-tzdb job cannot see any of the ten provenance vectors. Submodule or subtree both work; a data-only package per ecosystem is worth publishing for consumers who accept a dev-dependency, even though the projects that matter most will not use it.

---

## 8. Adoption mechanics

### 8.1 The concrete opening: OCPS's matrix is unmeasured

`[FACT]` OCPS — the Open Cron Pattern Specification — publishes an "Implementation Conformance Matrix" covering **17 libraries across 9 language families**, carried in tables of **21 rows** (the 17 libraries plus 3 daemons and POSIX), including croner, node-schedule, node-cron, cron (npm), cron-parser, Cronos, croner-rust, Sidekiq-Cron, python-crontab and dragonmantank/cron-expression. `[DOC]` It states how the cells were filled: *"This table is based on analysis of official documentation and community knowledge. For the most accurate details, please refer to the documentation of the respective libraries."*

`[INFER]` **Not one cell in it was measured.** The specification exists, the matrix exists, implementers cite it, and croner has already shipped two breaking changes to conform to increment 1.4. What is missing is exactly the half this corpus produces — which makes contributing measured results to OCPS the single most concrete adoption path available: it requires nobody to adopt a library, founds no new standard, and improves an artefact the ecosystem already agreed to care about. `[FACT]` The corpus overlaps OCPS's implementation list on at least three engines it measured directly (croner, cron-parser, dragonmantank/cron-expression), and its 98 cron plus 10 tzdb vectors cover the increments OCPS's own report scores worst: 1.3 (`L`, `W`, `#`) at 53% any / **6%** full, and 1.4 (day-field logic and DST policy) at 47% any / **0%** cumulative full.

### 8.2 Should the corpus be offered *to* OCPS rather than founded as a rival?

Honestly assessed: **partly yes, and the split is determined by scope rather than by strategy.**

**For.** OCPS is a specification with a conformance matrix and no measurement; this is a measurement apparatus with no specification. They are complements, not competitors. `[INFER]` A measured cell replacing an unmeasured cell in an artefact implementers already cite is worth more than the same cell in a repository nobody has heard of, and it costs one pull request. OCPS also supplies what the corpus cannot supply itself: a masthead that is not the engine vendor's — the strongest available answer to §6.6.

**Against.** `[FACT]` OCPS covers cron only. The 76 RRULE vectors and much of `tzdb.provenance` have no home there, and RRULE is where the hardest findings sit — the errata contradiction, the set-operation divergence, 25 of the 31 `REJECT-BAD` verdicts. `[FACT]` OCPS's distribution is small (9 stars, 1 fork), its conformance document is a DRAFT generated 2025-10-28, measuring revision 1 of the specification rather than the 2026-06-07 revision 2 — and its governance carries the same conflict this corpus is trying to avoid: same organisation and author as croner. `[INFER]` Donating measurement into OCPS trades one neutrality problem for another; it does not dissolve it.

**Recommended split.** Offer the **cron half** — the 98 `CRON-*` vectors and the cron-side `TZDB-*` vectors, with raw output and reproduction script — to OCPS as a contribution to `CONFORMANCE.md`, under CC0 so accepting costs OCPS nothing and creates no dependency. Keep the **RRULE half, and the format, runner contract and classification taxonomy**, independent, because no body claims that scope: `[FACT]` libical's `icalrecur_test.txt` is a positional file inside one implementation's test tree with no other consumer found, and CalConnect runs interop events but publishes no fixture set. `[INFER]` Founding a rival to OCPS would be a mistake; founding the thing OCPS does not cover is not. One caution on expectations: `[FACT]` OCPS itself has 9 stars and 0 watchers, and its increment 1.4 records 0% cumulative full conformance. `[INFER]` The corpus should be offered because measurement is worth more than affiliation, not because OCPS's distribution will carry it.

### 8.3 The named first moves

1. **Publish the twenty-five conformance reports as they stand**, with `raw/` and the reproduction script. Zero coordination cost, and it is what makes every later claim checkable.
2. **File the five pathologies upstream, each with its vector ID and a reproduction under ten lines**: robfig/cron's non-termination on `CRON-DST-007`; ice_cube's non-termination on `RRULE-BY-032` and its `TZID` discard (47 failures, one fix); APScheduler's fixed-point iterator on `CRON-DST-016` and its numeric/named weekday disagreement on `CRON-DOW-013`; python-dateutil's `ValueError: unsupported RDATE parm: TZID=…` on a construct RFC 5545 §3.8.5.2 permits. `[INFER]` Each is the corpus's value proposition demonstrated at the smallest possible scale.
3. **Open a pull request against OCPS's `CONFORMANCE.md`**, replacing "based on analysis of official documentation and community knowledge" with measured cells for the implementations already covered, each linking to raw output and naming engine commit and tzdb release.
4. **Offer libical a JSONL export** of the RRULE vectors its format can express, and propose the reverse import, so the two corpora converge rather than fork.
5. **Approach BullMQ.** `[MEASURED]` The maintainer study identified it as the strongest corpus consumer in the ecosystem: it ships five cron engines across five languages (cron-parser in TS, croniter in Python, croner in Rust, `crontab` in Elixir, Cronos in .NET) and has no way today to know where they disagree. `[INFER]` A cross-language divergence report for exactly those five engines is its missing artefact, needs no dependency change, and is producible from the existing corpus in a day.
6. **Ask the `CORPUS_ONLY` maintainers to run it in CI** — node-cron, croner, Graphile Worker, Solid Queue, Oban. `[FACT]` All five have written or demonstrated policies ruling out a dependency, which makes the corpus the only artefact they can adopt.
7. **Close the Quartz gap.** `[MEASURED]` Quartz and Quartz.NET are the second-largest cron dialect and were unreachable in this run; every Quartz-shaped vector is currently graded against `[DOC]`-sourced cases. First task of v1.1.
8. **Publish a multi-tzdb CI example.** `[MEASURED]` No engine in the study runs its own tests against more than one tzdb release, and ten corpus vectors are invisible without it.

---

## Contradictions and unresolved conflicts

1. **Neutrality cannot be established, only made auditable.** §6.6 offers four structural properties and four commitments; none proves the classifications were not chosen to flatter an engine. The test that would settle it — an outside maintainer with commit rights, or transfer to a body that ships no engine — has not been performed and may not be available.

2. **Offering the cron half to OCPS both solves and reproduces the neutrality problem.** `[FACT]` OCPS shares an organisation and an author with croner, one of the measured engines. Contributing there gains an independent masthead in appearance while placing the corpus under governance with the same structural conflict. This section recommends it anyway, on the ground that a measured cell beats an unmeasured one; a reader who weights governance above measurement should reach the opposite conclusion, and the evidence forces neither.

3. **OCPS's dating looked inconsistent and has since been resolved.** `[FACT]` `CONFORMANCE.md` was generated 2025-10-28; OCPS 1.0 is recorded FINAL on 2026-06-07, 7 months and 10 days later — which read here as a conformance report predating the specification it measures. `[SPEC]` OCPS 1.0's revision history settles it: 2025-10-28 is revision 1 and 2026-06-07 is revision 2, so the report measures revision 1 and there is no anomaly. See `12-compatibility-doctrine.md` Contradictions #4, which supersedes this entry. The percentages quoted in §8 should be read as revision 1 figures.

4. **The fifty-line constraint and the richness of the format pull against each other.** `minimal_runner.py` is 40 lines because it implements two of five operations, ignores `context.policy`, and reads a tzdb path that exists only on Linux. A runner honouring every field would be several times longer. The constraint honestly proves that *joining* the corpus is cheap; read as "a complete runner is fifty lines" it is false.

5. **`CC0` for the vectors is contestable.** CC0 maximises embeddability and grants no patent rights; MIT is more familiar to software reviewers but attaches attribution to files designed to be copied and regenerated. Some corporate policies block each. The recommendation is CC0 with a pre-approved MIT fallback — a hedge, not a resolution.

6. **A scoring rule and a governance rule conflict.** §5.2 requires the `error` string beside every rejection-derived verdict because an accidental crash can score `PASS`; §6.1 makes narrowing an `expect` a MAJOR change. Fixing the underlying problem — distinguishing "rejected deliberately" from "raised internally" — is therefore a MAJOR change to the runner contract, and cannot ship as the patch it looks like.

---

## What this section does not establish

- **That anyone will adopt it.** `[FACT]` OCPS, the closest comparable artefact, has 9 stars and 0 watchers after publishing a FINAL specification and a conformance matrix; libical's recurrence test file has existed for years with no external consumer found. Nothing in the design overcomes the problem Phase I identified: a conformance corpus is a public good with a private cost, and no implementer benefits from a test that can only make their library look worse.

- **That the format is right.** JSON Lines, six classifications, five `expect` modes and the `wall|UTC` encoding are defensible and were exercised across 4,600 cells, but have been reviewed by nobody outside this study. `[MEASURED]` The run itself discovered three axis values the format's authors did not anticipate — evidence the taxonomy is incomplete rather than that it is sound.

- **That the classification procedure is reproducible.** §3.2 is written as a decision procedure but has been applied by one author. Whether two contributors would classify the same vector identically — particularly on the `POLICY_DEPENDENT` / `DIALECT_DEPENDENT` boundary, and on when a silence justifies `open` — is untested, and is the property on which the corpus's credibility most depends.

- **That the governance commitments are sufficient, or will be kept.** They are proposals for a repository that does not yet exist. The only one checkable from outside — shipping a vector the project's own engine fails — is checkable precisely because the others are not.

- **That the licence recommendation survives legal review.** It is argued from adoption mechanics, not from counsel. CC0's lack of a patent grant and its uneven enforceability in some jurisdictions are named here and not resolved.

- **That the corpus is complete enough to found a claim on.** `[MEASURED]` 184 vectors, no Java or .NET engine, one RFC 7529 probe, no execution-layer coverage, five vectors that cannot be scored at all, and a reference matcher not cross-checked against an independent implementation. The corpus makes claims falsifiable; it does not make them true.
