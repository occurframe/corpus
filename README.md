# Occurframe Corpus 1.0.0-rc2

This repository is the versioned, language-neutral authority for Occurframe recurring-time conformance. It contains authored specifications, Draft 2020-12 wire schemas, registries, one-JSON-file-per-vector canonical sources, an independent Python cron reference matcher, and immutable Phase II RC1 evidence.

The current corpus version is **`1.0.0-rc2`**. It is a release candidate, not stable `1.0.0`.

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

