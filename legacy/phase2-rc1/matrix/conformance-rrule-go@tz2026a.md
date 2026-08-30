# Conformance report — `rrule-go@tz2026a`

- engine: **rrule-go** v1.8.x (git teambition/rrule-go @e74d163 2023-04-01)
- runtime: go1.24.7
- tzdb: **2026a** (from /usr/share/zoneinfo)
- runner: runners/go
- corpus: 1.0.0-rc1

**Scored 72 of 184 vectors; 61 pass (84.7%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `empty` | 3 |
| `reject` | 2 |
| `degenerate` | 1 |
| `expand` | 1 |
| `rule-only` | 1 |
| `lazy-iterator` | 1 |
| `open` | 1 |
| `exclude-midnight-only` | 1 |
| `silent` | 1 |
| `instant-match` | 1 |
| `include` | 1 |
| `tzdb<=2026a` | 1 |

## FAIL (3)

- `RRULE-DST-009` Hourly recurrence across the fold: 25-hour day
  - engine gave: `2026-11-01T00:00:00-04:00|2026-11-01T04:00:00Z, 2026-11-01T01:00:00-04:00|2026-11-01T05:00:00Z, 2026-11-01T02:00:00-05:00|2026-11-01T07:00:00Z, 2026-11-01T03:00:00-05:00|2026-11-01T08:00:00Z`
  - corpus expects: `2026-11-01T00:00:00-04:00|2026-11-01T04:00:00Z, 2026-11-01T01:00:00-04:00|2026-11-01T05:00:00Z, 2026-11-01T01:00:00-05:00|2026-11-01T06:00:00Z, 2026-11-01T02:00:00-05:00|2026-11-01T07:00:00Z`
- `RRULE-DST-010` Hourly recurrence across the gap: 23-hour day
  - engine gave: `2026-03-08T00:00:00-05:00|2026-03-08T05:00:00Z, 2026-03-08T01:00:00-05:00|2026-03-08T06:00:00Z, 2026-03-08T03:00:00-04:00|2026-03-08T07:00:00Z, 2026-03-08T04:00:00-04:00|2026-03-08T08:00:00Z`
  - corpus expects: `2026-03-08T00:00:00-05:00|2026-03-08T05:00:00Z, 2026-03-08T01:00:00-05:00|2026-03-08T06:00:00Z, 2026-03-08T03:00:00-04:00|2026-03-08T07:00:00Z, 2026-03-08T04:00:00-04:00|2026-03-08T08:00:00Z`
- `RRULE-SET-010` EXRULE (removed from RFC 5545, present in RFC 2445)
  - engine gave: `2026-01-05T09:00:00-05:00|2026-01-05T14:00:00Z, 2026-01-06T09:00:00-05:00|2026-01-06T14:00:00Z, 2026-01-07T09:00:00-05:00|2026-01-07T14:00:00Z, 2026-01-08T09:00:00-05:00|2026-01-08T14:00:00Z`

## REJECT-BAD (5)

- `RRULE-BY-024` BYWEEKNO with FREQ=MONTHLY (forbidden)
  - engine gave: `2026-01-01T09:00:00, 2026-01-02T09:00:00, 2026-01-03T09:00:00`
- `RRULE-BY-025` Numeric BYDAY with FREQ=WEEKLY (forbidden)
  - engine gave: `2026-01-05T09:00:00, 2026-01-12T09:00:00, 2026-01-19T09:00:00`
- `RRULE-CORE-010` UNTIL value type mismatched with DTSTART (Z on a floating start)
  - engine gave: `1997-09-02T09:00:00, 1997-09-03T09:00:00, 1997-09-04T09:00:00`
- `RRULE-CORE-011` COUNT and UNTIL in the same RRULE (forbidden)
  - engine gave: `1997-09-02T09:00:00-04:00|1997-09-02T13:00:00Z, 1997-09-03T09:00:00-04:00|1997-09-03T13:00:00Z, 1997-09-04T09:00:00-04:00|1997-09-04T13:00:00Z`
- `RRULE-CORE-016` INTERVAL=0
  - engine gave: `1997-09-02T09:00:00, 1997-09-03T09:00:00, 1997-09-04T09:00:00`

## NOVEL (3)

- `RRULE-CORE-017` COUNT=0
  - engine gave: `1997-09-02T09:00:00, 1997-09-03T09:00:00, 1997-09-04T09:00:00`
- `RRULE-DST-001` Daily 02:30 across the US spring-forward gap
  - engine gave: `2026-03-06T02:30:00-05:00|2026-03-06T07:30:00Z, 2026-03-07T02:30:00-05:00|2026-03-07T07:30:00Z, 2026-03-08T01:30:00-05:00|2026-03-08T06:30:00Z, 2026-03-09T02:30:00-04:00|2026-03-09T06:30:00Z`
- `RRULE-SET-008` Two RRULEs in one component
  - engine gave: `2026-01-07T09:00:00-05:00|2026-01-07T14:00:00Z, 2026-01-14T09:00:00-05:00|2026-01-14T14:00:00Z`

