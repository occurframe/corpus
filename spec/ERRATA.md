# Specification errata

Corrections to the frozen specification, recorded rather than applied silently.
Each entry states what the original text said, what it conflicts with, the
precedence rule used, and what the resolved contract is. Superseded text is
never deleted: the Research II sources remain verbatim under
`legacy/phase2-rc1/research/`, and the affected specification section carries a
pointer here.

An erratum resolves a contradiction. It does not reopen a decision.

---

## ERRATA-001 — ORACLE ONLY CLI surface

**Status:** resolved · **Applies to:** `spec/CLI.md` §6, `RESEARCH-II.md` §6 command
table · **Specification version:** `1.0.0-rc1`

### What Research II froze

`RESEARCH-II.md` §6 records, under "Which commands exist":

> `occurframe test`, `occurframe explain`, `occurframe classify`,
> `occurframe occurrences`. No general-purpose scheduling CLI

`spec/CLI.md` §6.1 states the same decision as **"Ship a CLI. Ship four
commands."**, and §§6.3–6.6 freeze each command's semantics.

### What it conflicts with

The same document's executive verdict and decision gate:

> **GO — ORACLE ONLY** … Build the conformance oracle. **Do not build the
> reference engine in v1.**

and, under "Explicitly not authorised":

> A production recurrence engine, in any language.

The reference matcher is admitted only as a scoring instrument — "hardened and
kept explicitly as a *scoring instrument*, not shipped or promoted as a
scheduling library" (§5.3) — and `spec/COMPATIBILITY.md` records that it "lives
outside `runners/` so it can never be scored as an engine."

Three of the four frozen commands cannot be implemented without the thing §5
prohibits.

### Why `explain`, `classify` and `occurrences` require recurrence evaluation

Each is quoted from its own frozen section.

- **`occurrences`** (§6.6) "Emits occurrences as JSON objects … carrying instant,
  slot, and full resolution", and is justified as "the corpus's own generation
  path exposed … the same code path the conformance report scores." Under ORACLE
  ONLY there is no such path: the conformance report *observes external engines*
  and scores their answers against authored expectations. Occurframe computes no
  occurrence. Shipping this command means shipping a generator.
- **`classify`** (§6.5) reports "every dialect under which it parses, the
  occurrence sequence each produces over the window, and the first instant at
  which any two diverge." That is an evaluator run once per dialect, plus a
  parser for each of the register's 21 versioned dialect identifiers. It is the
  heaviest evaluation requirement of the three, not the lightest.
- **`explain`** (§6.4) emits "what the schedule denotes, which policy axes are
  reachable and which values apply, the anchor's synchronisation status … and —
  when `--from`/`--limit` are given — the next N occurrences with their full
  resolution records." Determining what a schedule denotes, and which policy axes
  are *reachable*, is evaluation against a named tzdb; the occurrence listing is
  generation outright. §5's `explain(sched) -> Explanation` is an operation of
  the specification API, which the same document says "Occurframe v1 does not
  ship … as a library."

None of the three can be honoured by observation alone. Each would require
Occurframe to own an answer rather than to measure one.

### Why `test` does not

`test` (§6.3) "Runs the conformance corpus against an engine adapter and emits a
conformance report." Its inputs are authored vectors and an external adapter's
answers; its output is a verdict produced by comparing the two. Every
recurrence computation happens inside the engine under test, in another process,
behind the runner protocol. `test` is oracle-native: it is the only one of the
four whose definition is satisfied by measuring.

### Precedence rule applied

> A final verdict and its explicit prohibition take precedence over lower-level
> interface text that cannot be implemented without violating that prohibition.

`RESEARCH-II.md` §5 is a decision gate with an explicit "not authorised" list.
The §6 command table and `spec/CLI.md` §6.1 are consequences recorded alongside
it. Where a consequence contradicts the decision it was derived from, the
decision governs and the consequence is corrected.

The alternative — preserving four command names by giving three of them new
meanings, or by wiring them to the reference matcher, one incumbent engine, or an
arbitrary adapter — was rejected. It would ship an Occurframe-owned answer under
a name the specification defines as a computed one, which is precisely the
neutrality the verdict protects: "shipping it costs the corpus its neutrality,
which is its only asset."

`spec/CLI.md` already anticipated this, in its own contradictions list: "A frozen
API for a library that v1 does not ship is an odd artefact."

### Resolved v1 command surface

Occurframe v1 ships exactly one semantic command, under both executable aliases:

```text
occurframe test
oframe test
```

`explain`, `classify` and `occurrences` are **deferred, engine-gated commands**.
They are not implemented, not shipped, not advertised in default help, and not
part of the v1 command contract. Their Research II semantics are preserved
verbatim in `spec/CLI.md` §6.7 and in the legacy sources, unchanged, so that the
gate can be walked without reopening research.

Active exit codes in v1 are those `test` can produce: `0`, `1`, `3`, `4`. Codes
`2` (Rejection) and `5` (Truncation) remain frozen in the specification and
inactive in the shipped product — both presuppose evaluating a caller's schedule.
They are not renumbered and not reused.

The specification API (`spec/CLI.md` §§1–5) is unchanged and remains what it
always was: a behavioural and conformance specification describing what a
conforming implementation exposes, not a library Occurframe v1 ships. The three
categories are kept distinct throughout the documentation — **specified
operation**, **implemented oracle tooling**, **future engine/API
implementation**.

### What would reopen this

The deferred commands become reconsiderable only when the engine gate in
`RESEARCH-II.md` §5 is satisfied:

> A named maintainer of a named project commits, in writing and in public, to
> adopt an Occurframe engine at a specified integration seam.

The gate is unchanged and remains closed by this erratum. Satisfying it does not
by itself ship the commands; it permits their recorded semantics to be
reconsidered. Nothing here weakens, narrows or restates the gate.

### What this erratum does not change

Corpus semantics, vector expectations, the canonical corpus digest,
classification taxonomy, civil-time doctrine, occurrence identity, dialect
semantics, the runner protocol, scoring, the recurrence/execution boundary, and
the engine reopening gate are all untouched. This erratum concerns the shipped
command surface and nothing else.
