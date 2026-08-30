# Versioning

The current release candidate is `1.0.0-rc2`. No stable `1.0.0` is published by this milestone.

Four identities version independently and are never conflated:

| Identity | Current | Owned by |
| --- | --- | --- |
| Behavioural specification | `1.0.0-rc1` | `spec/specification.json` |
| Corpus | `1.0.0-rc2` | this repository's vectors and registries |
| Runner protocol | `2.0` | `schemas/runner-protocol-v2.schema.json` |
| Occurframe tooling | separate | `occurframe/occurframe` |

The specification is the semantics an implementation is measured against; the
corpus is its executable form. They move for different reasons — a corrected
expectation changes the corpus, a corrected interface contract changes the
specification — so one number covering both would be a claim neither could keep.
Specification corrections are recorded as numbered errata in
[Errata](../spec/ERRATA.md) rather than applied silently; superseded text is
preserved.

Vector IDs are permanent and never reused. A correction that preserves the input may correct an expectation in place with reviewed evidence. A change to the input retires the old ID and records its successor; retired IDs remain in `registry/vector-ids.json` forever.

Dialect IDs are permanent and versioned. Configuration variants use separate IDs whenever the configuration changes semantic claims. New dialect entries may be added in a corpus minor version. Renaming or removal requires a corpus major version. Documentation/implementation disagreement is recorded with `evidence_grade: documentation_conflict`, not hidden.

Schema `$id` values are stable. Incompatible wire changes require a new schema identity and appropriate corpus major version. Runner protocol changes use their own protocol version.

Compatibility claims must name at least corpus version, dialect or RRULE profile, semantic policy claims, tzdb provenance, engine identity/provenance, and runtime. “Cron-compatible” is not a versioned identity.

