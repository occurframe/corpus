# Known Contradictions

## Reserved CLI versus the no-engine product verdict — RESOLVED

**Resolved by [ERRATA-001](../spec/ERRATA.md#errata-001--oracle-only-cli-surface).**

Research II reserved exactly `occurframe test`, `occurframe explain`, `occurframe classify`, and `occurframe occurrences` (with an `oframe` executable alias), while its own decision gate explicitly did not authorise a production recurrence engine in any language. `explain`, `classify` and especially `occurrences` each require Occurframe to compute occurrences rather than observe them, so three of the four commands could not be built without violating the verdict they were recorded beside.

ERRATA-001 applies the precedence rule that a final verdict governs lower-level interface text derived from it. Occurframe v1 ships one semantic command, `test`, which is satisfied by measuring an external engine. The other three are deferred behind the unchanged engine gate, with their frozen semantics preserved verbatim in `spec/CLI.md` §6.7. They were not redefined into corpus or report commands to preserve their names, and no evaluator was built, embedded, delegated to or renamed.

The specification API in `spec/CLI.md` §§1–5 is unchanged and remains specification-only: what a conforming implementation exposes, not a library Occurframe v1 ships.

## Historical RC1 error status

RC1 used one `error` status for both deliberate rejection and unexpected exceptions. Protocol v2 separates `rejection` from `engine_error`, but migration must not guess which old cells belong to which category. `migration-report.json` enumerates those ambiguous legacy cells.

