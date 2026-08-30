# Final Conceptual API and CLI

> **Amended by [ERRATA-001](ERRATA.md#errata-001--oracle-only-cli-surface).**
> §6 originally froze four shipped commands. Three of them —`explain`,
> `classify`, `occurrences` — cannot be implemented without the production
> recurrence engine that `RESEARCH-II.md` §5 explicitly does not authorise, so
> the verdict governs and they are deferred behind the engine gate. Occurframe
> v1 ships one semantic command, `test`. Their frozen semantics are preserved
> unchanged in §6.7, and the original Research II text is preserved verbatim at
> `legacy/phase2-rc1/research/17-conceptual-api-and-cli.md`. §§1–5 are
> unaffected.

Two surfaces are frozen here. Under the ORACLE ONLY verdict they have different standing, and the difference matters:

- **The specification API** (§1–§5) is the operation set the behavioural specification defines and the corpus tests. It is what a conforming implementation exposes. Occurframe v1 does not ship it as a library; it publishes it as the thing conformance is measured against, and the reference matcher implements the subset needed to score the corpus.
- **The CLI** (§6) is a shipped v1 artefact. It is the corpus runner, not a general-purpose scheduling tool. *As frozen this read "the corpus runner and the differ"; the differ is `classify`, deferred by ERRATA-001.*

No production code appears here. Signatures and type shapes are in scope; implementations are not.

---

## 1. Canonical terminology

**Frozen.** These words mean one thing each, across the specification, the corpus, the CLI and all documentation.

| Term | Meaning | Not to be called |
|---|---|---|
| **Schedule** | A value denoting a set of instants | "rule", "cron", "trigger", "timetable" |
| **Pattern** | The predicate family (cron) | "expression" |
| **Rule** | The anchored-generator family (RRULE) | "recurrence" |
| **Occurrence** | An instant with its slot and resolution | "run", "event", "fire time" |
| **Slot** | The durable logical position in a series | "occurrence ID" |
| **Resolution** | How an occurrence was produced | "metadata" |
| **Provenance** | tzdb version and dialect identifier | "version" |
| **Policy** | A civil-time or calendar decision attached to a schedule | "options", "settings", "config" |
| **Dialect** | A named, versioned cron semantics | "format", "flavour" |
| **Cadence** | Fixed-delay. Explicitly **not** a schedule | never used as a synonym for schedule |
| **Vector** | One corpus test case | "test", "fixture" |
| **Profile** | A named bundle of policy values | "preset", "mode" |

---

## 2. The occurrence object

```
Occurrence {
  slot : Slot {
    series_id : String            # caller-supplied, opaque
    nominal   : LocalDateTime     # no offset
    zone      : IanaZoneId
    fold      : 0 | 1
  }
  instant    : Instant            # RFC 3339 UTC
  offset     : UtcOffset          # consistency witness only; in no key
  resolution : Resolution {
    civil_anomaly  : None | Gap | Fold(First|Second)
    date_anomaly   : None | InvalidDate(policy_applied)
    policy_applied : { gap?, fold?, invalid_date? }   # reachable axes only
    tzdb_version   : String
  }
}
```

**An occurrence is never a bare timestamp.** This is the API's first substantive claim, and it is the one the differential matrix vindicates: every measured engine returns a bare datetime, so a caller cannot tell whether it landed in a fold, which of two possible instants it is, what policy produced it, or which tz-database it depends on.

---

## 3. Construction

```
Schedule.pattern(text, dialect, zone, policy?, bounds?)  -> Result<Schedule, Rejection>
Schedule.rule(text | parts, zone, anchor, policy?, bounds?) -> Result<Schedule, Rejection>
Schedule.interval(origin, every, zone, policy?)          -> Result<Schedule, Rejection>
Schedule.explicit(instants, zone)                        -> Result<Schedule, Rejection>

Schedule.daily(at, zone, ...)                            # sugar over rule()
Schedule.weekly(on, at, zone, ...)
Schedule.monthly(day, at, zone, ...)
```

Frozen properties:

1. **`zone` is required on every constructor.** No exceptions, `UTC` included.
2. **`dialect` is required on `pattern`.** There is no `Schedule.cron(text)`. A constructor that accepts a cron string without a dialect is a constructor that guesses, and four production day-of-week numbering bases make guessing wrong.
3. **`policy` is optional in the signature and conditionally required at construction.** It is omitted when no axis is reachable, and construction *fails* when a reachable axis is unspecified. The optionality is in the type, not in the semantics.
4. **Pattern and Rule are built by different calls**, because they are different objects. The anchor is a parameter of `rule` and does not exist on `pattern`.
5. **Construction returns a result value; it does not throw.** Validation is data.
6. **No mutation.** `with_policy(...)`, `with_bounds(...)` return new schedules with new fingerprints.

The two frozen reference calls:

```
Schedule.daily(at="03:00", zone="UTC")
Schedule.daily(at="02:30", zone="America/New_York", on_gap=Gap.SHIFT_FORWARD)
```

---

## 4. Query

```
between(sched, from: Instant, to: Instant, limit?: n)
    -> { occurrences: [Occurrence], truncated: bool, cost: CostReport }

next(sched, after: Occurrence)          -> Option<Occurrence>
previous(sched, before: Occurrence)     -> Option<Occurrence>
first_after(sched, instant: Instant)    -> Option<Occurrence>
nth(sched, n)                           -> Option<Occurrence>     # Rule only
contains(sched, instant)                -> Match | NoMatch        # native for Pattern
```

**`between` is the primitive.** Everything else derives from it, and the entire industry vocabulary of missed-run policy is a `filter → take → fold` over it.

**`next` and `previous` take an `Occurrence`, not an `Instant`.** This is the deliberate constraint Phase I asked for. `next(spec, now())` after a job completes is the accumulated-drift bug — it silently converts a calendar-anchored schedule into a cadence. Phase I's API sketch accepted an overload for both and merely labelled the hazard; this specification removes it. **`first_after(instant)` is the separately-named bootstrap**, used once when there is no previous occurrence, and its name says what it is.

`[MEASURED]` The hazard is not theoretical: a `Temporal.ZonedDateTime.add({days:1})` loop from 02:30 New York lands on 03:30 on the gap day and stays at 03:30 forever, while every anchored engine returns to 02:30 the next day.

**Every query is bounded and reports truncation.** `nth` is defined only for `Rule` and documents its cost class; on a `Pattern` it is a type error, not a runtime one.

### Set algebra

```
union(a, b)   difference(a, b)   intersection(a, b)   setpos(sched, positions, within)
```

`difference(weekdays, us_federal_holidays)` is the operation the category has wanted since CalConnect's 2006 answer to "every business day" was *enumerate the holidays as literal exception dates, per sender, forever*.

---

## 5. Diagnostics, provenance, identity

```
validate(sched)                          -> [Finding]        # Rejection | Warning | Fact
explain(sched)                           -> Explanation      # structured, not prose
diff_dialects(text, dialects, window)    -> DialectReport
lossiness(sched, target_format, horizon) -> LossinessReport
tzdb_version()                           -> String
revalidate(sched, from_tzdb, to_tzdb)    -> { moved: [Moved], policy_now_required: [PolicyNowRequired] }
fingerprint(sched)                       -> Fingerprint       # evidence, never a key
slot_id(sched, occurrence)               -> SlotId
admission_key(sched, occurrence)         -> AdmissionKey      # a constraint tuple, not a display value
serialize(sched) / deserialize(bytes)
```

`diff_dialects` is the migration and compatibility tool the doctrine chose over a converter. Its output is: the set of dialects under which the text parses, the distinct occurrence sequences produced under each, and **the first instant at which they diverge**. That last field is what makes the report actionable rather than alarming.

`explain` returns structure. English is a renderer over it, and the renderer and the generator share one code path — because a description computed independently of the computation is a second implementation, and second implementations diverge.

---

## 6. CLI

### 6.1 The decision

**Ship a CLI. Ship one semantic command. Do not ship a general-purpose scheduling CLI.**

*As frozen by Research II, this read:* **"Ship a CLI. Ship four commands. Do not
ship a general-purpose scheduling CLI."** Its justification was narrow and
specific: under ORACLE ONLY the corpus *is* the product, and a corpus that cannot
be run from a shell is not a product — it is a directory. Three of the four
commands exist to operate the corpus; the fourth exists because the measured
prevalence data shows schedule owners cannot currently answer a question about
their own schedules that a single command can answer.

[ERRATA-001](ERRATA.md#errata-001--oracle-only-cli-surface) corrects the count,
not the reasoning. Of the four, only `test` (§6.3) is satisfiable by measuring an
external engine. `explain`, `classify` and `occurrences` each require Occurframe
to compute occurrences itself, which `RESEARCH-II.md` §5 does not authorise in
v1. The corpus still needs a shell interface, and `test` is it.

**The v1 shipped command surface is therefore:**

```text
occurframe test
oframe test
```

`explain`, `classify` and `occurrences` are deferred behind the engine gate;
their frozen semantics are preserved in §6.7 and are not part of the v1 contract.

Commands considered and **rejected**: `occurframe validate` (folded into `explain`, which must validate to explain); `occurframe inspect` (an unfocused name for whatever `explain` does not cover); anything that runs, schedules, or waits.

### 6.2 Common contract

**Frozen for all commands.**

| Aspect | Rule |
|---|---|
| Output | `--format json` is the default when stdout is not a TTY; `--format text` when it is. Both are always available explicitly. JSON output is a single object with a `occurframe` version field. |
| Input | Positional argument, or `-` to read stdin. Line-oriented stdin means one schedule per line. |
| Timezone | `--zone <IANA>` — required wherever a schedule is evaluated. No default, no host-local fallback. |
| Dialect | `--dialect <id>` — required for any cron pattern. No default. |
| Policy | `--gap`, `--fold`, `--invalid-date`, `--wkst`, or `--profile <name>`. Supplying an unreachable axis is a Warning, not an error. |
| Bounds | `--from` and `--to`, or `--from` and `--limit`. **An unbounded query is refused.** |
| tzdb | `--tzdb <version>` pins; the version used is echoed in every output. |
| Colour | Never in JSON; `--no-color` honoured; respects `NO_COLOR`. |

**Exit codes, frozen.** The numbering is unchanged by ERRATA-001; the final
column records which codes the v1 shipped surface can actually produce, because
`2` and `5` presuppose evaluating a caller's schedule.

| Code | Meaning | v1 |
|---|---|---|
| 0 | Success; for `test`, full conformance | active |
| 1 | Conformance failure, or a divergence was found by `classify` | active (conformance failure only) |
| 2 | Rejection — the input is not a valid schedule | inactive; engine-gated |
| 3 | Usage error — a required flag is missing or unknown | active |
| 4 | Environment error — tzdb unavailable or its version undeterminable | active |
| 5 | Truncation reached before the requested window completed | inactive; engine-gated |

An inactive code is reserved, never reused and never renumbered: if the engine
gate opens, the deferred commands take the codes they were frozen with.

`[INFER]` Codes 1 and 2 are deliberately distinct: "your schedule is fine and the engines disagree about it" and "your schedule is not a schedule" are different facts, and a CI pipeline should be able to act on them differently.

### 6.3 `occurframe test`

Runs the conformance corpus against an engine adapter and emits a conformance report.

```
occurframe test --engine <adapter> [--corpus <path>] [--family <f>...]
                [--tzdb <version>] [--format json|text|junit]
```

- `--engine` names an adapter conforming to the runner contract in `oracle/docs/RUNNER-CONTRACT.md`. Third-party adapters are the point; the shipped ones are examples.
- Output is a conformance report naming corpus version, engine version, tzdb version, and per-vector verdicts. `--format junit` exists because the target is other projects' CI.
- **`POLICY_DEPENDENT` and `AMBIGUOUS_STANDARD` vectors are asserted against admissible *sets*, never single answers.** A verdict of "outside the admissible set" is a failure; "a different admissible member than last time" is a recorded change, not a failure.
- Exit 0 only on full conformance for the selected families.

### 6.7 Deferred commands — engine-gated, not part of v1

The three subsections below are preserved **verbatim as Research II froze them**.
They are not implemented, not shipped, and not advertised in the CLI's default
help. They are recorded so that the engine gate in `RESEARCH-II.md` §5 can be
walked through without reopening research, exactly as that section intends.

Each requires Occurframe to compute occurrences rather than observe them; see
[ERRATA-001](ERRATA.md#errata-001--oracle-only-cli-surface) for the per-command
reasoning. Nothing below may be read as describing shipped v1 behaviour, and none
of these names may be reused for a different operation while deferred.

#### 6.7.1 `occurframe explain`

```
occurframe explain <schedule> --zone Z [--dialect D] [--policy...] [--from T --limit N]
```

Emits the structured explanation: what the schedule denotes, which policy axes are reachable and which values apply, the anchor's synchronisation status, any Warning, the tzdb version, and — when `--from`/`--limit` are given — the next N occurrences with their full resolution records.

This is the command that answers requirement 9 from the UX analysis: *why did this occurrence move or get skipped during DST?* The answer is a field in the resolution record, not a support ticket.

#### 6.7.2 `occurframe classify`

```
occurframe classify <text|-> [--dialects D1,D2,...] [--window T0..T1] [--zone Z]
```

The differ. Given a cron string, reports every dialect under which it parses, the occurrence sequence each produces over the window, and the first instant at which any two diverge. Exit 1 if a divergence is found — so it is usable as a lint in CI.

Reading stdin line-by-line makes the practical case work: `cat crontab | occurframe classify - --dialects vixie,quartz,aws`.

`[MEASURED]` This is the command the prevalence corpus argues for. Kubernetes `spec.timeZone` was set in 6 of 279 measured CronJobs and resolved to a real zone in **zero** of them; 13 schedules used a fixed-offset `EST` where a DST zone was meant, one in a live production calendar feed. Those are findable by a lint and are not currently findable at all.

#### 6.7.3 `occurframe occurrences`

```
occurframe occurrences <schedule> --zone Z --from T0 (--to T1 | --limit N) [--dialect D] [--policy...]
```

Emits occurrences as JSON objects — one per line with `--format json` in a stream context — carrying instant, slot, and full resolution. Bounded by construction; exit 5 on truncation.

This is the corpus's own generation path exposed, which is what makes it useful: it is the same code path the conformance report scores.

---

## 7. Idiomatic mapping

The reference matcher is **Python**, and stays Python (`RESEARCH-II.md` §5). It exists, it grades 25 engine builds, and a normative reference that reads as pseudocode is worth more than a fast one. The Rust decision in `07-first-language.md` is recorded and gated; it applies to an engine that v1 does not build.

For a future implementation, the frozen mapping notes:

- **Rust.** `Result` for construction, exhaustive `match` on `Resolution`, a builder that cannot compile without a zone. Borrow `jiff`'s vocabulary where semantics coincide (`Disambiguation`, `OffsetConflict`) — but never its `to_zoned()` path, because a 1:1 disambiguation model cannot express `Skip` (zero occurrences) or `Both` (two).
- **TypeScript.** Discriminated unions map `Form` and `Resolution` cleanly. `Instant` must be `Temporal.ZonedDateTime`, never `Date`. The tzdb-provenance requirement is the hard part: `process.versions.tz` and the filesystem tzdb were measured to disagree in one container, so a conforming implementation must carry its own tzdb or fail.
- **Python.** Keyword arguments read best of the three and enforce least. `pandas.Timestamp.tz_localize`'s fail-closed `raise` defaults are the nearest existing precedent, and even they default one axis.

**"Semantic equivalence" means equivalence of computed answers under the corpus** — not equivalence of API guarantees. Rust can enforce the specification, TypeScript can express it, Python can document it. The specification says so rather than pretending otherwise.

---

## Contradictions and unresolved conflicts

1. **A frozen API for a library that v1 does not ship** is an odd artefact. Its justification is that the corpus tests operations, so the operations must be named — and that the gate in `RESEARCH-II.md` §5 should be walkable without reopening design. A reader may reasonably call it premature. **Partly resolved by [ERRATA-001](ERRATA.md#errata-001--oracle-only-cli-surface):** the oddity became a contradiction where §6 declared three of those unshipped operations to be shipped commands, and the verdict governs. The API itself remains specification-only and unchanged; the three commands are deferred.
2. **`next(Occurrence)` with no `Instant` overload is stricter than any incumbent** and will read as hostile to anyone porting existing code. `first_after` covers the bootstrap, but a caller who has stored only a timestamp — which is most of them — must reconstruct an occurrence to continue a series. That is the correct behaviour and it is a real migration cost.
3. **`occurframe classify` and `occurframe explain` overlap** at their edges; `explain` on a `Pattern` will want to say something about dialect sensitivity, which is `classify`'s job. The boundary drawn here (one schedule versus one string across many dialects) is defensible but not self-evident. *Both commands are deferred by ERRATA-001; the overlap is unresolved and inherited by whoever walks the engine gate.*
4. **`admission_key` is exposed in the API and is not a value to display.** Exposing something whose documentation says "do not show this to anyone" invites misuse.

## What this section does not establish

- That the API is pleasant. No user testing was conducted in either phase; the analysis in `05-policy-ux.md` is structural and grounded in real artefacts, and is not a substitute.
- That four commands are the right four. They were derived from the corpus's needs plus one measured gap, not from observing anyone's workflow.
- That the JSON output shapes survive contact with a consumer. `Resolution` in particular is a design-time convenience that may prove expensive to populate for every occurrence in a large window.
- That `diff_dialects`/`classify` can compute "the first instant at which they diverge" cheaply for all dialect pairs. It is stated as a requirement without a complexity analysis.
