# Conformance report — `php-cron-expression@tz2026a`

- engine: **php-cron-expression** dragonmantank/cron-expression @d425a24 2025-12-20
- runtime: php 8.4.21
- tzdb: **2026a** (from /usr/share/zoneinfo)
- runner: run_php.php
- corpus: 1.0.0-rc1

**Scored 107 of 184 vectors; 99 pass (92.5%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `skip` | 16 |
| `reject` | 15 |
| `or/vixie` | 6 |
| `reject-reversed` | 4 |
| `vixie-both` | 3 |
| `fold_both` | 3 |
| `supported` | 3 |
| `tzdb<=2026b` | 3 |
| `vixie-artefact` | 2 |
| `error-at-parse` | 2 |
| `exclusive` | 1 |
| `truncate-to-minute` | 1 |
| `rejected` | 1 |
| `or-any-nonstar` | 1 |
| `last-day-of-week-of-month` | 1 |
| `seconds-leading` | 1 |
| `three-letter-only` | 1 |
| `tzdb<=2026a` | 1 |
| `links-absent` | 1 |

## FAIL (7)

- `CRON-ANCH-003` Sub-minute start instant, seconds-granularity expression
  - engine said: `InvalidArgumentException: 6 is not a valid position`
- `CRON-DOW-007` Non-wrapping named day range SAT-SUN
  - engine gave: `2026-01-03T12:00:00, 2026-01-10T12:00:00, 2026-01-17T12:00:00, 2026-01-24T12:00:00`
- `CRON-DOW-011` Named range with a step: MON-FRI/2
  - engine gave: `2026-01-04T12:00:00, 2026-01-11T12:00:00, 2026-01-18T12:00:00, 2026-01-25T12:00:00`
- `CRON-DST-001` Spring-forward gap: 02:30 daily across the US DST start
  - engine gave: `2026-03-07T02:30:00-05:00|2026-03-07T07:30:00Z, 2026-03-08T03:30:00-04:00|2026-03-08T07:30:00Z, 2026-03-09T02:30:00-04:00|2026-03-09T06:30:00Z, 2026-03-10T02:30:00-04:00|2026-03-10T06:30:00Z`
- `CRON-EXT-005` LW: last weekday of the month
  - engine gave: `2026-01-31T09:00:00, 2026-02-02T09:00:00, 2026-03-02T09:00:00, 2026-05-30T09:00:00`
- `CRON-STEP-004` Step larger than the field range: */90 in minutes
  - engine gave: `2026-01-01T00:30:00, 2026-01-01T01:30:00, 2026-01-01T02:30:00, 2026-01-01T03:30:00`
- `TZDB-005` A gap that exists under one tzdb and not another (America/Vancouver 2027-03-14 02:30)
  - engine gave: `2027-03-12T02:30:00-08:00|2027-03-12T10:30:00Z, 2027-03-13T02:30:00-08:00|2027-03-13T10:30:00Z, 2027-03-14T03:30:00-07:00|2027-03-14T10:30:00Z, 2027-03-15T02:30:00-07:00|2027-03-15T09:30:00Z`

## NOVEL (1)

- `CRON-DAYF-013` The '*/100,1-7 * MON' first-Monday idiom weaponising the artefact
  - engine gave: `2026-01-02T00:00:00, 2026-01-03T00:00:00, 2026-01-04T00:00:00, 2026-01-05T00:00:00`

