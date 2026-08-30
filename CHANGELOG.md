# Changelog

All notable changes to the Occurframe corpus are recorded here. The corpus is
versioned independently of the Occurframe tooling and of the runner protocol.

Vector IDs are permanent and never reused. A correction that preserves the input
may correct an expectation in place with reviewed evidence; a change to the input
retires the old ID and records its successor. Retired IDs remain in
`registry/vector-ids.json` forever. See [Versioning](docs/VERSIONING.md).

## 1.0.0-rc2 — unreleased prerelease

The second release candidate. This is **not** stable `1.0.0`, and its
expectations may still be corrected with reviewed evidence before one exists.

```text
canonical digest: 4804772d20fb36c7329b2c5f2f28e264d9bc00b11e407e76d9836fc38cd80470
vectors:          184
```

### Added

- Authored, one-file-per-vector canonical sources for 184 vectors across
  fourteen families: `cron.anchoring`, `cron.day-fields`, `cron.dow-numbering`,
  `cron.dst`, `cron.extensions`, `cron.field-count`, `cron.invalid`,
  `cron.names`, `cron.steps`, `rrule.by`, `rrule.core`, `rrule.dst`,
  `rrule.sets` and `tzdb.provenance`.
- Draft 2020-12 wire schemas for vectors, normalized observations, conformance
  results, the release manifest, the four registries, and runner protocol v2.
- Authored registries for dialects, semantic axes, normative sources and stable
  vector IDs, with every vector reference resolved at validation time.
- Six-value vector classification — `NORMATIVE`, `POLICY_DEPENDENT`,
  `DIALECT_DEPENDENT`, `AMBIGUOUS_STANDARD`, `KNOWN_DIVERGENCE`, `INVALID` —
  independent of expectation mode.
- Expectation modes `single`, `reject`, `per_policy`, `per_dialect`,
  `admissible` and `open`, so that a case with several legitimate answers is
  recorded as such instead of one being declared the winner.
- Timezone-database provenance as a first-class, mechanically distinct concept:
  exact release, bounded range, or genuinely unknown.
- `reference/cron_ref.py`, an independent Python reference matcher, with its own
  test suite. It is a reference, not an authority: it never defines an
  expectation.
- `legacy/phase2-rc1/`, the immutable Phase II RC1 evidence, retained so the
  RC1 → RC2 migration can be audited. Historical evidence, not current
  authority.

### Changed from 1.0.0-rc1

- Runner protocol v2 replaces RC1's overloaded `error` outcome with five
  distinct terminal outcomes, so a deliberate rejection is no longer
  indistinguishable from an unexpected engine failure. RC1 `error` cells are
  never guessed into a v2 outcome; every ambiguous legacy cell is listed
  explicitly in `migration-report.json`.
- Semantic profile claims and dialect IDs became declared, validated identity
  rather than description, so a `per_policy` or `per_dialect` expectation is
  selected by what an engine declares about itself.

### Publication metadata (this change only)

- `LICENSE-CC0`, `LICENSE-APACHE` and `LICENSING.md`, recording the licence split
  the repository already intended: CC0-1.0 for the authored semantic data and
  documentation, Apache-2.0 for the reference matcher and its tests, and no
  blanket assertion over `legacy/`.
- This changelog and `release-notes/1.0.0-rc2.md`.

No vector, expectation, schema semantics, registry semantics or canonical corpus
digest changed. The canonical digest is derived from the authored vectors alone,
so adding repository metadata cannot alter it, and CI verifies this.

## 1.0.0-rc1 — historical

Preserved under `legacy/phase2-rc1/` as immutable evidence rather than as a
released artifact. Not current authority.
