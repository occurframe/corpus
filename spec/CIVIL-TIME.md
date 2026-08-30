# Final Civil-Time Policy Doctrine

Phase I's central ergonomic bet was that civil-time ambiguity must be **explicit and non-defaultable**. It also recorded that the bet was untested and was the design's most likely cause of outright rejection. Phase II tested it and found two things: the bet, as Phase I stated it, has already been run in public and lost; and a conditional form of it succeeds, is exactly decidable, and costs almost nothing in the common case.

This document is normative for the Occurframe specification. It supersedes Phase I doctrine positions 5, 6 and 7. It is stated in full even though v1 ships no engine (see `RESEARCH-II.md` §5): the policy vocabulary is one of the artefacts Occurframe publishes, and it is what the corpus's `POLICY_DEPENDENT` vectors are graded against. Where the text below reads as specifying a library — API signatures, `revalidate`, "the design ships a new failure mode" — it is describing the behaviour any implementation must have in order to conform, not work authorised for v1.

---

## 1. The evidence that reframed the question

### 1.1 The bet has been run and reversed

`[DOC]` The Python library `whenever` shipped 0.6.0 on 2024-07-04 with this changelog entry:

> "`disambiguate=` is non-optional for all relevant methods. **Rationale**: This makes it explicit how ambiguous and non-existent times are handled."

That is Phase I's doctrine, implemented by a careful author. **171 days later**, 0.6.16 (2024-12-22):

> "Make `disambiguate` argument optional, defaulting to `\"compatible\"`. **Rationale**: This required parameter was a frequent source of irritation for users… For those that do want to enforce explicit handling, a special stubs file or other plugin may be introduced."

`[INFER]` A designer who explicitly valued explicitness, in a library whose entire premise is correct civil-time handling, reversed the requirement in under six months on the basis of user irritation. Any doctrine that restates the unconditional form is proposing an experiment whose result is already published.

### 1.2 The other authorities all default *something*

| System | Gap/fold default | Note |
|---|---|---|
| TC39 Temporal | `disambiguation: 'compatible'` defaults; `offset: 'reject'` does not | `[DOC]` The champions' stated reason for not defaulting `offset` is that "there is no obvious default solution" — i.e. defaulting is the norm and non-defaulting is the exception requiring justification |
| jiff | `Disambiguation::Compatible` | `[DOC]` Chosen to agree with RFC 5545 |
| pandas | `ambiguous='raise'`, `nonexistent='raise'` | `[CODE]` **Fail-closed defaults** — a default that errors only when the ambiguity is live |
| Noda Time | `InUtc()` requires no resolver at all | `[DOC]` "there is no chance that this local date/time is ambiguous or skipped" |

`[INFER]` Noda Time's `InUtc()` is the key observation. The most rigorous civil-time library in existence already ships an API path with **no policy argument**, justified precisely on the grounds that the anomaly is unreachable. That is conditional requirement, discovered fifteen years ago and never generalised.

### 1.3 The reachability question is exactly decidable

`[CODE]` Measured across all 498 zones in tzdb 2026a, over 2026-09-01 → 2046-09-01:

- **342 of 498 zones (68.7%) have zero gap or fold anomalies.** Anomalies are not a property of the world in general; they are a property of a minority of zones.
- The cheap test — does the zone's POSIX footer declare a DST rule? — is **set-identical** to a full transition scan. Reachability is a table lookup, not an analysis.
- Within a transitioning zone, only **4.2–8.3% of the day** is affected.
- **1,020 of 1,440 minutes-of-day are anomaly-free in every zone on earth**, forming a contiguous 04:00–20:59 band.
- 09:00, 12:00, 06:00 and 17:00: affected in **zero** zones. 02:00 and 02:30: affected in **121 and 120** zones respectively — the worst times on earth, and the folk-standard batch times.
- The whole-database scan costs **0.026 s**.

`[MEASURED]` And from the real-world corpus: **81.3% of hour-pinned local-frame schedules fire between 00:00 and 04:00.** The population concentrates in exactly the window where the policy matters, which is why the problem is real — and 83.4% of all schedules are UTC or otherwise unaffected, which is why demanding a policy from everyone is not.

### 1.4 Soundness is relative to a tzdb version, and that is a real cost

`[CODE]` 47 of the 342 currently-clean zones (13.7%) had anomalies within the last decade. `[DOC]` The existence proof for the clean→dirty direction: tzdb 2024a, released 2024-02-01, gave `Asia/Almaty` and `Asia/Qostanay` — no DST since 2005 — a one-hour fold at 23:00 local on 2024-02-29. **Twenty-nine days' notice.**

So a schedule that legitimately required no policy under tzdb 2026a can require one under 2026d. This is not a flaw in the design; it is the world. But it means the design ships a new failure mode — *a stored schedule going invalid without being touched* — and that failure mode must be handled by name, not discovered in production.

---

## 2. The doctrine

### 2.1 The reachability principle

> **A policy is required exactly when the schedule can provably reach the anomaly it governs, against a named tzdb version. Where it cannot, the field is absent — not defaulted, not silently supplied, not serialized.**

"Absent rather than defaulted" is load-bearing. A default that is written into a stored schedule is a decision the user never made, travelling forward in time to a tzdb release where it becomes wrong. Phase I's rule that named profiles must "expand to explicit values on serialization" would have planted exactly that fuse; it is hereby revoked. **A profile applied to a UTC schedule sets and serializes nothing.**

### 2.2 The mandatory/conditional split

**Unconditionally mandatory** — no schedule may be constructed without them:

| Field | Why |
|---|---|
| `zone` | An IANA zone identifier, including an explicit `UTC`. Bare offsets and abbreviations are rejected: `-05:00` matches at least five zones; `Etc/GMT+5` is UTC−5 with the sign inverted; "CST" means different things in China and North America. `[MEASURED]` 13 real schedules in the corpus use a fixed-offset `EST` where a DST zone was meant, one of them in a live production calendar feed. |
| `dialect` | For any imported cron pattern. There is no `cron` dialect — there are 21 registered ones. `[MEASURED]` Four distinct day-of-week numbering bases now exist in production, one of them internally inconsistent. |
| anchor semantics | Chosen by constructor, not by flag: a `Pattern` (predicate) and a `Rule` (anchored generator) are built by different calls, because they are different objects. |

**Conditionally mandatory** — required if and only if reachable, determined at construction against the named tzdb:

| Field | Values | Reachable when |
|---|---|---|
| `gap` | `Skip \| ShiftForward \| ClampToGapStart \| ClampToGapEnd \| Reject` | The zone has DST transitions and the schedule's local time can fall in a forward transition |
| `fold` | `First \| Second \| Both \| Reject` | …can fall in a backward transition |
| `invalid_date` | `Skip \| RollBackward \| RollForward \| Reject` | The rule can generate a nonexistent calendar date (day-of-month ≥ 29, Feb 29, `BYMONTHDAY=31`) |
| `wkst` | `MO…SU` | A weekly rule with `INTERVAL > 1`, or `BYWEEKNO` — the only cases where it changes the answer. `[MEASURED]` `WKST=SU` and `WKST=MO` on the same biweekly rule with a Sunday anchor produce schedules sharing **zero dates** |
| `offset_conflict` | `PreferInstant \| PreferWallClock \| Reject` | A stored occurrence carries an offset that disagrees with the current tzdb |

### 2.3 Cardinality, not offset

Gap and fold policies are defined over the **occurrence set's cardinality**, not over a local-time-to-instant mapping.

- `gap: Skip` yields **zero** occurrences that day. `fold: Both` yields **two**.
- `[DOC]` Neither is expressible in NodaTime's `Resolvers`, jiff's `Disambiguation`, TC39 Temporal's `disambiguation`, or any other substrate vocabulary surveyed, because a resolver maps one local time to one instant by construction. This is the specific gap the vocabulary fills, and it is why Occurframe's names cannot simply be borrowed from the substrate.
- `[SPEC]` It is what Temporal's proto already documents as behaviour — "that action will not be triggered on the day that has no 2:30am… an action that fires at 1:30am will be triggered twice" — that is `(Skip, Both)`, a pairing no surveyed library exposes as a choice — the survey being the six of `05-policy-ux.md` (pandas, TC39 Temporal, jiff, Noda Time, chrono, `whenever`), and `12-compatibility-doctrine.md` records that the register itself is incomplete — and it is what temporalio/temporal#8205 has been open since 2025-08-18 requesting.

### 2.4 Failure is by name

Where a policy axis is reachable and unspecified, construction **fails**, and the error names three things: the field, the first affected occurrence, and the fix. It never guesses.

```
PolicyRequired {
  field: "fold",
  because: "America/New_York has a backward transition at 2026-11-01T02:00 local;
            this schedule's 01:30 falls inside the repeated hour",
  first_affected: 2026-11-01T01:30 local,
  admissible: [First, Second, Both, Reject],
  tzdb: "2026a"
}
```

`[INFER]` A required argument whose error message contains the date of the first problem is a different user experience from a required argument that says "missing parameter." Phase II's judgement is that the `whenever` reversal was driven by the second, and that the first has not been tried.

### 2.5 Profiles

Named profiles are permitted as construction-time aliases:

```
Profile.debian_cron  = (gap: ShiftForward, fold: First)
Profile.rfc5545      = (gap: ShiftForward, fold: First, invalid_date: Skip)
Profile.temporal_io  = (gap: Skip,          fold: Both)
Profile.strict       = (gap: Reject,        fold: Reject, invalid_date: Reject)
```

Two constraints, both non-negotiable:

1. **A profile may only set fields that are reachable.** Applying `Profile.strict` to a UTC daily schedule sets nothing and serializes nothing.
2. **A profile name is never serialized.** The expanded, reachable-only values are.

### 2.6 Location, mutability, and identity

- **Policy lives on the schedule and is identity-bearing.** It participates in the spec fingerprint. Two schedules differing only in fold policy are different schedules.
- **A query may override a policy, and a query override is not identity-bearing.** This is what makes "show me what this would do under each policy" implementable without constructing throwaway schedules — the differ's core operation.
- **Policy never mutates.** `with_policy(...)` returns a new schedule with a new fingerprint. A stored schedule's meaning cannot change under its owner.

### 2.7 tzdb provenance and revalidation

- Every schedule records the **tzdb version** under which its reachability was determined.
- Every occurrence carries the tzdb version that produced it.
- `revalidate(schedule, from_tzdb, to_tzdb)` is a pure function of two tzdb handles returning:
  - `Moved { slot_id, was: Instant, now: Instant }` for each occurrence whose instant changed, and
  - `PolicyNowRequired { field, because, first_affected }` where a previously-unreachable axis has become reachable.
- `[INFER]` `PolicyNowRequired` is the named form of the `Asia/Almaty` failure mode. A host that never calls `revalidate` will run a stale schedule; the doctrine's contribution is that the condition has a name, a detector and a report, rather than being a silent hour of drift.

---

## 3. The frozen answers to the Phase I questions

| Question | Answer |
|---|---|
| Which policy choices are mandatory? | `zone` and `dialect` unconditionally; `gap`, `fold`, `invalid_date`, `wkst`, `offset_conflict` conditionally on reachability |
| Which can have defaults? | **None.** Unreachable axes are absent, not defaulted |
| Can defaults exist inside named profiles? | Profiles may *set* reachable fields at construction; they may not supply unreachable ones and are never serialized |
| Does policy live on the recurrence object or the query? | On the schedule, identity-bearing; a query override is permitted and is not identity-bearing |
| Can policy change after construction? | No. `with_policy` yields a new schedule and a new fingerprint |
| How are gap/fold represented? | Named enumerations over occurrence-set **cardinality**, not over offset selection |
| How is invalid-date behaviour represented? | `Skip \| RollBackward \| RollForward \| Reject`, aligned to RFC 7529's `SKIP=OMIT\|BACKWARD\|FORWARD` plus the `Reject` only `numpy.busday_offset` offers |
| How is timezone provenance exposed? | `tzdb_version` on the schedule and on every occurrence; `revalidate()` for change detection |

### The simplest cases, end to end

```
Schedule.daily(at="03:00", zone="UTC")
# succeeds. No policy field is required, set, or serialized.

Schedule.daily(at="02:30", zone="America/New_York", on_gap=Gap.SHIFT_FORWARD)
# succeeds with exactly one policy.
# 02:30 New York falls inside the gap window (02:00–02:59) and outside
# the fold window (01:00–01:59), so `fold` is unreachable and absent.
```

`[CODE]` Phase I's design demanded seven values for each of these; five and four respectively were unreachable. **If the second call had required three policies, the design would have failed.** It requires one.

---

## 4. Self-falsification

1. **This is a partial retreat and concedes the ergonomic point.** True. The unconditional form is abandoned. What survives is that where a decision is *live*, it is not made for you — which is pandas' fail-closed position, reached from the opposite direction.
2. **`PolicyNowRequired` is an unshipped failure mode.** Nothing in the surveyed corpus implements it, so its ergonomics are unknown. A stored schedule that becomes unconstructable on a data update is a novel operational event, and hosts may hate it. The alternative — silently applying a policy the user never chose — is worse, but "worse" is a judgement, not a measurement.
3. **Reachability is sound only relative to a tzdb, and hosts will pin badly.** A host that never updates its tzdb never sees `PolicyNowRequired` and is simply wrong instead. The doctrine cannot fix deployment hygiene.
4. **The 04:00–20:59 clean band invites a shortcut** — "just schedule at 09:00" — which is genuinely good advice and, if widely followed, would shrink the addressable problem the doctrine exists to solve. Occurframe should give that advice anyway.

## Contradictions and unresolved conflicts

1. **This doctrine revokes Phase I's expand-on-serialize rule** (position 6), which Phase I introduced specifically so that stored schedules would not depend on a library's defaults. The revocation achieves the same goal by a different route — absence rather than expansion — but a reader comparing the two documents will find a direct reversal.
2. **Query-level overrides are non-identity-bearing, and query-level overrides can change cardinality.** A preview under `fold: Both` shows an occurrence that a preview under `fold: First` does not. Nothing in the doctrine prevents a UI from displaying a non-identity-bearing preview as though it were the schedule.
3. **`offset_conflict` is listed as conditionally mandatory but its reachability test is not defined here**, because it depends on whether the *host* stores materialised occurrences — which is outside Occurframe. In practice it is required whenever a stored occurrence is re-resolved, and absent otherwise.

## What this section does not establish

- That the conditional design is usable. It is *less* ceremonious than the design that failed, which is a comparison, not a test. No user was asked, in either phase.
- That reachability computation is cheap at scale. 0.026 s for a whole-tzdb scan is a measurement of one scan, not of a service constructing thousands of schedules per second.
- That the cardinality-changing vocabulary can be introduced successfully. RFC 7529 is the closest precedent for new recurrence vocabulary in this family, and it has three partial implementations in eleven years.
