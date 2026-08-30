# Conformance report — `cron-parser@tzle2026a`

- engine: **cron-parser** 5.10.0 (git harrisiirak/cron-parser @7b3a0ad 2026-08-28)
- runtime: bun 1.3.13
- tzdb: **le2026a** (from runtime ICU (fingerprint le2026a))
- runner: run_js.ts
- corpus: 1.0.0-rc1

**Scored 107 of 184 vectors; 100 pass (93.5%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `skip` | 17 |
| `reject` | 15 |
| `or/vixie` | 6 |
| `reject-reversed` | 5 |
| `tzdb<=2026b` | 3 |
| `vixie-both` | 2 |
| `seconds-leading` | 2 |
| `error-at-parse` | 2 |
| `exclusive` | 1 |
| `truncate-to-minute` | 1 |
| `exact` | 1 |
| `vixie-artefact` | 1 |
| `reject-step` | 1 |
| `monday-zero` | 1 |
| `fold_both` | 1 |
| `supported` | 1 |
| `last-day-of-week-of-month` | 1 |
| `seconds` | 1 |
| `three-letter-only` | 1 |
| `accept` | 1 |
| `start-at` | 1 |
| `collapse-to-first` | 1 |
| `tzdb<=2026a` | 1 |
| `links-present` | 1 |

## FAIL (5)

- `CRON-DST-001` Spring-forward gap: 02:30 daily across the US DST start
  - engine gave: `2026-03-07T02:30:00-05:00|2026-03-07T07:30:00Z, 2026-03-08T03:30:00-04:00|2026-03-08T07:30:00Z, 2026-03-09T02:30:00-04:00|2026-03-09T06:30:00Z, 2026-03-10T02:30:00-04:00|2026-03-10T06:30:00Z`
- `CRON-DST-005` Two-hour DST transition (Antarctica/Troll): 01:30 daily
  - engine gave: `2026-03-27T01:30:00+00:00|2026-03-27T01:30:00Z, 2026-03-28T01:30:00+00:00|2026-03-28T01:30:00Z, 2026-03-29T03:30:00+02:00|2026-03-29T01:30:00Z, 2026-03-30T01:30:00+02:00|2026-03-29T23:30:00Z`
- `CRON-EXT-011` 'H' (Jenkins hash) in the minute field
  - engine gave: `2026-01-01T00:08:00`
- `CRON-STEP-003` 0/1 vs * — Quartz idiom in the seconds field
  - engine gave: `2026-01-01T00:00:01, 2026-01-01T00:00:02, 2026-01-01T00:00:03`
- `TZDB-005` A gap that exists under one tzdb and not another (America/Vancouver 2027-03-14 02:30)
  - engine gave: `2027-03-12T02:30:00-08:00|2027-03-12T10:30:00Z, 2027-03-13T02:30:00-08:00|2027-03-13T10:30:00Z, 2027-03-14T03:30:00-07:00|2027-03-14T10:30:00Z, 2027-03-15T02:30:00-07:00|2027-03-15T09:30:00Z`

## REJECT-BAD (2)

- `CRON-FIELDS-005` Four fields (too few)
  - engine gave: `2026-01-12T00:00:00`
- `CRON-INV-009` Empty expression
  - engine gave: `2026-01-01T00:01:00`

