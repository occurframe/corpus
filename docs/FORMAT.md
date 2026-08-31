# Corpus Format

Canonical vectors are individual UTF-8 JSON files at `vectors/<family>/<VECTOR-ID>.json`, validated by `schemas/vector.schema.json`. `corpus_version` is `1.0.0-rc3`; `schema_version` is `1.0.0`.

Each vector preserves stable ID, family, title, kind, operation, input, context, classification, semantic-axis references, normative evidence references, expectation, rationale, tags, lifecycle, and optional supersession. The six classifications and six expectation modes are independent; tooling must never infer one from the other.

Occurrence arrays are ordered normative or admissible sequences. Never sort or deduplicate them. An empty array is a successful empty occurrence result. In an expectation case, `occurrences: null` means deliberate rejection.

Reusable evidence title and URL live in `registry/sources.json`; vector-local quotations and editorial notes remain attached to `normative_evidence`. Every axis and source reference must resolve. Versioned cron dialect IDs resolve through `registry/dialects.json`.

Generated JSONL is a distribution format only. Deterministic packing sorts records by vector ID, uses stable object-key ordering and LF endings, and leaves every nested occurrence array untouched.

Timezone provenance is structured, never a fuzzy version string:

- `release_kind: exact` carries one exact release such as `2026a`;
- `release_kind: bounded` carries an inclusive minimum, maximum, or both, and may carry fingerprint evidence;
- `release_kind: unknown` records an unknown system database without pretending it is exact.

Thus exact `2026a`, `<=2026a`, `>=2026c`, unknown system zoneinfo, ICU fingerprinted to a range, and a package-provided exact release remain mechanically distinct.
