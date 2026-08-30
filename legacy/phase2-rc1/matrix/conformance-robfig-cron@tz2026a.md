# Conformance report — `robfig-cron@tz2026a`

- engine: **robfig-cron** v3.0.1 (git robfig/cron @bc59245 2021-01-06)
- runtime: go1.24.7
- tzdb: **2026a** (from /usr/share/zoneinfo)
- runner: runners/go
- corpus: 1.0.0-rc1

**Scored 107 of 184 vectors; 104 pass (97.2%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `reject` | 18 |
| `skip` | 15 |
| `or/vixie` | 6 |
| `reject-reversed` | 5 |
| `fold_both` | 4 |
| `tzdb<=2026b` | 3 |
| `vixie-artefact` | 2 |
| `monday-zero` | 2 |
| `empty` | 2 |
| `exclusive` | 1 |
| `truncate-to-minute` | 1 |
| `rejected` | 1 |
| `or-set-semantics` | 1 |
| `vixie-both` | 1 |
| `last-day-of-week-of-month` | 1 |
| `seconds-leading` | 1 |
| `three-letter-only` | 1 |
| `accept` | 1 |
| `start-at` | 1 |
| `collapse-to-first` | 1 |
| `tzdb<=2026a` | 1 |
| `tzdb<=2026a/gap-skip` | 1 |
| `links-present` | 1 |

## FAIL (1)

- `CRON-ANCH-003` Sub-minute start instant, seconds-granularity expression
  - engine said: `expected exactly 5 fields, found 6: [30 * * * * *]`

## HANG (1)

- `CRON-DST-007` A whole calendar day that does not exist (Pacific/Apia 2011-12-30)
  - engine said: `__TIMEOUT__ exceeded 8s`

## NOVEL (1)

- `CRON-DAYF-013` The '*/100,1-7 * MON' first-Monday idiom weaponising the artefact
  - engine gave: `2026-01-02T00:00:00, 2026-01-03T00:00:00, 2026-01-04T00:00:00, 2026-01-05T00:00:00`

