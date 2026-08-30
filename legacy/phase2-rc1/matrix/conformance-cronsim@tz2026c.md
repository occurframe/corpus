# Conformance report — `cronsim@tz2026c`

- engine: **cronsim** 2.7 (git cuu508/cronsim @fd2e617, tag 2.7)
- runtime: python 3.11.15
- tzdb: **2026c** (from PyPI tzdata 2026.3)
- runner: run_python.py
- corpus: 1.0.0-rc1

**Scored 107 of 184 vectors; 101 pass (94.4%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `skip` | 15 |
| `reject` | 13 |
| `or/vixie` | 6 |
| `reject-reversed` | 5 |
| `rejected` | 5 |
| `vixie-artefact` | 4 |
| `next_valid` | 4 |
| `vixie-both` | 3 |
| `tzdb>=2026c` | 3 |
| `supported` | 2 |
| `seconds-leading` | 2 |
| `error-at-parse` | 2 |
| `tzdb>=2026b` | 2 |
| `exclusive` | 1 |
| `truncate-to-minute` | 1 |
| `exact` | 1 |
| `fold_both` | 1 |
| `last-day-of-week-of-month` | 1 |
| `seconds` | 1 |
| `three-letter-only` | 1 |
| `accept` | 1 |
| `start-at` | 1 |
| `collapse-to-first` | 1 |
| `links-present` | 1 |

## FAIL (6)

- `CRON-FIELDS-008` Macro @daily
  - engine said: `CronSimError: Wrong number of fields`
  - corpus expects: `2026-01-02T00:00:00, 2026-01-03T00:00:00, 2026-01-04T00:00:00, 2026-01-05T00:00:00`
- `CRON-FIELDS-009` Macro @yearly
  - engine said: `CronSimError: Wrong number of fields`
  - corpus expects: `2027-01-01T00:00:00, 2028-01-01T00:00:00, 2029-01-01T00:00:00, 2030-01-01T00:00:00`
- `CRON-FIELDS-010` Macro @monthly
  - engine said: `CronSimError: Wrong number of fields`
  - corpus expects: `2026-02-01T00:00:00, 2026-03-01T00:00:00, 2026-04-01T00:00:00, 2026-05-01T00:00:00`
- `CRON-FIELDS-011` Macro @weekly
  - engine said: `CronSimError: Wrong number of fields`
  - corpus expects: `2026-01-04T00:00:00, 2026-01-11T00:00:00, 2026-01-18T00:00:00, 2026-01-25T00:00:00`
- `CRON-FIELDS-012` Macro @hourly
  - engine said: `CronSimError: Wrong number of fields`
  - corpus expects: `2026-01-01T01:00:00, 2026-01-01T02:00:00, 2026-01-01T03:00:00, 2026-01-01T04:00:00`
- `CRON-STEP-003` 0/1 vs * — Quartz idiom in the seconds field
  - engine gave: `2026-01-01T00:00:01, 2026-01-01T00:00:02, 2026-01-01T00:00:03`

