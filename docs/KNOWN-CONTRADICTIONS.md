# Known Contradictions

## Reserved CLI versus the no-engine product verdict

Research II reserves exactly `occurframe test`, `occurframe explain`, `occurframe classify`, and `occurframe occurrences` (with an `oframe` executable alias). The final product verdict simultaneously prohibits a production recurrence engine. `explain`, `classify`, and especially `occurrences` appear to require evaluator behavior.

This milestone records but does not resolve that contradiction. It implements no public CLI and no evaluator. A later doctrine decision must define whether those commands consume external observations, operate only on corpus knowledge, delegate to declared engines, or reopen the engine gate.

## Historical RC1 error status

RC1 used one `error` status for both deliberate rejection and unexpected exceptions. Protocol v2 separates `rejection` from `engine_error`, but migration must not guess which old cells belong to which category. `migration-report.json` enumerates those ambiguous legacy cells.

