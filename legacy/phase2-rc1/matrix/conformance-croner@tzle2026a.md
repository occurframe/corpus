# Conformance report — `croner@tzle2026a`

- engine: **croner** 10.0.1 (git Hexagon/croner @713ee72 2026-03-01)
- runtime: bun 1.3.13
- tzdb: **le2026a** (from runtime ICU (fingerprint le2026a))
- runner: run_js.ts
- corpus: 1.0.0-rc1

**Scored 107 of 184 vectors; 96 pass (89.7%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `skip` | 14 |
| `reject` | 8 |
| `or/vixie` | 6 |
| `reject-reversed` | 4 |
| `supported` | 4 |
| `vixie-both` | 3 |
| `tzdb<=2026b` | 3 |
| `vixie-artefact` | 2 |
| `fold_second` | 2 |
| `seconds-leading` | 2 |
| `empty` | 2 |
| `exclusive` | 1 |
| `truncate-to-minute` | 1 |
| `exact` | 1 |
| `or-any-nonstar` | 1 |
| `reject-step` | 1 |
| `wrap-modulo` | 1 |
| `accept-as-star` | 1 |
| `last-day-of-week-of-month` | 1 |
| `seconds` | 1 |
| `three-letter-only` | 1 |
| `accept` | 1 |
| `tzdb<=2026a` | 1 |
| `links-present` | 1 |

## FAIL (11)

- `CRON-DST-001` Spring-forward gap: 02:30 daily across the US DST start
  - engine gave: `2026-03-07T02:30:00-05:00|2026-03-07T07:30:00Z, 2026-03-08T03:30:00-04:00|2026-03-08T07:30:00Z, 2026-03-09T02:30:00-04:00|2026-03-09T06:30:00Z, 2026-03-10T02:30:00-04:00|2026-03-10T06:30:00Z`
- `CRON-DST-003` 30-minute DST transition (Lord Howe Island): 02:15 daily
  - engine gave: `2026-10-02T02:15:00+10:30|2026-10-01T15:45:00Z, 2026-10-03T02:15:00+10:30|2026-10-02T15:45:00Z, 2026-10-04T02:45:00+11:00|2026-10-03T15:45:00Z, 2026-10-05T02:15:00+11:00|2026-10-04T15:15:00Z`
- `CRON-DST-005` Two-hour DST transition (Antarctica/Troll): 01:30 daily
  - engine gave: `2026-03-27T01:30:00+00:00|2026-03-27T01:30:00Z, 2026-03-28T01:30:00+00:00|2026-03-28T01:30:00Z, 2026-03-29T03:30:00+02:00|2026-03-29T01:30:00Z, 2026-03-30T01:30:00+02:00|2026-03-29T23:30:00Z`
- `CRON-DST-007` A whole calendar day that does not exist (Pacific/Apia 2011-12-30)
  - engine gave: `2011-11-30T12:00:00-10:00|2011-11-30T22:00:00Z, 2011-12-31T12:00:00+14:00|2011-12-30T22:00:00Z, 2012-01-30T12:00:00+14:00|2012-01-29T22:00:00Z`
- `CRON-EXT-006` FRI#3: third Friday of the month
  - engine gave: `2026-01-01T09:00:00, 2026-01-02T09:00:00, 2026-01-03T09:00:00, 2026-01-04T09:00:00`
- `CRON-EXT-007` SUN#5 in a month with only four Sundays
  - engine gave: `2026-01-01T09:00:00, 2026-01-02T09:00:00, 2026-01-03T09:00:00, 2026-01-04T09:00:00`
- `CRON-EXT-008` FRIL / 6L: last Friday of the month
  - engine gave: `2026-01-01T09:00:00, 2026-01-02T09:00:00, 2026-01-03T09:00:00, 2026-01-04T09:00:00`
- `CRON-EXT-009` '?' in the day-of-month field with a restricted day-of-week
  - engine gave: `2026-01-01T12:00:00, 2026-01-02T12:00:00, 2026-01-03T12:00:00, 2026-01-04T12:00:00`
- `CRON-FIELDS-003` Seven-field Quartz form with an explicit year
  - engine gave: `2027-01-01T12:00:00, 2027-01-02T12:00:00, 2027-01-03T12:00:00, 2027-01-04T12:00:00`
- `CRON-STEP-009` Step in the day-of-month field: */10 does not mean every 10 days
  - engine gave: `2026-01-11T00:00:00, 2026-01-21T00:00:00, 2026-01-31T00:00:00, 2026-02-01T00:00:00`
  - corpus expects: `2026-01-11T00:00:00, 2026-01-21T00:00:00, 2026-01-31T00:00:00, 2026-02-01T00:00:00`
- `TZDB-005` A gap that exists under one tzdb and not another (America/Vancouver 2027-03-14 02:30)
  - engine gave: `2027-03-12T02:30:00-08:00|2027-03-12T10:30:00Z, 2027-03-13T02:30:00-08:00|2027-03-13T10:30:00Z, 2027-03-14T03:30:00-07:00|2027-03-14T10:30:00Z, 2027-03-15T02:30:00-07:00|2027-03-15T09:30:00Z`

