# Occurframe Corpus 1.0.0-rc3

This repository is the versioned, language-neutral authority for Occurframe recurring-time conformance. It contains authored specifications, Draft 2020-12 wire schemas, registries, one-JSON-file-per-vector canonical sources, an independent Python cron reference matcher, and immutable Phase II RC1 evidence.

The current corpus version is **`1.0.0-rc3`**. It is a release candidate, not stable `1.0.0`.

Occurframe is an executable conformance oracle, not a recurrence engine or scheduler. Generated JSONL packs, observations, matrices, reports, and incumbent behavior never define normative expectations.

Read [Authority](docs/AUTHORITY.md), [Format](docs/FORMAT.md), [Runner Protocol](docs/RUNNER-PROTOCOL.md), [Versioning](docs/VERSIONING.md), and [Contributing Vectors](docs/CONTRIBUTING-VECTORS.md) before changing authored data.

The canonical source hierarchy is:

```text
spec/        authored specification
schemas/     authoritative machine-readable wire contracts
registry/    authored registries
vectors/     canonical authored vectors
reference/   independent Python reference matcher
legacy/      immutable Phase II RC1 evidence
```

The corpus identity a consumer pins is:

```text
version:          1.0.0-rc3
canonical digest: c0a9cf0587c02ce5022cbb94d060e14d5b9d6f99c3210e512965f35062c4dfe0
vectors:          184
```

That digest is derived from the authored vectors alone, so repository metadata
never changes it.

The behavioural specification versions independently of the corpus. It is
currently **`1.0.0-rc1`**, declared in [`spec/specification.json`](spec/specification.json),
and its corrections are recorded in [Errata](spec/ERRATA.md). Under
[ERRATA-001](spec/ERRATA.md#errata-001--oracle-only-cli-surface), Occurframe v1
ships one semantic command, `occurframe test`; `explain`, `classify` and
`occurrences` are deferred behind the engine gate because each requires a
recurrence evaluator that the ORACLE ONLY verdict does not authorise.

See [Changelog](CHANGELOG.md) and [Release notes](release-notes/1.0.0-rc3.md).

## Licensing

The authored semantic data — `vectors/`, `schemas/`, `registry/`, `spec/`,
`docs/` — is dedicated to the public domain under CC0-1.0, so engine maintainers
can vendor vectors into their own test suites without friction. The independent
reference matcher in `reference/` and its tests are Apache-2.0. No blanket
licence is asserted over `legacy/`, which mixes Occurframe-authored research with
third-party-derived evidence. See [Licensing](LICENSING.md).
