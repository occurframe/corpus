# Occurframe Research II — Final Validation, UX Freeze, and Implementation Gate

**Status:** research complete · product frozen · implementation authorised for one artefact
**Window:** 2026-08-30
**Method:** ten parallel investigations against primary sources, plus two original empirical builds — a 9,485-schedule real-world corpus and a 184-vector conformance corpus executed against 25 engine builds in five languages
**Predecessor:** Occurframe Research I (`../` — 22 deliverables, 16 dossiers, verdict GO WITH REVISED SCOPE)

---

## 1. Executive verdict

# GO — ORACLE ONLY

Build the conformance oracle. **Do not build the reference engine in v1.** The engine is not refused permanently; it is gated on a single named condition stated in §7.

Phase I concluded that the surviving opportunity was "a language-neutral executable conformance oracle, plus a reference engine occupying the unowned layer of civil-time policy, occurrence identity and timezone provenance." Phase II set out to validate both halves. **The first half validated more strongly than expected. The second half failed.**

### What validated

**The divergence is worse than Phase I could show, and it is now measured rather than argued.** A 184-vector corpus run against 25 engine builds in five languages produced ~4,600 result cells. **157 of 184 vectors produce more than one distinct answer** across engines that support them; excluding the single worst outlier engine the floor is still **120 of 184 (65%)**. Two vectors produce six distinct answers. And the run found *pathologies*, not merely disagreements: `robfig/cron` — the engine Kubernetes CronJob vendors — **does not terminate** on the Pacific/Apia skipped calendar day; APScheduler 3.11.3 returns `2026-11-01T01:00:00-05:00` as a **permanent fixed point** across a New York fall-back, under its own documented calling convention; `ice_cube` discards `TZID` entirely; 31 inputs that a standard says MUST be rejected are accepted. `[MEASURED]`

**No such corpus exists, and the one artefact that claims to measure conformance does not.** OCPS — the Open Cron Pattern Specification, 1.0 FINAL — publishes a conformance matrix across 21 rows and states that it is "based on analysis of official documentation and community knowledge." `[FACT]` **Not one cell was measured.** `[INFER, from that stated method]` The specification exists, implementers cite it, and the executable half is missing. That gap is the product.

**Implementers do change semantics for a written specification.** `croner` (34.2M downloads/month, whose contributor guidance reads "Zero dependencies — do not add external dependencies") shipped v10.0.0 with two breaking, user-visible changes made solely to conform to OCPS 1.4. `[FACT]` A library that refuses dependencies accepted a specification. That is the adoption mechanism the category actually has — **but read this bullet with the retraction below**: the specification is not external to `croner`, because OCPS is co-published by `croner`'s own maintainer. What survives is that a *written specification* moved a shipped implementation's semantics; what does not survive is any inference about specifications an implementer does not control.

**And the policy UX problem has a real solution.** Phase I's requirement that civil-time policy be non-defaultable was its most likely cause of rejection. Phase II found it can be made **conditional and exactly decidable**: measured across all 498 zones in tzdb 2026a over twenty years, **342 zones (68.7%) have zero gap or fold anomalies**, and **1,020 of 1,440 minutes-of-day are anomaly-free in every zone on earth** (a contiguous 04:00–20:59 band). The whole-database scan costs 0.026 s. `[CODE]` So `Schedule.daily(at="03:00", zone="UTC")` requires nothing further, and `at="02:30", zone="America/New_York"` requires exactly one policy — because 02:30 New York falls in the gap window but not the fold window. Phase I's design demanded seven values where five are unreachable.

### What failed

**Nobody will consume the engine.** Phase II classified thirty constituencies (fourteen in `01-`, sixteen in `02-`). `LIKELY_ENGINE_CONSUMER`: **two**, both in Go — River (172 importers) and gocron v2 (502 importers), 674 combined, each behind a two-method interface that any fifty-line matcher satisfies, and both in ecosystems where the same capability is sold as a paid tier (River Pro, JobRunr Pro, Oban Pro). `CORPUS_ONLY` or `VOCABULARY_ONLY`: **thirteen** (eleven and two), including Kubernetes, Temporal, Spring, Quartz, Celery, Solid Queue and Oban. In JavaScript, Ruby and Elixir — the ecosystems with the largest install volume — there is **not one** likely engine consumer. `[INFER, from revealed preference]`

**The natural experiment has already been run four times.** `@rrulenet/rrule` is structurally the Occurframe engine hypothesis — a maintained engine behind the frozen incumbent's API, in the largest ecosystem, against `rrule` (no push since 2024-06-27, 211 open issues). It has **210 downloads/month against `rrule`'s 11,666,435: 0.0018%.** `[FACT]` `rrule-alt`: 0.013%. `rrule-rust` (faster, same API): 0.65%. `netresearch/go-cron` (a robfig fork with DST and panic fixes): 0.4% of the parent's stars. Four same-capability successors, three ecosystems, all under 0.7%. The one successor that reached 9.95% — `rrule-temporal` — did so by **changing the API and fixing packaging**, not by being more correct.

**And the study's best adoption datum was a self-citation.** Phase II's own red team verified that OCPS is published by `open-source-cron`, a three-member organisation whose members include the author of `croner` and `croner-rust` — two of the implementations OCPS grades. `[FACT]` The finding that "a zero-dependency library changed its semantics for a standard it does not control" is, on inspection, a maintainer conforming to a specification he co-publishes. This study did not see that from the inside on first pass. It is exactly the failure mode that shipping an engine alongside a conformance corpus would create for Occurframe, and it is the single most decisive argument in this report.

**The cheapest evidence is the most damning.** The reference matcher that grades all 25 production engines — `oracle/reference/cron_ref.py` — is **432 lines** `[CODE]`, was **written in one session** `[INFER]`, and is already trusted enough to score the matrix. Nothing in the corpus shows what the remaining 13–19 months of engine work would buy that those 432 lines do not.

### The verdict in one paragraph

The category's defect is that **no one can check anyone's work.** Twenty-five production engines disagree on 85% of a corpus written in a single session; two of them hang; the only published conformance matrix is unmeasured; and a single Prefect pull request records a UI and a server executing the same string four times differently while showing the user a grammatical English sentence describing neither. The instrument that fixes this is a corpus, and the corpus's only asset is that its author has nothing to sell. Occurframe should build the instrument, keep it vendor-free, and offer its cron half into OCPS's unmeasured matrix rather than founding a rival. An engine can follow if — and only if — a named integrator asks for one.

---

## 2. Existing findings accepted as baseline

Carried forward from Phase I without re-litigation. Each was re-tested only where Phase II produced contradicting evidence.

| # | Baseline | Phase II status |
|---|---|---|
| 1 | Recurrence and execution are separate; Occurframe does not own workers, sleeping, persistence, queues, retries, distribution or orchestration | **Held.** Reinforced: the two `LIKELY_ENGINE_CONSUMER` seams are both single-method `Next()` interfaces. |
| 2 | Cron patterns (predicate) and RRULE (anchored generator) are distinct semantic objects | **Held.** The corpus keeps them as separate vector families with separate normative sources; no unification was attempted or needed. |
| 3 | Fixed-delay is a *cadence*, not a recurrence; excluded from v1 | **Held.** |
| 4 | Missed-run policy lives above `between(spec, start, end)` | **Held.** |
| 5 | Civil-time ambiguity is real and materially divergent | **Strengthened from six engines on one case to 25 builds on 184 vectors.** |
| 6 | Correctness alone does not displace incumbents | **Strengthened decisively.** Four natural experiments, all under 0.7%. |

### Phase I claims that Phase II corrected

Twenty corrections are catalogued in `13-bibliography-ii.md` §7. The five that change a conclusion:

1. **The Kubernetes 100-missed-schedule cap no longer wedges permanently.** It emits a `TooManyMissedTimes` warning and continues. Phase I described a permanent stop. `[CODE]`
2. **"No system carries both a computed key and a surrogate" is false.** Airflow 3's `task_instance` has `id: uuid7 PRIMARY KEY` **plus** `UniqueConstraint(dag_id, task_id, run_id, map_index)` — and the composite key was *demoted* from primary key by migration `d59cbbef95eb`. Dual identity is deployed practice, not an untested idea. `[CODE]`
3. **The spec fingerprint must not be part of the identity key.** Phase I doctrine position 18 put it there. If it is in the key, editing a schedule at 09:59 re-keys the 10:00 occurrence and it fires twice. Kubernetes, Solid Queue and Temporal all key on a stable series name; none hashes the spec. `[CODE]`
4. **`robfig/cron /v3` has 5,585 importers, not ~11,500.** `[FACT]`
5. **The divergence headline is 157/184, not 164/184** — the higher figure counted an `unsupported` cell as a distinct answer. Excluding the outlier engine that discards `TZID`, the floor is 120/184. Quote 157; the floor is 120. `[MEASURED]`

---

## 3. Findings that decided the verdict

### 3.1 Adoption (`01-`, `02-`)

| Classification | Constituencies |
|---|---|
| `LIKELY_ENGINE_CONSUMER` | River (172 Go importers), gocron v2 (502) |
| `POSSIBLE_ENGINE_CONSUMER` | BullMQ (only via `settings.repeatStrategy`, never as a dependency), kelektiv `cron`, pg-boss, Prefect (vendors croniter), Airflow (AIP-39 seam), asynq, Hangfire (source-drop only), db-scheduler |
| `VOCABULARY_ONLY` | Temporal (#8205 open since 2025-08-18, requesting exactly a gap/fold vocabulary), rrule.js dependents as a class |
| `CORPUS_ONLY` | Kubernetes, Spring, Quartz, Celery, django-celery-beat, go-quartz, Solid Queue, Oban, node-cron, croner, Graphile Worker |
| `UNLIKELY` | APScheduler, JobRunr, node-schedule, rrule.js |

Twenty-seven of the thirty constituencies appear above; the remaining three — Agenda, Inngest and Trigger.dev — are classified `UNKNOWN` in `01-` §8 and are omitted here.

**Kubernetes — the highest-value target — is structurally closed.** A replacement must be pure Go, original source rather than a fork, add zero transitive dependencies, carry a CNCF-allowlisted licence, obtain `dep-approvers` sign-off separately from SIG-Apps, and — decisively — be **bit-exact with `robfig/cron` v3.0.1 on every currently-valid `spec.schedule`**, because a compatible API change must not alter "interpretation of existing API types, fields, and values." Any dialect or DST change is therefore a KEP plus a feature gate. `[DOC]` The negative control is exact: a free drop-in robfig fork carrying DST and panic fixes has 61 stars against the parent's 14.1k.

**But the corpus reaches all of them**, because it requires nobody to take a dependency.

### 3.2 Prevalence (`03-`)

Original corpus: **9,485 schedule declarations** across **21 mechanisms** from **1,875 repositories and 6 live public calendar feeds**, built by blobless clone and sparse checkout across five documented sampling frames (5,082 repositories cloned).

| Bucket | Raw | Deduplicated |
|---|---|---|
| `PORTABLE` | 83.4% | 67.0% |
| `CIVIL_TIME_POLICY_RELEVANT` | 7.3% | 14.2% |
| `DEFINITELY_DIALECT_SENSITIVE` | 4.4% | 11.7% |
| `CALENDAR_EDGE_RELEVANT` | 4.7% | 6.8% |
| `INSUFFICIENT_CONTEXT` | 0.2% | 0.4% |
| **non-`PORTABLE`** | **16.4%** | **32.6%** (22.9% with boilerplate removed) |

**The headline is mostly a statement about GitHub Actions**, which is 41.9% of the corpus, is UTC-only by design, and is 96.9% portable. Where a scheduler exposes civil time the numbers invert: **Kubernetes CronJob 76.7% non-portable, sidekiq-cron 65.5%, crontab 49.2%, production calendar feeds 89.9%.** Two independently constructed sampling frames agree to within 0.1 percentage points, which is the study's main internal-validity check.

The high-value tail is genuinely thin — **54 literal month-end schedules (0.6%) and 7 DOM+DOW collisions (0.07%)** — but every one is a real semantic fork, and one of them is `apache/airflow`'s own `21 13 29 2 4`, which under Vixie means "Thursdays in February *or* 29 February" and under AND semantics means essentially never. And: **`spec.timeZone` is set in 6 of 279 Kubernetes CronJobs and resolves to a real zone in zero of them.** 81.3% of hour-pinned local-frame schedules fire between 00:00 and 04:00 — the worst window on earth.

`[INFER]` Prevalence supports the oracle and does not support the engine. A 16.4% raw rate is ample justification for an instrument that tells you which of your schedules are in that 16.4%; it is thin justification for asking 83.4% of users to change dependency.

### 3.3 The oracle (`06-`, `09-`, `10-`)

184 vectors — 65 `NORMATIVE`, 37 `DIALECT_DEPENDENT`, 33 `POLICY_DEPENDENT`, 24 `INVALID`, 21 `AMBIGUOUS_STANDARD`, 4 `KNOWN_DIVERGENCE` — across cron (98), RRULE (76) and tzdb provenance (10). Twenty-five engine builds in Python, JavaScript, Go, PHP and Ruby, each pinned to a recorded tzdb version, several run against two tzdb versions to isolate provenance effects. Five language runners, plus a complete minimal runner in 40 lines of code, proving the format's cross-language claim.

Three findings a reader should carry:

1. **The pathologies are the part that would justify an engine, and they are rare.** Two non-terminations, one non-monotonic iterator, 31 wrongly-accepted invalid inputs. Against that, `BYSETPOS`, `WKST` and every `BYMONTHDAY` edge are **unanimous across all five reachable RRULE engines**. The incumbents are not broadly broken; they are narrowly and specifically broken, in ways a corpus names precisely and a rewrite does not.
2. **tzdb provenance is a first-class axis.** Same library, same version, same machine, two `zoneinfo` paths → answers an hour apart. On one vector, a tzdb release removes the transition entirely, so the DST policy is not even reachable. A test suite that pins DST policy but not tzdb release passes or fails on when the container image was built.
3. **Three policy-axis values were discovered by running the corpus**, not by reading standards. The instrument produces findings.

### 3.4 Policy UX (`05-`)

Conditional requirement works and is exactly decidable — see §1. The cautionary datum is equally clear: **`whenever` 0.6.0 made `disambiguate=` non-optional on 2024-07-04 and reversed it 171 days later** in 0.6.16, because the required parameter "was a frequent source of irritation for users." `[DOC]` Phase II's conditional design is a genuine improvement on the design that failed, not a restatement of it — but it introduces a new failure mode (a stored schedule becoming invalid when a tzdb update makes it ambiguous; `Asia/Almaty` acquired a fold with **29 days' notice** in tzdb 2024a) that any implementation must handle explicitly.

### 3.5 Identity (`04-`)

Four notions of "the same occurrence"; three at the occurrence layer. The Phase I conflict was a use/mention error — `../evidence/11-execution-vs-recurrence.md` meant the value a unique constraint compares; `../evidence/14-occurrence-identity-vendor-models.md` meant the durable name a receipt points at. Both were right about their own object. Resolved in `14-doctrine-identity.md`.

### 3.6 Language (`07-`)

Rust wins on the doctrine's own criteria (weighted 8.03 against Python 5.73, TypeScript 5.55, Go 4.60 rejected), and the two reasons are real: only Rust can report its tzdb version *and* put a versioned tzdb in a browser at acceptable size, and abi3 has collapsed the packaging objection (polars now ships eight `cp310-abi3` wheels including `win_arm64`). But the decision inverts to TypeScript the moment the four provenance/WASM/FFI/reference criteria — 55% of the weight, all of which the *engine* thesis introduced — are relaxed.

**Under ORACLE ONLY the language decision is recorded and not exercised.** See §6.

---

## 4. Final opportunity score

Scored separately, because the two artefacts have different fates and a blended score would hide the finding.

| # | Dimension | Oracle | Engine | Note |
|---|---|---|---|---|
| 1 | Inherited market | **9** | **9** | Same category, same universality. |
| 2 | Pain severity | **6** | **6** | Real, production-affecting, rare-but-nasty. |
| 3 | Pain recurrence | **7** | **7** | Now partly measured: 16.4% raw, 76.7% of K8s CronJobs. |
| 4 | Fragmentation | **10** | **10** | 157/184 vectors divergent across 25 builds; the best-measured dimension in either phase. |
| 5 | Successor gap | **9** | **4** | No cross-language conformance corpus exists anywhere; the only published matrix is unmeasured. Against: two Go seams totalling 674 importers. |
| 6 | Migration friction | **9** | **3** | The corpus requires no dependency from anyone. The engine faces provable conversion impossibilities and a Kubernetes bar of bit-exactness. |
| 7 | Six-month feasibility | **9** | **1** | The corpus is substantially built: 184 vectors, 25 engines, 5 runners, a scoring matrix. The engine is 14–20 months single-language. |
| 8 | Correctness differentiation | **9** | **7** | The corpus *is* the differentiation and it already produced novel findings. |
| 9 | Multilingual consistency | **9** | **3** | Language-neutral by construction; five runners exist. The engine needs WASM plus a binding strategy. |
| 10 | Category recognition | **4** | **2** | Corpora accrue authority slowly; libical's 123-case file is consumed by nobody and OCPS has 9 stars. |
| | **Mean** | **8.1** | **5.2** | |

---

## 5. Decision gate

# GO — ORACLE ONLY

### Authorised for implementation

1. **The conformance corpus** — the 184 vectors, their format, classification taxonomy and versioning scheme, hardened and moved into a dedicated repository with a permissive licence.
2. **The differential runner and published results** — the five language runners, the minimal-runner proof, the scoring matrix, and a public differential report naming engines, versions and tzdb provenance.
3. **The reference matcher** — `cron_ref.py`, hardened and kept explicitly as a *scoring instrument*, not shipped or promoted as a scheduling library. It stays in Python: it exists, it grades 25 engines, and a readable reference reads as pseudocode.
4. **The policy and identity vocabulary as a written specification** — the civil-time policy axes and the dual-identity model, published so that Temporal (`VOCABULARY_ONLY`, with an open ticket) and others can adopt the names without adopting anything else.
5. **The dialect register** — 17 dialects across 21 versioned identifiers, with what a compatibility claim is permitted to say.

### Explicitly not authorised

- A production recurrence engine, in any language.
- Language bindings, WASM builds, or a browser preview module.
- Any package published as a scheduling dependency.

### The single gate that reopens the engine decision

> **A named maintainer of a named project commits, in writing and in public, to adopt an Occurframe engine at a specified integration seam.**

The realistic candidates, in order, are gocron v2 (`Cron{IsValid, Next}`), River (`PeriodicSchedule{Next}`), BullMQ (`settings.repeatStrategy`), and Airflow (`Timetable`). Until one of those exists, building an engine is building for a market too small and too Go-shaped to justify the cost — two `LIKELY` seams with 674 combined importers, against an engine the study prices at 14–20 months — and every hour spent on it is an hour not spent on the artefact that all thirty classified constituencies could use without taking a dependency.

This is a gate, not a refusal. The Rust decision, the architecture in `11-implementation-plan.md`, and the behavioural specification in `16-v1-specification.md` are all recorded so that the gate can be walked through without reopening research.

### Why not the other verdicts

- **STRONG GO** is refuted by `@rrulenet/rrule` at 0.0018% and by zero likely consumers in the three largest ecosystems.
- **GO — ORACLE + NARROW REFERENCE ENGINE** was the expected answer and is the one this study talked itself out of. The narrowest defensible engine is a reference implementation of the corpus — and that already exists in 432 lines. Anything larger is scope the evidence does not support, and shipping it costs the corpus its neutrality, which is its only asset.
- **HOLD** would be dishonest. The decisive questions were answerable from evidence and were answered.
- **NO-GO** is refuted by the corpus itself: 157 divergent vectors, two hangs, 31 unperformed MUST-rejections and an unmeasured industry conformance matrix constitute a real, cheap, unoccupied contribution.

---

## 6. What this freezes

| Decision | Answer | Where |
|---|---|---|
| What Occurframe is | A conformance oracle, a policy and identity vocabulary, a differential runner, and a dialect register | §5, `10-oracle-product.md` |
| What objects exist | Vector, dialect, policy profile, tzdb pin, conformance report; and in the specification: schedule, occurrence, slot, resolution, provenance | `16-v1-specification.md` |
| Which semantics are canonical | None are invented. `NORMATIVE` where a standard says so; `AMBIGUOUS_STANDARD` with admissible sets where it does not | `12-compatibility-doctrine.md` |
| Which policies are explicit | Conditionally mandatory: required iff provably reachable against a named tzdb; absent, never defaulted, where unreachable | `15-doctrine-civil-time.md` |
| How occurrence identity works | Dual — coarse `slot_id`, an admission guard on the instant, a host-minted `materialisation_id`. The spec fingerprint is evidence, never a key | `14-doctrine-identity.md` |
| First language | Reference matcher: Python (exercised now). Engine: Rust (recorded, gated) | §5, `07-first-language.md` |
| First API | The specification's operation set; the corpus runner contract | `17-conceptual-api-and-cli.md` |
| Which commands exist | `occurframe test`, `occurframe explain`, `occurframe classify`, `occurframe occurrences`. No general-purpose scheduling CLI | `17-conceptual-api-and-cli.md` |
| How errors behave | Three outcome classes — Rejection, Warning, Fact — with a stable code namespace | `16-v1-specification.md` §7 |
| What serialization looks like | The vector format for the corpus; the schedule envelope for the specification, with policies expanded and tzdb pinned | `16-v1-specification.md` §6 |
| What compatibility means | A claim naming corpus version, dialect, policy profile and tzdb. Never a bare "RFC 5545 compliant" | `12-compatibility-doctrine.md` |
| What the oracle contains | 184 vectors in six classifications across three families, with 2,432 frozen incumbent observations | `06-conformance-oracle.md` |
| What v1 refuses | The non-goals list — no engine, no bindings, no scheduling dependency | `16-v1-specification.md` §9 |

---

## 7. The next task

The implementation task is authorable now, without further product decisions:

> **Task: Implement Occurframe v1 Foundation**
> Split the corpus at `phase-2/oracle/` into the `occurframe/corpus` repository under a permissive licence. Harden the vector format and the runner contract to `docs/FORMAT.md` and `docs/RUNNER-CONTRACT.md`. Harden `reference/cron_ref.py` as the scoring instrument. Re-run the five language runners and reproduce the matrix byte-identically as a regression gate. Expand coverage in the families the matrix shows as thin. Publish the differential report. Offer the 98 cron and 10 tzdb-provenance vectors into OCPS's conformance matrix as measured cells.

Milestones, entry and exit criteria, CI shape and the multi-tzdb test matrix are specified in `11-implementation-plan.md`; the milestones that concern the engine (M0 WASM spike onward) are deferred behind the §5 gate.

---

## 8. Remaining non-blocking questions

None of these blocks implementation. Each is worth answering during it.

1. **Will OCPS accept measured cells?** The single most concrete adoption path, and untested. It is also complicated by OCPS sharing an organisation and an author with `croner`, one of the engines it grades — so contributing measurement improves the artefact but does not dissolve the neutrality problem, it relocates it.
2. **Does a public differential report change any engine's behaviour?** The clean test: file the two non-termination bugs and the APScheduler fixed point, and observe. If maintainers fix what the corpus finds, the corpus has authority. If they do not, it has none, and that is worth knowing before expanding it.
3. **What is the RRULE corpus's home?** OCPS is cron-only, and the hardest findings are on the RRULE side. CalConnect is the obvious venue and was not approached.
4. **Is the 16.4% prevalence figure stable outside GitHub?** The corpus is GitHub-shaped. An enterprise crontab and Kubernetes scan would be the strongest possible corroboration and the natural first application of the tooling.
5. **Would any of the eleven `CORPUS_ONLY` constituencies run the corpus in their own CI?** That is the corpus's actual adoption metric, and no one has been asked.
6. **What happens to a stored schedule when a tzdb update makes it ambiguous?** The specification defines `revalidate`; nothing has implemented it, and the `Asia/Almaty` 29-days-notice case shows the window is real.
7. **Quartz and Spring were never measured** — no JVM engine was reachable in the test environment. They are the register's largest hole and two of the most-deployed dialects.

---

## 9. Method and limits

Ten parallel investigations against primary sources, with two original empirical builds. WebSearch and WebFetch were available; GitHub's REST API worked unauthenticated but code search did not; **npm, PyPI and crates.io installs were blocked (HTTP 403)**, so all 25 engine builds were vendored from GitHub source and the schedule corpus was built by blobless clone plus sparse checkout rather than code search. No JVM or .NET engine was reachable, which is a real coverage hole.

**No maintainer was contacted.** Every adoption classification is reconstructed revealed preference from issues, pull requests, dependency policies, KEPs, vendor directories and changelogs, and is labelled `[INFER]` accordingly. The brief invited direct contact where legitimately available; none was, and nothing was fabricated to fill the gap. This is the single largest limitation of the adoption analysis, and it cuts both ways: the classifications may be too pessimistic as easily as too optimistic.

Citation hazards found while compiling `13-bibliography-ii.md` are listed there and include an irreconcilable `cron-parser` download figure across three readings, and ~80 GitHub links mechanically reconstructed from shorthand references.

---

## 10. Document map

| # | Deliverable | File |
|---|---|---|
| 1 | Executive verdict | this document §1 |
| 2 | Baseline accepted | this document §2 |
| 3 | Maintainer/adoption analysis | `01-maintainers-js-ruby-elixir.md`, `02-maintainers-py-go-jvm-k8s.md` |
| 4 | Dependency-acceptance matrix | `02-` §8 and this document §3.1 |
| 5 | Schedule-corpus methodology | `03-schedule-prevalence.md` §1–3 |
| 6 | Prevalence results | `03-schedule-prevalence.md` §4–7 |
| 7 | Occurrence-identity comparison | `04-occurrence-identity.md` |
| 8 | Final identity doctrine | `14-doctrine-identity.md` |
| 9 | API usability analysis | `05-policy-ux.md` |
| 10 | Final civil-time policy doctrine | `15-doctrine-civil-time.md` |
| 11 | Conformance-corpus specification | `06-conformance-oracle.md`, `10-oracle-product.md` |
| 12 | Incumbent differential matrix | `09-differential-matrix.md` |
| 13 | Oracle product definition | `10-oracle-product.md` |
| 14 | Reference-engine decision | this document §5 |
| 15 | First-language decision | `07-first-language.md`, this document §5–6 |
| 16 | v1 Behavioral Specification | `16-v1-specification.md` |
| 17 | Final conceptual API | `17-conceptual-api-and-cli.md` §1–5 |
| 18 | CLI specification | `17-conceptual-api-and-cli.md` §6 |
| 19 | Serialization / versioning | `16-v1-specification.md` §6 |
| 20 | Error and diagnostics model | `16-v1-specification.md` §7 |
| 21 | Compatibility / import doctrine | `12-compatibility-doctrine.md` |
| 22 | Determinism / provenance doctrine | `16-v1-specification.md` §8 |
| 23 | Explicit v1 non-goals | `16-v1-specification.md` §9 |
| 24 | Implementation architecture | `11-implementation-plan.md` §1–2 |
| 25 | Repository / package structure | `11-implementation-plan.md` §3 |
| 26 | Implementation sequence | `11-implementation-plan.md` §4 |
| 27 | Acceptance / certification strategy | `11-implementation-plan.md` §5 |
| 28 | Strongest NO-GO case | `08-falsification-ii.md` |
| 29 | Final opportunity score | this document §4 |
| 30 | Final decision gate | this document §5 |
| 31 | Remaining non-blocking questions | this document §8 |
| 32 | Bibliography | `13-bibliography-ii.md` |
| — | Built artefacts | `oracle/`, `schedule-corpus/` |
