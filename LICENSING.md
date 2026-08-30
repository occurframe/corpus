# Licensing

This repository publishes material under more than one licence. The split
follows Research II §7.2, which recommends `CC0-1.0` for the corpus data and
documentation, and `Apache-2.0` for reference and tooling code.

| Path | Licence | Full text |
| --- | --- | --- |
| `vectors/` | CC0-1.0 | `LICENSE-CC0` |
| `schemas/` | CC0-1.0 | `LICENSE-CC0` |
| `registry/` | CC0-1.0 | `LICENSE-CC0` |
| `spec/` | CC0-1.0 | `LICENSE-CC0` |
| `docs/` | CC0-1.0 | `LICENSE-CC0` |
| `README.md`, `CHANGELOG.md`, `release-notes/` | CC0-1.0 | `LICENSE-CC0` |
| `reference/` | Apache-2.0 | `LICENSE-APACHE` |
| `tests/` | Apache-2.0 | `LICENSE-APACHE` |
| `legacy/` | see below | — |

## Why the corpus data is CC0-1.0

A conformance corpus is only useful if anyone can use it without asking: engine
maintainers embedding vectors in their own test suites, standards bodies quoting
them, downstream distributions repackaging them. A public-domain dedication
removes the attribution and compatibility frictions that would otherwise make a
maintainer hesitate to vendor a vector into their repository.

CC0-1.0 covers the authored semantic data: the vectors, the registries of
dialects, semantic axes, sources and stable vector IDs, the wire schemas, the
specification prose and the documentation.

## Why the reference matcher is Apache-2.0

`reference/cron_ref.py` is an independent Python reference implementation, and
`tests/reference/` exercises it. That is code, not data, so it carries a code
licence with an explicit patent grant and warranty disclaimer.

Note the consequence: the reference matcher is **not** public domain, and a
statement that "the corpus is CC0" is imprecise if it is taken to cover
`reference/`. The corpus *semantic data* is CC0-1.0; the reference code is
Apache-2.0.

## `legacy/` — unresolved, and deliberately not asserted

`legacy/phase2-rc1/` preserves Phase II RC1 as immutable historical evidence. It
is a mixture: Occurframe's own research prose and build tooling, and material
that is derived from or describes third-party engines — provenance records, raw
observations produced by running other projects' software, and conformance
matrices about them.

**No blanket licence is asserted over `legacy/`.** Dedicating that whole tree to
the public domain would purport to license material whose upstream rights are not
Occurframe's to give away, and pretending otherwise would be worse than leaving
it open. The tree is retained for reproducibility and audit of the RC1 → RC2
migration.

This is a genuine open question for the repository owner: the `legacy/` tree
needs a per-directory determination — Occurframe-authored prose and build scripts
can take one of the licences above, while third-party-derived provenance and
observation material needs its upstream terms recorded rather than replaced. That
determination has not been made and is not made here.

## Trademark

Nothing in these licences grants rights to the Occurframe name or to any
third-party engine name appearing in vectors, registries, provenance records or
evidence. Engine names are used to identify the implementations that were
measured.
