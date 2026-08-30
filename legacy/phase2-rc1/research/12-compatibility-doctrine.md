# Compatibility doctrine

Phase I wrote its compatibility section for a product that is no longer being built. Phase II's verdict is **ORACLE ONLY**: Occurframe ships an executable conformance corpus, a policy and identity vocabulary, a differential runner with published results, and dialect documentation — no production recurrence engine in v1. The 432-line `reference/cron_ref.py` derives expected values from a declared policy and lives outside `runners/` so it can never be scored as an engine.

Compatibility therefore no longer means *can our engine replace yours*. It means: **how does the corpus name, classify and test the semantics that already exist, without arbitrating what the standards do not settle?** Six doctrines follow, then an explicit revision of Phase I. Lossless bidirectional conversion remains impossible, and Phase II adds two new impossibilities — one created by the standardisation attempt itself.

**Epistemic key.** `[SPEC]` normative standards text · `[DOC]` vendor or project documentation · `[CODE]` read from source · `[FACT]` a checkable state of the world · `[MEASURED]` produced by running the corpus at `oracle/` on 2026-08-30 · `[INFER]` derivation from labelled evidence.

---

## 1. The dialect register

### 1.1 Why, and what a dialect is

`[MEASURED]` 37 of 184 vectors are `DIALECT_DEPENDENT` — unanswerable until the asker states which syntax family the expression is written in — carrying up to eight labelled cases each. A case label means something only if the dialect it names is a **stable, versioned, citable identifier**; otherwise `PASS[quartz-1-7]` is folklore, not a measurement.

`[INFER]` The boundary the register enforces: **a policy is what a deployment chooses and can change without touching the expression; a dialect is what the expression is written in.** A product may offer a policy as configuration; it cannot offer a dialect as configuration without demanding the user declare which dialect their stored strings were written in — which nobody recorded.

`[MEASURED]` A **configuration variant is a first-class entry**: croner's `legacyMode` flips five vectors' verdicts in both directions. "croner's behaviour" is not a well-formed subject.

### 1.2 The entry

Twelve fields, in order: **1** `dialect_id` — `vendor.name@version`, permanent, never reused, bracketed suffix for a configuration variant; **2** field count and order; **3** DOW numbering base, including whether `7` is admitted; **4** DOM/DOW combination rule, as a `cron.dom_dow` value; **5** step semantics — interval or field-local filter, and which of `*/n`, `a-b/n`, `a/n` are admitted; **6** supported extensions; **7** macro set with expansions; **8** timezone binding; **9** documented DST behaviour, gap and fold; **10** normative source, by `manifest.json` key; **11** claiming implementations; **12** the vectors that pin it.

Two governance rules. **Entries are append-only within a corpus MAJOR** — adding a dialect or case is MINOR, renaming or removing one is MAJOR. And **every entry carries an evidence grade**: `[MEASURED]` where the run exercised an implementation, `[DOC]`/`[SPEC]` where it did not. `[MEASURED]` No Java or .NET engine was reachable, so Quartz and Spring are `[DOC]`-graded and every Quartz-shaped vector is graded against enumerated cases, never against Quartz. That hole is visible *in the register*, not in a footnote.

### 1.3 The register — syntax

**17 dialects, 4 of which carry registered configuration variants: 21 identifiers.**

| `dialect_id` | fields & order | DOW base | DOM/DOW | steps | extensions | macros |
|---|---|---|---|---|---|---|
| `posix.crontab@2017` `[SPEC]` | 5 `min hr dom mon dow` | `0–6`, 0=SUN, **no 7** | `or-set-semantics` ("element or list") | **none defined** | none | none |
| `vixie-cronie@crontab5` `[CODE]` | 5 | `0–7`, 0 and 7 = SUN | `or/vixie` — OR unless a day field's **first character** is `*` | `*/n`, `a-b/n`; field-local | cronie `~` | `@yearly @annually @monthly @weekly @daily @midnight @hourly @reboot` |
| `quartz@2.3` `[DOC]` | 6–7 `sec min hr dom mon dow [year]` | **`1–7`, 1=SUN** | `reject`; `?` required in one day field | `*/n`, `a-b/n`, **`a/n`** | `L L-n dL nW LW d#n ?` | none |
| `spring@5.3` `[DOC]` | 6 `sec min hr dom mon dow` | `0–7`, **0 and 7 = SUN** | `and` `[INFER]` | `*/n`, `a-b/n`, `a/n` | `L L-n dL nW LW d#n ?` | Vixie set minus `@reboot`, 6-field expansions |
| `aws.eventbridge-scheduler@2022` `[DOC]` | **6 `min hr dom mon dow year`** | `1–7`, 1=SUN | `reject`; "you must use `?` in the other" | `*/n`, `a-b/n`, `a/n` | `L W # ?` | `rate()`, `at()` — no `@` |
| `robfig@3.0.1` = `k8s.cronjob@1.27+` `[CODE]` | 5 (6 with `WithSeconds()`) | `0–6` | `or/vixie` | `*/n`, `a-b/n` | none | Vixie set + **`@every <dur>`** |
| `croniter@6.3` `[MEASURED]` | 5, 6, 7 | `0–7` | `or/vixie` | `*/n`, `a-b/n`, `a/n` | `L W # H R ?` | Vixie set |
| `cron-parser@5.10` `[MEASURED]` | 5, 6 | `0–7` | `or/vixie` | `*/n`, `a-b/n`, `a/n` | `L # ?`, `H`+`hashSeed` | Vixie set |
| `croner@10.0.1` `[MEASURED]` | 5, 6, 7 | `0–7` | `or-any-nonstar` | `*/n`, `a-b/n`, `a/n` | accepts **and ignores** `# L ?` | Vixie set |
| `apscheduler3@3.11.3` `[MEASURED]` | 5 (`from_crontab`) | **numeric `0–6`, 0=MON; named SUN–SAT Sunday-based** | `and+monday-zero` | `*/n`, `a-b/n`; **ignores steps on named ranges** | none | **none** |
| `dragonmantank@3.x` `[MEASURED]` | 5 | `0–7` | `or-any-nonstar` | `*/n`, `a-b/n`; **step modulo range** on `*/90` | `L W #` (`LW` **wrong**) | Vixie set |
| `fugit@1.11` `[MEASURED]` | 5, 6 | `0–7` | `or/vixie` | `*/n`, `a-b/n` | `L # % & ~`, natural language | Vixie set |
| `ocps@1.0` `[SPEC]` FINAL rev 2, 2026-06-07 | **5 only** | `0–7`, "0 and 7 MUST both be treated as Sunday" | `or` (§6.1) | `*/n`, `a-b/n` only — **`a/n` MUST be a parse error** | **none** | **none** |
| `ocps@1.1` DRAFT | as 1.0 | as 1.0 | as 1.0 | as 1.0 | none | Vixie set, **case-sensitive**; `@reboot` MUST parse, MAY be rejected at runtime |
| `ocps@1.2` DRAFT | **5, 6 (`sec`-leading), 7 (`sec`…`year`)**; year **only** in 7-field | as 1.0 | as 1.0 | as 1.0 | none | as 1.1 |
| `ocps@1.3` DRAFT | as 1.2 | as 1.0 | as 1.0 | as 1.0 | **`L`, `W`, `#` on the OCPS base**: `D#N` with `D`=0–7; `5L`, `FRI#L` | as 1.1 |
| `ocps@1.4` DRAFT | as 1.2 | as 1.0 | **`or` normative; `+MON` = portable AND** | as 1.0 | as 1.3, plus `?` **"formally defined as non-portable"**, alias for `*`, day fields only | as 1.1 |

`[MEASURED]` **Four registered configuration variants**, each a separate identifier, differ from their parents only as named: `croniter[day_or=False]` and `croner[legacyMode=false]` change DOM/DOW to `and` (the latter also *honours* `# L W ?` and the Quartz 7-field form rather than ignoring them); `cron-parser[strict]` and `robfig[seconds]` make six fields mandatory.

### 1.4 The register — binding, DST, provenance

| `dialect_id` | timezone binding | documented DST (gap / fold) | source · claimants | pinning vectors |
|---|---|---|---|---|
| `posix.crontab@2017` | process environment | **silent** | `posix-crontab` · POSIX.1-2017 | `CRON-FIELDS-001`, `CRON-DOW-001` |
| `vixie-cronie@crontab5` | `CRON_TZ=` per table, after the assignment; Vixie `TZ=` *"ignored other than for the command it runs"* | *"Jobs … scheduled during the 'missing times' will never be run"*; fixed-time and wildcard differ, **and cronie's two man pages contradict each other** | `crontab5`, `vixie-cron.c` · cronie, Debian cron | `CRON-DAYF-001..006`, `CRON-DST-001..020`, `CRON-FIELDS-008..013` |
| `quartz@2.3` | `TimeZone` object | gap skip, fold once — in an FAQ only | `quartz` · Quartz, Quartz.NET, go-quartz | `CRON-FIELDS-003`, `CRON-EXT-006..009`, `CRON-STEP-002/003` — **`[DOC]`, never measured** |
| `spring@5.3` | caller's `Temporal`; `@Scheduled(zone=)` | gap **no fire that day** (#28245 closed `declined`); fold **unstated** | `spring-cronexpression` · Spring 5.3+ | `CRON-FIELDS-002`, `CRON-EXT-013` — **`[DOC]`** |
| `aws.eventbridge-scheduler@2022` | any IANA zone, per schedule | *"skipped"* / *"runs only once and does not repeat"* | `aws-eventbridge` · EventBridge Scheduler | `CRON-FIELDS-002/007`, `CRON-EXT-009` |
| `robfig@3.0.1` / `k8s.cronjob` | `WithLocation`, in-band `TZ=`/`CRON_TZ=`; `[CODE]` Kubernetes rewrites `.spec.timeZone` **into that same in-band prefix**, and both MUST NOT be set | gap skip, fold both `[MEASURED]`; **KEP-3140 states no DST policy at all** | `robfig-cron`, `kep-3140` · Kubernetes CronJob, Temporal, River, asynq | `CRON-DST-001..020`, `CRON-DST-007` (**HANG**) |
| `croniter@6.3` | aware `start_time` | gap `next_valid`, fold `both` | `croniter-docs` · croniter | `CRON-FIELDS-002/004` (**`seconds_trailing`**), `CRON-DAYF-002` |
| `cron-parser@5.10` | Luxon zone | gap shift-by-delta, fold skip | `cron-parser-docs` · BullMQ (TS), Prefect UI | `CRON-DST-001/003`, `CRON-FIELDS-002` |
| `croner@10.0.1` | zone option | gap shift-by-delta, fold **second** pass | `croner-docs`, `ocps` · croner, croner-rust | `CRON-DST-003/004/006`, `CRON-EXT-005/006` |
| `apscheduler3@3.11.3` | `timezone=` | gap **pre-gap offset** (an imaginary wall time); fold both, **then a fixed point** | `apscheduler-docs` · APScheduler 3.x | `CRON-DOW-013`, `CRON-DST-001/003/016` |
| `dragonmantank@3.x` | `DateTimeZone` | gap shift-by-delta, fold both | `php-cron-expression` · Laravel scheduler | `CRON-EXT-005`, `CRON-DOW-007/011`, `CRON-STEP-004` |
| `fugit@1.11` | **IANA zone inside the expression string** | **undocumented**; measured gap skip, fold skip | `fugit-docs` · fugit, rufus-scheduler, sidekiq-cron | `CRON-DST-001/002`, `CRON-INV-002` |
| `ocps@1.0..1.4` | **"timezone-agnostic"** — §6.4 requires interpretation against implementation local time, mechanism undefined | 1.0–1.3 silent. **1.4 §4.3.1: gap SHOULD skip; fold SHOULD run once, at the first occurrence** — RECOMMENDED, not MUST | `ocps` · 17 libraries in OCPS's own matrix; croner shipped two breaking changes for 1.4 | `CRON-DAYF-002`, `CRON-FIELDS-008..012`, `CRON-EXT-001..008` |

### 1.5 Where a dialect's documentation contradicts its implementation

Cases where "declare your dialect" does not close the question.

- `[CODE]` **Vixie.** `crontab(5)` conditions the day-field OR on a field *"not being `*`"*; `entry.c` conditions it on the field's **first character**, before parsing: `if (ch == '*') e->flags |= DOM_STAR;`. `[MEASURED]` `CRON-DAYF-010` (`0 12 *,10 * 2`) and `-011` (`0 12 10,* * 2`) denote the same set and **the engines swap sides between the two spellings** — which is why those four vectors are `KNOWN_DIVERGENCE`, not `DIALECT_DEPENDENT`.
- `[DOC]`/`[FACT]` **Spring.** The javadoc says `L` may stand alone in the day-of-week field; issue **#29884** reports the implementation throws unless `L` carries a prefix, and asks that the *documentation* be corrected. `CRON-EXT-013` records it as `AMBIGUOUS_STANDARD`.
- `[MEASURED]` **croner.** Its default legacy mode **accepts and ignores** `#`, `L` and `?` — parse-then-ignore, the most dangerous behaviour available, shipped as a default. (By contrast dragonmantank's wrong `LW` is a defect, not a dialect, and earns no register value.)

### 1.6 The two newly measured entries, and one register error

`[MEASURED]` **A third numbering base, internally inconsistent.** APScheduler 3.11.3's `CronTrigger.from_crontab()` maps numeric `0` to **Monday** and rejects `7`, while mapping `SUN` to Sunday:

```
0 12 * * 0 -> 2026-01-05 Mon      0 12 * * SUN -> 2026-01-04 Sun
0 12 * * 7 -> ERROR (max is 6)    0 12 * * MON -> 2026-01-05 Mon
```

`[INFER]` Two spellings of "Sunday" in one engine denote different days, inside a method whose documented purpose is crontab compatibility; every numeric weekday copied from a crontab shifts forward one day, silently. `CRON-DOW-013` makes it a single scoreable `NORMATIVE` failure that only APScheduler fails. The register therefore holds **four** bases — `0–7` both-Sunday, POSIX `0–6`, Quartz `1=SUN`, APScheduler numeric `0=MON` — and the fourth is not internally consistent, so `cron.dow_numbering` alone does not describe it.

`[MEASURED]` **A trailing-seconds reading of the sixth field.** `CRON-FIELDS-002`, `0 15 10 * * *`: five builds read leading seconds, three reject, and **croniter reads the sixth field as *trailing* seconds** — `15:00:00, :01, :02, :03`; `CRON-FIELDS-004` confirms it is systematic. `[INFER]` The corpus anticipated Quartz's leading seconds and EventBridge's trailing year; `seconds_trailing` was measured, not predicted, and a documentation survey would not have found it.

`[MEASURED]` **A register error in the corpus itself.** `CRON-FIELDS-002`'s `year-trailing` case note attributes that reading to "AWS EventBridge, Spring", but `[DOC]` Spring is **seconds-leading**. A PATCH correction under the corpus's own governance, reported rather than quietly fixed, because the neutrality claim rests on exactly that.

---

## 2. What a compatibility claim may say

### 2.1 The grammar

```abnf
claim       = subject SP "conforms to" SP corpus-ref SP "under" SP dialect-ref
              SP profile-ref SP tzdb-ref ":" SP result
subject     = engine-name SP engine-version SP "(" provenance ")" [ config ]
config      = "[" flag "=" value *( "," flag "=" value ) "]"
provenance  = release-id / ( vcs-host SP repo SP "@" commit )
corpus-ref  = "Occurframe conformance corpus" SP semver
dialect-ref = "dialect" SP dialect-id          ; a §1 register identifier
profile-ref = "policy profile" SP "{" axis ":" value *( "," axis ":" value ) "}"
tzdb-ref    = "tzdb" SP release SP "(" tzdb-source ")"
result      = passed "of" scored "scored vectors pass" ";" SP failed "fail"
              SP "(" 1*vector-id ")" ";" SP na "not applicable" ";" SP n "pathologies"
```

> *"cron-parser 5.10.0 (github.com/harrisiirak/cron-parser @7b3a0ad) conforms to Occurframe conformance corpus **1.2.0** under dialect **`cron-parser@5.10`**, policy profile `{cron.dom_dow: or/vixie, cron.dst_gap: shift_one_hour, cron.dst_fold: first, cron.sixth_field: seconds, cron.start_inclusivity: exclusive}`, tzdb **≤2026a** (runtime ICU, fingerprinted): 100 of 107 scored vectors pass; 7 fail (`CRON-DST-003`, …); 77 not applicable; 2 REJECT-BAD."*

### 2.2 The evidence that must back it

Five artefacts, all required, all publishable. **(1) Raw runner output, verbatim**, exception classes and messages included — `[MEASURED]` a `PASS` can be earned by an accidental crash (dateutil's `TypeError` scores `PASS` on `RRULE-SET-004`, which admits rejection), so a report MUST print the `error` string beside any rejection-derived verdict. **(2) Corpus version, engine version *with VCS provenance*, and tzdb release with its source** — the result record makes all three mandatory, so a claim cannot be assembled without them. **(3) Audited tzdb provenance**: `[MEASURED]` where the runtime exposes no version the runner MUST fingerprint against `TZDB-001/002/003` — Bun exposes nothing, Node 22.22.2 reports `2025c` and fingerprints as ≤2026a — so self-reported zone data is not evidence. **(4) The policy profile in the corpus's axis vocabulary**, with the vector count behind each value, from **(5)** a run against at least two tzdb releases.

### 2.3 Forbidden

**"RFC 5545 compliant" · "POSIX cron compatible" · "cron compatible" · "DST-safe" · "100% conformant" · any rate quoted without the policy profile beside it.** Each is a defect in whatever report emits it.

Four constraints. A claim **may not aggregate across configurations** — the bracketed suffix is part of the subject; **may not cite a corpus MAJOR other than the run's**; on a `POLICY_DEPENDENT` vector speaks only for the *declared* policy; and **may not be made at all** on the five `open` vectors or the two unscoreable boundary vectors. `[INFER]` The rate is not the claim: `[MEASURED]` `cron-parser[strict]` scores 60.7% because six fields are mandatory there, ice_cube 18.3% because it discards `TZID` — 47 failures, one fix.

---

## 3. Import doctrine

### 3.1 Cron dialects

**Lossless:** the token sequence, and nothing else. `[INFER]` A cron string is a wall-clock predicate; zone, tzdb release, dialect, DOM/DOW resolution, DST policy, anchor inclusivity and sixth-field reading are all outside the artefact. `[MEASURED]` 89% of vectors produce more than one distinct answer (157 excluding `N/A`; 120 among engines that attempt timezone semantics). **Lossy:** a dialect *declared by the importer* plus the tokens is a complete import, but that declaration is an assertion about the source system, not a fact recovered from the string. **Impossible:** three results, one retained and two new.

> **Impossibility 2 (retained).** The DOM/DOW rule has **five incompatible production resolutions** — OR (Vixie, POSIX, robfig/Kubernetes, OCPS 1.4); AND (fcron, micron strict, node-cron, Cronos); "Nth such weekday of the month" (dcron); parse error with `?` required (Quartz, AWS); mutual exclusion via `*` (Vercel) — plus per-job configurability. `[MEASURED]` `CRON-DAYF-002` enumerates **eight** cases and measured four answers in one run, including APScheduler's `and+monday-zero`, a resolution Phase I did not have. **No expression restricting both day fields is safe to copy between any two categories, and the resolution is not recoverable from the artefact.**

> **Impossibility 3 (new).** **The Quartz extension set has forked from the Quartz numbering base.** `[DOC]` Quartz defines `dayMap.put("SUN", 1)`, so `#` and weekday-`L` are numbered 1=SUN. `[DOC]` Spring's `CronExpression` adopted Quartz's whole extension set — `L`, `L-n`, `dL`, `nW`, `LW`, `d#n` — on the Vixie base, and its javadoc gives `5#2` as *"second Friday"*. `[SPEC]` OCPS 1.3 §4.2 independently adopted the same syntax on the same base — *"`D#N`, where `D` is the day of the week number (0-7)"*, with `2#3` = *"the third Tuesday"* and §4.1's `5L` = *"the last Friday"*. `[INFER]` Under Quartz, `2#3` is the third **Monday** and `5L` the last **Thursday**. Three current specifications define identical syntax and disagree by one day on every numeric weekday, and **nothing in the string distinguishes them** — a collision between three normative documents, not a divergence a maintainer could fix, and one third of it created by the standardisation attempt. `[DOC]`/`[SPEC]`, not `[MEASURED]`: no JVM engine was reachable, and measuring it is the first task of corpus v1.1.

> **Impossibility 4 (new).** **The six-field form is MUST-defined two ways and measured a third.** `[SPEC]` OCPS 1.2 §4.2: the year field *"may be used only in the 7-field pattern, together with the `seconds` field"*, and *"In a 6-field pattern, the fields MUST be interpreted … as `SECOND MINUTE HOUR DAY-OF-MONTH MONTH DAY-OF-WEEK`."* `[DOC]` AWS EventBridge Scheduler requires exactly six, `min hr dom mon dow year`. `[MEASURED]` croniter reads the sixth as *trailing seconds*. EventBridge's `cron(15 10 * * ? *)` is 10:15 daily; the same tokens under OCPS 1.2 are second 15, minute 10, every hour — **twenty-four firings a day against one** — and OCPS 1.4 §4.2 additionally makes the `?` in the month field a parse error. `[MEASURED]` `CRON-FIELDS-004` measures the third reading: `*/15 * * * * *` is 5,760 firings a day seconds-leading and **86,400** under croniter's. A six-field cron expression is not lossy to import; it is **undecidable from the artefact**, with two of three readings mandated by MUSTs in different specifications.

A weaker fourth result: `[SPEC]` OCPS 1.0 rev 2 requires a step operator *"not preceded by `*` or a full range `A-B` (e.g., `/30`, `0/15`, or `10/10`)"* to be a parse error, while `[DOC]` Quartz, Spring and AWS all document `0/15`; `[MEASURED]` on `CRON-STEP-002` (`5/20`) eleven builds accept and five reject, and the prevalence study found `graylog2/graylog2-server`'s live `0 0 1/14 * MON-FRI`. `[INFER]` "OCPS 1.0 compliant" and "Quartz compatible" are mutually exclusive *claims* about any `N/M` expression.

### 3.2 RFC 5545 RRULE

**Lossless: the `BY*` core** — Phase II's most important positive result. `[MEASURED]` On `RRULE-BY-012/013/014` (`BYSETPOS`), `-017/018/019` (`WKST`) and `-005`–`010` (`BYMONTHDAY` 31, 30, 29, −1, `1,-1`, yearly 29 February), **all five reachable engines agree with each other and with the RFC's printed instance lists.** Any claim that RRULE expansion is broadly unreliable is falsified.

**Lossy:** `DTSTART`'s four roles (`RRULE-CORE-003`, `rrule.dtstart_emission`); truncation of an unbounded rule (`RRULE-CORE-013`, `rrule.truncation`); `UNTIL`'s UTC coupling (`RRULE-CORE-007..010`); `RSCALE`/`SKIP`, where `[MEASURED]` "silently ignored" is the dangerous answer because the rule parses and yields a plausible different set (`RRULE-BY-011`).

**Impossible: set operations and the prose-only MUSTs.** `[MEASURED]` `rrule.sets` is the least interoperable family measured — no vector unanimous, four at five answers — and `RRULE-SET-006` decides occurrence identity three-to-one: dateutil, php-rrule and rrule-go match an `EXDATE` **by instant**, rrule.js **by wall time**. **25 of the 31 `REJECT-BAD` verdicts fall on RRULE**: `COUNT`+`UNTIL` accepted by four of five, `INTERVAL=0` by three, `BYMONTHDAY=32` by three of which one hangs. `[INFER]` What the ABNF expresses is enforced; what only the prose forbids is not, so an importer cannot rely on the source having validated anything.

### 3.3 RFC 8984 JSCalendar

**Lossless:** the whole `RecurrenceRule` object — the RRULE algebra with the fusions unpacked. **Lossy:** `[SPEC]` `until` is a `LocalDateTime` where RFC 5545's is a fixed instant, so a tzdb revision between write and read moves one relative to the other; and legislating that the start *"is always the first occurrence in the expansion … even if it would normally not match the rule"* makes a series whose anchor is **not** an occurrence unrepresentable. **Impossible:** `[FACT]` no analogue of `RANGE=THISANDFUTURE`, and the conversion document remains `draft-ietf-calext-jscalendar-icalendar-25` in WG Last Call — **the round-trip mapping is not a published RFC.**

### 3.4 Microsoft Graph / MS-OXOCAL

**Lossless:** patterns whose ordinal, weekday set and interval fit the fixed templates. **Lossy:** `[SPEC]` MS-OXCICAL instructs implementers to *"gracefully fail to map any recurrences that do not fit the templates"* — a sanctioned data-loss path — and `[DOC]` `iCalUId` differs per occurrence, so merging a Graph feed with a Google feed on it fragments one series into N or collides N into one.

> **Impossibility 1 (retained, unchanged).** `[SPEC]` MS-OXCICAL §2.1.3.2.3 states that under RFC 2445 a `BYMONTHDAY` of 29, 30 or 31 **"MUST skip over months that do not have a sufficient number of days"** while *"[c]onversely, [MS-OXOCAL] specifies"* the corresponding pattern **"MUST occur on the last day"** of such months. Seven occurrences a year against twelve — **25 over five years** — and the round trip does not return the input, because MS-OXCICAL emits `BYMONTHDAY=-1` for day 31. RFC 5545 cannot say "clamp" without `RSCALE`; Outlook has no pattern for "omit". `[DOC]` Stripe clamps, so the RFC's mandatory behaviour is the minority behaviour among deployed systems. `[MEASURED]` Phase II confirms the RFC side is what engines do: `RRULE-BY-005`–`010` are unanimous.

### 3.5 Google Calendar

**Lossless:** `RRULE`/`RDATE`/`EXDATE` as content lines; `(recurringEventId, originalStartTime)` as the documented key. **Lossy:** `[DOC]` the 730-instance expansion cap, and `EXDATE` *"must point to a valid instance generated by the recurrence rule"*, so re-expansion that shifts instants orphans exclusions. **Impossible:** `[DOC]` *"Changing all following instances resets any exceptions happening after the target instance."* A tail edit destroys the tail's overrides, where `THISANDFUTURE` shifts them and EventKit's `.futureEvents` is undocumented — three irreconcilable outcomes for one user action, and no format carries the intent.

### 3.6 The lossiness report as an artefact

Emitted **per conversion**, never per format. Required fields:

| field | content |
|---|---|
| `source_dialect` / `target_dialect` | §1 register identifiers, configuration suffixes included |
| `corpus_version` · `tzdb` · `tzdb_source` | what the classification and horizon were computed against |
| `input` | the artefact, verbatim |
| `dropped` | constructs in the source and inexpressible in the target, each with the vector ID demonstrating it |
| `resolved` | each MUST-level conflict met, **which source was preferred and which sacrificed**, by `manifest.json` key |
| `policy_assumed` | every axis whose value was assumed rather than declared, with the assumed value |
| `horizon` | the declared window, as an interval |
| `occurrence_delta` | **mandatory** — how many occurrences the two interpretations differ by over `horizon`, plus the first divergent instant |
| `unclassifiable` | constructs whose occurrence set is not a function of the artefact (`@reboot`, Jenkins `H`, cronie `~`, FHIR event-relative anchors, ISDA holiday calendars) |

`[INFER]` **`occurrence_delta` is what makes the report actionable.** *"Some constructs may not be supported"* is a warning log; *"`BYMONTHDAY=31` was exported as `BYMONTHDAY=-1`; over five years the two interpretations differ by 25 occurrences, first diverging 2026-02-28"* is a decision. A report that cannot compute a delta must say so in `unclassifiable` rather than emit zero.

---

## 4. Classification over conversion

**Doctrine.** *The corpus, and any tool built on it, classifies. It does not convert. Where conversion is offered at all it is offered as a lossiness report over a declared endpoint pair, never as a transformation of a bare artefact.*

Three `[MEASURED]` grounds, ascending. **(1)** The target's semantics are not recoverable from the source's string: 37 `DIALECT_DEPENDENT` vectors, plus 4 `KNOWN_DIVERGENCE` vectors where not even a dialect declaration helps. **(2)** A converter must choose a policy the source never recorded: all 20 `cron.dst` vectors are `POLICY_DEPENDENT` over five gap/fold policies, and the family contains **zero** `NORMATIVE` vectors, because crontab(5) legislates for a daemon and says nothing about a library returning a set. **(3)** The answer moves under the converter's feet: `TZDB-005` produced **six** answers factoring into two axes, one being the tzdb release — and under ≥2026b the transition does not exist, so the DST policy is never reached.

`[FACT]` **Prefect PR #22404 is the case where a real project reached this conclusion subtractively.** Inside one product the JS UI parser (`cron-parser`, with `cronstrue` rendering English) and the Python server parser (`croniter`) disagreed on `0 23/6 * * *`: cron-parser reads `N/M` as "start at N, step M" and yields **only 23:00**; croniter normalises to `N-<fieldMax>/M` and, at `N == fieldMax`, expands the whole field — **00, 06, 12, 18**. One occurrence against four, in a PR titled *"Reject server-diverging cron slash-step expressions"* which records that *"Any six-field cron entirely reverses field interpretation."* `[FACT]` The expression was displayed as *"On the hour, every 6 hours, starting at 11:00 PM"* — grammatical, specific, plausible and wrong, which **defeated human review**. `[INFER]` Prefect made the divergent subset unwritable: the right instinct reached from the inside, subtractive because it had no vocabulary for the alternative. A classifier is the additive generalisation — instead of forbidding the string, show both readings and where they part.

### The classifier output

Given a string and, optionally, a zone and anchor:

```jsonc
{ "input": "0 23/6 * * *", "corpus_version": "1.2.0",
  "tzdb": "2026c", "tzdb_source": "PyPI tzdata 2026.3",
  "zone": "America/New_York", "anchor": "2026-01-01T00:00:00", "horizon": "P1Y",

  "parses_under": [
    {"dialect_id":"vixie-cronie@crontab5","status":"reject","reason":"step not preceded by '*' or a range"},
    {"dialect_id":"ocps@1.0","status":"reject","reason":"OCPS 1.0 §6.2: '0/15','10/10' MUST be parse errors"},
    {"dialect_id":"quartz@2.3","status":"ok"},
    {"dialect_id":"cron-parser@5.10","status":"ok"},
    {"dialect_id":"croniter@6.3","status":"ok"} ],

  "sequences": [
    {"label":"start_at","dialects":["quartz@2.3","cron-parser@5.10"],
     "occurrences":["2026-01-01T23:00:00-05:00|2026-01-02T04:00:00Z","…"],"per_day":1},
    {"label":"whole_cycle","dialects":["croniter@6.3"],
     "occurrences":["2026-01-01T00:00:00-05:00|2026-01-01T05:00:00Z","…"],"per_day":4} ],

  "first_divergence":"2026-01-01T00:00:00-05:00|2026-01-01T05:00:00Z",
  "divergent_axes":["cron.bare_start_step"], "vectors":["CRON-STEP-002","CRON-STEP-003"],
  "classification":"DIALECT_DEPENDENT",
  "verdict":"AMBIGUOUS — 2 distinct sequences over P1Y; declare a dialect" }
```

Four rules govern it. **It never picks** — one sequence is a finding, several are a finding, neither is a recommendation. **It cites vector IDs**, so every claim is checkable and can be wrong. **It reports the first divergent instant**, because "these differ" is not actionable. **It states the tzdb release**, because on `TZDB-005` the release changes the number of sequences. `[MEASURED]` The prevalence study bounds the noise: DOM+DOW collisions appear in **7 of 9,485** deployed declarations, and every one is a genuine semantic fork — a tool firing on under 1% of a real corpus and right every time is a different product from a converter that must be right on all of it.

---

## 5. The `AMBIGUOUS_STANDARD` discipline

**Doctrine, normative.** *Where the source standard supplies no answer, none may be manufactured. A vector may not be promoted to `NORMATIVE` on the strength of "most engines do X", "the obvious reading is X", or "our engine does X". Where the admissible space is finite it is enumerated and each case cites the ambiguity; where it is not, `expect.mode = "open"` records the behaviour and grades nothing, and the note must say **why** the space cannot be enumerated.*

`[MEASURED]` 21 vectors carry `AMBIGUOUS_STANDARD`, five use `open`, 122 cells are `RECORD` — measured, deliberately never scored. `[INFER]` An honest `open` beats a fabricated answer, which would convert a finding about the *standard* into a finding about an *engine* — the exact error the corpus exists to prevent.

**Two Verified errata editing one sentence incompatibly.** `[SPEC]` Errata **1913** and **3779** are both *Verified* and *Technical* and edit the same sentence of §3.3.10 into *"when the BYWEEKNO or BYMONTH rule parts are not present"* and *"when the BYMONTH rule part is not present"*. The corrected texts are not nested and **there is no consolidated text of §3.3.10**. `RRULE-BY-026` (`FREQ=YEARLY;BYWEEKNO=20;BYDAY=2MO`) is `open`: under 1913 the numeric prefix is invalid here, under 3779 it means the second Monday of the year. `[MEASURED]` Four engines return empty, two reject. **No engine can be graded, and saying so is the finding.**

**An "editorial" erratum that changes expansion semantics, implemented by one engine.** `[FACT]` Erratum **3747** is *Verified* and classed **Editorial**, yet it deletes the WEEKLY and MONTHLY clauses from Note 2 of the expand/limit table — the clauses making `FREQ=YEARLY;BYWEEKNO=n;BYDAY=MO` mean "the Monday of ISO week *n*". `[MEASURED]` `RRULE-BY-027`: dateutil, rrule.js, rrule-go and php-rrule *expand* across twelve months; **ice_cube alone limits to March**, and ice_cube is the 18.3% outlier on nearly everything else. `[INFER]` "RFC 5545 plus verified errata" and "matches the ecosystem" are here mutually exclusive, and the corpus refuses to pick.

**Silence rather than contradiction.** `RRULE-CORE-017` (`COUNT=0`) and `-018` (`UNTIL` before `DTSTART`) name a state RFC 5545 never names — a valid rule generating zero instances — where `[FACT]` sabre/vobject throws `NoInstancesException` and returns **HTTP 500 on CalDAV sync** for a rule other servers accept; `CRON-INV-007`/`-011` are the cron mirror. `[FACT]` Erratum **6316** (2020, still *Reported*) is the adjacent silence: does a `VALUE=DATE` `EXDATE` exclude the whole day or only midnight?

**Two normative sources satisfied by different engines.** `CRON-DST-001` and `-007` each cite `[SPEC]` RFC 5545 §3.3.5 via erratum 4271 (*a nonexistent local time "is interpreted using the UTC offset before the gap"* — APScheduler's answer) **and** `[DOC]` crontab(5) (*such jobs "will never be run"* — cron-parser's and fugit's). `[MEASURED]` `CRON-DST-007` produces **six** behaviours, one a non-terminating search: three of them satisfy neither cited source.

**Where the domain ends.** `CRON-EXT-011` (Jenkins `H`), `CRON-EXT-012` (cronie `~`), `CRON-FIELDS-013` (`@reboot`) and `RRULE-SET-011` (`RDATE;VALUE=PERIOD`) are recorded and marked unscoreable — a machine-readable boundary.

---

## 6. Migration doctrine for schedule owners

### What the corpus lets an operator learn

1. **Which schedules are ambiguous at all.** `[MEASURED]` Across 9,485 deployed declarations, **16.4%** of raw occurrences and **32.6%** of distinct expressions are non-`PORTABLE`; pure cron expressions, **11.7%**. `[INFER]` The complement is the more useful half.
2. **Which construct makes a schedule ambiguous, by vector ID** — not "may not be portable" but "`CRON-STEP-002`: eleven engines read `1/14` as start-at, five reject, OCPS 1.0 rev 2 requires rejection."
3. **What their current engine implements**, as a policy profile: `[MEASURED]` `or/vixie`, `dow=both`, `sixth_field=seconds_trailing`, `dst_gap=next_valid`, `start_inclusivity=exclusive` for croniter. **That is the migration document**, and no library's documentation answers it today.
4. **Which schedules sit in the DST window.** `[MEASURED]` **81.3% of hour-pinned local-frame schedules fire between 00:00 and 04:00**; 32.3% of all pinned-hour schedules fire at hour zero.
5. **Whether the zone they declared exists.** `[MEASURED]` **142 of 488 explicit-timezone declarations name something that is not a tzdb identifier**; excluding 120 copies of RFC 2445's `US-Eastern`, **22 independent real cases** remain — Windows zone ids, Outlook display strings, vendor-namespaced VTIMEZONE references, leading-slash mangling, free text — each resolving by engine-defined fallback, usually to UTC, silently.
6. **Two operational findings, checkable.** `[MEASURED]` **Kubernetes `spec.timeZone` was set in 6 of 279 CronJobs (2.2%) and resolved to a real zone in *zero*** — in all six the value is a Helm variable defaulting to empty, on a field stable since 1.27; meanwhile `@daily` and `0 0 * * *` are 67% of CronJob schedules and both mean "midnight in whatever zone the kube-controller-manager happens to be in". `[CODE]` `.spec.timeZone`, when set, is rewritten into robfig's in-band `TZ=` prefix, so Kubernetes' zone semantics *are* robfig's, gap and fold included, and `[FACT]` **KEP-3140 states no DST policy at all.** And `[MEASURED]` **13 declarations use `EST`, a fixed-offset tzdb alias that never observes daylight time, where a DST-observing zone was almost certainly meant** — Fedora's `DTSTART;TZID=EST:20260520T140000` is the live case, and the same calendar uses `TZID=PST` and `TZID=CST`, which are not tzdb zones at all. `[MEASURED]` `TZDB-006` is the corollary: under 2026c `America/Edmonton` reports **CST** at −06:00, so any system persisting an offset or abbreviation rather than an IANA identifier stores a wrong answer from that release on.

### What it cannot tell them

**Whether a schedule is *wrong*** — `[MEASURED]` "non-portable" is not "broken"; most non-portable schedules run correctly forever because they only ever meet one engine. **What the author meant** — 2,018 schedules pinned to a single UTC hour may encode mis-recorded local intent, unobservable from a file, so all were excluded from every bucket. **Anything about the execution layer** — missed runs, catch-up, overlap, idempotency and identity across restarts. **Anything about enterprise schedulers** — `[MEASURED]` **1** EventBridge `schedule_expression` in 1,613 Terraform files, **0** Cloud Scheduler jobs. **The dialect a stored string was written in** — Phase I's load-bearing statement, unweakened: *schedules stored as bare cron strings with no recorded zone or dialect can only be re-authored, not converted.*

`[INFER]` **The corpus converts an unbounded audit into a bounded one.** It cannot tell an operator their schedules are right. It can name the handful not decidable from what they stored, cite the construct, and give them the vector to argue with.

---

## 7. Explicit revision of Phase I

`../11-compatibility-migration.md` §1's four buckets are imperatives addressed to an engine. Each row now re-reads as **SURVIVES** (it restates as corpus scope, an axis or a vector), **VOID** (a product instruction with no corpus meaning, or falsified), or **DEFERRED** (live again only if the named external integration commitment triggers the engine decision).

| Phase I row — in Phase I's order: 7 MUST PRESERVE, then 7 SHOULD IMPROVE, then 7 SHOULD REPLACE | Status under ORACLE ONLY |
|---|---|
| Compact string denoting an infinite set | **SURVIVES** as scope — `input.count` is mandatory because no standard supplies the bound. |
| RRULE's BY-part algebra | **SURVIVES, strengthened** — `[MEASURED]` unanimous across every reachable engine; the most interoperable thing measured. |
| Pattern/exception separation | **SURVIVES, tone inverted** — `[MEASURED]` `rrule.sets` is the *least* interoperable family. Right factoring, worst implemented. |
| Determinism given fixed tzdata | **SURVIVES, amended** — determinism is a function of `(rule, anchor, zone, **tzdb release**)`; `TZDB-001`–`006` make the release audited. |
| Positional recurrence-id as rendezvous hint | **VOID as written** — superseded by `04-occurrence-identity.md`; it describes only N1 (the slot), an execution-layer concern the corpus excludes. |
| RFC 5545 wire syntax as export | **DEFERRED** — the corpus consumes content lines as vector input and emits nothing. |
| 5-field cron as input surface | **VOID as instruction; SURVIVES as coverage weighting** — 98 of 184 vectors are `CRON-*`. |
| `DTSTART`'s four roles | **SURVIVES as `rrule.dtstart_emission`** + `RRULE-CORE-003`; `[MEASURED]` four of five engines converged where the standard said undefined. |
| `UNTIL`'s UTC coupling | **SURVIVES as `RRULE-CORE-007`–`010`**; the improvement itself is void. |
| Invalid-date policy gated behind `RSCALE` | **SURVIVES as `rrule.rscale_support`** + `RRULE-BY-011`: "silently ignored" is the dangerous answer. |
| Fused ordinal tokens `BYDAY=2FR` | **VOID** — no axis, no vector, no measurement. |
| Multiple `RRULE`s, fuzzy union | **SURVIVES as `rrule.multiple_rrule`** + `RRULE-SET-008`, where `[MEASURED]` rrule-go **drops the first rule entirely**. |
| `EXRULE` deprecated with no successor | **SURVIVES as `RRULE-SET-010`**; `[MEASURED]` rrule-go ignores it and returns the unfiltered set. |
| Spreading / jitter | **VOID for the corpus, DEFERRED for a product** — `CRON-EXT-011/012` mark it outside the domain. |
| Expand/limit 9×7 table | **SURVIVES as `AMBIGUOUS_STANDARD`** (`RRULE-BY-027`, `rrule.note2`), now with the measurement Phase I lacked. |
| `TZID` as opaque file-scoped string | **SURVIVES, strengthened** — `TZDB-006` plus 22 real non-tzdb identifiers in deployed data. |
| Positional occurrence identity *(contested)* | **VOID.** `04-occurrence-identity.md` resolves Phase I's conflict as a use/mention error and lands on **Model C dual identity**: a coarse computed `slot_id`, an exact computed `instant` as a unique constraint never a primary key, and a host-minted `materialisation_id` as the receipt's PK. Neither Phase I horn survives; the corpus tests none of it. |
| Holidays as baked-in `EXDATE`s | **DEFERRED** — external-calendar dependence is outside the corpus by the rule that excludes Jenkins `H`. |
| `RANGE=THISANDFUTURE` | **DEFERRED** — series mutation is execution-layer; no vector, no axis. |
| Cron's DOM/DOW rule | **VOID as instruction; SURVIVES as the register's centrepiece** — eight cases across six vectors plus four `KNOWN_DIVERGENCE` vectors; OCPS 1.4's `+` is a register value, not a recommendation. |
| `?` with three meanings | **SURVIVES as `cron.qmark`** + `CRON-EXT-009/010`; `[SPEC]` OCPS 1.4 §4.2 now declares `?` *"formally defined as non-portable"*. |

**All seven MUST NOT REPEAT rows survive**, because they warned about *specification technique* and the corpus is a specification artefact. Each becomes testable: never-firing acceptance → `cron.empty_set` + `CRON-INV-007/011`, `RRULE-CORE-017/018`; unbounded expansion → `rrule.truncation` + `RRULE-CORE-013`; a grammar admitting nonsense → now `[MEASURED]`, 31 `REJECT-BAD` on the prose-only MUSTs; silent omission as the only invalid-date policy → `RRULE-BY-005`–`010`, unanimous, so the objection is to the rule not the engines; "undefined" as a device → **partly falsified** by `RRULE-CORE-003`. Two are **promoted**: out-of-band configuration becomes §2.3's claim rule, two default conformance levels becomes the policy-profile reporting requirement.

Phase I's §5 posture also revises. Part 2 — *"a conformance corpus, in libical's existing format"* — is **superseded**: `[MEASURED]` libical's format fails on six counts (no stable identifier, no classification, no timezone provenance, no citation, no policy declaration, a bespoke syntax). Parts 3 and 4 — the lossiness report with an occurrence-count delta, and a classifier rather than a converter — **survive and are specified normatively in §3.6 and §4**. Part 1, "parser compatibility with declared semantics", is **DEFERRED**: it describes an engine's API.

---

## Contradictions and unresolved conflicts

1. **Two Verified errata cannot both be applied.** 1913 and 3779; no consolidated text; `RRULE-BY-026` cannot be graded. Unresolvable by the corpus. On `RRULE-BY-027` the related conflict is that "RFC 5545 plus verified errata" and "matches the ecosystem" are mutually exclusive, and §2's grammar deliberately cannot express "plus errata".
2. **Impossibility 3 is `[DOC]`/`[SPEC]`, not `[MEASURED]`.** It follows from three published documents, but the corpus has zero measured Quartz cells; if Quartz's shipped behaviour differs from its documentation the way Vixie's does, the result changes shape.
3. **Spring's DOM/DOW rule is `[INFER]`** — read from the shape of `CronExpression`'s field loop through a single source fetch, not from a maintainer statement or a measurement. Flagged in the register; measure before quoting.
4. **OCPS's documents are inconsistent, and Phase II's account needs correcting.** `10-oracle-product.md` records the dating as unresolved — a report generated 2025-10-28 measuring a specification finalised 2026-06-07. `[SPEC]` OCPS 1.0's revision history resolves it: **revision 1 is 2025-10-28, revision 2 is 2026-06-07** (a step-notation clarification), so the report measures revision 1. `[FACT]` What remains inconsistent is the count: the adoption summary says *"the 17 libraries listed below"* while the tables carry **21 rows** — 17 libraries, 3 daemons and POSIX.
5. **The register describes claims, and a claim can be false.** §1.5 records both sides where documentation and implementation disagree, but the register has no mechanism to declare one authoritative and should not acquire one.
6. **A crash can still score `PASS`.** §2.2 requires the `error` string beside every rejection-derived verdict, but the real fix — distinguishing "rejected deliberately" from "raised internally" — is a runner-contract change and therefore a corpus MAJOR. Relatedly, Impossibility 4's deltas are expression-specific (~2×, 15×, 24× on three expressions): the impossibility is structural, the number is not.

---

## What this section does not establish

- **That the register is complete.** 17 dialects is a set chosen by argument, and `[MEASURED]` the run itself discovered three axis values the corpus's authors did not anticipate. fcron, GNU micron, dcron, Cronos, node-cron, saffron, systemd `OnCalendar` and Renovate's later.js prose all have register-shaped semantics and no entry.
- **That the claim grammar would be adopted.** It is argued from what makes a claim falsifiable, not from vendor behaviour. `[FACT]` OCPS, the closest comparable artefact, has 9 stars and 0 watchers, and no incumbent benefits from a claim format that can only make their library look worse.
- **That the classification procedure is reproducible.** §5's discipline has been applied by one author. Whether two contributors would classify a vector identically — particularly on the `POLICY_DEPENDENT`/`DIALECT_DEPENDENT` boundary, and on when a silence justifies `open` — is untested, and it is the property on which the corpus's credibility most depends.
- **That the lossiness report is implementable for every endpoint pair**, or any migration cost. `occurrence_delta` is computable only where both interpretations are functions of the artefact plus a declared context; for ISDA business-day adjustment, FHIR event-relative anchors, Jenkins `H` and cronie `~` it is not. Neither phase located published data on real cron-to-anything migrations.
- **That the prevalence figures generalise.** `[MEASURED]` 41.9% of the schedule corpus is GitHub Actions, structurally the safest possible case, and enterprise and business-facing schedules are essentially absent. The Kubernetes `timeZone` and `EST` findings hold *within* public open source and say nothing about private codebases.
- **That any of this survives the engine decision.** Every DEFERRED row above becomes live again if the named external integration commitment triggers. These doctrines are written for a corpus, and a corpus is a weaker thing to be right about than an engine.
