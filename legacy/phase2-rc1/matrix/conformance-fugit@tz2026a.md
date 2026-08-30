# Conformance report — `fugit@tz2026a`

- engine: **fugit** git floraison/fugit @efda655 2026-07-21
- runtime: ruby 3.3.6
- tzdb: **2026a** (from /usr/share/zoneinfo)
- runner: run_ruby.rb
- corpus: 1.0.0-rc1

**Scored 107 of 184 vectors; 104 pass (97.2%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `skip` | 20 |
| `reject` | 13 |
| `or/vixie` | 6 |
| `wrap-modulo` | 5 |
| `vixie-both` | 3 |
| `tzdb<=2026b` | 3 |
| `or-set-semantics` | 2 |
| `seconds-leading` | 2 |
| `error-at-parse` | 2 |
| `exclusive` | 1 |
| `truncate-to-minute` | 1 |
| `exact` | 1 |
| `vixie-artefact` | 1 |
| `reject-step` | 1 |
| `supported` | 1 |
| `last-day-of-week-of-month` | 1 |
| `seconds` | 1 |
| `three-letter-only` | 1 |
| `accept` | 1 |
| `start-at` | 1 |
| `collapse-to-first` | 1 |
| `tzdb<=2026a` | 1 |
| `tzdb<=2026a/gap-skip` | 1 |
| `links-absent` | 1 |

## FAIL (2)

- `CRON-EXT-012` cronie's '~' random operator
  - engine gave: `2026-01-01T00:08:00`
- `CRON-STEP-003` 0/1 vs * — Quartz idiom in the seconds field
  - engine gave: `2026-01-01T00:00:01, 2026-01-01T00:00:02, 2026-01-01T00:00:03`

## REJECT-BAD (1)

- `CRON-INV-002` Hour 24
  - engine gave: `2026-01-01T00:01:00`

