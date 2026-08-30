# Conformance report — `croniter[day_or=False]@tz2026a`

- engine: **croniter[day_or=False]** 6.3.0.dev0 (git kiorky/croniter @3dd4d14 2026-08-14)
- runtime: python 3.11.15
- tzdb: **2026a** (from /usr/share/zoneinfo)
- runner: run_python.py
- corpus: 1.0.0-rc1

**Scored 107 of 184 vectors; 103 pass (96.3%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `skip` | 12 |
| `reject` | 12 |
| `and` | 6 |
| `wrap-modulo` | 5 |
| `next_valid` | 4 |
| `fold_both` | 4 |
| `vixie-both` | 3 |
| `supported` | 3 |
| `tzdb<=2026b` | 3 |
| `vixie-artefact` | 2 |
| `or-set-semantics` | 2 |
| `error-at-parse` | 2 |
| `exclusive` | 1 |
| `truncate-to-minute` | 1 |
| `last-day-of-week-of-month` | 1 |
| `seconds-leading` | 1 |
| `three-letter-only` | 1 |
| `accept` | 1 |
| `start-at` | 1 |
| `collapse-to-first` | 1 |
| `tzdb<=2026a` | 1 |
| `tzdb<=2026a/next-valid` | 1 |
| `links-absent` | 1 |

## FAIL (4)

- `CRON-ANCH-003` Sub-minute start instant, seconds-granularity expression
  - engine gave: `2026-01-01T12:30:00, 2026-01-01T12:30:01, 2026-01-01T12:30:02`
- `CRON-FIELDS-002` Six-field form: is the extra field seconds or year?
  - engine gave: `2026-01-10T15:00:00, 2026-01-10T15:00:01, 2026-01-10T15:00:02, 2026-01-10T15:00:03`
- `CRON-FIELDS-004` Seconds granularity: every 15 seconds
  - engine gave: `2026-01-01T00:00:01, 2026-01-01T00:00:02, 2026-01-01T00:00:03, 2026-01-01T00:00:04`
- `CRON-STEP-003` 0/1 vs * — Quartz idiom in the seconds field
  - engine gave: `2026-01-01T00:00:01, 2026-01-01T00:00:02, 2026-01-01T00:00:03`

