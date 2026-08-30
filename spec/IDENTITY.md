# Final Occurrence-Identity Doctrine

Phase I called this "the single most important unresolved conflict in the entire study" and took a side it flagged as its weakest load-bearing position. Phase II resolved it, and the resolution begins with a diagnosis: **the Phase I conflict was a use/mention error.** `../evidence/11-execution-vs-recurrence.md` meant by "identity" *the value a unique constraint compares in order to admit an occurrence at most once*. `../evidence/14-occurrence-identity-vendor-models.md` meant *the durable name that a receipt, an audit trail or a detached override points at*. Both were correct about their own object, and neither object is the other. The domain contains more than one notion of "the same occurrence," and overloading one identifier across them is what makes every surveyed vendor's behaviour undefined or destructive under rule mutation.

This document is normative for the Occurframe specification. It is stated in full even though v1 ships no engine (see `RESEARCH-II.md` §5), because the vocabulary is one of the artefacts Occurframe publishes, and because Temporal — classified `VOCABULARY_ONLY` — has an open request for precisely this.

---

## 1. The notions of sameness

Four exist. Three are at the occurrence layer; the fourth belongs to execution and is out of scope.

| | Notion | Question it answers | Granularity | Owner |
|---|---|---|---|---|
| **N1** | **Slot** | "Which occurrence in the series is this?" — *the Tuesday standup* | Coarser than an instant, deliberately | Recurrence |
| **N2** | **Instant** | "Has this exact moment already been admitted?" | The computed UTC instant | Recurrence |
| **N3** | **Materialisation** | "Which attempt-bearing record is this?" | One per admission | Execution |
| **N4** | **Attempt** | "Which try was this?" | One per retry | Execution — **out of scope** |

`[FACT]` **N1's coarseness is not an Occurframe invention; it is what every calendar vendor independently built.** Microsoft's `PidLidGlobalObjectId` carries year, month and day only, and `CleanGlobalObjectId` zeroes even those to form the series key. EWS `OccurrenceItemId` is `(RecurringMasterId, InstanceIndex)` — a position, with no time in it at all. Microsoft Graph's `occurrenceId` is `OID.{seriesMasterId}.{yyyy-MM-dd}`. Dagster's partition key is `"2024-01-01"`. Four independent systems, four encodings, all *deliberately coarser than the instant*.

`[INFER]` N1 and N2 differ by exactly one line: **N2 moves when the time of day changes; N1 does not.** Move the standup from 10:00 to 11:00 and it is still the same standup (N1 preserved) but a different moment (N2 changed). That single distinction is what Phase I collapsed, and collapsing it is why a single identifier cannot serve both.

`[INFER]` The "user-visible event" the brief lists as a candidate notion is **not primitive**. It is N1 for addressing plus N3 for content. A calendar UI lets you drag "the 3pm on the 14th" — an N1 reference — and what moves is the content of a materialisation.

---

## 2. Model comparison

Phase II tested Models A (deterministic/computed), B (surrogate) and C (dual) against twenty mutation and distribution scenarios. The full matrix is in `04-occurrence-identity.md`; the decisive rows:

| Scenario | A: computed only | B: surrogate only | C: dual |
|---|---|---|---|
| Two nodes enumerate the same occurrence | ✅ agree without coordination | ❌ impossible before materialisation | ✅ N2 agrees |
| Backfill a period predating the schedule | ✅ names are computed | ❌ nothing was ever minted | ✅ |
| Change time of day, occurrence already ran | ❌ re-keys; the past receipt orphans | ✅ survives | ✅ N1 survives, N2 changes as it should |
| tzdb update moves the instant | ❌ re-keys silently | ✅ survives | ✅ N1 survives; N2 change is *detectable* |
| Reschedule one occurrence | ❌ the override orphans (the RFC 5545 `RECURRENCE-ID` failure) | ✅ | ✅ |
| Edit the rule at 09:59 for a 10:00 occurrence | ❌ **double-fires** if the spec is in the key | ✅ | ✅ |
| Retry after crash | — | ✅ | ✅ N3 |
| Duplicate the schedule under a new name | ✅ distinct | ✅ distinct | ✅ distinct |

**Model A fails on mutation. Model B fails on coordination and backfill. Model C passes both.**

`[CODE]` **And Phase I's objection to Model C — "no surveyed system does this" — is false.** Airflow 3's `task_instance` carries `id: uuid7 PRIMARY KEY` **and** `UniqueConstraint(dag_id, task_id, run_id, map_index)`. The composite key was *demoted* from primary key by migration `d59cbbef95eb`, which is the exact move this doctrine prescribes: keep the semantic key as a constraint, mint a surrogate as the record's identity. Solid Queue arrived at the same shape independently, and Temporal, Microsoft Graph and JMAP each carry both on different objects.

---

## 3. The doctrine

### 3.1 Three identifiers

```
slot_id            = (series_id, nominal_local_datetime, zone_id, fold)
admission_key      = (series_id, instant_utc, resolution)        -- a UNIQUE constraint, not a value to display
materialisation_id = host-minted UUIDv7                          -- primary key of the receipt
```

**`slot_id` — the durable name.**
- Derived from the *nominal* local date-time the rule produced, **before** any jitter and **before** any per-occurrence override.
- Carries `zone_id` because "10:00 in New York" and "10:00 in London" are different slots.
- Carries `fold ∈ {0,1}` (PEP 495 semantics) so that the two occurrences of a repeated local hour under a `Both` fold policy are distinguishable. `[SPEC]` Neither RFC 5545 nor RFC 8984 can express this, which is a real interchange limitation and is recorded as such in `12-compatibility-doctrine.md`.
- **Stable under**: time-of-day change is *not* stable — changing the time changes the slot, which is correct, because "the 10:00" and "the 11:00" are different slots even in the same series. Stable under tzdb updates, policy changes, dialect reinterpretation, and any spec edit that does not move that occurrence's nominal local time.
- **`series_id` is caller-supplied and opaque to Occurframe.** It is not derived from the rule. Kubernetes keys on `cj.Name`, Solid Queue on `task_key`, Temporal on a configured `WorkflowId`; none derives it from the schedule. Occurframe follows.

**`admission_key` — the coordination-free guard.**
- A uniqueness constraint over `(series_id, instant_utc, resolution)`, enforced by the host's store, in the same transaction that records the admission.
- `instant_utc` is the computed instant; `resolution` distinguishes occurrences that share an instant for different reasons (chiefly under `Both`).
- This is the fencing token that Kleppmann observes Redlock lacks: monotone, derived without coordination, and checkable by the resource itself. It requires only that every node compute the same instant from the same spec and the same pinned tzdb — a determinism property testable exhaustively in CI, unlike the bounded-clock assumptions that locks require.
- **It is a constraint, not a display value.** Nothing should render it to a user or store it as a foreign key.

**`materialisation_id` — the receipt's identity.**
- Minted by the host, UUIDv7 (time-ordered, index-friendly).
- One slot may have many materialisations: Temporal backfill uses `ALLOW_DUPLICATE`; Dagster re-materialises the same partition key. A model that forbids this cannot express backfill or re-run.
- Occurframe never mints it and never requires it. It appears in the specification only so that receipts have a defined shape.

### 3.2 The spec fingerprint is evidence, never a key

`[CODE]` **This overturns Phase I doctrine position 18.** If the fingerprint is in the key, editing a schedule at 09:59 re-keys its 10:00 occurrence, the admission guard no longer matches, and the occurrence fires twice. Kubernetes (`cj.Name`), Solid Queue (`task_key`) and Temporal (configured workflow ID) all key on a stable series name and none hashes the spec.

The fingerprint's correct home is the receipt, recording *which version of the schedule produced this occurrence* — exactly Airflow's `dag_version_id`. It answers "why did this fire then?" after the fact, which is the question it is actually good for.

### 3.3 The offset is a witness, not a key component

The UTC offset in force at an occurrence is serialized alongside it as an RFC 9557-style consistency witness. It participates in **no** identifier. Its purpose is to make `revalidate()` implementable: on a tzdb change, a stored occurrence whose recorded offset no longer matches the recomputed one is a *detected* move rather than a silent one.

### 3.4 Re-keying semantics

When a schedule changes:

| Change | `slot_id` | `admission_key` | Required action |
|---|---|---|---|
| Time of day | new slots from the change forward | new | Past receipts retain their old slots; they are history, not orphans |
| Zone | new slots from the change forward | new | Same |
| Gap/fold/invalid-date policy | unchanged where the occurrence was unaffected; new where cardinality changed | changes only where the instant changed | `revalidate()` reports the delta |
| Dialect reinterpretation | may change any slot | may change any instant | Treat as a new series; require an explicit operator acknowledgement |
| Anchor, `COUNT`, `UNTIL`, `INTERVAL` | unchanged for occurrences that survive | unchanged | Occurrences that no longer exist are simply absent; their receipts remain |
| Add/remove an exception | unchanged for surviving occurrences | unchanged | The excluded slot has no future occurrence; its history stands |
| tzdb update | unchanged | changes where the instant moved | `revalidate()` returns `Moved{slot_id, was, now}` |

`[INFER]` The invariant that makes this coherent: **`slot_id` is a function of what the rule *says*; `admission_key` is a function of what the rule *computes*.** Changes to the calendar of the world move the second and not the first, which is exactly what a human means when they say the meeting is still the same meeting.

---

## 4. Serialization fields

Normative for any occurrence Occurframe's specification describes.

```
occurrence:
  slot:
    series_id      : string          # caller-supplied, opaque
    nominal        : local date-time # no offset
    zone           : IANA zone id
    fold           : 0 | 1
  instant          : RFC 3339 UTC
  offset           : ±HH:MM          # witness only
  resolution:
    civil_anomaly  : none | gap | fold
    date_anomaly   : none | invalid_date
    policy_applied : { gap?, fold?, invalid_date? }   # only the axes that were reachable
    tzdb_version   : string          # e.g. "2026c"
  spec_fingerprint : string          # evidence; never a key
```

A receipt adds `materialisation_id`, `admitted_at`, `outcome` and `attempt`, all host-owned.

---

## 5. The boundary objection, answered

**Objection.** `materialisation_id` is minted by the execution layer, so a dual-identity doctrine appears to violate the recurrence/execution separation the whole project rests on.

**Answer.** It does not, because Occurframe does not mint it, require it, or depend on it. Occurframe defines `slot_id` and the `admission_key`, both of which are pure functions of the schedule and a pinned tzdb. The specification *names* `materialisation_id` only so that the two layers have a shared word for the thing the receipt is keyed by — the same service Occurframe performs for `MissedPolicy`, which it also defines and does not execute. The boundary holds: **Occurframe mints the key; the host writes the row.**

**Bounded concession.** A host that never materialises anything (a UI computing a preview, a linter classifying a crontab) uses `slot_id` and nothing else, and that is a complete and correct use of the model. The third identifier is optional in a way the first two are not.

---

## 6. Self-falsification

The strongest case against this doctrine, stated as well as the evidence permits:

1. **Three identifiers with three invalidation conditions is a specification no consumer will implement correctly.** This is the red team's strongest point and it is not fully answerable. The mitigation is that the three are *layered*: a preview needs one, a deduplicating scheduler needs two, an auditing system needs three, and each layer is complete on its own. But a specification whose correct use requires understanding which layer you are in has a real adoption cost.
2. **`fold` in the slot key is unrepresentable in the two interchange formats that matter.** RFC 5545 and RFC 8984 cannot carry it. Any system that round-trips through iCalendar loses the distinction, so under a `Both` fold policy the two occurrences become indistinguishable on export. This is a genuine, unfixable limitation of the surrounding standards, and it caps what interchange can preserve.
3. **`series_id` being caller-supplied moves a hard problem outward.** If a caller reuses a `series_id` across semantically different schedules, every guarantee here dissolves. Occurframe cannot detect that. The vendor precedent is unanimous, which is the defence, but "everyone else also pushed this outward" is a weak one.

**What would overturn the doctrine:** a demonstration that a single identifier can survive both a time-of-day change and coordination-free derivation. Phase II found no such construction, and the scenario matrix in `04-occurrence-identity.md` §3 is the argument that none exists.

---

## Contradictions and unresolved conflicts

1. **This doctrine contradicts Phase I doctrine position 18** on the spec fingerprint, and Phase I's `../15-conceptual-api.md` §5 encodes the superseded version in `occurrence_id`. Phase I's text stands as the record of what was believed; this document supersedes it.
2. **`resolution` in the admission key is doing subtle work.** Under `Both`, two occurrences share a nominal local time and differ by offset — so the *instant* differs and the guard works without `resolution`. `resolution` is needed only for the pathological case where a policy produces two occurrences at the same instant, which Phase II could not construct but also could not prove impossible. It is retained defensively.
3. **N4 (attempt) is declared out of scope but appears in the receipt shape** as `attempt`. That is a host field named for completeness, not an Occurframe concern; a reader could reasonably call it scope creep in the specification.

## What this section does not establish

- That any host will implement the dual model. Airflow 3 and Solid Queue arrived at it independently, which is evidence it is discoverable, not evidence it is adoptable as a specification.
- That `slot_id`'s encoding is right. The four vendor encodings surveyed disagree with each other and with this one; nothing establishes that a fifth encoding is what the world needs.
- That the coarseness of `slot_id` matches user intuition. No user was asked what "the same occurrence" means to them, in either phase.
