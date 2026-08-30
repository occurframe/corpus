# Occurframe v1 Behavioral Specification

This is the normative specification that the conformance corpus encodes. Under the ORACLE ONLY verdict (`RESEARCH-II.md` §5) Occurframe ships no engine in v1, so this document does not describe a library's behaviour — it describes **the semantics against which any implementation, incumbent or new, can be tested.** The corpus is its executable form; the reference matcher is a proof that it is satisfiable.

Every behaviour carries exactly one status:

| Status | Meaning |
|---|---|
| **MANDATORY** | A conforming implementation must behave this way. No configuration may change it. |
| **CONFIGURABLE** | The caller selects from a named enumeration. The specification defines the values and forbids a default where the choice is live. |
| **COMPATIBILITY_PROFILE** | The behaviour is determined by a named, versioned dialect or profile identifier. It is never inferred from the input. |
| **OUT_OF_SCOPE** | Occurframe does not define it. An implementation may do anything, including nothing. |

**No behaviour in this specification may be platform-dependent.** Where a host cannot supply what a MANDATORY behaviour requires — most often a tzdb version — the implementation must fail loudly rather than proceed silently.

---

## 1. Objects

**MANDATORY.** Five objects exist. Nothing else is normative.

| Object | Definition |
|---|---|
| **Schedule** | A value denoting a set of instants. Comprises a *form*, a *zone*, a *policy set*, *bounds*, and optional *exclusions* and *inclusions*. Computable without a clock. |
| **Form** | One of `Pattern`, `Rule`, `Interval`, `Explicit`. A tagged union, not a unification. |
| **Occurrence** | An instant, plus its slot, plus the resolution facts that produced it. **Never a bare timestamp.** |
| **Resolution** | The record of how an occurrence was produced: the offset in force, whether a civil or date anomaly was encountered, which policy values applied, and the tzdb version. |
| **Provenance** | The tzdb version, and for a `Pattern`, the dialect identifier. |

`Cadence` (fixed-delay) is **OUT_OF_SCOPE**. It is a feedback loop whose occurrence set does not exist until execution happens; it cannot be previewed, backfilled, or agreed on by two nodes. Java, db-scheduler and tokio all separate it structurally, and so does this specification — by refusing it.

---

## 2. Terminology: Pattern vs Rule

**MANDATORY.** The two semantic families are named and never merged.

- A **Pattern** is a *predicate over instants*: `is_due(pattern, t) -> bool`. It has no anchor, no first or last occurrence, no count, and no memory. Cron is a Pattern.
- A **Rule** is a *generator from an anchor*: `expand(rule, anchor) -> [Instant]`. It has an origin, may be bounded by count or end date, and each member has a position. RFC 5545 RRULE is a Rule.

**MANDATORY.** Operations that are native to one family and derived in the other must document their cost class. `contains` is native for `Pattern` and derived for `Rule`; `nth` is native for `Rule` and **undefined** for `Pattern`, because a predicate has no ordinal.

**MANDATORY.** An implementation must not accept a Pattern where a Rule is required, or convert between them silently.

---

## 3. Pattern (cron) semantics

**COMPATIBILITY_PROFILE.** Every Pattern carries a dialect identifier drawn from the register in `12-compatibility-doctrine.md` — 17 dialects across 21 versioned identifiers. There is no generic `cron` dialect and none may be inferred from the string.

The dialect determines, at minimum:

| Aspect | Why it is dialect-scoped |
|---|---|
| Field count and order | 5, 6 (seconds-leading), 6 (seconds-trailing), 6 (year-trailing), 7. `[MEASURED]` `cron(15 10 * * ? *)` is one firing per day or twenty-four depending on which 6-field reading applies. |
| Day-of-week numbering base | Four bases exist in production, as the register in `12-compatibility-doctrine.md` §1.6 holds them: `0–7` both-Sunday (Vixie), POSIX `0–6`, `1=SUN` (Quartz/AWS), and APScheduler numeric `0=MON`. `[MEASURED]` APScheduler is internally inconsistent — numeric Monday-based, named Sunday-based. |
| DOM/DOW combination | Five resolutions: OR, AND, "Nth weekday of month", parse error, mutual exclusion via `*`. |
| Step semantics | Whether `N/M` means "start at N, step M to field max". |
| Extension set | `L`, `W`, `#`, `LW`, `L-n`, `dL`, macros, `H`. `[FACT]` Three current specifications assign `5#2`/`2#3` different weekdays because the extension set has forked from its numbering base. |
| Range wrapping | Whether `22-2` and `FRI-MON` are legal. |

**MANDATORY.** An implementation must reject a Pattern whose dialect it does not implement, naming the dialect. It must not parse it under a neighbouring dialect.

**MANDATORY.** A Pattern has no `COUNT`, no `UNTIL` and no anchor. Bounds on a Pattern are properties of the *query*, not of the Pattern.

---

## 4. Rule (RRULE) semantics

**MANDATORY.** The base profile is RFC 5545 §3.3.10 as amended by verified errata, plus RFC 7529 `SKIP`, plus RFC 8984's two legislated resolutions. Where the errata conflict, the specification states its resolution explicitly and the corpus classifies the vector `AMBIGUOUS_STANDARD`.

`[FACT]` The known conflicts, each of which the specification must resolve by name rather than by silence: verified errata 1913 and 3779 edit the same BYDAY sentence incompatibly; "editorial" erratum 3747 changes expansion semantics for `FREQ=YEARLY` and exactly one measured engine implements it.

### 4.1 Anchor

**MANDATORY.** The anchor is always the first occurrence, following RFC 8984 verbatim: "the initial date-time … is always the first occurrence in the expansion (and is counted if the recurrence is limited by a `count` property), even if it would normally not match the rule."

**MANDATORY.** An anchor that does not satisfy the rule is **valid and flagged**. Construction succeeds; validation emits a Warning naming the discrepancy; `explain` states it. `[FACT]` This is the case on which four named vendors produced three different behaviours in a single CalConnect interop test.

### 4.2 Bounds

- **MANDATORY.** `count` and `until` together are an **error**, not a `min()`. `[MEASURED]` Four of five reachable RRULE engines accept the forbidden combination.
- **MANDATORY.** `until` is inclusive.
- **MANDATORY.** `until` is stored in the schedule's zone. RFC 5545's UTC coupling is a *serialization* rule, applied on export and not imposed on the model.
- **MANDATORY.** `count` counts occurrences **after** exclusions are applied. This is a deliberate divergence from RFC 5545's under-specified reading, and any RRULE export must report it as lossy.
- **MANDATORY.** "Valid rule, empty occurrence set" is a **named state**, not an error and not an undifferentiated empty list. `[FACT]` The alternative produced an HTTP 500 on calendar sync in a shipping server.

### 4.3 Exclusions and inclusions

**MANDATORY.** Exclusions and inclusions are **schedules**, composed by set difference and union — not date lists. A literal date list is the degenerate `Explicit` form.

**MANDATORY.** Exclusion cannot be expressed as a modification of the generating rule. `[FACT]` `EXRULE` was removed from RFC 5545 for the recorded reason that it "is hard to implement, meaning that many CUAs either didn't support it or had a broken implementation."

**MANDATORY.** Exclusion takes precedence over inclusion. Duplicate instants from a rule and an explicit inclusion collapse to one occurrence.

---

## 5. Civil time

Fully specified in `15-doctrine-civil-time.md`. The normative summary:

| Behaviour | Status |
|---|---|
| `zone` is an IANA identifier, including explicit `UTC`; bare offsets and abbreviations rejected | **MANDATORY** |
| `gap` ∈ `Skip \| ShiftForward \| ClampToGapStart \| ClampToGapEnd \| Reject` | **CONFIGURABLE**, required iff reachable |
| `fold` ∈ `First \| Second \| Both \| Reject` | **CONFIGURABLE**, required iff reachable |
| `invalid_date` ∈ `Skip \| RollBackward \| RollForward \| Reject` | **CONFIGURABLE**, required iff reachable |
| `wkst` ∈ `MO…SU` | **CONFIGURABLE**, required iff it changes the answer |
| `offset_conflict` ∈ `PreferInstant \| PreferWallClock \| Reject` | **CONFIGURABLE**, required iff a stored occurrence is being re-resolved |
| Policies are defined over occurrence-set **cardinality** | **MANDATORY** |
| An unreachable axis is **absent**, never defaulted and never serialized | **MANDATORY** |
| A reachable, unspecified axis fails construction with the field, the first affected occurrence and the admissible values | **MANDATORY** |
| Named profiles set reachable fields at construction; profile names are never serialized | **CONFIGURABLE** |
| Reachability is determined against a named tzdb version | **MANDATORY** |
| Zone-identifier resolution failure policy ∈ `Fail \| Quarantine \| FollowLink` | **CONFIGURABLE** |
| Canonicalising zone identifiers through Links on write | **Forbidden** (MANDATORY) |

---

## 6. Serialization and versioning

### 6.1 The schedule envelope

**MANDATORY.** The serialized form is the record, not a string. Strings are codecs.

```
{
  "occurframe": "1",                    # spec major version
  "form": { "kind": "pattern|rule|interval|explicit", ... },
  "zone": "America/New_York",
  "policy": { ... },                    # reachable axes only; may be absent entirely
  "bounds": { ... },
  "exclude": [ <schedule>, ... ],
  "include": [ <schedule>, ... ],
  "provenance": { "tzdb": "2026a", "dialect": "vixie-cronie@2026" },
  "fingerprint": "<hash>"
}
```

**MANDATORY.** `fingerprint` is a deterministic hash of the semantic content under a specified canonicalisation. It is **evidence, never a key** (`14-doctrine-identity.md` §3.2).

**MANDATORY.** A profile name never appears. Only expanded, reachable values do.

### 6.2 Versioning rules

- **MANDATORY.** A change to the specification that alters any occurrence's instant, presence or slot is a **major** version bump, is listed in the corpus diff, and is detectable by running the corpus.
- **MANDATORY.** An implementation version bump must never silently change occurrence times. `[FACT]` The counter-example is on the record: Hangfire swapped NCrontab for Cronos beneath every stored schedule.
- **MANDATORY.** A serialized schedule declares the spec major version it was written under. An implementation that does not support that version rejects the schedule; it does not guess.
- **CONFIGURABLE.** Reading a schedule serialized under an older major version, with a migration report.

### 6.3 Corpus versioning

**MANDATORY.** The corpus versions independently of any implementation, on its own cadence — tzdb releases roughly four times a year; implementations, whenever. A vector's expectation may be corrected without invalidating past conformance reports, because a report names the corpus version it was run against.

---

## 7. Error and diagnostics model

**MANDATORY.** Exactly three outcome classes. They are never conflated, and each carries a stable code from a documented namespace.

| Class | Meaning | Examples |
|---|---|---|
| **Rejection** | The input is not a schedule. Construction fails. | Malformed syntax; missing zone; unknown dialect; `count` and `until` together; a reachable policy axis left unspecified; an unsupported spec version |
| **Warning** | Well-formed and suspicious. Construction succeeds. | Anchor does not satisfy the rule; the rule generates zero occurrences within a declared horizon; the expression's meaning differs across dialects; the schedule references data that makes it non-self-contained |
| **Fact** | A property of a produced occurrence. Not a problem. | Which offset applied; which policy fired; that the nominal date was invalid and was rolled |

**MANDATORY.** Every Rejection names the offending field, and — where the failure is a reachable-but-unspecified policy — the first affected occurrence and the admissible values. `[INFER]` A required argument whose error contains the date of the first problem is a materially different experience from one that says "missing parameter," and the difference is plausibly what separates this design from the `whenever` reversal.

**MANDATORY.** Silent acceptance of an expression that can never fire is forbidden. `0 0 31 2 *` produces a Warning naming the emptiness. `[MEASURED]` 31 inputs that a standard says MUST be rejected are currently accepted across the measured engines.

**MANDATORY.** `explain` returns **structured facts**, not prose. Human rendering is a separate, replaceable layer over the structure.

**MANDATORY.** The explainer and the generator share one code path. `[MEASURED]` A description generated independently of the computation is a second implementation, and second implementations diverge: `cronstrue` renders `0 22-2 * * *` as "Every hour, between 10:00 PM and 02:00 AM" for an expression four of five executors reject.

---

## 8. Determinism and provenance

- **MANDATORY.** Occurrence computation is a **pure function**. It never reads a clock. `now` is always a parameter.
- **MANDATORY.** Given the same schedule and the same pinned tzdb version, every conforming implementation on every platform produces the same occurrences, in the same order, with the same slots. This is the property the corpus tests and the property that makes coordination-free deduplication sound.
- **MANDATORY.** Every occurrence carries the tzdb version that produced it. An implementation that cannot determine its tzdb version **must fail**, not guess. `[CODE]` This is not hypothetical: Node reports `process.versions.tz` = 2025c while its filesystem tzdb is 2026a; Python's `zoneinfo` exposes no version at all and searches `TZPATH` before the `tzdata` wheel; Go's `time/tzdata` exports nothing.
- **MANDATORY.** `revalidate(schedule, from_tzdb, to_tzdb)` returns `Moved{slot, was, now}` and `PolicyNowRequired{field, because, first_affected}`.
- **MANDATORY.** Ordering is ascending by instant. Where two occurrences share an instant, ordering is by slot, then by fold branch. There is no unspecified ordering.
- **MANDATORY.** Deduplication is by instant within a single query result; the admission-level guard is `14-doctrine-identity.md` §3.1 and belongs to the host.
- **MANDATORY.** Every query is **bounded by construction** and reports truncation explicitly. `[MEASURED]` Four RRULE libraries ship four different silent truncation caps — 730, 732, 1,000, 100,000 — which alone guarantee divergent output on an unbounded rule. Silence is the defect; the cap is not.
- **MANDATORY.** Resource limits are declared, not discovered. An implementation states its maximum window, maximum occurrences per query, and maximum expansion depth, and returns a truncation indicator rather than an exception when it reaches them.
- **MANDATORY.** Non-termination is a conformance failure. `[MEASURED]` Two measured engines fail to terminate on valid input — one of them the engine Kubernetes CronJob vendors.
- **MANDATORY.** Infinite recurrence is representable and never materialised. `Unbounded` is a legal bound; only a bounded query may be executed against it.

---

## 9. Explicit v1 non-goals

Occurframe v1 is not, and will not become:

1. A job runner, queue, worker pool, or scheduler daemon.
2. A durable-execution or workflow platform.
3. A distributed lock service.
4. **A production recurrence engine** — deferred behind the gate in `RESEARCH-II.md` §5.
5. A new cron dialect. `[FACT]` OCPS increment 1.4 — the increment that legislates the day-field rule — records 0% cumulative full conformance across its matrix.
6. A holiday or business-day **data** distribution. The ISDA conventions are specified; the calendars are host-supplied with declared provenance.
7. A time-zone database.
8. A calendar server, or a CalDAV/iTIP implementation.
9. A general date-time library. It specifies behaviour that one provides.
10. A natural-language date parser. `[DOC]` Human-facing surfaces converge on roughly 22 phrase shapes; competing on expressiveness targets the empty part of the market.
11. A fixed-delay scheduler. Cadence is refused by name.
12. A silent cross-dialect converter. Classification is provably correct where conversion is provably unsafe.
13. A faster drop-in for any incumbent. `[FACT]` `rrule-rust` — faster, same API — holds 0.65% of `rrule`'s downloads.
14. Non-Gregorian `RSCALE`. Standardised, real, and with three partial implementations in eleven years.
15. Sub-second recurrence. Nothing in either phase's pain corpus asks for it; the systems that need it use monotonic timers, which are cadences.

---

## Contradictions and unresolved conflicts

1. **This specification defines behaviour for a library that v1 does not ship.** That is deliberate — the corpus tests semantics, and semantics need a normative statement — but a reader may reasonably ask what it means for a specification to be MANDATORY when no implementation is authorised. The answer is that it is mandatory *for conformance claims*, which incumbents may make and Occurframe may not.
2. **§4.2's `count`-after-exclusions rule diverges from RFC 5545 deliberately**, so an Occurframe-conformant RRULE implementation is, on that point, non-conformant to the RFC. The corpus classifies the vector `AMBIGUOUS_STANDARD` and records both; the specification still picks a side, which is a stronger act than the corpus's own discipline elsewhere allows.
3. **§8 requires an implementation to fail if it cannot determine its tzdb version**, which — as §8's own evidence shows — disqualifies straightforward implementations in Node, Python and Go. That is either the specification's most important requirement or its most unrealistic, and Phase II cannot tell which.
4. **§3 requires a dialect on every Pattern**, but 83.4% of measured real-world schedules are portable across the dialects that matter to them. The requirement is right for the 16.4% and is pure ceremony for the rest.

## What this section does not establish

- That any implementation will adopt these semantics. Conformance is voluntary and no maintainer has been asked.
- That the MANDATORY set is minimal. It was derived from measured divergence, not from a minimality proof; a smaller set may cover the same divergences.
- That the three-class error model is sufficient. It is the model Phase I derived and Phase II did not test it against a real implementation.
- That the specification is complete enough to be implemented without questions. The corpus is the check on that, and the corpus has 184 vectors against a semantic surface that plausibly needs several hundred.
