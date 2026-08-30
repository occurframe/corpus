# Conformance report — `cron-parser[strict]@tzle2026a`

- engine: **cron-parser[strict]** 5.10.0 (git harrisiirak/cron-parser @7b3a0ad 2026-08-28)
- runtime: bun 1.3.13
- tzdb: **le2026a** (from runtime ICU (fingerprint le2026a))
- runner: run_js.ts
- corpus: 1.0.0-rc1

**Scored 107 of 184 vectors; 65 pass (60.7%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `rejected` | 41 |
| `reject` | 27 |
| `reject-reversed` | 5 |
| `monday-zero` | 2 |
| `seconds-leading` | 2 |
| `error-at-parse` | 2 |
| `exact` | 1 |
| `reject-step` | 1 |
| `quartz-1-7` | 1 |
| `last-day-of-week-of-month` | 1 |
| `seconds` | 1 |
| `three-letter-only` | 1 |
| `links-absent` | 1 |

## FAIL (42)

- `CRON-ANCH-001` Start instant exactly on an occurrence: inclusive or exclusive?
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-ANCH-002` Sub-minute start instant (seconds and micros in the anchor)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-ANCH-004` Cron has no anchor: '*/7' in the day field restarts each month
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-08T00:00:00, 2026-01-15T00:00:00, 2026-01-22T00:00:00, 2026-01-29T00:00:00`
- `CRON-DOW-008` Lowercase day name
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-04T12:00:00, 2026-01-11T12:00:00, 2026-01-18T12:00:00, 2026-01-25T12:00:00`
- `CRON-DOW-009` Lowercase month and day names
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-05T12:00:00, 2026-01-12T12:00:00, 2026-01-19T12:00:00, 2026-01-26T12:00:00`
- `CRON-DOW-013` Numeric and named spellings of the same weekday must agree (0 vs SUN)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-04T12:00:00, 2026-01-11T12:00:00, 2026-01-18T12:00:00`
- `CRON-DST-001` Spring-forward gap: 02:30 daily across the US DST start
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-002` Autumn fold: 01:30 daily across the US DST end
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-003` 30-minute DST transition (Lord Howe Island): 02:15 daily
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-004` 30-minute fold (Lord Howe Island): 01:45 daily
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-005` Two-hour DST transition (Antarctica/Troll): 01:30 daily
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-006` Two-hour fold (Antarctica/Troll): 01:30 daily
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-007` A whole calendar day that does not exist (Pacific/Apia 2011-12-30)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-008` Zero-offset-change transition (Asia/Amman, October 2022)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-009` Zero-offset-change transition (Asia/Damascus, October 2022)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-010` Non-hour standard offset (+05:45, Asia/Kathmandu)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-011` Non-hour standard offset (+08:45, Australia/Eucla)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-012` Historical standard-offset change (Europe/Lisbon, 1992-09-27)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-013` Historical DST rule change (US Energy Policy Act, 2007)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-014` Southern-hemisphere spring forward (America/Santiago)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-015` Half-hour standard offset with DST (America/St_Johns, -03:30)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-016` Hourly schedule across the fold: how many 01:00s?
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-017` Half-hourly schedule across the gap: how many firings?
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-018` Extreme positive offset (+14:00, Pacific/Kiritimati)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-019` Extreme negative offset (-11:00, Pacific/Niue)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-DST-020` Weekly schedule landing exactly on the transition Sunday
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `CRON-FIELDS-001` Five-field form (POSIX / Vixie baseline)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-01T10:15:00, 2026-01-02T10:15:00, 2026-01-03T10:15:00, 2026-01-04T10:15:00`
- `CRON-INV-012` Whitespace-tolerant parsing (tabs and multiple spaces)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-01T12:00:00, 2026-01-02T12:00:00, 2026-01-03T12:00:00`
- `CRON-STEP-001` */35 in the minute field: step does not mean interval
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-01T00:35:00, 2026-01-01T01:00:00, 2026-01-01T01:35:00, 2026-01-01T02:00:00`
- `CRON-STEP-003` 0/1 vs * — Quartz idiom in the seconds field
  - engine gave: `2026-01-01T00:00:01, 2026-01-01T00:00:02, 2026-01-01T00:00:03`
- `CRON-STEP-006` Range with a step: 10-16/2 (documented form)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-01T10:00:00, 2026-01-01T12:00:00, 2026-01-01T14:00:00, 2026-01-01T16:00:00`
- `CRON-STEP-008` */1 (identity step)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-01T00:01:00, 2026-01-01T00:02:00, 2026-01-01T00:03:00`
- `CRON-STEP-009` Step in the day-of-month field: */10 does not mean every 10 days
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-11T00:00:00, 2026-01-21T00:00:00, 2026-01-31T00:00:00, 2026-02-01T00:00:00`
- `CRON-STEP-010` Comma list mixing a range-step and a literal
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-01T02:00:00, 2026-01-01T04:00:00, 2026-01-01T06:00:00, 2026-01-01T23:00:00`
- `CRON-STEP-012` Step applied to a single '*' in the month field
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-04-01T00:00:00, 2026-07-01T00:00:00, 2026-10-01T00:00:00, 2027-01-01T00:00:00`
- `TZDB-001` America/Vancouver noon daily across 2026-11-01 (BC abolished DST in tzdb 2026b)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `TZDB-002` America/Edmonton noon daily across 2026-11-01 (Alberta abolished DST in tzdb 2026c)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `TZDB-003` Africa/Casablanca: Morocco moves to permanent UTC on 2026-09-20
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `TZDB-005` A gap that exists under one tzdb and not another (America/Vancouver 2027-03-14 02:30)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `TZDB-006` Zone abbreviation is not a stable identifier (Edmonton reports CST at -06:00)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
- `TZDB-007` A zone whose historical data changed: Europe/Lisbon 1992
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `1992-09-25T12:00:00+01:00|1992-09-25T11:00:00Z, 1992-09-26T12:00:00+01:00|1992-09-26T11:00:00Z, 1992-09-27T12:00:00+01:00|1992-09-27T11:00:00Z, 1992-09-28T12:00:00+01:00|1992-09-28T11:00:00Z`
- `TZDB-010` Etc/GMT+5 has a NEGATIVE offset (POSIX sign inversion)
  - engine said: `Error: Invalid cron expression, expected 6 fields`
  - corpus expects: `2026-01-14T12:00:00-05:00|2026-01-14T17:00:00Z, 2026-01-15T12:00:00-05:00|2026-01-15T17:00:00Z`

