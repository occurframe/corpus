# Conformance report — `python-dateutil@tz2026c`

- engine: **python-dateutil** 2.9.0.post0
- runtime: python 3.11.15
- tzdb: **2026c** (from PyPI tzdata 2026.3)
- runner: run_python.py
- corpus: 1.0.0-rc1

**Scored 72 of 184 vectors; 60 pass (83.3%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `reject` | 4 |
| `empty` | 4 |
| `rejected` | 4 |
| `degenerate` | 1 |
| `expand` | 1 |
| `rule-only` | 1 |
| `lazy-iterator` | 1 |
| `open` | 1 |
| `silent` | 1 |
| `instant-match` | 1 |
| `union` | 1 |
| `rfc2445` | 1 |
| `tzdb<=2026a` | 1 |

## FAIL (6)

- `RRULE-DST-009` Hourly recurrence across the fold: 25-hour day
  - engine gave: `2026-11-01T00:00:00-04:00|2026-11-01T04:00:00Z, 2026-11-01T01:00:00-04:00|2026-11-01T05:00:00Z, 2026-11-01T02:00:00-05:00|2026-11-01T07:00:00Z, 2026-11-01T03:00:00-05:00|2026-11-01T08:00:00Z`
  - corpus expects: `2026-11-01T00:00:00-04:00|2026-11-01T04:00:00Z, 2026-11-01T01:00:00-04:00|2026-11-01T05:00:00Z, 2026-11-01T01:00:00-05:00|2026-11-01T06:00:00Z, 2026-11-01T02:00:00-05:00|2026-11-01T07:00:00Z`
- `RRULE-DST-010` Hourly recurrence across the gap: 23-hour day
  - engine gave: `2026-03-08T00:00:00-05:00|2026-03-08T05:00:00Z, 2026-03-08T01:00:00-05:00|2026-03-08T06:00:00Z, 2026-03-08T02:00:00-04:00|2026-03-08T06:00:00Z, 2026-03-08T03:00:00-04:00|2026-03-08T07:00:00Z`
  - corpus expects: `2026-03-08T00:00:00-05:00|2026-03-08T05:00:00Z, 2026-03-08T01:00:00-05:00|2026-03-08T06:00:00Z, 2026-03-08T03:00:00-04:00|2026-03-08T07:00:00Z, 2026-03-08T04:00:00-04:00|2026-03-08T08:00:00Z`
- `RRULE-SET-002` RDATE adds an instance outside the RRULE
  - engine said: `ValueError: unsupported RDATE parm: TZID=AMERICA/NEW_YORK`
  - corpus expects: `2026-01-05T09:00:00-05:00|2026-01-05T14:00:00Z, 2026-01-07T14:00:00-05:00|2026-01-07T19:00:00Z, 2026-01-12T09:00:00-05:00|2026-01-12T14:00:00Z, 2026-01-19T09:00:00-05:00|2026-01-19T14:00:00Z`
- `RRULE-SET-003` EXDATE takes precedence over RDATE for the same instant
  - engine said: `ValueError: unsupported RDATE parm: TZID=AMERICA/NEW_YORK`
  - corpus expects: `2026-01-05T09:00:00-05:00|2026-01-05T14:00:00Z, 2026-01-12T09:00:00-05:00|2026-01-12T14:00:00Z`
- `RRULE-SET-007` Duplicate instants from RRULE and RDATE are coalesced
  - engine said: `ValueError: unsupported RDATE parm: TZID=AMERICA/NEW_YORK`
  - corpus expects: `2026-01-05T09:00:00-05:00|2026-01-05T14:00:00Z, 2026-01-06T09:00:00-05:00|2026-01-06T14:00:00Z, 2026-01-07T09:00:00-05:00|2026-01-07T14:00:00Z`
- `RRULE-SET-014` RDATE and RRULE producing instants one second apart
  - engine said: `ValueError: unsupported RDATE parm: TZID=AMERICA/NEW_YORK`
  - corpus expects: `2026-01-05T09:00:00-05:00|2026-01-05T14:00:00Z, 2026-01-06T09:00:00-05:00|2026-01-06T14:00:00Z, 2026-01-06T09:00:01-05:00|2026-01-06T14:00:01Z, 2026-01-07T09:00:00-05:00|2026-01-07T14:00:00Z`

## REJECT-BAD (5)

- `RRULE-BY-024` BYWEEKNO with FREQ=MONTHLY (forbidden)
  - engine gave: `2026-01-01T09:00:00, 2026-01-02T09:00:00, 2026-01-03T09:00:00`
- `RRULE-BY-025` Numeric BYDAY with FREQ=WEEKLY (forbidden)
  - engine gave: `2026-01-05T09:00:00, 2026-01-12T09:00:00, 2026-01-19T09:00:00`
- `RRULE-BY-032` BYMONTHDAY=32
- `RRULE-CORE-011` COUNT and UNTIL in the same RRULE (forbidden)
  - engine gave: `1997-09-02T09:00:00-04:00|1997-09-02T13:00:00Z, 1997-09-03T09:00:00-04:00|1997-09-03T13:00:00Z, 1997-09-04T09:00:00-04:00|1997-09-04T13:00:00Z`
- `RRULE-CORE-016` INTERVAL=0
  - engine gave: `1997-09-02T09:00:00`

## NOVEL (1)

- `RRULE-DST-001` Daily 02:30 across the US spring-forward gap
  - engine gave: `2026-03-06T02:30:00-05:00|2026-03-06T07:30:00Z, 2026-03-07T02:30:00-05:00|2026-03-07T07:30:00Z, 2026-03-08T02:30:00-04:00|2026-03-08T06:30:00Z, 2026-03-09T02:30:00-04:00|2026-03-09T06:30:00Z`

