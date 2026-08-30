# Conformance report — `cronstrue@tzle2026a`

- engine: **cronstrue** 3.24.0 (git bradymholt/cRonstrue @b62884a 2026-08-21)
- runtime: bun 1.3.13
- tzdb: **le2026a** (from runtime ICU (fingerprint le2026a))
- runner: run_js.ts
- corpus: 1.0.0-rc1

**Scored 19 of 184 vectors; 15 pass (78.9%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `accepted` | 88 |
| `reject` | 2 |
| `rejected` | 1 |
| `three-letter-only` | 1 |

## FAIL (1)

- `CRON-INV-012` Whitespace-tolerant parsing (tabs and multiple spaces)
  - engine said: `String: Error: Expression has only 4 parts. At least 5 parts are required.`
  - corpus expects: `2026-01-01T12:00:00, 2026-01-02T12:00:00, 2026-01-03T12:00:00`

## REJECT-BAD (3)

- `CRON-INV-010` Truncated range
  - engine gave: `DESCRIPTION:At 12:00 AM, between day 1 and  of the month`
- `CRON-STEP-005` Step of zero
  - engine gave: `DESCRIPTION:Every 0 minutes`
- `CRON-STEP-011` Negative step
  - engine gave: `DESCRIPTION:Every -5 minutes`

