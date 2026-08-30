# Conformance report — `apscheduler3@tz2026c`

- engine: **apscheduler3** 3.11.3 (git agronholm/apscheduler @4308ec9, tag 3.11.3)
- runtime: python 3.11.15
- tzdb: **2026c** (from PyPI tzdata 2026.3)
- runner: run_python.py
- corpus: 1.0.0-rc1

**Scored 107 of 184 vectors; 85 pass (79.4%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `reject` | 19 |
| `skip` | 10 |
| `rejected` | 6 |
| `and+monday-zero` | 5 |
| `and` | 4 |
| `reject-reversed` | 4 |
| `monday-zero` | 3 |
| `tzdb>=2026c` | 3 |
| `fold_both` | 2 |
| `empty` | 2 |
| `tzdb>=2026b` | 2 |
| `inclusive` | 1 |
| `truncate-to-minute` | 1 |
| `reject-step` | 1 |
| `wrap-modulo` | 1 |
| `last-day-of-week-of-month` | 1 |
| `seconds-leading` | 1 |
| `three-letter-only` | 1 |
| `start-at` | 1 |
| `links-present` | 1 |

## FAIL (22)

- `CRON-ANCH-003` Sub-minute start instant, seconds-granularity expression
  - engine said: `ValueError: Wrong number of fields; got 6, expected 5`
- `CRON-ANCH-004` Cron has no anchor: '*/7' in the day field restarts each month
  - engine gave: `2026-01-01T00:00:00, 2026-01-08T00:00:00, 2026-01-15T00:00:00, 2026-01-22T00:00:00`
  - corpus expects: `2026-01-08T00:00:00, 2026-01-15T00:00:00, 2026-01-22T00:00:00, 2026-01-29T00:00:00`
- `CRON-DOW-011` Named range with a step: MON-FRI/2
  - engine gave: `2026-01-01T12:00:00, 2026-01-02T12:00:00, 2026-01-05T12:00:00, 2026-01-06T12:00:00`
- `CRON-DOW-013` Numeric and named spellings of the same weekday must agree (0 vs SUN)
  - engine gave: `2026-01-05T12:00:00, 2026-01-12T12:00:00, 2026-01-19T12:00:00`
  - corpus expects: `2026-01-04T12:00:00, 2026-01-11T12:00:00, 2026-01-18T12:00:00`
- `CRON-DST-001` Spring-forward gap: 02:30 daily across the US DST start
  - engine gave: `2026-03-07T02:30:00-05:00|2026-03-07T07:30:00Z, 2026-03-08T02:30:00-05:00|2026-03-08T07:30:00Z, 2026-03-09T02:30:00-04:00|2026-03-09T06:30:00Z, 2026-03-10T02:30:00-04:00|2026-03-10T06:30:00Z`
- `CRON-DST-003` 30-minute DST transition (Lord Howe Island): 02:15 daily
  - engine gave: `2026-10-02T02:15:00+10:30|2026-10-01T15:45:00Z, 2026-10-03T02:15:00+10:30|2026-10-02T15:45:00Z, 2026-10-04T02:15:00+10:30|2026-10-03T15:45:00Z, 2026-10-05T02:15:00+11:00|2026-10-04T15:15:00Z`
- `CRON-DST-005` Two-hour DST transition (Antarctica/Troll): 01:30 daily
  - engine gave: `2026-03-27T01:30:00+00:00|2026-03-27T01:30:00Z, 2026-03-28T01:30:00+00:00|2026-03-28T01:30:00Z, 2026-03-29T01:30:00+00:00|2026-03-29T01:30:00Z, 2026-03-30T01:30:00+02:00|2026-03-29T23:30:00Z`
- `CRON-DST-007` A whole calendar day that does not exist (Pacific/Apia 2011-12-30)
  - engine gave: `2011-11-30T12:00:00-10:00|2011-11-30T22:00:00Z, 2011-12-30T12:00:00-10:00|2011-12-30T22:00:00Z, 2012-01-30T12:00:00+14:00|2012-01-29T22:00:00Z`
- `CRON-DST-016` Hourly schedule across the fold: how many 01:00s?
  - engine gave: `2026-11-01T00:00:00-04:00|2026-11-01T04:00:00Z, 2026-11-01T01:00:00-04:00|2026-11-01T05:00:00Z, 2026-11-01T01:00:00-05:00|2026-11-01T06:00:00Z, 2026-11-01T01:00:00-05:00|2026-11-01T06:00:00Z`
- `CRON-DST-017` Half-hourly schedule across the gap: how many firings?
  - engine gave: `2026-03-08T00:00:00-05:00|2026-03-08T05:00:00Z, 2026-03-08T00:30:00-05:00|2026-03-08T05:30:00Z, 2026-03-08T01:00:00-05:00|2026-03-08T06:00:00Z, 2026-03-08T01:30:00-05:00|2026-03-08T06:30:00Z`
- `CRON-DST-018` Extreme positive offset (+14:00, Pacific/Kiritimati)
  - engine gave: `2026-01-01T00:00:00+14:00|2025-12-31T10:00:00Z, 2026-01-02T00:00:00+14:00|2026-01-01T10:00:00Z, 2026-01-03T00:00:00+14:00|2026-01-02T10:00:00Z`
- `CRON-DST-019` Extreme negative offset (-11:00, Pacific/Niue)
  - engine gave: `2026-01-01T00:00:00-11:00|2026-01-01T11:00:00Z, 2026-01-02T00:00:00-11:00|2026-01-02T11:00:00Z, 2026-01-03T00:00:00-11:00|2026-01-03T11:00:00Z`
- `CRON-FIELDS-008` Macro @daily
  - engine said: `ValueError: Wrong number of fields; got 1, expected 5`
  - corpus expects: `2026-01-02T00:00:00, 2026-01-03T00:00:00, 2026-01-04T00:00:00, 2026-01-05T00:00:00`
- `CRON-FIELDS-009` Macro @yearly
  - engine said: `ValueError: Wrong number of fields; got 1, expected 5`
  - corpus expects: `2027-01-01T00:00:00, 2028-01-01T00:00:00, 2029-01-01T00:00:00, 2030-01-01T00:00:00`
- `CRON-FIELDS-010` Macro @monthly
  - engine said: `ValueError: Wrong number of fields; got 1, expected 5`
  - corpus expects: `2026-02-01T00:00:00, 2026-03-01T00:00:00, 2026-04-01T00:00:00, 2026-05-01T00:00:00`
- `CRON-FIELDS-011` Macro @weekly
  - engine said: `ValueError: Wrong number of fields; got 1, expected 5`
  - corpus expects: `2026-01-04T00:00:00, 2026-01-11T00:00:00, 2026-01-18T00:00:00, 2026-01-25T00:00:00`
- `CRON-FIELDS-012` Macro @hourly
  - engine said: `ValueError: Wrong number of fields; got 1, expected 5`
  - corpus expects: `2026-01-01T01:00:00, 2026-01-01T02:00:00, 2026-01-01T03:00:00, 2026-01-01T04:00:00`
- `CRON-STEP-001` */35 in the minute field: step does not mean interval
  - engine gave: `2026-01-01T00:00:00, 2026-01-01T00:35:00, 2026-01-01T01:00:00, 2026-01-01T01:35:00`
  - corpus expects: `2026-01-01T00:35:00, 2026-01-01T01:00:00, 2026-01-01T01:35:00, 2026-01-01T02:00:00`
- `CRON-STEP-008` */1 (identity step)
  - engine gave: `2026-01-01T00:00:00, 2026-01-01T00:01:00, 2026-01-01T00:02:00`
  - corpus expects: `2026-01-01T00:01:00, 2026-01-01T00:02:00, 2026-01-01T00:03:00`
- `CRON-STEP-009` Step in the day-of-month field: */10 does not mean every 10 days
  - engine gave: `2026-01-01T00:00:00, 2026-01-11T00:00:00, 2026-01-21T00:00:00, 2026-01-31T00:00:00`
  - corpus expects: `2026-01-11T00:00:00, 2026-01-21T00:00:00, 2026-01-31T00:00:00, 2026-02-01T00:00:00`
- `CRON-STEP-010` Comma list mixing a range-step and a literal
  - engine gave: `2026-01-01T00:00:00, 2026-01-01T02:00:00, 2026-01-01T04:00:00, 2026-01-01T06:00:00`
  - corpus expects: `2026-01-01T02:00:00, 2026-01-01T04:00:00, 2026-01-01T06:00:00, 2026-01-01T23:00:00`
- `CRON-STEP-012` Step applied to a single '*' in the month field
  - engine gave: `2026-01-01T00:00:00, 2026-04-01T00:00:00, 2026-07-01T00:00:00, 2026-10-01T00:00:00`
  - corpus expects: `2026-04-01T00:00:00, 2026-07-01T00:00:00, 2026-10-01T00:00:00, 2027-01-01T00:00:00`

