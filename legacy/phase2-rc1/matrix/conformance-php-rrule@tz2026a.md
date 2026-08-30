# Conformance report — `php-rrule@tz2026a`

- engine: **php-rrule** rlanvin/php-rrule @93a083d 2026-07-29
- runtime: php 8.4.21
- tzdb: **2026a** (from /usr/share/zoneinfo)
- runner: run_php.php
- corpus: 1.0.0-rc1

**Scored 72 of 184 vectors; 68 pass (94.4%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `empty` | 3 |
| `reject` | 2 |
| `degenerate` | 1 |
| `rejected` | 1 |
| `expand` | 1 |
| `rule-only` | 1 |
| `lazy-iterator` | 1 |
| `open` | 1 |
| `exclude-midnight-only` | 1 |
| `silent` | 1 |
| `instant-match` | 1 |
| `union` | 1 |
| `rfc2445` | 1 |
| `include` | 1 |
| `tzdb<=2026a` | 1 |

## FAIL (3)

- `RRULE-DST-009` Hourly recurrence across the fold: 25-hour day
  - engine gave: `2026-11-01T00:00:00-04:00|2026-11-01T04:00:00Z, 2026-11-01T01:00:00-04:00|2026-11-01T05:00:00Z, 2026-11-01T02:00:00-05:00|2026-11-01T07:00:00Z, 2026-11-01T03:00:00-05:00|2026-11-01T08:00:00Z`
  - corpus expects: `2026-11-01T00:00:00-04:00|2026-11-01T04:00:00Z, 2026-11-01T01:00:00-04:00|2026-11-01T05:00:00Z, 2026-11-01T01:00:00-05:00|2026-11-01T06:00:00Z, 2026-11-01T02:00:00-05:00|2026-11-01T07:00:00Z`
- `RRULE-DST-010` Hourly recurrence across the gap: 23-hour day
  - engine gave: `2026-03-08T00:00:00-05:00|2026-03-08T05:00:00Z, 2026-03-08T01:00:00-05:00|2026-03-08T06:00:00Z, 2026-03-08T03:00:00-04:00|2026-03-08T07:00:00Z, 2026-03-08T04:00:00-04:00|2026-03-08T08:00:00Z`
  - corpus expects: `2026-03-08T00:00:00-05:00|2026-03-08T05:00:00Z, 2026-03-08T01:00:00-05:00|2026-03-08T06:00:00Z, 2026-03-08T03:00:00-04:00|2026-03-08T07:00:00Z, 2026-03-08T04:00:00-04:00|2026-03-08T08:00:00Z`
- `RRULE-SET-011` RDATE with a PERIOD value
  - engine gave: `2026-01-05T09:00:00-05:00|2026-01-05T14:00:00Z, 2026-01-12T09:00:00-05:00|2026-01-12T14:00:00Z`

## NOVEL (1)

- `RRULE-DST-001` Daily 02:30 across the US spring-forward gap
  - engine gave: `2026-03-06T02:30:00-05:00|2026-03-06T07:30:00Z, 2026-03-07T02:30:00-05:00|2026-03-07T07:30:00Z, 2026-03-08T03:30:00-04:00|2026-03-08T07:30:00Z, 2026-03-09T02:30:00-04:00|2026-03-09T06:30:00Z`

