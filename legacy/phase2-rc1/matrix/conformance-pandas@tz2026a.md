# Conformance report — `pandas@tz2026a`

- engine: **pandas** 3.0.2
- runtime: python 3.11.15
- tzdb: **2026a** (from /usr/share/zoneinfo)
- runner: run_python.py
- corpus: 1.0.0-rc1

**Scored 16 of 184 vectors; 13 pass (81.2%).** The remainder are operations this engine does not implement, or vectors the corpus records without scoring.

## Policies and dialects this engine implements

| axis value observed | vectors |
|---|--:|
| `rejected` | 4 |
| `empty` | 1 |
| `tzdb<=2026a` | 1 |

## FAIL (2)

- `RRULE-DST-002` Daily 01:30 across the US autumn fold
  - engine said: `ValueError: Cannot infer dst time from 2026-11-01 01:30:00, try using the 'ambiguous' argument`
  - corpus expects: `2026-10-30T01:30:00-04:00|2026-10-30T05:30:00Z, 2026-10-31T01:30:00-04:00|2026-10-31T05:30:00Z, 2026-11-01T01:30:00-04:00|2026-11-01T05:30:00Z, 2026-11-02T01:30:00-05:00|2026-11-02T06:30:00Z`
- `RRULE-DST-007` UTC DTSTART is immune to DST by construction
  - engine gave: `2026-03-06T07:30:00, 2026-03-07T07:30:00, 2026-03-08T07:30:00, 2026-03-09T07:30:00`
  - corpus expects: `2026-03-06T07:30:00+00:00|2026-03-06T07:30:00Z, 2026-03-07T07:30:00+00:00|2026-03-07T07:30:00Z, 2026-03-08T07:30:00+00:00|2026-03-08T07:30:00Z, 2026-03-09T07:30:00+00:00|2026-03-09T07:30:00Z`

## NOVEL (1)

- `RRULE-DST-001` Daily 02:30 across the US spring-forward gap
  - engine said: `ValueError: 2026-03-08 02:30:00 is a nonexistent time due to daylight savings time. Try using the 'nonexistent' argument.`

