# Measured divergences

Every vector on which two engine builds produced different output. `ERROR` means the engine rejected the input, `HANG` that it did not terminate, `EMPTY` that it returned no occurrences.


## `CRON-DST-007` — A whole calendar day that does not exist (Pacific/Apia 2011-12-30)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `0 12 30 * *` from `2011-11-01T00:00:00` zone `Pacific/Apia` × 3

**6 distinct answers:**

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c** → admissible case `next_valid`
  <br>`2011-11-30T12:00:00-10:00<br>2011-11-30T22:00:00Z<br>2011-12-31T00:00:00+14:00<br>2011-12-30T10:00:00Z<br>2012-01-30T12:00:00+14:00<br>2012-01-29T22:00:00Z`

- **cron-parser@tzle2026a, fugit@tz2026a, php-cron-expression@tz2026a** → admissible case `skip`
  <br>`2011-11-30T12:00:00-10:00<br>2011-11-30T22:00:00Z<br>2012-01-30T12:00:00+14:00<br>2012-01-29T22:00:00Z<br>2012-03-30T12:00:00+14:00<br>2012-03-29T22:00:00Z`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2011-11-30T12:00:00-10:00<br>2011-11-30T22:00:00Z<br>2011-12-30T12:00:00-10:00<br>2011-12-30T22:00:00Z<br>2012-01-30T12:00:00+14:00<br>2012-01-29T22:00:00Z`

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a**
  <br>`2011-11-30T12:00:00-10:00<br>2011-11-30T22:00:00Z<br>2011-12-31T12:00:00+14:00<br>2011-12-30T22:00:00Z<br>2012-01-30T12:00:00+14:00<br>2012-01-29T22:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`

- **robfig-cron@tz2026a**
  <br>`HANG`


## `TZDB-005` — A gap that exists under one tzdb and not another (America/Vancouver 2027-03-14 02:30)

*POLICY_DEPENDENT* · family `tzdb.provenance` · policy axis `tz.tzdb_version|cron.dst_gap`

input: `30 2 * * *` from `2027-03-12T00:00:00` zone `America/Vancouver` × 4

**6 distinct answers:**

- **apscheduler3@tz2026c, croniter@tz2026c, croniter[day_or=False]@tz2026c, cronsim@tz2026c** → admissible case `tzdb>=2026b`
  <br>`2027-03-12T02:30:00-07:00<br>2027-03-12T09:30:00Z<br>2027-03-13T02:30:00-07:00<br>2027-03-13T09:30:00Z<br>2027-03-14T02:30:00-07:00<br>2027-03-14T09:30:00Z<br>2027-03-15T02:30:00-07:00<br>2027-03-15T09:30:00Z`

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, php-cron-expression@tz2026a**
  <br>`2027-03-12T02:30:00-08:00<br>2027-03-12T10:30:00Z<br>2027-03-13T02:30:00-08:00<br>2027-03-13T10:30:00Z<br>2027-03-14T03:30:00-07:00<br>2027-03-14T10:30:00Z<br>2027-03-15T02:30:00-07:00<br>2027-03-15T09:30:00Z`

- **croniter@tz2026a, croniter[day_or=False]@tz2026a, cronsim@tz2026a** → admissible case `tzdb<=2026a/next-valid`
  <br>`2027-03-12T02:30:00-08:00<br>2027-03-12T10:30:00Z<br>2027-03-13T02:30:00-08:00<br>2027-03-13T10:30:00Z<br>2027-03-14T03:00:00-07:00<br>2027-03-14T10:00:00Z<br>2027-03-15T02:30:00-07:00<br>2027-03-15T09:30:00Z`

- **fugit@tz2026a, robfig-cron@tz2026a** → admissible case `tzdb<=2026a/gap-skip`
  <br>`2027-03-12T02:30:00-08:00<br>2027-03-12T10:30:00Z<br>2027-03-13T02:30:00-08:00<br>2027-03-13T10:30:00Z<br>2027-03-15T02:30:00-07:00<br>2027-03-15T09:30:00Z<br>2027-03-16T02:30:00-07:00<br>2027-03-16T09:30:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`

- **apscheduler3@tz2026a**
  <br>`2027-03-12T02:30:00-08:00<br>2027-03-12T10:30:00Z<br>2027-03-13T02:30:00-08:00<br>2027-03-13T10:30:00Z<br>2027-03-14T02:30:00-08:00<br>2027-03-14T10:30:00Z<br>2027-03-15T02:30:00-07:00<br>2027-03-15T09:30:00Z`


## `CRON-DST-001` — Spring-forward gap: 02:30 daily across the US DST start

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 2 * * *` from `2026-03-07T00:00:00` zone `America/New_York` × 4

**5 distinct answers:**

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c** → admissible case `next_valid`
  <br>`2026-03-07T02:30:00-05:00<br>2026-03-07T07:30:00Z<br>2026-03-08T03:00:00-04:00<br>2026-03-08T07:00:00Z<br>2026-03-09T02:30:00-04:00<br>2026-03-09T06:30:00Z<br>2026-03-10T02:30:00-04:00<br>2026-03-10T06:30:00Z`

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, php-cron-expression@tz2026a**
  <br>`2026-03-07T02:30:00-05:00<br>2026-03-07T07:30:00Z<br>2026-03-08T03:30:00-04:00<br>2026-03-08T07:30:00Z<br>2026-03-09T02:30:00-04:00<br>2026-03-09T06:30:00Z<br>2026-03-10T02:30:00-04:00<br>2026-03-10T06:30:00Z`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-03-07T02:30:00-05:00<br>2026-03-07T07:30:00Z<br>2026-03-08T02:30:00-05:00<br>2026-03-08T07:30:00Z<br>2026-03-09T02:30:00-04:00<br>2026-03-09T06:30:00Z<br>2026-03-10T02:30:00-04:00<br>2026-03-10T06:30:00Z`

- **fugit@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-03-07T02:30:00-05:00<br>2026-03-07T07:30:00Z<br>2026-03-09T02:30:00-04:00<br>2026-03-09T06:30:00Z<br>2026-03-10T02:30:00-04:00<br>2026-03-10T06:30:00Z<br>2026-03-11T02:30:00-04:00<br>2026-03-11T06:30:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-003` — 30-minute DST transition (Lord Howe Island): 02:15 daily

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `15 2 * * *` from `2026-10-02T00:00:00` zone `Australia/Lord_Howe` × 4

**5 distinct answers:**

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c** → admissible case `next_valid`
  <br>`2026-10-02T02:15:00+10:30<br>2026-10-01T15:45:00Z<br>2026-10-03T02:15:00+10:30<br>2026-10-02T15:45:00Z<br>2026-10-04T02:30:00+11:00<br>2026-10-03T15:30:00Z<br>2026-10-05T02:15:00+11:00<br>2026-10-04T15:15:00Z`

- **cron-parser@tzle2026a, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-10-02T02:15:00+10:30<br>2026-10-01T15:45:00Z<br>2026-10-03T02:15:00+10:30<br>2026-10-02T15:45:00Z<br>2026-10-05T02:15:00+11:00<br>2026-10-04T15:15:00Z<br>2026-10-06T02:15:00+11:00<br>2026-10-05T15:15:00Z`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-10-02T02:15:00+10:30<br>2026-10-01T15:45:00Z<br>2026-10-03T02:15:00+10:30<br>2026-10-02T15:45:00Z<br>2026-10-04T02:15:00+10:30<br>2026-10-03T15:45:00Z<br>2026-10-05T02:15:00+11:00<br>2026-10-04T15:15:00Z`

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a**
  <br>`2026-10-02T02:15:00+10:30<br>2026-10-01T15:45:00Z<br>2026-10-03T02:15:00+10:30<br>2026-10-02T15:45:00Z<br>2026-10-04T02:45:00+11:00<br>2026-10-03T15:45:00Z<br>2026-10-05T02:15:00+11:00<br>2026-10-04T15:15:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-005` — Two-hour DST transition (Antarctica/Troll): 01:30 daily

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 1 * * *` from `2026-03-27T00:00:00` zone `Antarctica/Troll` × 4

**5 distinct answers:**

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c** → admissible case `next_valid`
  <br>`2026-03-27T01:30:00+00:00<br>2026-03-27T01:30:00Z<br>2026-03-28T01:30:00+00:00<br>2026-03-28T01:30:00Z<br>2026-03-29T03:00:00+02:00<br>2026-03-29T01:00:00Z<br>2026-03-30T01:30:00+02:00<br>2026-03-29T23:30:00Z`

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a**
  <br>`2026-03-27T01:30:00+00:00<br>2026-03-27T01:30:00Z<br>2026-03-28T01:30:00+00:00<br>2026-03-28T01:30:00Z<br>2026-03-29T03:30:00+02:00<br>2026-03-29T01:30:00Z<br>2026-03-30T01:30:00+02:00<br>2026-03-29T23:30:00Z`

- **fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-03-27T01:30:00+00:00<br>2026-03-27T01:30:00Z<br>2026-03-28T01:30:00+00:00<br>2026-03-28T01:30:00Z<br>2026-03-30T01:30:00+02:00<br>2026-03-29T23:30:00Z<br>2026-03-31T01:30:00+02:00<br>2026-03-30T23:30:00Z`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-03-27T01:30:00+00:00<br>2026-03-27T01:30:00Z<br>2026-03-28T01:30:00+00:00<br>2026-03-28T01:30:00Z<br>2026-03-29T01:30:00+00:00<br>2026-03-29T01:30:00Z<br>2026-03-30T01:30:00+02:00<br>2026-03-29T23:30:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `RRULE-DST-001` — Daily 02:30 across the US spring-forward gap

*AMBIGUOUS_STANDARD* · family `rrule.dst` · policy axis `rrule.gap`

input:
```
DTSTART;TZID=America/New_York:20260306T023000
RRULE:FREQ=DAILY;COUNT=4
```

**5 distinct answers:**

- **python-dateutil@tz2026a, python-dateutil@tz2026c**
  <br>`2026-03-06T02:30:00-05:00<br>2026-03-06T07:30:00Z<br>2026-03-07T02:30:00-05:00<br>2026-03-07T07:30:00Z<br>2026-03-08T02:30:00-04:00<br>2026-03-08T06:30:00Z<br>2026-03-09T02:30:00-04:00<br>2026-03-09T06:30:00Z`

- **php-rrule@tz2026a, rrule.js@tzle2026a**
  <br>`2026-03-06T02:30:00-05:00<br>2026-03-06T07:30:00Z<br>2026-03-07T02:30:00-05:00<br>2026-03-07T07:30:00Z<br>2026-03-08T03:30:00-04:00<br>2026-03-08T07:30:00Z<br>2026-03-09T02:30:00-04:00<br>2026-03-09T06:30:00Z`

- **pandas@tz2026a, pandas@tz2026c** → admissible case `rejected`
  <br>`ERROR`

- **ice_cube@tz2026a**
  <br>`2026-03-06T02:30:00+00:00<br>2026-03-06T02:30:00Z<br>2026-03-07T02:30:00+00:00<br>2026-03-07T02:30:00Z<br>2026-03-08T02:30:00+00:00<br>2026-03-08T02:30:00Z<br>2026-03-09T02:30:00+00:00<br>2026-03-09T02:30:00Z`

- **rrule-go@tz2026a**
  <br>`2026-03-06T02:30:00-05:00<br>2026-03-06T07:30:00Z<br>2026-03-07T02:30:00-05:00<br>2026-03-07T07:30:00Z<br>2026-03-08T01:30:00-05:00<br>2026-03-08T06:30:00Z<br>2026-03-09T02:30:00-04:00<br>2026-03-09T06:30:00Z`


## `RRULE-DST-005` — Daily 01:30 in Antarctica/Troll (two-hour transition)

*AMBIGUOUS_STANDARD* · family `rrule.dst` · policy axis `rrule.gap`

input:
```
DTSTART;TZID=Antarctica/Troll:20260327T013000
RRULE:FREQ=DAILY;COUNT=4
```

**5 distinct answers:**

- **python-dateutil@tz2026a, python-dateutil@tz2026c**
  <br>`2026-03-27T01:30:00+00:00<br>2026-03-27T01:30:00Z<br>2026-03-28T01:30:00+00:00<br>2026-03-28T01:30:00Z<br>2026-03-29T01:30:00+02:00<br>2026-03-28T23:30:00Z<br>2026-03-30T01:30:00+02:00<br>2026-03-29T23:30:00Z`

- **php-rrule@tz2026a, rrule-go@tz2026a**
  <br>`2026-03-27T01:30:00+00:00<br>2026-03-27T01:30:00Z<br>2026-03-28T01:30:00+00:00<br>2026-03-28T01:30:00Z<br>2026-03-29T03:30:00+02:00<br>2026-03-29T01:30:00Z<br>2026-03-30T01:30:00+02:00<br>2026-03-29T23:30:00Z`

- **pandas@tz2026a, pandas@tz2026c** → admissible case `rejected`
  <br>`ERROR`

- **rrule.js@tzle2026a**
  <br>`2026-03-27T01:30:00+00:00<br>2026-03-27T01:30:00Z<br>2026-03-28T01:30:00+00:00<br>2026-03-28T01:30:00Z<br>2026-03-28T23:30:00+00:00<br>2026-03-28T23:30:00Z<br>2026-03-30T01:30:00+02:00<br>2026-03-29T23:30:00Z`

- **ice_cube@tz2026a**
  <br>`2026-03-27T01:30:00+00:00<br>2026-03-27T01:30:00Z<br>2026-03-28T01:30:00+00:00<br>2026-03-28T01:30:00Z<br>2026-03-29T01:30:00+00:00<br>2026-03-29T01:30:00Z<br>2026-03-30T01:30:00+00:00<br>2026-03-30T01:30:00Z`


## `RRULE-DST-006` — A monthly recurrence across the Apia date-line jump

*AMBIGUOUS_STANDARD* · family `rrule.dst` · policy axis `rrule.gap`

input:
```
DTSTART;TZID=Pacific/Apia:20111030T120000
RRULE:FREQ=MONTHLY;BYMONTHDAY=30;COUNT=4
```

**5 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2011-10-30T12:00:00-10:00<br>2011-10-30T22:00:00Z<br>2011-11-30T12:00:00-10:00<br>2011-11-30T22:00:00Z<br>2011-12-29T12:00:00-10:00<br>2011-12-29T22:00:00Z<br>2012-01-30T12:00:00+14:00<br>2012-01-29T22:00:00Z`

- **python-dateutil@tz2026a, python-dateutil@tz2026c**
  <br>`2011-10-30T12:00:00-10:00<br>2011-10-30T22:00:00Z<br>2011-11-30T12:00:00-10:00<br>2011-11-30T22:00:00Z<br>2011-12-30T12:00:00-10:00<br>2011-12-30T22:00:00Z<br>2012-01-30T12:00:00+14:00<br>2012-01-29T22:00:00Z`

- **ice_cube@tz2026a**
  <br>`2011-10-30T12:00:00+00:00<br>2011-10-30T12:00:00Z<br>2011-11-30T12:00:00+00:00<br>2011-11-30T12:00:00Z<br>2011-12-30T12:00:00+00:00<br>2011-12-30T12:00:00Z<br>2012-01-30T12:00:00+00:00<br>2012-01-30T12:00:00Z`

- **php-rrule@tz2026a**
  <br>`2011-10-30T12:00:00-10:00<br>2011-10-30T22:00:00Z<br>2011-11-30T12:00:00-10:00<br>2011-11-30T22:00:00Z<br>2011-12-31T12:00:00+14:00<br>2011-12-30T22:00:00Z<br>2012-01-30T12:00:00+14:00<br>2012-01-29T22:00:00Z`


## `RRULE-SET-002` — RDATE adds an instance outside the RRULE

*NORMATIVE* · family `rrule.sets` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=WEEKLY;COUNT=3
RDATE;TZID=America/New_York:20260107T140000
```

**5 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **php-rrule@tz2026a, rrule-go@tz2026a**
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-07T14:00:00-05:00<br>2026-01-07T19:00:00Z<br>2026-01-12T09:00:00-05:00<br>2026-01-12T14:00:00Z<br>2026-01-19T09:00:00-05:00<br>2026-01-19T14:00:00Z`

- **python-dateutil@tz2026a, python-dateutil@tz2026c** → admissible case `rejected`
  <br>`ERROR`

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-07T14:00:00+00:00<br>2026-01-07T14:00:00Z<br>2026-01-12T09:00:00+00:00<br>2026-01-12T09:00:00Z<br>2026-01-19T09:00:00+00:00<br>2026-01-19T09:00:00Z`

- **rrule.js@tzle2026a**
  <br>`2026-01-07T14:00:00-05:00<br>2026-01-07T19:00:00Z<br>2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-12T09:00:00-05:00<br>2026-01-12T14:00:00Z<br>2026-01-19T09:00:00-05:00<br>2026-01-19T14:00:00Z`


## `RRULE-SET-007` — Duplicate instants from RRULE and RDATE are coalesced

*NORMATIVE* · family `rrule.sets` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=DAILY;COUNT=3
RDATE;TZID=America/New_York:20260106T090000
```

**5 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **php-rrule@tz2026a, rrule-go@tz2026a**
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-06T09:00:00-05:00<br>2026-01-06T14:00:00Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z`

- **python-dateutil@tz2026a, python-dateutil@tz2026c** → admissible case `rejected`
  <br>`ERROR`

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-06T09:00:00+00:00<br>2026-01-06T09:00:00Z<br>2026-01-07T09:00:00+00:00<br>2026-01-07T09:00:00Z`

- **rrule.js@tzle2026a**
  <br>`2026-01-06T09:00:00-05:00<br>2026-01-06T14:00:00Z<br>2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z`


## `RRULE-SET-008` — Two RRULEs in one component

*AMBIGUOUS_STANDARD* · family `rrule.sets` · policy axis `rrule.multiple_rrule`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=2
RRULE:FREQ=WEEKLY;BYDAY=WE;COUNT=2
```

**5 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c** → admissible case `union`
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z<br>2026-01-12T09:00:00-05:00<br>2026-01-12T14:00:00Z<br>2026-01-14T09:00:00-05:00<br>2026-01-14T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-07T09:00:00+00:00<br>2026-01-07T09:00:00Z<br>2026-01-12T09:00:00+00:00<br>2026-01-12T09:00:00Z<br>2026-01-14T09:00:00+00:00<br>2026-01-14T09:00:00Z`

- **rrule.js@tzle2026a**
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-12T09:00:00-05:00<br>2026-01-12T14:00:00Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z<br>2026-01-14T09:00:00-05:00<br>2026-01-14T14:00:00Z`

- **rrule-go@tz2026a**
  <br>`2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z<br>2026-01-14T09:00:00-05:00<br>2026-01-14T14:00:00Z`


## `RRULE-SET-014` — RDATE and RRULE producing instants one second apart

*NORMATIVE* · family `rrule.sets` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=DAILY;COUNT=3
RDATE;TZID=America/New_York:20260106T090001
```

**5 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **php-rrule@tz2026a, rrule-go@tz2026a**
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-06T09:00:00-05:00<br>2026-01-06T14:00:00Z<br>2026-01-06T09:00:01-05:00<br>2026-01-06T14:00:01Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z`

- **python-dateutil@tz2026a, python-dateutil@tz2026c** → admissible case `rejected`
  <br>`ERROR`

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-06T09:00:00+00:00<br>2026-01-06T09:00:00Z<br>2026-01-06T09:00:01+00:00<br>2026-01-06T09:00:01Z<br>2026-01-07T09:00:00+00:00<br>2026-01-07T09:00:00Z`

- **rrule.js@tzle2026a**
  <br>`2026-01-06T09:00:01-05:00<br>2026-01-06T14:00:01Z<br>2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-06T09:00:00-05:00<br>2026-01-06T14:00:00Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z`


## `CRON-DAYF-002` — crontab(5)'s own worked example (1st and 15th, plus every Friday)

*DIALECT_DEPENDENT* · family `cron.day-fields` · policy axis `cron.dom_dow`

input: `30 4 1,15 * 5` from `2026-01-01T00:00:00` zone `None` × 8

**4 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croniter@tz2026a, croniter@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `or/vixie`
  <br>`2026-01-01T04:30:00<br>2026-01-02T04:30:00<br>2026-01-09T04:30:00<br>2026-01-15T04:30:00<br>2026-01-16T04:30:00<br>2026-01-23T04:30:00<br>2026-01-30T04:30:00<br>2026-02-01T04:30:00`

- **croner[legacyMode=false]@tzle2026a, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c** → admissible case `and`
  <br>`2026-05-01T04:30:00<br>2026-05-15T04:30:00<br>2027-01-01T04:30:00<br>2027-01-15T04:30:00<br>2027-10-01T04:30:00<br>2027-10-15T04:30:00<br>2028-09-01T04:30:00<br>2028-09-15T04:30:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c** → admissible case `and+monday-zero`
  <br>`2026-08-01T04:30:00<br>2026-08-15T04:30:00<br>2027-05-01T04:30:00<br>2027-05-15T04:30:00<br>2028-01-01T04:30:00<br>2028-01-15T04:30:00<br>2028-04-01T04:30:00<br>2028-04-15T04:30:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-DAYF-006` — The 'first Monday' idiom written naively (a DOM/DOW trap)

*DIALECT_DEPENDENT* · family `cron.day-fields` · policy axis `cron.dom_dow`

input: `0 6 1-7 * 1` from `2026-01-01T00:00:00` zone `None` × 8

**4 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croniter@tz2026a, croniter@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `or/vixie`
  <br>`2026-01-01T06:00:00<br>2026-01-02T06:00:00<br>2026-01-03T06:00:00<br>2026-01-04T06:00:00<br>2026-01-05T06:00:00<br>2026-01-06T06:00:00<br>2026-01-07T06:00:00<br>2026-01-12T06:00:00`

- **croner[legacyMode=false]@tzle2026a, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c** → admissible case `and`
  <br>`2026-01-05T06:00:00<br>2026-02-02T06:00:00<br>2026-03-02T06:00:00<br>2026-04-06T06:00:00<br>2026-05-04T06:00:00<br>2026-06-01T06:00:00<br>2026-07-06T06:00:00<br>2026-08-03T06:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c** → admissible case `and+monday-zero`
  <br>`2026-01-06T06:00:00<br>2026-02-03T06:00:00<br>2026-03-03T06:00:00<br>2026-04-07T06:00:00<br>2026-05-05T06:00:00<br>2026-06-02T06:00:00<br>2026-07-07T06:00:00<br>2026-08-04T06:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-DAYF-010` — DOM_STAR first-character artefact: 0 12 *,10 * 2

*KNOWN_DIVERGENCE* · family `cron.day-fields` · policy axis `cron.dom_dow`

input: `0 12 *,10 * 2` from `2026-01-01T00:00:00` zone `None` × 6

**4 distinct answers:**

- **croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, robfig-cron@tz2026a** → admissible case `vixie-artefact`
  <br>`2026-01-06T12:00:00<br>2026-01-13T12:00:00<br>2026-01-20T12:00:00<br>2026-01-27T12:00:00<br>2026-02-03T12:00:00<br>2026-02-10T12:00:00`

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **croner@tzle2026a, php-cron-expression@tz2026a** → admissible case `or-any-nonstar`
  <br>`2026-01-01T12:00:00<br>2026-01-02T12:00:00<br>2026-01-03T12:00:00<br>2026-01-04T12:00:00<br>2026-01-05T12:00:00<br>2026-01-06T12:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c** → admissible case `and+monday-zero`
  <br>`2026-01-07T12:00:00<br>2026-01-14T12:00:00<br>2026-01-21T12:00:00<br>2026-01-28T12:00:00<br>2026-02-04T12:00:00<br>2026-02-11T12:00:00`


## `CRON-DAYF-011` — DOM_STAR first-character artefact: 0 12 10,* * 2

*KNOWN_DIVERGENCE* · family `cron.day-fields` · policy axis `cron.dom_dow`

input: `0 12 10,* * 2` from `2026-01-01T00:00:00` zone `None` × 6

**4 distinct answers:**

- **croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a, robfig-cron@tz2026a** → admissible case `or-set-semantics`
  <br>`2026-01-06T12:00:00<br>2026-01-13T12:00:00<br>2026-01-20T12:00:00<br>2026-01-27T12:00:00<br>2026-02-03T12:00:00<br>2026-02-10T12:00:00`

- **croner@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, php-cron-expression@tz2026a** → admissible case `vixie-artefact`
  <br>`2026-01-01T12:00:00<br>2026-01-02T12:00:00<br>2026-01-03T12:00:00<br>2026-01-04T12:00:00<br>2026-01-05T12:00:00<br>2026-01-06T12:00:00`

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **apscheduler3@tz2026a, apscheduler3@tz2026c** → admissible case `and+monday-zero`
  <br>`2026-01-07T12:00:00<br>2026-01-14T12:00:00<br>2026-01-21T12:00:00<br>2026-01-28T12:00:00<br>2026-02-04T12:00:00<br>2026-02-11T12:00:00`


## `CRON-DAYF-012` — DOM_STAR first-character artefact: 0 12 1-31 * 2

*KNOWN_DIVERGENCE* · family `cron.day-fields` · policy axis `cron.dom_dow`

input: `0 12 1-31 * 2` from `2026-01-01T00:00:00` zone `None` × 6

**4 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croniter@tz2026a, croniter@tz2026c, cronsim@tz2026a, cronsim@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `vixie-artefact`
  <br>`2026-01-01T12:00:00<br>2026-01-02T12:00:00<br>2026-01-03T12:00:00<br>2026-01-04T12:00:00<br>2026-01-05T12:00:00<br>2026-01-06T12:00:00`

- **croner[legacyMode=false]@tzle2026a, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a** → admissible case `or-set-semantics`
  <br>`2026-01-06T12:00:00<br>2026-01-13T12:00:00<br>2026-01-20T12:00:00<br>2026-01-27T12:00:00<br>2026-02-03T12:00:00<br>2026-02-10T12:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c** → admissible case `and+monday-zero`
  <br>`2026-01-07T12:00:00<br>2026-01-14T12:00:00<br>2026-01-21T12:00:00<br>2026-01-28T12:00:00<br>2026-02-04T12:00:00<br>2026-02-11T12:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-DOW-011` — Named range with a step: MON-FRI/2

*DIALECT_DEPENDENT* · family `cron.names` · policy axis `cron.step_on_named_range`

input: `0 12 * * MON-FRI/2` from `2026-01-01T00:00:00` zone `None` × 6

**4 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, robfig-cron@tz2026a** → admissible case `accept`
  <br>`2026-01-02T12:00:00<br>2026-01-05T12:00:00<br>2026-01-07T12:00:00<br>2026-01-09T12:00:00<br>2026-01-12T12:00:00<br>2026-01-14T12:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-01-01T12:00:00<br>2026-01-02T12:00:00<br>2026-01-05T12:00:00<br>2026-01-06T12:00:00<br>2026-01-07T12:00:00<br>2026-01-08T12:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **php-cron-expression@tz2026a**
  <br>`2026-01-04T12:00:00<br>2026-01-11T12:00:00<br>2026-01-18T12:00:00<br>2026-01-25T12:00:00<br>2026-02-01T12:00:00<br>2026-02-08T12:00:00`


## `CRON-DST-004` — 30-minute fold (Lord Howe Island): 01:45 daily

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `45 1 * * *` from `2026-04-03T00:00:00` zone `Australia/Lord_Howe` × 4

**4 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `fold_both`
  <br>`2026-04-03T01:45:00+11:00<br>2026-04-02T14:45:00Z<br>2026-04-04T01:45:00+11:00<br>2026-04-03T14:45:00Z<br>2026-04-05T01:45:00+11:00<br>2026-04-04T14:45:00Z<br>2026-04-05T01:45:00+10:30<br>2026-04-04T15:15:00Z`

- **cron-parser@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a** → admissible case `skip`
  <br>`2026-04-03T01:45:00+11:00<br>2026-04-02T14:45:00Z<br>2026-04-04T01:45:00+11:00<br>2026-04-03T14:45:00Z<br>2026-04-05T01:45:00+11:00<br>2026-04-04T14:45:00Z<br>2026-04-06T01:45:00+10:30<br>2026-04-05T15:15:00Z`

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a** → admissible case `fold_second`
  <br>`2026-04-03T01:45:00+11:00<br>2026-04-02T14:45:00Z<br>2026-04-04T01:45:00+11:00<br>2026-04-03T14:45:00Z<br>2026-04-05T01:45:00+10:30<br>2026-04-04T15:15:00Z<br>2026-04-06T01:45:00+10:30<br>2026-04-05T15:15:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-006` — Two-hour fold (Antarctica/Troll): 01:30 daily

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 1 * * *` from `2026-10-24T00:00:00` zone `Antarctica/Troll` × 4

**4 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a** → admissible case `skip`
  <br>`2026-10-24T01:30:00+02:00<br>2026-10-23T23:30:00Z<br>2026-10-25T01:30:00+02:00<br>2026-10-24T23:30:00Z<br>2026-10-26T01:30:00+00:00<br>2026-10-26T01:30:00Z<br>2026-10-27T01:30:00+00:00<br>2026-10-27T01:30:00Z`

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, robfig-cron@tz2026a** → admissible case `fold_both`
  <br>`2026-10-24T01:30:00+02:00<br>2026-10-23T23:30:00Z<br>2026-10-25T01:30:00+02:00<br>2026-10-24T23:30:00Z<br>2026-10-25T01:30:00+00:00<br>2026-10-25T01:30:00Z<br>2026-10-26T01:30:00+00:00<br>2026-10-26T01:30:00Z`

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a** → admissible case `fold_second`
  <br>`2026-10-24T01:30:00+02:00<br>2026-10-23T23:30:00Z<br>2026-10-25T01:30:00+00:00<br>2026-10-25T01:30:00Z<br>2026-10-26T01:30:00+00:00<br>2026-10-26T01:30:00Z<br>2026-10-27T01:30:00+00:00<br>2026-10-27T01:30:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-016` — Hourly schedule across the fold: how many 01:00s?

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `0 * * * *` from `2026-11-01T00:00:00` zone `America/New_York` × 6

**4 distinct answers:**

- **cron-parser@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `fold_both`
  <br>`2026-11-01T01:00:00-04:00<br>2026-11-01T05:00:00Z<br>2026-11-01T01:00:00-05:00<br>2026-11-01T06:00:00Z<br>2026-11-01T02:00:00-05:00<br>2026-11-01T07:00:00Z<br>2026-11-01T03:00:00-05:00<br>2026-11-01T08:00:00Z`

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a, fugit@tz2026a** → admissible case `skip`
  <br>`2026-11-01T01:00:00-04:00<br>2026-11-01T05:00:00Z<br>2026-11-01T02:00:00-05:00<br>2026-11-01T07:00:00Z<br>2026-11-01T03:00:00-05:00<br>2026-11-01T08:00:00Z<br>2026-11-01T04:00:00-05:00<br>2026-11-01T09:00:00Z`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-11-01T00:00:00-04:00<br>2026-11-01T04:00:00Z<br>2026-11-01T01:00:00-04:00<br>2026-11-01T05:00:00Z<br>2026-11-01T01:00:00-05:00<br>2026-11-01T06:00:00Z<br>2026-11-01T01:00:00-05:00<br>2026-11-01T06:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-STEP-009` — Step in the day-of-month field: */10 does not mean every 10 days

*NORMATIVE* · family `cron.steps` · policy axis `None`

input: `0 0 */10 * *` from `2026-01-01T00:00:00` zone `None` × 8

**4 distinct answers:**

- **cron-parser@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-11T00:00:00<br>2026-01-21T00:00:00<br>2026-01-31T00:00:00<br>2026-02-01T00:00:00<br>2026-02-11T00:00:00<br>2026-02-21T00:00:00<br>2026-03-01T00:00:00<br>2026-03-11T00:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-01-01T00:00:00<br>2026-01-11T00:00:00<br>2026-01-21T00:00:00<br>2026-01-31T00:00:00<br>2026-02-01T00:00:00<br>2026-02-11T00:00:00<br>2026-02-21T00:00:00<br>2026-03-01T00:00:00`

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a**
  <br>`2026-01-11T00:00:00<br>2026-01-21T00:00:00<br>2026-01-31T00:00:00<br>2026-02-01T00:00:00<br>2026-02-11T00:00:00<br>2026-02-21T00:00:00<br>2026-03-11T00:00:00<br>2026-03-21T00:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `RRULE-BY-025` — Numeric BYDAY with FREQ=WEEKLY (forbidden)

*INVALID* · family `rrule.by` · policy axis `None`

input:
```
DTSTART:20260105T090000
RRULE:FREQ=WEEKLY;BYDAY=2MO;COUNT=3
```

**4 distinct answers:**

- **python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-01-05T09:00:00<br>2026-01-12T09:00:00<br>2026-01-19T09:00:00`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-12T09:00:00<br>2026-02-09T09:00:00<br>2026-03-09T09:00:00`

- **php-rrule@tz2026a**
  <br>`ERROR`


## `RRULE-BY-032` — BYMONTHDAY=32

*INVALID* · family `rrule.by` · policy axis `None`

input:
```
DTSTART:20260101T090000
RRULE:FREQ=MONTHLY;BYMONTHDAY=32;COUNT=1
```

**4 distinct answers:**

- **python-dateutil@tz2026a, python-dateutil@tz2026c, rrule.js@tzle2026a**
  <br>`EMPTY`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **php-rrule@tz2026a, rrule-go@tz2026a**
  <br>`ERROR`

- **ice_cube@tz2026a**
  <br>`HANG`


## `RRULE-CORE-006` — UNTIL one second before an instance excludes it

*NORMATIVE* · family `rrule.core` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=DAILY;UNTIL=19970904T125959Z
```

**4 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-03T09:00:00-04:00<br>1997-09-03T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-02T09:00:00+00:00<br>1997-09-02T09:00:00Z<br>1997-09-03T09:00:00+00:00<br>1997-09-03T09:00:00Z<br>1997-09-04T09:00:00+00:00<br>1997-09-04T09:00:00Z`

- **rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-03T09:00:00-04:00<br>1997-09-03T13:00:00Z<br>1997-09-04T09:00:00-04:00<br>1997-09-04T13:00:00Z`


## `RRULE-CORE-007` — UNTIL must be UTC when DTSTART carries a TZID (erratum 3883's example, corrected)

*NORMATIVE* · family `rrule.core` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=HOURLY;INTERVAL=3;UNTIL=19970902T210000Z
```

**4 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-02T12:00:00-04:00<br>1997-09-02T16:00:00Z<br>1997-09-02T15:00:00-04:00<br>1997-09-02T19:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-02T09:00:00+00:00<br>1997-09-02T09:00:00Z<br>1997-09-02T12:00:00+00:00<br>1997-09-02T12:00:00Z<br>1997-09-02T15:00:00+00:00<br>1997-09-02T15:00:00Z<br>1997-09-02T18:00:00+00:00<br>1997-09-02T18:00:00Z`

- **rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-02T12:00:00-04:00<br>1997-09-02T16:00:00Z<br>1997-09-02T15:00:00-04:00<br>1997-09-02T19:00:00Z<br>1997-09-02T18:00:00-04:00<br>1997-09-02T22:00:00Z`


## `RRULE-CORE-008` — The uncorrected erratum-3883 example (UNTIL=...T170000Z)

*NORMATIVE* · family `rrule.core` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=HOURLY;INTERVAL=3;UNTIL=19970902T170000Z
```

**4 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-02T12:00:00-04:00<br>1997-09-02T16:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-02T09:00:00+00:00<br>1997-09-02T09:00:00Z<br>1997-09-02T12:00:00+00:00<br>1997-09-02T12:00:00Z<br>1997-09-02T15:00:00+00:00<br>1997-09-02T15:00:00Z`

- **rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-02T12:00:00-04:00<br>1997-09-02T16:00:00Z<br>1997-09-02T15:00:00-04:00<br>1997-09-02T19:00:00Z`


## `RRULE-CORE-011` — COUNT and UNTIL in the same RRULE (forbidden)

*INVALID* · family `rrule.core` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=DAILY;COUNT=10;UNTIL=19970904T130000Z
```

**4 distinct answers:**

- **python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-03T09:00:00-04:00<br>1997-09-03T13:00:00Z<br>1997-09-04T09:00:00-04:00<br>1997-09-04T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-02T09:00:00+00:00<br>1997-09-02T09:00:00Z<br>1997-09-03T09:00:00+00:00<br>1997-09-03T09:00:00Z<br>1997-09-04T09:00:00+00:00<br>1997-09-04T09:00:00Z`

- **php-rrule@tz2026a**
  <br>`ERROR`


## `RRULE-CORE-016` — INTERVAL=0

*INVALID* · family `rrule.core` · policy axis `None`

input:
```
DTSTART:19970902T090000
RRULE:FREQ=DAILY;INTERVAL=0;COUNT=3
```

**4 distinct answers:**

- **ice_cube@tz2026a, pandas@tz2026a, pandas@tz2026c, php-rrule@tz2026a**
  <br>`ERROR`

- **python-dateutil@tz2026a, python-dateutil@tz2026c**
  <br>`1997-09-02T09:00:00`

- **rrule-go@tz2026a**
  <br>`1997-09-02T09:00:00<br>1997-09-03T09:00:00<br>1997-09-04T09:00:00`

- **rrule.js@tzle2026a**
  <br>`EMPTY`


## `RRULE-DST-010` — Hourly recurrence across the gap: 23-hour day

*NORMATIVE* · family `rrule.dst` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260308T000000
RRULE:FREQ=HOURLY;COUNT=5
```

**4 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c, rrule.js@tzle2026a**
  <br>`2026-03-08T00:00:00-05:00<br>2026-03-08T05:00:00Z<br>2026-03-08T01:00:00-05:00<br>2026-03-08T06:00:00Z<br>2026-03-08T03:00:00-04:00<br>2026-03-08T07:00:00Z<br>2026-03-08T04:00:00-04:00<br>2026-03-08T08:00:00Z`

- **python-dateutil@tz2026a, python-dateutil@tz2026c**
  <br>`2026-03-08T00:00:00-05:00<br>2026-03-08T05:00:00Z<br>2026-03-08T01:00:00-05:00<br>2026-03-08T06:00:00Z<br>2026-03-08T02:00:00-04:00<br>2026-03-08T06:00:00Z<br>2026-03-08T03:00:00-04:00<br>2026-03-08T07:00:00Z`

- **php-rrule@tz2026a, rrule-go@tz2026a**
  <br>`2026-03-08T00:00:00-05:00<br>2026-03-08T05:00:00Z<br>2026-03-08T01:00:00-05:00<br>2026-03-08T06:00:00Z<br>2026-03-08T03:00:00-04:00<br>2026-03-08T07:00:00Z<br>2026-03-08T04:00:00-04:00<br>2026-03-08T08:00:00Z`

- **ice_cube@tz2026a**
  <br>`2026-03-08T00:00:00+00:00<br>2026-03-08T00:00:00Z<br>2026-03-08T01:00:00+00:00<br>2026-03-08T01:00:00Z<br>2026-03-08T02:00:00+00:00<br>2026-03-08T02:00:00Z<br>2026-03-08T03:00:00+00:00<br>2026-03-08T03:00:00Z`


## `RRULE-SET-003` — EXDATE takes precedence over RDATE for the same instant

*NORMATIVE* · family `rrule.sets` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=WEEKLY;COUNT=2
RDATE;TZID=America/New_York:20260107T140000
EXDATE;TZID=America/New_York:20260107T140000
```

**4 distinct answers:**

- **php-rrule@tz2026a, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-12T09:00:00-05:00<br>2026-01-12T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **python-dateutil@tz2026a, python-dateutil@tz2026c** → admissible case `rejected`
  <br>`ERROR`

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-12T09:00:00+00:00<br>2026-01-12T09:00:00Z`


## `RRULE-SET-004` — EXDATE with VALUE=DATE against a DATE-TIME DTSTART (erratum 6316, open since 2020)

*AMBIGUOUS_STANDARD* · family `rrule.sets` · policy axis `rrule.exdate_value_type`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=HOURLY;INTERVAL=6;COUNT=8
EXDATE;VALUE=DATE:20260106
```

**4 distinct answers:**

- **php-rrule@tz2026a, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `exclude-midnight-only`
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-05T15:00:00-05:00<br>2026-01-05T20:00:00Z<br>2026-01-05T21:00:00-05:00<br>2026-01-06T02:00:00Z<br>2026-01-06T03:00:00-05:00<br>2026-01-06T08:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **python-dateutil@tz2026a, python-dateutil@tz2026c** → admissible case `reject`
  <br>`ERROR`

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-05T15:00:00+00:00<br>2026-01-05T15:00:00Z<br>2026-01-05T21:00:00+00:00<br>2026-01-05T21:00:00Z<br>2026-01-06T03:00:00+00:00<br>2026-01-06T03:00:00Z`


## `RRULE-SET-006` — EXDATE in a different zone naming the same instant

*AMBIGUOUS_STANDARD* · family `rrule.sets` · policy axis `rrule.exdate_matching`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=DAILY;COUNT=3
EXDATE;TZID=Europe/London:20260106T140000
```

**4 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a** → admissible case `instant-match`
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-06T09:00:00+00:00<br>2026-01-06T09:00:00Z<br>2026-01-07T09:00:00+00:00<br>2026-01-07T09:00:00Z`

- **rrule.js@tzle2026a** → admissible case `wall-time-match`
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-06T09:00:00-05:00<br>2026-01-06T14:00:00Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z`


## `RRULE-SET-010` — EXRULE (removed from RFC 5545, present in RFC 2445)

*DIALECT_DEPENDENT* · family `rrule.sets` · policy axis `rrule.exrule`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=DAILY;COUNT=10
EXRULE:FREQ=WEEKLY;BYDAY=SA,SU
```

**4 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule.js@tzle2026a** → admissible case `rfc2445`
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-06T09:00:00-05:00<br>2026-01-06T14:00:00Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z<br>2026-01-08T09:00:00-05:00<br>2026-01-08T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-06T09:00:00+00:00<br>2026-01-06T09:00:00Z<br>2026-01-07T09:00:00+00:00<br>2026-01-07T09:00:00Z<br>2026-01-08T09:00:00+00:00<br>2026-01-08T09:00:00Z`

- **rrule-go@tz2026a**
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-06T09:00:00-05:00<br>2026-01-06T14:00:00Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z<br>2026-01-08T09:00:00-05:00<br>2026-01-08T14:00:00Z`


## `RRULE-SET-011` — RDATE with a PERIOD value

*DIALECT_DEPENDENT* · family `rrule.sets` · policy axis `rrule.rdate_period`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=WEEKLY;COUNT=2
RDATE;VALUE=PERIOD:20260107T140000Z/PT1H
```

**4 distinct answers:**

- **python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `reject`
  <br>`ERROR`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-07T14:00:00+00:00<br>2026-01-07T14:00:00Z<br>2026-01-12T09:00:00+00:00<br>2026-01-12T09:00:00Z`

- **php-rrule@tz2026a**
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-12T09:00:00-05:00<br>2026-01-12T14:00:00Z`


## `RRULE-SET-012` — RDATE before DTSTART

*AMBIGUOUS_STANDARD* · family `rrule.sets` · policy axis `rrule.rdate_before_dtstart`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=WEEKLY;COUNT=2
RDATE;TZID=America/New_York:20251229T090000
```

**4 distinct answers:**

- **php-rrule@tz2026a, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `include`
  <br>`2025-12-29T09:00:00-05:00<br>2025-12-29T14:00:00Z<br>2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-12T09:00:00-05:00<br>2026-01-12T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **python-dateutil@tz2026a, python-dateutil@tz2026c** → admissible case `reject`
  <br>`ERROR`

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-12T09:00:00+00:00<br>2026-01-12T09:00:00Z`


## `CRON-ANCH-001` — Start instant exactly on an occurrence: inclusive or exclusive?

*POLICY_DEPENDENT* · family `cron.anchoring` · policy axis `cron.start_inclusivity`

input: `0 12 * * *` from `2026-01-01T12:00:00` zone `None` × 3

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `exclusive`
  <br>`2026-01-02T12:00:00<br>2026-01-03T12:00:00<br>2026-01-04T12:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c** → admissible case `inclusive`
  <br>`2026-01-01T12:00:00<br>2026-01-02T12:00:00<br>2026-01-03T12:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-ANCH-003` — Sub-minute start instant, seconds-granularity expression

*POLICY_DEPENDENT* · family `cron.anchoring` · policy axis `cron.start_truncation`

input: `30 * * * * *` from `2026-01-01T12:00:15` zone `None` × 3

**3 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `exact`
  <br>`2026-01-01T12:00:30<br>2026-01-01T12:01:30<br>2026-01-01T12:02:30`

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c**
  <br>`2026-01-01T12:30:00<br>2026-01-01T12:30:01<br>2026-01-01T12:30:02`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-ANCH-004` — Cron has no anchor: '*/7' in the day field restarts each month

*NORMATIVE* · family `cron.anchoring` · policy axis `None`

input: `0 0 */7 * *` from `2026-01-01T00:00:00` zone `None` × 10

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-08T00:00:00<br>2026-01-15T00:00:00<br>2026-01-22T00:00:00<br>2026-01-29T00:00:00<br>2026-02-01T00:00:00<br>2026-02-08T00:00:00<br>2026-02-15T00:00:00<br>2026-02-22T00:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-01-01T00:00:00<br>2026-01-08T00:00:00<br>2026-01-15T00:00:00<br>2026-01-22T00:00:00<br>2026-01-29T00:00:00<br>2026-02-01T00:00:00<br>2026-02-08T00:00:00<br>2026-02-15T00:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DAYF-001` — Friday the 13th: the canonical DOM/DOW collision

*DIALECT_DEPENDENT* · family `cron.day-fields` · policy axis `cron.dom_dow`

input: `0 12 13 * FRI` from `2026-01-01T00:00:00` zone `None` × 6

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croniter@tz2026a, croniter@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `or/vixie`
  <br>`2026-01-02T12:00:00<br>2026-01-09T12:00:00<br>2026-01-13T12:00:00<br>2026-01-16T12:00:00<br>2026-01-23T12:00:00<br>2026-01-30T12:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, croner[legacyMode=false]@tzle2026a, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c** → admissible case `and`
  <br>`2026-02-13T12:00:00<br>2026-03-13T12:00:00<br>2026-11-13T12:00:00<br>2027-08-13T12:00:00<br>2028-10-13T12:00:00<br>2029-04-13T12:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-DAYF-003` — dcron's own worked example, read by four dialects

*DIALECT_DEPENDENT* · family `cron.day-fields` · policy axis `cron.dom_dow`

input: `0 11 1,5 * mon-wed` from `2026-01-01T00:00:00` zone `None` × 8

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croniter@tz2026a, croniter@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `or/vixie`
  <br>`2026-01-01T11:00:00<br>2026-01-05T11:00:00<br>2026-01-06T11:00:00<br>2026-01-07T11:00:00<br>2026-01-12T11:00:00<br>2026-01-13T11:00:00<br>2026-01-14T11:00:00<br>2026-01-19T11:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, croner[legacyMode=false]@tzle2026a, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c** → admissible case `and`
  <br>`2026-01-05T11:00:00<br>2026-04-01T11:00:00<br>2026-05-05T11:00:00<br>2026-06-01T11:00:00<br>2026-07-01T11:00:00<br>2026-08-05T11:00:00<br>2026-09-01T11:00:00<br>2026-10-05T11:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-DAYF-004` — Single DOM element with a single DOW element

*DIALECT_DEPENDENT* · family `cron.day-fields` · policy axis `cron.dom_dow`

input: `0 0 1 * SUN` from `2026-01-01T00:00:00` zone `None` × 6

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croniter@tz2026a, croniter@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `or/vixie`
  <br>`2026-01-04T00:00:00<br>2026-01-11T00:00:00<br>2026-01-18T00:00:00<br>2026-01-25T00:00:00<br>2026-02-01T00:00:00<br>2026-02-08T00:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, croner[legacyMode=false]@tzle2026a, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c** → admissible case `and`
  <br>`2026-02-01T00:00:00<br>2026-03-01T00:00:00<br>2026-11-01T00:00:00<br>2027-08-01T00:00:00<br>2028-10-01T00:00:00<br>2029-04-01T00:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-DAYF-005` — Range DOM with a single DOW: month-end or Monday

*DIALECT_DEPENDENT* · family `cron.day-fields` · policy axis `cron.dom_dow`

input: `0 0 29-31 * MON` from `2026-01-01T00:00:00` zone `None` × 8

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croniter@tz2026a, croniter@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `or/vixie`
  <br>`2026-01-05T00:00:00<br>2026-01-12T00:00:00<br>2026-01-19T00:00:00<br>2026-01-26T00:00:00<br>2026-01-29T00:00:00<br>2026-01-30T00:00:00<br>2026-01-31T00:00:00<br>2026-02-02T00:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, croner[legacyMode=false]@tzle2026a, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c** → admissible case `and`
  <br>`2026-03-30T00:00:00<br>2026-06-29T00:00:00<br>2026-08-31T00:00:00<br>2026-11-30T00:00:00<br>2027-03-29T00:00:00<br>2027-05-31T00:00:00<br>2027-08-30T00:00:00<br>2027-11-29T00:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-DAYF-013` — The '*/100,1-7 * MON' first-Monday idiom weaponising the artefact

*KNOWN_DIVERGENCE* · family `cron.day-fields` · policy axis `cron.dom_dow`

input: `0 0 */100,1-7 * MON` from `2026-01-01T00:00:00` zone `None` × 6

**3 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, fugit@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject-step`
  <br>`ERROR`

- **croniter@tz2026a, croniter@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-02T00:00:00<br>2026-01-03T00:00:00<br>2026-01-04T00:00:00<br>2026-01-05T00:00:00<br>2026-01-06T00:00:00<br>2026-01-07T00:00:00`

- **croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c** → admissible case `vixie-artefact`
  <br>`2026-01-05T00:00:00<br>2026-02-02T00:00:00<br>2026-03-02T00:00:00<br>2026-04-06T00:00:00<br>2026-05-04T00:00:00<br>2026-06-01T00:00:00`


## `CRON-DOW-001` — Day-of-week 0

*DIALECT_DEPENDENT* · family `cron.dow-numbering` · policy axis `cron.dow_numbering`

input: `0 12 * * 0` from `2026-01-01T00:00:00` zone `None` × 4

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `vixie-both`
  <br>`2026-01-04T12:00:00<br>2026-01-11T12:00:00<br>2026-01-18T12:00:00<br>2026-01-25T12:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c** → admissible case `monday-zero`
  <br>`2026-01-05T12:00:00<br>2026-01-12T12:00:00<br>2026-01-19T12:00:00<br>2026-01-26T12:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `quartz-1-7`
  <br>`ERROR`


## `CRON-DOW-007` — Non-wrapping named day range SAT-SUN

*NORMATIVE* · family `cron.dow-numbering` · policy axis `cron.range_wrap`

input: `0 12 * * SAT-SUN` from `2026-01-01T00:00:00` zone `None` × 6

**3 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a** → admissible case `wrap-modulo`
  <br>`2026-01-03T12:00:00<br>2026-01-04T12:00:00<br>2026-01-10T12:00:00<br>2026-01-11T12:00:00<br>2026-01-17T12:00:00<br>2026-01-18T12:00:00`

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject-reversed`
  <br>`ERROR`

- **php-cron-expression@tz2026a**
  <br>`2026-01-03T12:00:00<br>2026-01-10T12:00:00<br>2026-01-17T12:00:00<br>2026-01-24T12:00:00<br>2026-01-31T12:00:00<br>2026-02-07T12:00:00`


## `CRON-DOW-013` — Numeric and named spellings of the same weekday must agree (0 vs SUN)

*NORMATIVE* · family `cron.dow-numbering` · policy axis `None`

input: `0 12 * * 0` from `2026-01-01T00:00:00` zone `None` × 3

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-04T12:00:00<br>2026-01-11T12:00:00<br>2026-01-18T12:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-01-05T12:00:00<br>2026-01-12T12:00:00<br>2026-01-19T12:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-002` — Autumn fold: 01:30 daily across the US DST end

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 1 * * *` from `2026-10-30T00:00:00` zone `America/New_York` × 4

**3 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `fold_both`
  <br>`2026-10-30T01:30:00-04:00<br>2026-10-30T05:30:00Z<br>2026-10-31T01:30:00-04:00<br>2026-10-31T05:30:00Z<br>2026-11-01T01:30:00-04:00<br>2026-11-01T05:30:00Z<br>2026-11-01T01:30:00-05:00<br>2026-11-01T06:30:00Z`

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a** → admissible case `skip`
  <br>`2026-10-30T01:30:00-04:00<br>2026-10-30T05:30:00Z<br>2026-10-31T01:30:00-04:00<br>2026-10-31T05:30:00Z<br>2026-11-01T01:30:00-04:00<br>2026-11-01T05:30:00Z<br>2026-11-02T01:30:00-05:00<br>2026-11-02T06:30:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-017` — Half-hourly schedule across the gap: how many firings?

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `*/30 * * * *` from `2026-03-08T00:00:00` zone `America/New_York` × 8

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-03-08T00:30:00-05:00<br>2026-03-08T05:30:00Z<br>2026-03-08T01:00:00-05:00<br>2026-03-08T06:00:00Z<br>2026-03-08T01:30:00-05:00<br>2026-03-08T06:30:00Z<br>2026-03-08T03:00:00-04:00<br>2026-03-08T07:00:00Z`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-03-08T00:00:00-05:00<br>2026-03-08T05:00:00Z<br>2026-03-08T00:30:00-05:00<br>2026-03-08T05:30:00Z<br>2026-03-08T01:00:00-05:00<br>2026-03-08T06:00:00Z<br>2026-03-08T01:30:00-05:00<br>2026-03-08T06:30:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-018` — Extreme positive offset (+14:00, Pacific/Kiritimati)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `0 0 * * *` from `2026-01-01T00:00:00` zone `Pacific/Kiritimati` × 3

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-01-02T00:00:00+14:00<br>2026-01-01T10:00:00Z<br>2026-01-03T00:00:00+14:00<br>2026-01-02T10:00:00Z<br>2026-01-04T00:00:00+14:00<br>2026-01-03T10:00:00Z`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-01-01T00:00:00+14:00<br>2025-12-31T10:00:00Z<br>2026-01-02T00:00:00+14:00<br>2026-01-01T10:00:00Z<br>2026-01-03T00:00:00+14:00<br>2026-01-02T10:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-019` — Extreme negative offset (-11:00, Pacific/Niue)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `0 0 * * *` from `2026-01-01T00:00:00` zone `Pacific/Niue` × 3

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-01-02T00:00:00-11:00<br>2026-01-02T11:00:00Z<br>2026-01-03T00:00:00-11:00<br>2026-01-03T11:00:00Z<br>2026-01-04T00:00:00-11:00<br>2026-01-04T11:00:00Z`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-01-01T00:00:00-11:00<br>2026-01-01T11:00:00Z<br>2026-01-02T00:00:00-11:00<br>2026-01-02T11:00:00Z<br>2026-01-03T00:00:00-11:00<br>2026-01-03T11:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-EXT-005` — LW: last weekday of the month

*DIALECT_DEPENDENT* · family `cron.extensions` · policy axis `cron.W`

input: `0 9 LW * *` from `2026-01-01T00:00:00` zone `None` × 6

**3 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c** → admissible case `supported`
  <br>`2026-01-30T09:00:00<br>2026-02-27T09:00:00<br>2026-03-31T09:00:00<br>2026-04-30T09:00:00<br>2026-05-29T09:00:00<br>2026-06-30T09:00:00`

- **php-cron-expression@tz2026a**
  <br>`2026-01-31T09:00:00<br>2026-02-02T09:00:00<br>2026-03-02T09:00:00<br>2026-05-30T09:00:00<br>2026-06-01T09:00:00<br>2026-07-30T09:00:00`


## `CRON-EXT-006` — FRI#3: third Friday of the month

*DIALECT_DEPENDENT* · family `cron.extensions` · policy axis `cron.hash`

input: `0 0 9 ? * FRI#3 *` from `2026-01-01T00:00:00` zone `None` × 5

**3 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **croner@tzle2026a**
  <br>`2026-01-01T09:00:00<br>2026-01-02T09:00:00<br>2026-01-03T09:00:00<br>2026-01-04T09:00:00<br>2026-01-05T09:00:00`

- **croner[legacyMode=false]@tzle2026a** → admissible case `supported`
  <br>`2026-01-16T09:00:00<br>2026-02-20T09:00:00<br>2026-03-20T09:00:00<br>2026-04-17T09:00:00<br>2026-05-15T09:00:00`


## `CRON-EXT-007` — SUN#5 in a month with only four Sundays

*DIALECT_DEPENDENT* · family `cron.extensions` · policy axis `cron.hash`

input: `0 0 9 ? * SUN#5 *` from `2026-01-01T00:00:00` zone `None` × 4

**3 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **croner@tzle2026a**
  <br>`2026-01-01T09:00:00<br>2026-01-02T09:00:00<br>2026-01-03T09:00:00<br>2026-01-04T09:00:00`

- **croner[legacyMode=false]@tzle2026a** → admissible case `skip-month`
  <br>`2026-03-29T09:00:00<br>2026-05-31T09:00:00<br>2026-08-30T09:00:00<br>2026-11-29T09:00:00`


## `CRON-EXT-008` — FRIL / 6L: last Friday of the month

*DIALECT_DEPENDENT* · family `cron.extensions` · policy axis `cron.L`

input: `0 0 9 ? * FRIL *` from `2026-01-01T00:00:00` zone `None` × 5

**3 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **croner@tzle2026a**
  <br>`2026-01-01T09:00:00<br>2026-01-02T09:00:00<br>2026-01-03T09:00:00<br>2026-01-04T09:00:00<br>2026-01-05T09:00:00`

- **croner[legacyMode=false]@tzle2026a** → admissible case `supported`
  <br>`2026-01-30T09:00:00<br>2026-02-27T09:00:00<br>2026-03-27T09:00:00<br>2026-04-24T09:00:00<br>2026-05-29T09:00:00`


## `CRON-EXT-009` — '?' in the day-of-month field with a restricted day-of-week

*DIALECT_DEPENDENT* · family `cron.extensions` · policy axis `cron.qmark`

input: `0 0 12 ? * MON *` from `2026-01-01T00:00:00` zone `None` × 4

**3 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **croner@tzle2026a**
  <br>`2026-01-01T12:00:00<br>2026-01-02T12:00:00<br>2026-01-03T12:00:00<br>2026-01-04T12:00:00`

- **croner[legacyMode=false]@tzle2026a** → admissible case `supported`
  <br>`2026-01-05T12:00:00<br>2026-01-12T12:00:00<br>2026-01-19T12:00:00<br>2026-01-26T12:00:00`


## `CRON-FIELDS-002` — Six-field form: is the extra field seconds or year?

*DIALECT_DEPENDENT* · family `cron.field-count` · policy axis `cron.sixth_field`

input: `0 15 10 * * *` from `2026-01-01T00:00:00` zone `None` × 4

**3 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `seconds-leading`
  <br>`2026-01-01T10:15:00<br>2026-01-02T10:15:00<br>2026-01-03T10:15:00<br>2026-01-04T10:15:00`

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c**
  <br>`2026-01-10T15:00:00<br>2026-01-10T15:00:01<br>2026-01-10T15:00:02<br>2026-01-10T15:00:03`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-FIELDS-003` — Seven-field Quartz form with an explicit year

*DIALECT_DEPENDENT* · family `cron.field-count` · policy axis `cron.field_count`

input: `0 0 12 ? * MON 2027` from `2026-01-01T00:00:00` zone `None` × 4

**3 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **croner@tzle2026a**
  <br>`2027-01-01T12:00:00<br>2027-01-02T12:00:00<br>2027-01-03T12:00:00<br>2027-01-04T12:00:00`

- **croner[legacyMode=false]@tzle2026a** → admissible case `quartz7`
  <br>`2027-01-04T12:00:00<br>2027-01-11T12:00:00<br>2027-01-18T12:00:00<br>2027-01-25T12:00:00`


## `CRON-FIELDS-004` — Seconds granularity: every 15 seconds

*DIALECT_DEPENDENT* · family `cron.field-count` · policy axis `cron.seconds`

input: `*/15 * * * * *` from `2026-01-01T00:00:00` zone `None` × 6

**3 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `seconds`
  <br>`2026-01-01T00:00:15<br>2026-01-01T00:00:30<br>2026-01-01T00:00:45<br>2026-01-01T00:01:00<br>2026-01-01T00:01:15<br>2026-01-01T00:01:30`

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c**
  <br>`2026-01-01T00:00:01<br>2026-01-01T00:00:02<br>2026-01-01T00:00:03<br>2026-01-01T00:00:04<br>2026-01-01T00:00:05<br>2026-01-01T00:00:06`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-STEP-001` — */35 in the minute field: step does not mean interval

*NORMATIVE* · family `cron.steps` · policy axis `None`

input: `*/35 * * * *` from `2026-01-01T00:00:00` zone `None` × 6

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-01T00:35:00<br>2026-01-01T01:00:00<br>2026-01-01T01:35:00<br>2026-01-01T02:00:00<br>2026-01-01T02:35:00<br>2026-01-01T03:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-01-01T00:00:00<br>2026-01-01T00:35:00<br>2026-01-01T01:00:00<br>2026-01-01T01:35:00<br>2026-01-01T02:00:00<br>2026-01-01T02:35:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-STEP-004` — Step larger than the field range: */90 in minutes

*DIALECT_DEPENDENT* · family `cron.steps` · policy axis `cron.step_gt_field`

input: `*/90 * * * *` from `2026-01-01T00:00:00` zone `None` × 4

**3 distinct answers:**

- **cron-parser@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, robfig-cron@tz2026a** → admissible case `collapse-to-first`
  <br>`2026-01-01T01:00:00<br>2026-01-01T02:00:00<br>2026-01-01T03:00:00<br>2026-01-01T04:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **php-cron-expression@tz2026a**
  <br>`2026-01-01T00:30:00<br>2026-01-01T01:30:00<br>2026-01-01T02:30:00<br>2026-01-01T03:30:00`


## `CRON-STEP-008` — */1 (identity step)

*NORMATIVE* · family `cron.steps` · policy axis `None`

input: `*/1 * * * *` from `2026-01-01T00:00:00` zone `None` × 3

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-01T00:01:00<br>2026-01-01T00:02:00<br>2026-01-01T00:03:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-01-01T00:00:00<br>2026-01-01T00:01:00<br>2026-01-01T00:02:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-STEP-010` — Comma list mixing a range-step and a literal

*NORMATIVE* · family `cron.steps` · policy axis `None`

input: `0 0-6/2,23 * * *` from `2026-01-01T00:00:00` zone `None` × 6

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-01T02:00:00<br>2026-01-01T04:00:00<br>2026-01-01T06:00:00<br>2026-01-01T23:00:00<br>2026-01-02T00:00:00<br>2026-01-02T02:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-01-01T00:00:00<br>2026-01-01T02:00:00<br>2026-01-01T04:00:00<br>2026-01-01T06:00:00<br>2026-01-01T23:00:00<br>2026-01-02T00:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-STEP-012` — Step applied to a single '*' in the month field

*NORMATIVE* · family `cron.steps` · policy axis `None`

input: `0 0 1 */3 *` from `2026-01-01T00:00:00` zone `None` × 6

**3 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-04-01T00:00:00<br>2026-07-01T00:00:00<br>2026-10-01T00:00:00<br>2027-01-01T00:00:00<br>2027-04-01T00:00:00<br>2027-07-01T00:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c**
  <br>`2026-01-01T00:00:00<br>2026-04-01T00:00:00<br>2026-07-01T00:00:00<br>2026-10-01T00:00:00<br>2027-01-01T00:00:00<br>2027-04-01T00:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `RRULE-BY-001` — Monthly on the first Friday for 10 occurrences (RFC example)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970905T090000
RRULE:FREQ=MONTHLY;COUNT=10;BYDAY=1FR
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-05T09:00:00-04:00<br>1997-09-05T13:00:00Z<br>1997-10-03T09:00:00-04:00<br>1997-10-03T13:00:00Z<br>1997-11-07T09:00:00-05:00<br>1997-11-07T14:00:00Z<br>1997-12-05T09:00:00-05:00<br>1997-12-05T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-05T09:00:00+00:00<br>1997-09-05T09:00:00Z<br>1997-10-03T09:00:00+00:00<br>1997-10-03T09:00:00Z<br>1997-11-07T09:00:00+00:00<br>1997-11-07T09:00:00Z<br>1997-12-05T09:00:00+00:00<br>1997-12-05T09:00:00Z`


## `RRULE-BY-002` — Monthly on the second-to-last Monday (RFC example)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970922T090000
RRULE:FREQ=MONTHLY;BYDAY=-2MO;COUNT=4
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-22T09:00:00-04:00<br>1997-09-22T13:00:00Z<br>1997-10-20T09:00:00-04:00<br>1997-10-20T13:00:00Z<br>1997-11-17T09:00:00-05:00<br>1997-11-17T14:00:00Z<br>1997-12-22T09:00:00-05:00<br>1997-12-22T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-22T09:00:00+00:00<br>1997-09-22T09:00:00Z<br>1997-10-20T09:00:00+00:00<br>1997-10-20T09:00:00Z<br>1997-11-17T09:00:00+00:00<br>1997-11-17T09:00:00Z<br>1997-12-22T09:00:00+00:00<br>1997-12-22T09:00:00Z`


## `RRULE-BY-003` — BYDAY=5SU in months that have only four Sundays

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260101T090000
RRULE:FREQ=MONTHLY;BYDAY=5SU;COUNT=5
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-03-29T09:00:00-04:00<br>2026-03-29T13:00:00Z<br>2026-05-31T09:00:00-04:00<br>2026-05-31T13:00:00Z<br>2026-08-30T09:00:00-04:00<br>2026-08-30T13:00:00Z<br>2026-11-29T09:00:00-05:00<br>2026-11-29T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-03-29T09:00:00+00:00<br>2026-03-29T09:00:00Z<br>2026-05-31T09:00:00+00:00<br>2026-05-31T09:00:00Z<br>2026-08-30T09:00:00+00:00<br>2026-08-30T09:00:00Z<br>2026-11-29T09:00:00+00:00<br>2026-11-29T09:00:00Z`


## `RRULE-BY-004` — BYDAY=-1SU (last Sunday) never skips a month

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260101T090000
RRULE:FREQ=MONTHLY;BYDAY=-1SU;COUNT=5
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-01-25T09:00:00-05:00<br>2026-01-25T14:00:00Z<br>2026-02-22T09:00:00-05:00<br>2026-02-22T14:00:00Z<br>2026-03-29T09:00:00-04:00<br>2026-03-29T13:00:00Z<br>2026-04-26T09:00:00-04:00<br>2026-04-26T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-25T09:00:00+00:00<br>2026-01-25T09:00:00Z<br>2026-02-22T09:00:00+00:00<br>2026-02-22T09:00:00Z<br>2026-03-29T09:00:00+00:00<br>2026-03-29T09:00:00Z<br>2026-04-26T09:00:00+00:00<br>2026-04-26T09:00:00Z`


## `RRULE-BY-005` — BYMONTHDAY=31: months without a 31st are omitted

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260131T090000
RRULE:FREQ=MONTHLY;BYMONTHDAY=31;COUNT=6
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-01-31T09:00:00-05:00<br>2026-01-31T14:00:00Z<br>2026-03-31T09:00:00-04:00<br>2026-03-31T13:00:00Z<br>2026-05-31T09:00:00-04:00<br>2026-05-31T13:00:00Z<br>2026-07-31T09:00:00-04:00<br>2026-07-31T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-31T09:00:00+00:00<br>2026-01-31T09:00:00Z<br>2026-03-31T09:00:00+00:00<br>2026-03-31T09:00:00Z<br>2026-05-31T09:00:00+00:00<br>2026-05-31T09:00:00Z<br>2026-07-31T09:00:00+00:00<br>2026-07-31T09:00:00Z`


## `RRULE-BY-006` — BYMONTHDAY=30: February always omitted

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260130T090000
RRULE:FREQ=MONTHLY;BYMONTHDAY=30;COUNT=5
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-01-30T09:00:00-05:00<br>2026-01-30T14:00:00Z<br>2026-03-30T09:00:00-04:00<br>2026-03-30T13:00:00Z<br>2026-04-30T09:00:00-04:00<br>2026-04-30T13:00:00Z<br>2026-05-30T09:00:00-04:00<br>2026-05-30T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-30T09:00:00+00:00<br>2026-01-30T09:00:00Z<br>2026-03-30T09:00:00+00:00<br>2026-03-30T09:00:00Z<br>2026-04-30T09:00:00+00:00<br>2026-04-30T09:00:00Z<br>2026-05-30T09:00:00+00:00<br>2026-05-30T09:00:00Z`


## `RRULE-BY-007` — BYMONTHDAY=29: February appears only in leap years

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20270129T090000
RRULE:FREQ=MONTHLY;BYMONTHDAY=29;COUNT=14
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2027-01-29T09:00:00-05:00<br>2027-01-29T14:00:00Z<br>2027-03-29T09:00:00-04:00<br>2027-03-29T13:00:00Z<br>2027-04-29T09:00:00-04:00<br>2027-04-29T13:00:00Z<br>2027-05-29T09:00:00-04:00<br>2027-05-29T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2027-01-29T09:00:00+00:00<br>2027-01-29T09:00:00Z<br>2027-03-29T09:00:00+00:00<br>2027-03-29T09:00:00Z<br>2027-04-29T09:00:00+00:00<br>2027-04-29T09:00:00Z<br>2027-05-29T09:00:00+00:00<br>2027-05-29T09:00:00Z`


## `RRULE-BY-008` — BYMONTHDAY=-1 (last day of month) never skips

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20270131T090000
RRULE:FREQ=MONTHLY;BYMONTHDAY=-1;COUNT=5
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2027-01-31T09:00:00-05:00<br>2027-01-31T14:00:00Z<br>2027-02-28T09:00:00-05:00<br>2027-02-28T14:00:00Z<br>2027-03-31T09:00:00-04:00<br>2027-03-31T13:00:00Z<br>2027-04-30T09:00:00-04:00<br>2027-04-30T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2027-01-31T09:00:00+00:00<br>2027-01-31T09:00:00Z<br>2027-02-28T09:00:00+00:00<br>2027-02-28T09:00:00Z<br>2027-03-31T09:00:00+00:00<br>2027-03-31T09:00:00Z<br>2027-04-30T09:00:00+00:00<br>2027-04-30T09:00:00Z`


## `RRULE-BY-009` — BYMONTHDAY=1,-1 (first and last day, RFC example)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970930T090000
RRULE:FREQ=MONTHLY;BYMONTHDAY=1,-1;COUNT=5
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-30T09:00:00-04:00<br>1997-09-30T13:00:00Z<br>1997-10-01T09:00:00-04:00<br>1997-10-01T13:00:00Z<br>1997-10-31T09:00:00-05:00<br>1997-10-31T14:00:00Z<br>1997-11-01T09:00:00-05:00<br>1997-11-01T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-30T09:00:00+00:00<br>1997-09-30T09:00:00Z<br>1997-10-01T09:00:00+00:00<br>1997-10-01T09:00:00Z<br>1997-10-31T09:00:00+00:00<br>1997-10-31T09:00:00Z<br>1997-11-01T09:00:00+00:00<br>1997-11-01T09:00:00Z`


## `RRULE-BY-010` — Yearly on 29 February

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20240229T090000
RRULE:FREQ=YEARLY;BYMONTH=2;BYMONTHDAY=29;COUNT=3
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2024-02-29T09:00:00-05:00<br>2024-02-29T14:00:00Z<br>2028-02-29T09:00:00-05:00<br>2028-02-29T14:00:00Z<br>2032-02-29T09:00:00-05:00<br>2032-02-29T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2024-02-29T09:00:00+00:00<br>2024-02-29T09:00:00Z<br>2028-02-29T09:00:00+00:00<br>2028-02-29T09:00:00Z<br>2032-02-29T09:00:00+00:00<br>2032-02-29T09:00:00Z`


## `RRULE-BY-012` — BYSETPOS=3 over BYDAY=TU,WE,TH (RFC example)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970904T090000
RRULE:FREQ=MONTHLY;BYDAY=TU,WE,TH;BYSETPOS=3;COUNT=3
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-04T09:00:00-04:00<br>1997-09-04T13:00:00Z<br>1997-10-07T09:00:00-04:00<br>1997-10-07T13:00:00Z<br>1997-11-06T09:00:00-05:00<br>1997-11-06T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-04T09:00:00+00:00<br>1997-09-04T09:00:00Z<br>1997-10-07T09:00:00+00:00<br>1997-10-07T09:00:00Z<br>1997-11-06T09:00:00+00:00<br>1997-11-06T09:00:00Z`


## `RRULE-BY-013` — BYSETPOS=-2 (second-to-last weekday of the month, RFC example)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970929T090000
RRULE:FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-2;COUNT=7
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-29T09:00:00-04:00<br>1997-09-29T13:00:00Z<br>1997-10-30T09:00:00-05:00<br>1997-10-30T14:00:00Z<br>1997-11-27T09:00:00-05:00<br>1997-11-27T14:00:00Z<br>1997-12-30T09:00:00-05:00<br>1997-12-30T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-29T09:00:00+00:00<br>1997-09-29T09:00:00Z<br>1997-10-30T09:00:00+00:00<br>1997-10-30T09:00:00Z<br>1997-11-27T09:00:00+00:00<br>1997-11-27T09:00:00Z<br>1997-12-30T09:00:00+00:00<br>1997-12-30T09:00:00Z`


## `RRULE-BY-014` — BYSETPOS with FREQ=WEEKLY (a period with at most 7 candidates)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;BYSETPOS=-1;COUNT=4
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-01-09T09:00:00-05:00<br>2026-01-09T14:00:00Z<br>2026-01-16T09:00:00-05:00<br>2026-01-16T14:00:00Z<br>2026-01-23T09:00:00-05:00<br>2026-01-23T14:00:00Z<br>2026-01-30T09:00:00-05:00<br>2026-01-30T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-09T09:00:00+00:00<br>2026-01-09T09:00:00Z<br>2026-01-16T09:00:00+00:00<br>2026-01-16T09:00:00Z<br>2026-01-23T09:00:00+00:00<br>2026-01-23T09:00:00Z<br>2026-01-30T09:00:00+00:00<br>2026-01-30T09:00:00Z`


## `RRULE-BY-017` — WKST=MO with INTERVAL=2 (RFC's own WKST example)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970805T090000
RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=4;BYDAY=TU,SU;WKST=MO
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-08-05T09:00:00-04:00<br>1997-08-05T13:00:00Z<br>1997-08-10T09:00:00-04:00<br>1997-08-10T13:00:00Z<br>1997-08-19T09:00:00-04:00<br>1997-08-19T13:00:00Z<br>1997-08-24T09:00:00-04:00<br>1997-08-24T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-08-05T09:00:00+00:00<br>1997-08-05T09:00:00Z<br>1997-08-10T09:00:00+00:00<br>1997-08-10T09:00:00Z<br>1997-08-19T09:00:00+00:00<br>1997-08-19T09:00:00Z<br>1997-08-24T09:00:00+00:00<br>1997-08-24T09:00:00Z`


## `RRULE-BY-018` — WKST=SU with INTERVAL=2 (same rule, different week start)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970805T090000
RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=4;BYDAY=TU,SU;WKST=SU
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-08-05T09:00:00-04:00<br>1997-08-05T13:00:00Z<br>1997-08-17T09:00:00-04:00<br>1997-08-17T13:00:00Z<br>1997-08-19T09:00:00-04:00<br>1997-08-19T13:00:00Z<br>1997-08-31T09:00:00-04:00<br>1997-08-31T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-08-05T09:00:00+00:00<br>1997-08-05T09:00:00Z<br>1997-08-17T09:00:00+00:00<br>1997-08-17T09:00:00Z<br>1997-08-19T09:00:00+00:00<br>1997-08-19T09:00:00Z<br>1997-08-31T09:00:00+00:00<br>1997-08-31T09:00:00Z`


## `RRULE-BY-019` — WKST default is MO when omitted

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970805T090000
RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=4;BYDAY=TU,SU
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-08-05T09:00:00-04:00<br>1997-08-05T13:00:00Z<br>1997-08-10T09:00:00-04:00<br>1997-08-10T13:00:00Z<br>1997-08-19T09:00:00-04:00<br>1997-08-19T13:00:00Z<br>1997-08-24T09:00:00-04:00<br>1997-08-24T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-08-05T09:00:00+00:00<br>1997-08-05T09:00:00Z<br>1997-08-17T09:00:00+00:00<br>1997-08-17T09:00:00Z<br>1997-08-19T09:00:00+00:00<br>1997-08-19T09:00:00Z<br>1997-08-31T09:00:00+00:00<br>1997-08-31T09:00:00Z`


## `RRULE-BY-020` — BYWEEKNO=20 with BYDAY=MO (RFC example)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970512T090000
RRULE:FREQ=YEARLY;BYWEEKNO=20;BYDAY=MO;COUNT=3
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-05-12T09:00:00-04:00<br>1997-05-12T13:00:00Z<br>1998-05-11T09:00:00-04:00<br>1998-05-11T13:00:00Z<br>1999-05-17T09:00:00-04:00<br>1999-05-17T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `RRULE-BY-021` — BYWEEKNO=1 across a year boundary (ISO 8601 week 1)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260101T090000
RRULE:FREQ=YEARLY;BYWEEKNO=1;BYDAY=MO;COUNT=4
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2027-01-04T09:00:00-05:00<br>2027-01-04T14:00:00Z<br>2028-01-03T09:00:00-05:00<br>2028-01-03T14:00:00Z<br>2029-01-01T09:00:00-05:00<br>2029-01-01T14:00:00Z<br>2029-12-31T09:00:00-05:00<br>2029-12-31T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `RRULE-BY-022` — BYWEEKNO=53 in a year that has no week 53

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20261228T090000
RRULE:FREQ=YEARLY;BYWEEKNO=53;BYDAY=MO;COUNT=3
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-12-28T09:00:00-05:00<br>2026-12-28T14:00:00Z<br>2032-12-27T09:00:00-05:00<br>2032-12-27T14:00:00Z<br>2037-12-28T09:00:00-05:00<br>2037-12-28T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `RRULE-BY-023` — BYWEEKNO with WKST=SU (weeks are not ISO weeks any more)

*AMBIGUOUS_STANDARD* · family `rrule.by` · policy axis `rrule.byweekno_wkst`

input:
```
DTSTART;TZID=America/New_York:20260101T090000
RRULE:FREQ=YEARLY;BYWEEKNO=1;BYDAY=SU;WKST=SU;COUNT=3
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-01-04T09:00:00-05:00<br>2026-01-04T14:00:00Z<br>2027-01-03T09:00:00-05:00<br>2027-01-03T14:00:00Z<br>2028-01-02T09:00:00-05:00<br>2028-01-02T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `RRULE-BY-024` — BYWEEKNO with FREQ=MONTHLY (forbidden)

*INVALID* · family `rrule.by` · policy axis `None`

input:
```
DTSTART:20260101T090000
RRULE:FREQ=MONTHLY;BYWEEKNO=1;COUNT=3
```

**3 distinct answers:**

- **python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-01-01T09:00:00<br>2026-01-02T09:00:00<br>2026-01-03T09:00:00`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a, php-rrule@tz2026a**
  <br>`ERROR`


## `RRULE-BY-026` — Numeric BYDAY with FREQ=YEARLY and BYWEEKNO present (errata 1913 vs 3779)

*AMBIGUOUS_STANDARD* · family `rrule.by` · policy axis `rrule.byday_ordinal_scope`

input:
```
DTSTART;TZID=America/New_York:20260101T090000
RRULE:FREQ=YEARLY;BYWEEKNO=20;BYDAY=2MO;COUNT=3
```

**3 distinct answers:**

- **python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`EMPTY`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a, php-rrule@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `RRULE-BY-027` — FREQ=YEARLY with BYMONTHDAY only (erratum 3747's Note 2)

*AMBIGUOUS_STANDARD* · family `rrule.by` · policy axis `rrule.note2`

input:
```
DTSTART;TZID=America/New_York:20260315T090000
RRULE:FREQ=YEARLY;BYMONTHDAY=15;COUNT=4
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `expand`
  <br>`2026-03-15T09:00:00-04:00<br>2026-03-15T13:00:00Z<br>2026-04-15T09:00:00-04:00<br>2026-04-15T13:00:00Z<br>2026-05-15T09:00:00-04:00<br>2026-05-15T13:00:00Z<br>2026-06-15T09:00:00-04:00<br>2026-06-15T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-03-15T09:00:00+00:00<br>2026-03-15T09:00:00Z<br>2027-03-15T09:00:00+00:00<br>2027-03-15T09:00:00Z<br>2028-03-15T09:00:00+00:00<br>2028-03-15T09:00:00Z<br>2029-03-15T09:00:00+00:00<br>2029-03-15T09:00:00Z`


## `RRULE-BY-028` — BYMONTH with FREQ=MONTHLY (limit, not expand)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260115T090000
RRULE:FREQ=MONTHLY;BYMONTH=3,6,9,12;COUNT=4
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-03-15T09:00:00-04:00<br>2026-03-15T13:00:00Z<br>2026-06-15T09:00:00-04:00<br>2026-06-15T13:00:00Z<br>2026-09-15T09:00:00-04:00<br>2026-09-15T13:00:00Z<br>2026-12-15T09:00:00-05:00<br>2026-12-15T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-03-15T09:00:00+00:00<br>2026-03-15T09:00:00Z<br>2026-06-15T09:00:00+00:00<br>2026-06-15T09:00:00Z<br>2026-09-15T09:00:00+00:00<br>2026-09-15T09:00:00Z<br>2026-12-15T09:00:00+00:00<br>2026-12-15T09:00:00Z`


## `RRULE-BY-029` — BYHOUR expands under FREQ=DAILY

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260101T090000
RRULE:FREQ=DAILY;BYHOUR=9,17;COUNT=4
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-01-01T09:00:00-05:00<br>2026-01-01T14:00:00Z<br>2026-01-01T17:00:00-05:00<br>2026-01-01T22:00:00Z<br>2026-01-02T09:00:00-05:00<br>2026-01-02T14:00:00Z<br>2026-01-02T17:00:00-05:00<br>2026-01-02T22:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-01T09:00:00+00:00<br>2026-01-01T09:00:00Z<br>2026-01-01T17:00:00+00:00<br>2026-01-01T17:00:00Z<br>2026-01-02T09:00:00+00:00<br>2026-01-02T09:00:00Z<br>2026-01-02T17:00:00+00:00<br>2026-01-02T17:00:00Z`


## `RRULE-BY-030` — US presidential election day (RFC example: BYDAY+BYMONTHDAY intersection)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19961105T090000
RRULE:FREQ=YEARLY;INTERVAL=4;BYMONTH=11;BYDAY=TU;BYMONTHDAY=2,3,4,5,6,7,8;COUNT=3
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1996-11-05T09:00:00-05:00<br>1996-11-05T14:00:00Z<br>2000-11-07T09:00:00-05:00<br>2000-11-07T14:00:00Z<br>2004-11-02T09:00:00-05:00<br>2004-11-02T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1996-11-05T09:00:00+00:00<br>1996-11-05T09:00:00Z<br>2000-11-07T09:00:00+00:00<br>2000-11-07T09:00:00Z<br>2004-11-02T09:00:00+00:00<br>2004-11-02T09:00:00Z`


## `RRULE-BY-031` — Invalid dates are ignored, not clamped (RFC example)

*NORMATIVE* · family `rrule.by` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20070115T090000
RRULE:FREQ=MONTHLY;BYMONTHDAY=15,30;COUNT=5
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2007-01-15T09:00:00-05:00<br>2007-01-15T14:00:00Z<br>2007-01-30T09:00:00-05:00<br>2007-01-30T14:00:00Z<br>2007-02-15T09:00:00-05:00<br>2007-02-15T14:00:00Z<br>2007-03-15T09:00:00-04:00<br>2007-03-15T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2007-01-15T09:00:00+00:00<br>2007-01-15T09:00:00Z<br>2007-01-30T09:00:00+00:00<br>2007-01-30T09:00:00Z<br>2007-02-15T09:00:00+00:00<br>2007-02-15T09:00:00Z<br>2007-03-15T09:00:00+00:00<br>2007-03-15T09:00:00Z`


## `RRULE-CORE-003` — DTSTART unsynchronised with the rule (the RFC calls this undefined)

*AMBIGUOUS_STANDARD* · family `rrule.core` · policy axis `rrule.dtstart_emission`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=MONTHLY;BYDAY=FR;BYMONTHDAY=13;COUNT=4
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `rule-only`
  <br>`1998-02-13T09:00:00-05:00<br>1998-02-13T14:00:00Z<br>1998-03-13T09:00:00-05:00<br>1998-03-13T14:00:00Z<br>1998-11-13T09:00:00-05:00<br>1998-11-13T14:00:00Z<br>1999-08-13T09:00:00-04:00<br>1999-08-13T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1998-02-13T09:00:00+00:00<br>1998-02-13T09:00:00Z<br>1998-03-13T09:00:00+00:00<br>1998-03-13T09:00:00Z<br>1998-11-13T09:00:00+00:00<br>1998-11-13T09:00:00Z<br>1999-08-13T09:00:00+00:00<br>1999-08-13T09:00:00Z`


## `RRULE-CORE-004` — RFC 5545's Friday-the-13th example verbatim, with its EXDATE

*NORMATIVE* · family `rrule.core` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
EXDATE;TZID=America/New_York:19970902T090000
RRULE:FREQ=MONTHLY;BYDAY=FR;BYMONTHDAY=13
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1998-02-13T09:00:00-05:00<br>1998-02-13T14:00:00Z<br>1998-03-13T09:00:00-05:00<br>1998-03-13T14:00:00Z<br>1998-11-13T09:00:00-05:00<br>1998-11-13T14:00:00Z<br>1999-08-13T09:00:00-04:00<br>1999-08-13T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1998-02-13T09:00:00+00:00<br>1998-02-13T09:00:00Z<br>1998-03-13T09:00:00+00:00<br>1998-03-13T09:00:00Z<br>1998-11-13T09:00:00+00:00<br>1998-11-13T09:00:00Z<br>1999-08-13T09:00:00+00:00<br>1999-08-13T09:00:00Z`


## `RRULE-CORE-005` — UNTIL is inclusive when it names an instance exactly

*NORMATIVE* · family `rrule.core` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=DAILY;UNTIL=19970904T130000Z
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-03T09:00:00-04:00<br>1997-09-03T13:00:00Z<br>1997-09-04T09:00:00-04:00<br>1997-09-04T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-02T09:00:00+00:00<br>1997-09-02T09:00:00Z<br>1997-09-03T09:00:00+00:00<br>1997-09-03T09:00:00Z<br>1997-09-04T09:00:00+00:00<br>1997-09-04T09:00:00Z`


## `RRULE-CORE-010` — UNTIL value type mismatched with DTSTART (Z on a floating start)

*INVALID* · family `rrule.core` · policy axis `None`

input:
```
DTSTART:19970902T090000
RRULE:FREQ=DAILY;UNTIL=19970904T130000Z
```

**3 distinct answers:**

- **ice_cube@tz2026a, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00<br>1997-09-03T09:00:00<br>1997-09-04T09:00:00`

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c**
  <br>`ERROR`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``


## `RRULE-CORE-013` — Infinite recurrence with no COUNT and no UNTIL

*POLICY_DEPENDENT* · family `rrule.core` · policy axis `rrule.truncation`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=DAILY
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `lazy-iterator`
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-03T09:00:00-04:00<br>1997-09-03T13:00:00Z<br>1997-09-04T09:00:00-04:00<br>1997-09-04T13:00:00Z<br>1997-09-05T09:00:00-04:00<br>1997-09-05T13:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`1997-09-02T09:00:00+00:00<br>1997-09-02T09:00:00Z<br>1997-09-03T09:00:00+00:00<br>1997-09-03T09:00:00Z<br>1997-09-04T09:00:00+00:00<br>1997-09-04T09:00:00Z<br>1997-09-05T09:00:00+00:00<br>1997-09-05T09:00:00Z`


## `RRULE-CORE-017` — COUNT=0

*AMBIGUOUS_STANDARD* · family `rrule.core` · policy axis `rrule.count_zero`

input:
```
DTSTART:19970902T090000
RRULE:FREQ=DAILY;COUNT=0
```

**3 distinct answers:**

- **ice_cube@tz2026a, pandas@tz2026a, pandas@tz2026c, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule.js@tzle2026a** → admissible case `empty`
  <br>`EMPTY`

- **rrule-go@tz2026a**
  <br>`1997-09-02T09:00:00<br>1997-09-03T09:00:00<br>1997-09-04T09:00:00`

- **php-rrule@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `RRULE-DST-002` — Daily 01:30 across the US autumn fold

*NORMATIVE* · family `rrule.dst` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20261030T013000
RRULE:FREQ=DAILY;COUNT=4
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-10-30T01:30:00-04:00<br>2026-10-30T05:30:00Z<br>2026-10-31T01:30:00-04:00<br>2026-10-31T05:30:00Z<br>2026-11-01T01:30:00-04:00<br>2026-11-01T05:30:00Z<br>2026-11-02T01:30:00-05:00<br>2026-11-02T06:30:00Z`

- **pandas@tz2026a, pandas@tz2026c** → admissible case `rejected`
  <br>`ERROR`

- **ice_cube@tz2026a**
  <br>`2026-10-30T01:30:00+00:00<br>2026-10-30T01:30:00Z<br>2026-10-31T01:30:00+00:00<br>2026-10-31T01:30:00Z<br>2026-11-01T01:30:00+00:00<br>2026-11-01T01:30:00Z<br>2026-11-02T01:30:00+00:00<br>2026-11-02T01:30:00Z`


## `RRULE-DST-004` — Weekly 02:15 in Lord Howe (30-minute transition)

*AMBIGUOUS_STANDARD* · family `rrule.dst` · policy axis `rrule.gap`

input:
```
DTSTART;TZID=Australia/Lord_Howe:20260919T021500
RRULE:FREQ=WEEKLY;COUNT=4
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-09-19T02:15:00+10:30<br>2026-09-18T15:45:00Z<br>2026-09-26T02:15:00+10:30<br>2026-09-25T15:45:00Z<br>2026-10-03T02:15:00+10:30<br>2026-10-02T15:45:00Z<br>2026-10-10T02:15:00+11:00<br>2026-10-09T15:15:00Z`

- **pandas@tz2026a, pandas@tz2026c** → admissible case `rejected`
  <br>`ERROR`

- **ice_cube@tz2026a**
  <br>`2026-09-19T02:15:00+00:00<br>2026-09-19T02:15:00Z<br>2026-09-26T02:15:00+00:00<br>2026-09-26T02:15:00Z<br>2026-10-03T02:15:00+00:00<br>2026-10-03T02:15:00Z<br>2026-10-10T02:15:00+00:00<br>2026-10-10T02:15:00Z`


## `RRULE-DST-009` — Hourly recurrence across the fold: 25-hour day

*NORMATIVE* · family `rrule.dst` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20261101T000000
RRULE:FREQ=HOURLY;COUNT=5
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a**
  <br>`2026-11-01T00:00:00-04:00<br>2026-11-01T04:00:00Z<br>2026-11-01T01:00:00-04:00<br>2026-11-01T05:00:00Z<br>2026-11-01T02:00:00-05:00<br>2026-11-01T07:00:00Z<br>2026-11-01T03:00:00-05:00<br>2026-11-01T08:00:00Z`

- **pandas@tz2026a, pandas@tz2026c, rrule.js@tzle2026a**
  <br>`2026-11-01T00:00:00-04:00<br>2026-11-01T04:00:00Z<br>2026-11-01T01:00:00-04:00<br>2026-11-01T05:00:00Z<br>2026-11-01T01:00:00-05:00<br>2026-11-01T06:00:00Z<br>2026-11-01T02:00:00-05:00<br>2026-11-01T07:00:00Z`

- **ice_cube@tz2026a**
  <br>`2026-11-01T00:00:00+00:00<br>2026-11-01T00:00:00Z<br>2026-11-01T01:00:00+00:00<br>2026-11-01T01:00:00Z<br>2026-11-01T02:00:00+00:00<br>2026-11-01T02:00:00Z<br>2026-11-01T03:00:00+00:00<br>2026-11-01T03:00:00Z`


## `RRULE-SET-001` — EXDATE removes an instance the RRULE generates

*NORMATIVE* · family `rrule.sets` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=DAILY;COUNT=5
EXDATE;TZID=America/New_York:20260107T090000
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-06T09:00:00-05:00<br>2026-01-06T14:00:00Z<br>2026-01-08T09:00:00-05:00<br>2026-01-08T14:00:00Z<br>2026-01-09T09:00:00-05:00<br>2026-01-09T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-06T09:00:00+00:00<br>2026-01-06T09:00:00Z<br>2026-01-08T09:00:00+00:00<br>2026-01-08T09:00:00Z<br>2026-01-09T09:00:00+00:00<br>2026-01-09T09:00:00Z`


## `RRULE-SET-005` — EXDATE naming an instant the rule never generates

*POLICY_DEPENDENT* · family `rrule.sets` · policy axis `rrule.exdate_unmatched`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=DAILY;COUNT=3
EXDATE;TZID=America/New_York:20260106T100000
```

**3 distinct answers:**

- **php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `silent`
  <br>`2026-01-05T09:00:00-05:00<br>2026-01-05T14:00:00Z<br>2026-01-06T09:00:00-05:00<br>2026-01-06T14:00:00Z<br>2026-01-07T09:00:00-05:00<br>2026-01-07T14:00:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``

- **ice_cube@tz2026a**
  <br>`2026-01-05T09:00:00+00:00<br>2026-01-05T09:00:00Z<br>2026-01-06T09:00:00+00:00<br>2026-01-06T09:00:00Z<br>2026-01-07T09:00:00+00:00<br>2026-01-07T09:00:00Z`


## `TZDB-001` — America/Vancouver noon daily across 2026-11-01 (BC abolished DST in tzdb 2026b)

*POLICY_DEPENDENT* · family `tzdb.provenance` · policy axis `tz.tzdb_version`

input: `0 12 * * *` from `2026-10-30T00:00:00` zone `America/Vancouver` × 4

**3 distinct answers:**

- **apscheduler3@tz2026a, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter[day_or=False]@tz2026a, cronsim@tz2026a, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `tzdb<=2026a`
  <br>`2026-10-30T12:00:00-07:00<br>2026-10-30T19:00:00Z<br>2026-10-31T12:00:00-07:00<br>2026-10-31T19:00:00Z<br>2026-11-01T12:00:00-08:00<br>2026-11-01T20:00:00Z<br>2026-11-02T12:00:00-08:00<br>2026-11-02T20:00:00Z`

- **apscheduler3@tz2026c, croniter@tz2026c, croniter[day_or=False]@tz2026c, cronsim@tz2026c** → admissible case `tzdb>=2026b`
  <br>`2026-10-30T12:00:00-07:00<br>2026-10-30T19:00:00Z<br>2026-10-31T12:00:00-07:00<br>2026-10-31T19:00:00Z<br>2026-11-01T12:00:00-07:00<br>2026-11-01T19:00:00Z<br>2026-11-02T12:00:00-07:00<br>2026-11-02T19:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `TZDB-002` — America/Edmonton noon daily across 2026-11-01 (Alberta abolished DST in tzdb 2026c)

*POLICY_DEPENDENT* · family `tzdb.provenance` · policy axis `tz.tzdb_version`

input: `0 12 * * *` from `2026-10-30T00:00:00` zone `America/Edmonton` × 4

**3 distinct answers:**

- **apscheduler3@tz2026a, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter[day_or=False]@tz2026a, cronsim@tz2026a, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `tzdb<=2026b`
  <br>`2026-10-30T12:00:00-06:00<br>2026-10-30T18:00:00Z<br>2026-10-31T12:00:00-06:00<br>2026-10-31T18:00:00Z<br>2026-11-01T12:00:00-07:00<br>2026-11-01T19:00:00Z<br>2026-11-02T12:00:00-07:00<br>2026-11-02T19:00:00Z`

- **apscheduler3@tz2026c, croniter@tz2026c, croniter[day_or=False]@tz2026c, cronsim@tz2026c** → admissible case `tzdb>=2026c`
  <br>`2026-10-30T12:00:00-06:00<br>2026-10-30T18:00:00Z<br>2026-10-31T12:00:00-06:00<br>2026-10-31T18:00:00Z<br>2026-11-01T12:00:00-06:00<br>2026-11-01T18:00:00Z<br>2026-11-02T12:00:00-06:00<br>2026-11-02T18:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `TZDB-003` — Africa/Casablanca: Morocco moves to permanent UTC on 2026-09-20

*POLICY_DEPENDENT* · family `tzdb.provenance` · policy axis `tz.tzdb_version`

input: `0 12 * * *` from `2026-09-18T00:00:00` zone `Africa/Casablanca` × 4

**3 distinct answers:**

- **apscheduler3@tz2026a, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter[day_or=False]@tz2026a, cronsim@tz2026a, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `tzdb<=2026b`
  <br>`2026-09-18T12:00:00+01:00<br>2026-09-18T11:00:00Z<br>2026-09-19T12:00:00+01:00<br>2026-09-19T11:00:00Z<br>2026-09-20T12:00:00+01:00<br>2026-09-20T11:00:00Z<br>2026-09-21T12:00:00+01:00<br>2026-09-21T11:00:00Z`

- **apscheduler3@tz2026c, croniter@tz2026c, croniter[day_or=False]@tz2026c, cronsim@tz2026c** → admissible case `tzdb>=2026c`
  <br>`2026-09-18T12:00:00+01:00<br>2026-09-18T11:00:00Z<br>2026-09-19T12:00:00+01:00<br>2026-09-19T11:00:00Z<br>2026-09-20T12:00:00+00:00<br>2026-09-20T12:00:00Z<br>2026-09-21T12:00:00+00:00<br>2026-09-21T12:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `TZDB-004` — RRULE weekly at 12:00 in America/Vancouver across the same boundary

*POLICY_DEPENDENT* · family `tzdb.provenance` · policy axis `tz.tzdb_version`

input:
```
DTSTART;TZID=America/Vancouver:20261018T120000
RRULE:FREQ=WEEKLY;COUNT=4
```

**3 distinct answers:**

- **pandas@tz2026a, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `tzdb<=2026a`
  <br>`2026-10-18T12:00:00-07:00<br>2026-10-18T19:00:00Z<br>2026-10-25T12:00:00-07:00<br>2026-10-25T19:00:00Z<br>2026-11-01T12:00:00-08:00<br>2026-11-01T20:00:00Z<br>2026-11-08T12:00:00-08:00<br>2026-11-08T20:00:00Z`

- **ice_cube@tz2026a**
  <br>`2026-10-18T12:00:00+00:00<br>2026-10-18T12:00:00Z<br>2026-10-25T12:00:00+00:00<br>2026-10-25T12:00:00Z<br>2026-11-01T12:00:00+00:00<br>2026-11-01T12:00:00Z<br>2026-11-08T12:00:00+00:00<br>2026-11-08T12:00:00Z`

- **pandas@tz2026c** → admissible case `tzdb>=2026b`
  <br>`2026-10-18T12:00:00-07:00<br>2026-10-18T19:00:00Z<br>2026-10-25T12:00:00-07:00<br>2026-10-25T19:00:00Z<br>2026-11-01T12:00:00-07:00<br>2026-11-01T19:00:00Z<br>2026-11-08T12:00:00-07:00<br>2026-11-08T19:00:00Z`


## `TZDB-006` — Zone abbreviation is not a stable identifier (Edmonton reports CST at -06:00)

*POLICY_DEPENDENT* · family `tzdb.provenance` · policy axis `tz.tzdb_version`

input: `0 12 * * *` from `2027-01-14T00:00:00` zone `America/Edmonton` × 2

**3 distinct answers:**

- **apscheduler3@tz2026a, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter[day_or=False]@tz2026a, cronsim@tz2026a, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `tzdb<=2026b`
  <br>`2027-01-14T12:00:00-07:00<br>2027-01-14T19:00:00Z<br>2027-01-15T12:00:00-07:00<br>2027-01-15T19:00:00Z`

- **apscheduler3@tz2026c, croniter@tz2026c, croniter[day_or=False]@tz2026c, cronsim@tz2026c** → admissible case `tzdb>=2026c`
  <br>`2027-01-14T12:00:00-06:00<br>2027-01-14T18:00:00Z<br>2027-01-15T12:00:00-06:00<br>2027-01-15T18:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-ANCH-002` — Sub-minute start instant (seconds and micros in the anchor)

*POLICY_DEPENDENT* · family `cron.anchoring` · policy axis `cron.start_truncation`

input: `0 12 * * *` from `2026-01-01T12:00:30` zone `None` × 2

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `truncate-to-minute`
  <br>`2026-01-02T12:00:00<br>2026-01-03T12:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DOW-002` — Day-of-week 7

*DIALECT_DEPENDENT* · family `cron.dow-numbering` · policy axis `cron.dow_numbering`

input: `0 12 * * 7` from `2026-01-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a** → admissible case `vixie-both`
  <br>`2026-01-04T12:00:00<br>2026-01-11T12:00:00<br>2026-01-18T12:00:00<br>2026-01-25T12:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser[strict]@tzle2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `monday-zero`
  <br>`ERROR`


## `CRON-DOW-003` — Day-of-week 0 and 7 in one list

*DIALECT_DEPENDENT* · family `cron.dow-numbering` · policy axis `cron.dow_numbering`

input: `0 12 * * 0,7` from `2026-01-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a** → admissible case `vixie-both`
  <br>`2026-01-04T12:00:00<br>2026-01-11T12:00:00<br>2026-01-18T12:00:00<br>2026-01-25T12:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `monday-zero`
  <br>`ERROR`


## `CRON-DOW-005` — Wrapping named day range FRI-MON

*DIALECT_DEPENDENT* · family `cron.dow-numbering` · policy axis `cron.range_wrap`

input: `0 12 * * FRI-MON` from `2026-01-01T00:00:00` zone `None` × 6

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject-reversed`
  <br>`ERROR`

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a** → admissible case `wrap-modulo`
  <br>`2026-01-02T12:00:00<br>2026-01-03T12:00:00<br>2026-01-04T12:00:00<br>2026-01-05T12:00:00<br>2026-01-09T12:00:00<br>2026-01-10T12:00:00`


## `CRON-DOW-006` — Wrapping numeric day range 5-1

*DIALECT_DEPENDENT* · family `cron.dow-numbering` · policy axis `cron.range_wrap`

input: `0 12 * * 5-1` from `2026-01-01T00:00:00` zone `None` × 6

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject-reversed`
  <br>`ERROR`

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a** → admissible case `wrap-modulo`
  <br>`2026-01-02T12:00:00<br>2026-01-03T12:00:00<br>2026-01-04T12:00:00<br>2026-01-05T12:00:00<br>2026-01-09T12:00:00<br>2026-01-10T12:00:00`


## `CRON-DOW-008` — Lowercase day name

*NORMATIVE* · family `cron.names` · policy axis `None`

input: `0 12 * * sun` from `2026-01-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-04T12:00:00<br>2026-01-11T12:00:00<br>2026-01-18T12:00:00<br>2026-01-25T12:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DOW-009` — Lowercase month and day names

*NORMATIVE* · family `cron.names` · policy axis `None`

input: `0 12 * jan,dec mon` from `2026-01-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-05T12:00:00<br>2026-01-12T12:00:00<br>2026-01-19T12:00:00<br>2026-01-26T12:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DOW-012` — Named month range wrapping the year boundary: NOV-FEB

*DIALECT_DEPENDENT* · family `cron.names` · policy axis `cron.range_wrap`

input: `0 12 1 NOV-FEB *` from `2026-01-01T00:00:00` zone `None` × 5

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject-reversed`
  <br>`ERROR`

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a** → admissible case `wrap-modulo`
  <br>`2026-01-01T12:00:00<br>2026-02-01T12:00:00<br>2026-11-01T12:00:00<br>2026-12-01T12:00:00<br>2027-01-01T12:00:00`


## `CRON-DST-008` — Zero-offset-change transition (Asia/Amman, October 2022)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 0 * * *` from `2022-10-27T00:00:00` zone `Asia/Amman` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2022-10-27T00:30:00+03:00<br>2022-10-26T21:30:00Z<br>2022-10-28T00:30:00+03:00<br>2022-10-27T21:30:00Z<br>2022-10-29T00:30:00+03:00<br>2022-10-28T21:30:00Z<br>2022-10-30T00:30:00+03:00<br>2022-10-29T21:30:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-009` — Zero-offset-change transition (Asia/Damascus, October 2022)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 0 * * *` from `2022-10-27T00:00:00` zone `Asia/Damascus` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2022-10-27T00:30:00+03:00<br>2022-10-26T21:30:00Z<br>2022-10-28T00:30:00+03:00<br>2022-10-27T21:30:00Z<br>2022-10-29T00:30:00+03:00<br>2022-10-28T21:30:00Z<br>2022-10-30T00:30:00+03:00<br>2022-10-29T21:30:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-010` — Non-hour standard offset (+05:45, Asia/Kathmandu)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 0 * * *` from `2026-01-01T00:00:00` zone `Asia/Kathmandu` × 3

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-01-01T00:30:00+05:45<br>2025-12-31T18:45:00Z<br>2026-01-02T00:30:00+05:45<br>2026-01-01T18:45:00Z<br>2026-01-03T00:30:00+05:45<br>2026-01-02T18:45:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-011` — Non-hour standard offset (+08:45, Australia/Eucla)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 0 * * *` from `2026-01-01T00:00:00` zone `Australia/Eucla` × 3

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-01-01T00:30:00+08:45<br>2025-12-31T15:45:00Z<br>2026-01-02T00:30:00+08:45<br>2026-01-01T15:45:00Z<br>2026-01-03T00:30:00+08:45<br>2026-01-02T15:45:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-012` — Historical standard-offset change (Europe/Lisbon, 1992-09-27)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `0 12 * * *` from `1992-09-25T00:00:00` zone `Europe/Lisbon` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`1992-09-25T12:00:00+01:00<br>1992-09-25T11:00:00Z<br>1992-09-26T12:00:00+01:00<br>1992-09-26T11:00:00Z<br>1992-09-27T12:00:00+01:00<br>1992-09-27T11:00:00Z<br>1992-09-28T12:00:00+01:00<br>1992-09-28T11:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-013` — Historical DST rule change (US Energy Policy Act, 2007)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `0 12 * * *` from `2007-03-09T00:00:00` zone `America/New_York` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2007-03-09T12:00:00-05:00<br>2007-03-09T17:00:00Z<br>2007-03-10T12:00:00-05:00<br>2007-03-10T17:00:00Z<br>2007-03-11T12:00:00-04:00<br>2007-03-11T16:00:00Z<br>2007-03-12T12:00:00-04:00<br>2007-03-12T16:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-014` — Southern-hemisphere spring forward (America/Santiago)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 2 * * *` from `2026-09-05T00:00:00` zone `America/Santiago` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-09-05T02:30:00-04:00<br>2026-09-05T06:30:00Z<br>2026-09-06T02:30:00-03:00<br>2026-09-06T05:30:00Z<br>2026-09-07T02:30:00-03:00<br>2026-09-07T05:30:00Z<br>2026-09-08T02:30:00-03:00<br>2026-09-08T05:30:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-015` — Half-hour standard offset with DST (America/St_Johns, -03:30)

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 23 * * *` from `2026-03-07T00:00:00` zone `America/St_Johns` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-03-07T23:30:00-03:30<br>2026-03-08T03:00:00Z<br>2026-03-08T23:30:00-02:30<br>2026-03-09T02:00:00Z<br>2026-03-09T23:30:00-02:30<br>2026-03-10T02:00:00Z<br>2026-03-10T23:30:00-02:30<br>2026-03-11T02:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-DST-020` — Weekly schedule landing exactly on the transition Sunday

*POLICY_DEPENDENT* · family `cron.dst` · policy axis `cron.dst_gap|cron.dst_fold`

input: `30 2 * * SUN` from `2026-03-01T00:00:00` zone `Europe/London` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `skip`
  <br>`2026-03-01T02:30:00+00:00<br>2026-03-01T02:30:00Z<br>2026-03-08T02:30:00+00:00<br>2026-03-08T02:30:00Z<br>2026-03-15T02:30:00+00:00<br>2026-03-15T02:30:00Z<br>2026-03-22T02:30:00+00:00<br>2026-03-22T02:30:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-EXT-001` — L in the day-of-month field (last day of month)

*DIALECT_DEPENDENT* · family `cron.extensions` · policy axis `cron.L`

input: `0 9 L * *` from `2027-01-01T00:00:00` zone `None` × 5

**2 distinct answers:**

- **cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a** → admissible case `supported`
  <br>`2027-01-31T09:00:00<br>2027-02-28T09:00:00<br>2027-03-31T09:00:00<br>2027-04-30T09:00:00<br>2027-05-31T09:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser[strict]@tzle2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-EXT-003` — 15W: nearest weekday to the 15th

*DIALECT_DEPENDENT* · family `cron.extensions` · policy axis `cron.W`

input: `0 9 15W * *` from `2026-01-01T00:00:00` zone `None` × 8

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, php-cron-expression@tz2026a** → admissible case `supported`
  <br>`2026-01-15T09:00:00<br>2026-02-16T09:00:00<br>2026-03-16T09:00:00<br>2026-04-15T09:00:00<br>2026-05-15T09:00:00<br>2026-06-15T09:00:00<br>2026-07-15T09:00:00<br>2026-08-14T09:00:00`


## `CRON-EXT-004` — 1W when the 1st is a Saturday (must not jump into last month)

*DIALECT_DEPENDENT* · family `cron.extensions` · policy axis `cron.W`

input: `0 9 1W * *` from `2026-07-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, php-cron-expression@tz2026a** → admissible case `supported`
  <br>`2026-07-01T09:00:00<br>2026-08-03T09:00:00<br>2026-09-01T09:00:00<br>2026-10-01T09:00:00`


## `CRON-EXT-010` — '?' in both day fields

*AMBIGUOUS_STANDARD* · family `cron.extensions` · policy axis `cron.qmark`

input: `0 0 12 ? * ? *` from `2026-01-01T00:00:00` zone `None` × 3

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **croner@tzle2026a, croner[legacyMode=false]@tzle2026a** → admissible case `accept-as-star`
  <br>`2026-01-01T12:00:00<br>2026-01-02T12:00:00<br>2026-01-03T12:00:00`


## `CRON-EXT-011` — 'H' (Jenkins hash) in the minute field

*DIALECT_DEPENDENT* · family `cron.extensions` · policy axis `cron.hash_H`

input: `H * * * *` from `2026-01-01T00:00:00` zone `None` × 1

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, cronstrue@tzle2026a, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **cron-parser@tzle2026a**
  <br>`2026-01-01T00:08:00`


## `CRON-EXT-012` — cronie's '~' random operator

*DIALECT_DEPENDENT* · family `cron.extensions` · policy axis `cron.random`

input: `~ * * * *` from `2026-01-01T00:00:00` zone `None` × 1

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, cronstrue@tzle2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`

- **fugit@tz2026a**
  <br>`2026-01-01T00:08:00`


## `CRON-FIELDS-001` — Five-field form (POSIX / Vixie baseline)

*NORMATIVE* · family `cron.field-count` · policy axis `None`

input: `15 10 * * *` from `2026-01-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-01T10:15:00<br>2026-01-02T10:15:00<br>2026-01-03T10:15:00<br>2026-01-04T10:15:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-FIELDS-005` — Four fields (too few)

*INVALID* · family `cron.field-count` · policy axis `None`

input: `0 12 * *` from `2026-01-01T00:00:00` zone `None` × 1

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, cronstrue@tzle2026a, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a**
  <br>`ERROR`

- **cron-parser@tzle2026a**
  <br>`2026-01-12T00:00:00`


## `CRON-FIELDS-008` — Macro @daily

*NORMATIVE* · family `cron.field-count` · policy axis `None`

input: `@daily` from `2026-01-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a**
  <br>`2026-01-02T00:00:00<br>2026-01-03T00:00:00<br>2026-01-04T00:00:00<br>2026-01-05T00:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cronsim@tz2026a, cronsim@tz2026c** → admissible case `rejected`
  <br>`ERROR`


## `CRON-FIELDS-009` — Macro @yearly

*NORMATIVE* · family `cron.field-count` · policy axis `None`

input: `@yearly` from `2026-01-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a**
  <br>`2027-01-01T00:00:00<br>2028-01-01T00:00:00<br>2029-01-01T00:00:00<br>2030-01-01T00:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cronsim@tz2026a, cronsim@tz2026c** → admissible case `rejected`
  <br>`ERROR`


## `CRON-FIELDS-010` — Macro @monthly

*NORMATIVE* · family `cron.field-count` · policy axis `None`

input: `@monthly` from `2026-01-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a**
  <br>`2026-02-01T00:00:00<br>2026-03-01T00:00:00<br>2026-04-01T00:00:00<br>2026-05-01T00:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cronsim@tz2026a, cronsim@tz2026c** → admissible case `rejected`
  <br>`ERROR`


## `CRON-FIELDS-011` — Macro @weekly

*NORMATIVE* · family `cron.field-count` · policy axis `None`

input: `@weekly` from `2026-01-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a**
  <br>`2026-01-04T00:00:00<br>2026-01-11T00:00:00<br>2026-01-18T00:00:00<br>2026-01-25T00:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cronsim@tz2026a, cronsim@tz2026c** → admissible case `rejected`
  <br>`ERROR`


## `CRON-FIELDS-012` — Macro @hourly

*NORMATIVE* · family `cron.field-count` · policy axis `None`

input: `@hourly` from `2026-01-01T00:00:00` zone `None` × 4

**2 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a**
  <br>`2026-01-01T01:00:00<br>2026-01-01T02:00:00<br>2026-01-01T03:00:00<br>2026-01-01T04:00:00`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cronsim@tz2026a, cronsim@tz2026c** → admissible case `rejected`
  <br>`ERROR`


## `CRON-INV-002` — Hour 24

*INVALID* · family `cron.invalid` · policy axis `None`

input: `* 24 * * *` from `2026-01-01T00:00:00` zone `None` × 1

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, cronstrue@tzle2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a**
  <br>`ERROR`

- **fugit@tz2026a**
  <br>`2026-01-01T00:01:00`


## `CRON-INV-007` — 30 February — syntactically valid, semantically empty

*AMBIGUOUS_STANDARD* · family `cron.invalid` · policy axis `cron.empty_set`

input: `0 0 30 2 *` from `2026-01-01T00:00:00` zone `None` × 1

**2 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `error-at-parse`
  <br>`ERROR`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, robfig-cron@tz2026a** → admissible case `empty`
  <br>`EMPTY`


## `CRON-INV-009` — Empty expression

*INVALID* · family `cron.invalid` · policy axis `None`

input: `` from `2026-01-01T00:00:00` zone `None` × 1

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, cronstrue@tzle2026a, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a**
  <br>`ERROR`

- **cron-parser@tzle2026a**
  <br>`2026-01-01T00:01:00`


## `CRON-INV-011` — Day-of-month 31 in a month that never has 31 days

*AMBIGUOUS_STANDARD* · family `cron.invalid` · policy axis `cron.empty_set`

input: `0 0 31 4 *` from `2026-01-01T00:00:00` zone `None` × 1

**2 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `error-at-parse`
  <br>`ERROR`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, robfig-cron@tz2026a** → admissible case `empty`
  <br>`EMPTY`


## `CRON-INV-012` — Whitespace-tolerant parsing (tabs and multiple spaces)

*NORMATIVE* · family `cron.invalid` · policy axis `None`

input: `0	12  *   *  *` from `2026-01-01T00:00:00` zone `None` × 3

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-01T12:00:00<br>2026-01-02T12:00:00<br>2026-01-03T12:00:00`

- **cron-parser[strict]@tzle2026a, cronstrue@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-STEP-002` — 5/20: bare value with a step (start-at semantics)

*DIALECT_DEPENDENT* · family `cron.steps` · policy axis `cron.bare_start_step`

input: `5/20 * * * *` from `2026-01-01T00:00:00` zone `None` × 6

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, robfig-cron@tz2026a** → admissible case `start-at`
  <br>`2026-01-01T00:05:00<br>2026-01-01T00:25:00<br>2026-01-01T00:45:00<br>2026-01-01T01:05:00<br>2026-01-01T01:25:00<br>2026-01-01T01:45:00`

- **cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, php-cron-expression@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-STEP-003` — 0/1 vs * — Quartz idiom in the seconds field

*DIALECT_DEPENDENT* · family `cron.steps` · policy axis `cron.bare_start_step`

input: `0/1 * * * * *` from `2026-01-01T00:00:00` zone `None` × 3

**2 distinct answers:**

- **cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, robfig-cron[seconds]@tz2026a**
  <br>`2026-01-01T00:00:01<br>2026-01-01T00:00:02<br>2026-01-01T00:00:03`

- **apscheduler3@tz2026a, apscheduler3@tz2026c, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a** → admissible case `reject`
  <br>`ERROR`


## `CRON-STEP-006` — Range with a step: 10-16/2 (documented form)

*NORMATIVE* · family `cron.steps` · policy axis `None`

input: `0 10-16/2 * * *` from `2026-01-01T00:00:00` zone `None` × 5

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-01T10:00:00<br>2026-01-01T12:00:00<br>2026-01-01T14:00:00<br>2026-01-01T16:00:00<br>2026-01-02T10:00:00`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `CRON-STEP-007` — Step on a wrapping range: 22-2/2 in hours

*DIALECT_DEPENDENT* · family `cron.steps` · policy axis `cron.range_wrap`

input: `0 22-2/2 * * *` from `2026-01-01T00:00:00` zone `None` × 5

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, cron-parser[strict]@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, cronsim@tz2026a, cronsim@tz2026c, php-cron-expression@tz2026a, robfig-cron@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `reject-reversed`
  <br>`ERROR`

- **croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, fugit@tz2026a** → admissible case `wrap-modulo`
  <br>`2026-01-01T02:00:00<br>2026-01-01T22:00:00<br>2026-01-02T00:00:00<br>2026-01-02T02:00:00<br>2026-01-02T22:00:00`


## `RRULE-BY-011` — Yearly on 29 February with RSCALE and SKIP=BACKWARD (RFC 7529)

*DIALECT_DEPENDENT* · family `rrule.by` · policy axis `rrule.rscale_support`

input:
```
DTSTART;TZID=America/New_York:20240229T090000
RRULE:RSCALE=GREGORIAN;FREQ=YEARLY;SKIP=BACKWARD;COUNT=3
```

**2 distinct answers:**

- **ice_cube@tz2026a, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `reject`
  <br>`ERROR`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``


## `RRULE-BY-015` — BYSETPOS=0 (out of range)

*INVALID* · family `rrule.by` · policy axis `None`

input:
```
DTSTART:19970904T090000
RRULE:FREQ=MONTHLY;BYDAY=TU;BYSETPOS=0;COUNT=3
```

**2 distinct answers:**

- **ice_cube@tz2026a, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`ERROR`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``


## `RRULE-BY-016` — BYSETPOS without any other BY* rule part

*AMBIGUOUS_STANDARD* · family `rrule.by` · policy axis `rrule.bysetpos_alone`

input:
```
DTSTART:19970904T090000
RRULE:FREQ=MONTHLY;BYSETPOS=1;COUNT=3
```

**2 distinct answers:**

- **ice_cube@tz2026a, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `degenerate`
  <br>`1997-09-04T09:00:00<br>1997-10-04T09:00:00<br>1997-11-04T09:00:00`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``


## `RRULE-CORE-001` — RFC 5545 §3.8.5.3 worked example: daily for 10 occurrences

*NORMATIVE* · family `rrule.core` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=DAILY;COUNT=10
```

**2 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-03T09:00:00-04:00<br>1997-09-03T13:00:00Z<br>1997-09-04T09:00:00-04:00<br>1997-09-04T13:00:00Z<br>1997-09-05T09:00:00-04:00<br>1997-09-05T13:00:00Z`

- **ice_cube@tz2026a**
  <br>`1997-09-02T09:00:00+00:00<br>1997-09-02T09:00:00Z<br>1997-09-03T09:00:00+00:00<br>1997-09-03T09:00:00Z<br>1997-09-04T09:00:00+00:00<br>1997-09-04T09:00:00Z<br>1997-09-05T09:00:00+00:00<br>1997-09-05T09:00:00Z`


## `RRULE-CORE-002` — COUNT includes DTSTART when DTSTART matches the rule

*NORMATIVE* · family `rrule.core` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=DAILY;COUNT=1
```

**2 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z`

- **ice_cube@tz2026a**
  <br>`1997-09-02T09:00:00+00:00<br>1997-09-02T09:00:00Z`


## `RRULE-CORE-009` — UNTIL with a floating DTSTART must be floating

*NORMATIVE* · family `rrule.core` · policy axis `None`

input:
```
DTSTART:19970902T090000
RRULE:FREQ=DAILY;UNTIL=19970904T090000
```

**2 distinct answers:**

- **ice_cube@tz2026a, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00<br>1997-09-03T09:00:00<br>1997-09-04T09:00:00`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``


## `RRULE-CORE-012` — INTERVAL counts periods from DTSTART, not from the calendar

*NORMATIVE* · family `rrule.core` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5
```

**2 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00-04:00<br>1997-09-02T13:00:00Z<br>1997-09-12T09:00:00-04:00<br>1997-09-12T13:00:00Z<br>1997-09-22T09:00:00-04:00<br>1997-09-22T13:00:00Z<br>1997-10-02T09:00:00-04:00<br>1997-10-02T13:00:00Z`

- **ice_cube@tz2026a**
  <br>`1997-09-02T09:00:00+00:00<br>1997-09-02T09:00:00Z<br>1997-09-12T09:00:00+00:00<br>1997-09-12T09:00:00Z<br>1997-09-22T09:00:00+00:00<br>1997-09-22T09:00:00Z<br>1997-10-02T09:00:00+00:00<br>1997-10-02T09:00:00Z`


## `RRULE-CORE-015` — FREQ missing

*INVALID* · family `rrule.core` · policy axis `None`

input:
```
DTSTART:19970902T090000
RRULE:COUNT=5
```

**2 distinct answers:**

- **ice_cube@tz2026a, pandas@tz2026a, pandas@tz2026c, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a**
  <br>`ERROR`

- **rrule.js@tzle2026a**
  <br>`1997-09-02T09:00:00<br>1998-09-02T09:00:00<br>1999-09-02T09:00:00<br>2000-09-02T09:00:00<br>2001-09-02T09:00:00`


## `RRULE-CORE-018` — UNTIL earlier than DTSTART (empty recurrence set)

*AMBIGUOUS_STANDARD* · family `rrule.core` · policy axis `rrule.empty_set`

input:
```
DTSTART;TZID=America/New_York:19970902T090000
RRULE:FREQ=DAILY;UNTIL=19970901T130000Z
```

**2 distinct answers:**

- **ice_cube@tz2026a, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `empty`
  <br>`EMPTY`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``


## `RRULE-DST-003` — A recurrence whose local time is stable but whose UTC offset changes (the DST-safe property)

*NORMATIVE* · family `rrule.dst` · policy axis `None`

input:
```
DTSTART;TZID=America/New_York:20260301T090000
RRULE:FREQ=WEEKLY;COUNT=3
```

**2 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-03-01T09:00:00-05:00<br>2026-03-01T14:00:00Z<br>2026-03-08T09:00:00-04:00<br>2026-03-08T13:00:00Z<br>2026-03-15T09:00:00-04:00<br>2026-03-15T13:00:00Z`

- **ice_cube@tz2026a**
  <br>`2026-03-01T09:00:00+00:00<br>2026-03-01T09:00:00Z<br>2026-03-08T09:00:00+00:00<br>2026-03-08T09:00:00Z<br>2026-03-15T09:00:00+00:00<br>2026-03-15T09:00:00Z`


## `RRULE-DST-007` — UTC DTSTART is immune to DST by construction

*NORMATIVE* · family `rrule.dst` · policy axis `None`

input:
```
DTSTART:20260306T073000Z
RRULE:FREQ=DAILY;COUNT=4
```

**2 distinct answers:**

- **ice_cube@tz2026a, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2026-03-06T07:30:00+00:00<br>2026-03-06T07:30:00Z<br>2026-03-07T07:30:00+00:00<br>2026-03-07T07:30:00Z<br>2026-03-08T07:30:00+00:00<br>2026-03-08T07:30:00Z<br>2026-03-09T07:30:00+00:00<br>2026-03-09T07:30:00Z`

- **pandas@tz2026a, pandas@tz2026c**
  <br>`2026-03-06T07:30:00<br>2026-03-07T07:30:00<br>2026-03-08T07:30:00<br>2026-03-09T07:30:00`


## `RRULE-DST-011` — Zero-offset transition: Asia/Amman abolishes DST (2022)

*NORMATIVE* · family `rrule.dst` · policy axis `None`

input:
```
DTSTART;TZID=Asia/Amman:20221027T003000
RRULE:FREQ=DAILY;COUNT=4
```

**2 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2022-10-27T00:30:00+03:00<br>2022-10-26T21:30:00Z<br>2022-10-28T00:30:00+03:00<br>2022-10-27T21:30:00Z<br>2022-10-29T00:30:00+03:00<br>2022-10-28T21:30:00Z<br>2022-10-30T00:30:00+03:00<br>2022-10-29T21:30:00Z`

- **ice_cube@tz2026a**
  <br>`2022-10-27T00:30:00+00:00<br>2022-10-27T00:30:00Z<br>2022-10-28T00:30:00+00:00<br>2022-10-28T00:30:00Z<br>2022-10-29T00:30:00+00:00<br>2022-10-29T00:30:00Z<br>2022-10-30T00:30:00+00:00<br>2022-10-30T00:30:00Z`


## `RRULE-DST-012` — Zero-offset transition: Asia/Damascus abolishes DST (2022)

*NORMATIVE* · family `rrule.dst` · policy axis `None`

input:
```
DTSTART;TZID=Asia/Damascus:20221027T003000
RRULE:FREQ=DAILY;COUNT=4
```

**2 distinct answers:**

- **pandas@tz2026a, pandas@tz2026c, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a**
  <br>`2022-10-27T00:30:00+03:00<br>2022-10-26T21:30:00Z<br>2022-10-28T00:30:00+03:00<br>2022-10-27T21:30:00Z<br>2022-10-29T00:30:00+03:00<br>2022-10-28T21:30:00Z<br>2022-10-30T00:30:00+03:00<br>2022-10-29T21:30:00Z`

- **ice_cube@tz2026a**
  <br>`2022-10-27T00:30:00+00:00<br>2022-10-27T00:30:00Z<br>2022-10-28T00:30:00+00:00<br>2022-10-28T00:30:00Z<br>2022-10-29T00:30:00+00:00<br>2022-10-29T00:30:00Z<br>2022-10-30T00:30:00+00:00<br>2022-10-30T00:30:00Z`


## `RRULE-SET-009` — Every instance excluded: an empty recurrence set

*POLICY_DEPENDENT* · family `rrule.sets` · policy axis `rrule.empty_set`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
RRULE:FREQ=DAILY;COUNT=2
EXDATE;TZID=America/New_York:20260105T090000,20260106T090000
```

**2 distinct answers:**

- **ice_cube@tz2026a, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `empty`
  <br>`EMPTY`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``


## `RRULE-SET-013` — EXDATE alone with no RRULE

*AMBIGUOUS_STANDARD* · family `rrule.sets` · policy axis `rrule.dtstart_emission`

input:
```
DTSTART;TZID=America/New_York:20260105T090000
EXDATE;TZID=America/New_York:20260105T090000
```

**2 distinct answers:**

- **ice_cube@tz2026a, php-rrule@tz2026a, python-dateutil@tz2026a, python-dateutil@tz2026c, rrule-go@tz2026a, rrule.js@tzle2026a** → admissible case `empty`
  <br>`EMPTY`

- **pandas@tz2026a, pandas@tz2026c**
  <br>``


## `TZDB-007` — A zone whose historical data changed: Europe/Lisbon 1992

*NORMATIVE* · family `tzdb.provenance` · policy axis `None`

input: `0 12 * * *` from `1992-09-25T00:00:00` zone `Europe/Lisbon` × 4

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`1992-09-25T12:00:00+01:00<br>1992-09-25T11:00:00Z<br>1992-09-26T12:00:00+01:00<br>1992-09-26T11:00:00Z<br>1992-09-27T12:00:00+01:00<br>1992-09-27T11:00:00Z<br>1992-09-28T12:00:00+01:00<br>1992-09-28T11:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`


## `TZDB-009` — Deprecated zone alias (US/Pacific)

*DIALECT_DEPENDENT* · family `tzdb.provenance` · policy axis `tz.link_handling`

input: `0 12 * * *` from `2026-01-14T00:00:00` zone `US/Pacific` × 2

**2 distinct answers:**

- **apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026c, croniter[day_or=False]@tz2026c, cronsim@tz2026c, robfig-cron@tz2026a** → admissible case `links-present`
  <br>`2026-01-14T12:00:00-08:00<br>2026-01-14T20:00:00Z<br>2026-01-15T12:00:00-08:00<br>2026-01-15T20:00:00Z`

- **apscheduler3@tz2026a, cron-parser[strict]@tzle2026a, croniter@tz2026a, croniter[day_or=False]@tz2026a, cronsim@tz2026a, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron[seconds]@tz2026a** → admissible case `links-absent`
  <br>`ERROR`


## `TZDB-010` — Etc/GMT+5 has a NEGATIVE offset (POSIX sign inversion)

*NORMATIVE* · family `tzdb.provenance` · policy axis `None`

input: `0 12 * * *` from `2026-01-14T00:00:00` zone `Etc/GMT+5` × 2

**2 distinct answers:**

- **apscheduler3@tz2026a, apscheduler3@tz2026c, cron-parser@tzle2026a, croner@tzle2026a, croner[legacyMode=false]@tzle2026a, croniter@tz2026a, croniter@tz2026c, croniter[day_or=False]@tz2026a, croniter[day_or=False]@tz2026c, cronsim@tz2026a, cronsim@tz2026c, fugit@tz2026a, php-cron-expression@tz2026a, robfig-cron@tz2026a**
  <br>`2026-01-14T12:00:00-05:00<br>2026-01-14T17:00:00Z<br>2026-01-15T12:00:00-05:00<br>2026-01-15T17:00:00Z`

- **cron-parser[strict]@tzle2026a, robfig-cron[seconds]@tz2026a** → admissible case `rejected`
  <br>`ERROR`

