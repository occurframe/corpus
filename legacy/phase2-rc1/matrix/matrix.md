# Differential conformance matrix

Corpus 1.0.0-rc1 · 184 vectors × 25 engine builds = 4600 measured cells · 164 vectors show >1 distinct answer.

Legend: `P` pass · `R` correctly rejected an invalid input · `F` fail · `N` novel behaviour on an already-ambiguous vector · `x` accepted an input that must be rejected · `H` did not terminate · `.` recorded, not scored · `-` operation not implemented.

## Engine builds

| key | engine | version | runtime | tzdb | tzdb source |
|---|---|---|---|---|---|
| `apscheduler3@tz2026a` | apscheduler3 | 3.11.3 (git agronholm/apscheduler @4308ec9, tag 3.11.3) | python 3.11.15 | **2026a** | /usr/share/zoneinfo |
| `apscheduler3@tz2026c` | apscheduler3 | 3.11.3 (git agronholm/apscheduler @4308ec9, tag 3.11.3) | python 3.11.15 | **2026c** | PyPI tzdata 2026.3 |
| `cron-parser@tzle2026a` | cron-parser | 5.10.0 (git harrisiirak/cron-parser @7b3a0ad 2026-08-28) | bun 1.3.13 | **le2026a** | runtime ICU (fingerprint le2026a) |
| `cron-parser[strict]@tzle2026a` | cron-parser[strict] | 5.10.0 (git harrisiirak/cron-parser @7b3a0ad 2026-08-28) | bun 1.3.13 | **le2026a** | runtime ICU (fingerprint le2026a) |
| `croner@tzle2026a` | croner | 10.0.1 (git Hexagon/croner @713ee72 2026-03-01) | bun 1.3.13 | **le2026a** | runtime ICU (fingerprint le2026a) |
| `croner[legacyMode=false]@tzle2026a` | croner[legacyMode=false] | 10.0.1 (git Hexagon/croner @713ee72 2026-03-01) | bun 1.3.13 | **le2026a** | runtime ICU (fingerprint le2026a) |
| `croniter@tz2026a` | croniter | 6.3.0.dev0 (git kiorky/croniter @3dd4d14 2026-08-14) | python 3.11.15 | **2026a** | /usr/share/zoneinfo |
| `croniter@tz2026c` | croniter | 6.3.0.dev0 (git kiorky/croniter @3dd4d14 2026-08-14) | python 3.11.15 | **2026c** | PyPI tzdata 2026.3 |
| `croniter[day_or=False]@tz2026a` | croniter[day_or=False] | 6.3.0.dev0 (git kiorky/croniter @3dd4d14 2026-08-14) | python 3.11.15 | **2026a** | /usr/share/zoneinfo |
| `croniter[day_or=False]@tz2026c` | croniter[day_or=False] | 6.3.0.dev0 (git kiorky/croniter @3dd4d14 2026-08-14) | python 3.11.15 | **2026c** | PyPI tzdata 2026.3 |
| `cronsim@tz2026a` | cronsim | 2.7 (git cuu508/cronsim @fd2e617, tag 2.7) | python 3.11.15 | **2026a** | /usr/share/zoneinfo |
| `cronsim@tz2026c` | cronsim | 2.7 (git cuu508/cronsim @fd2e617, tag 2.7) | python 3.11.15 | **2026c** | PyPI tzdata 2026.3 |
| `cronstrue@tzle2026a` | cronstrue | 3.24.0 (git bradymholt/cRonstrue @b62884a 2026-08-21) | bun 1.3.13 | **le2026a** | runtime ICU (fingerprint le2026a) |
| `fugit@tz2026a` | fugit | git floraison/fugit @efda655 2026-07-21 | ruby 3.3.6 | **2026a** | /usr/share/zoneinfo |
| `ice_cube@tz2026a` | ice_cube | git seejohnrun/ice_cube @32ff145 2026-01-20 | ruby 3.3.6 | **2026a** | /usr/share/zoneinfo |
| `pandas@tz2026a` | pandas | 3.0.2 | python 3.11.15 | **2026a** | /usr/share/zoneinfo |
| `pandas@tz2026c` | pandas | 3.0.2 | python 3.11.15 | **2026c** | PyPI tzdata 2026.3 |
| `php-cron-expression@tz2026a` | php-cron-expression | dragonmantank/cron-expression @d425a24 2025-12-20 | php 8.4.21 | **2026a** | /usr/share/zoneinfo |
| `php-rrule@tz2026a` | php-rrule | rlanvin/php-rrule @93a083d 2026-07-29 | php 8.4.21 | **2026a** | /usr/share/zoneinfo |
| `python-dateutil@tz2026a` | python-dateutil | 2.9.0.post0 | python 3.11.15 | **2026a** | /usr/share/zoneinfo |
| `python-dateutil@tz2026c` | python-dateutil | 2.9.0.post0 | python 3.11.15 | **2026c** | PyPI tzdata 2026.3 |
| `robfig-cron@tz2026a` | robfig-cron | v3.0.1 (git robfig/cron @bc59245 2021-01-06) | go1.24.7 | **2026a** | /usr/share/zoneinfo |
| `robfig-cron[seconds]@tz2026a` | robfig-cron[seconds] | v3.0.1 (git robfig/cron @bc59245 2021-01-06) | go1.24.7 | **2026a** | /usr/share/zoneinfo |
| `rrule-go@tz2026a` | rrule-go | v1.8.x (git teambition/rrule-go @e74d163 2023-04-01) | go1.24.7 | **2026a** | /usr/share/zoneinfo |
| `rrule.js@tzle2026a` | rrule.js | 2.8.0 (git jkbrzt/rrule @9f2061f 2023-11-10) | bun 1.3.13 | **le2026a** | runtime ICU (fingerprint le2026a) |

## Scoreboard

| engine build | scored | passed | rate | P | R | F | N | x | H | . | - |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `apscheduler3@tz2026a` | 107 | 84 | 78.5% | 69 | 15 | 23 | 0 | 0 | 0 | 0 | 77 |
| `apscheduler3@tz2026c` | 107 | 85 | 79.4% | 70 | 15 | 22 | 0 | 0 | 0 | 0 | 77 |
| `cron-parser@tzle2026a` | 107 | 100 | 93.5% | 87 | 13 | 5 | 0 | 2 | 0 | 0 | 77 |
| `cron-parser[strict]@tzle2026a` | 107 | 65 | 60.7% | 50 | 15 | 42 | 0 | 0 | 0 | 0 | 77 |
| `croner@tzle2026a` | 107 | 96 | 89.7% | 81 | 15 | 11 | 0 | 0 | 0 | 0 | 77 |
| `croner[legacyMode=false]@tzle2026a` | 107 | 101 | 94.4% | 86 | 15 | 6 | 0 | 0 | 0 | 0 | 77 |
| `croniter@tz2026a` | 107 | 102 | 95.3% | 87 | 15 | 4 | 1 | 0 | 0 | 0 | 77 |
| `croniter@tz2026c` | 107 | 102 | 95.3% | 87 | 15 | 4 | 1 | 0 | 0 | 0 | 77 |
| `croniter[day_or=False]@tz2026a` | 107 | 103 | 96.3% | 88 | 15 | 4 | 0 | 0 | 0 | 0 | 77 |
| `croniter[day_or=False]@tz2026c` | 107 | 103 | 96.3% | 88 | 15 | 4 | 0 | 0 | 0 | 0 | 77 |
| `cronsim@tz2026a` | 107 | 101 | 94.4% | 86 | 15 | 6 | 0 | 0 | 0 | 0 | 77 |
| `cronsim@tz2026c` | 107 | 101 | 94.4% | 86 | 15 | 6 | 0 | 0 | 0 | 0 | 77 |
| `cronstrue@tzle2026a` | 19 | 15 | 78.9% | 3 | 12 | 1 | 0 | 3 | 0 | 88 | 77 |
| `fugit@tz2026a` | 107 | 104 | 97.2% | 90 | 14 | 2 | 0 | 1 | 0 | 0 | 77 |
| `ice_cube@tz2026a` | 71 | 13 | 18.3% | 9 | 4 | 47 | 7 | 3 | 1 | 5 | 108 |
| `pandas@tz2026a` | 16 | 13 | 81.2% | 11 | 2 | 2 | 1 | 0 | 0 | 2 | 166 |
| `pandas@tz2026c` | 16 | 13 | 81.2% | 11 | 2 | 2 | 1 | 0 | 0 | 2 | 166 |
| `php-cron-expression@tz2026a` | 107 | 99 | 92.5% | 84 | 15 | 7 | 1 | 0 | 0 | 0 | 77 |
| `php-rrule@tz2026a` | 72 | 68 | 94.4% | 60 | 8 | 3 | 1 | 0 | 0 | 5 | 107 |
| `python-dateutil@tz2026a` | 72 | 60 | 83.3% | 57 | 3 | 6 | 1 | 5 | 0 | 5 | 107 |
| `python-dateutil@tz2026c` | 72 | 60 | 83.3% | 57 | 3 | 6 | 1 | 5 | 0 | 5 | 107 |
| `robfig-cron@tz2026a` | 107 | 104 | 97.2% | 89 | 15 | 1 | 1 | 0 | 1 | 0 | 77 |
| `robfig-cron[seconds]@tz2026a` | 107 | 65 | 60.7% | 50 | 15 | 42 | 0 | 0 | 0 | 0 | 77 |
| `rrule-go@tz2026a` | 72 | 61 | 84.7% | 58 | 3 | 3 | 3 | 5 | 0 | 5 | 107 |
| `rrule.js@tzle2026a` | 72 | 57 | 79.2% | 56 | 1 | 6 | 2 | 7 | 0 | 5 | 107 |

## Matrix

Columns, in order: **1**=`apscheduler3@tz2026a` · **2**=`apscheduler3@tz2026c` · **3**=`cron-parser@tzle2026a` · **4**=`cron-parser[strict]@tzle2026a` · **5**=`croner@tzle2026a` · **6**=`croner[legacyMode=false]@tzle2026a` · **7**=`croniter@tz2026a` · **8**=`croniter@tz2026c` · **9**=`croniter[day_or=False]@tz2026a` · **10**=`croniter[day_or=False]@tz2026c` · **11**=`cronsim@tz2026a` · **12**=`cronsim@tz2026c` · **13**=`cronstrue@tzle2026a` · **14**=`fugit@tz2026a` · **15**=`ice_cube@tz2026a` · **16**=`pandas@tz2026a` · **17**=`pandas@tz2026c` · **18**=`php-cron-expression@tz2026a` · **19**=`php-rrule@tz2026a` · **20**=`python-dateutil@tz2026a` · **21**=`python-dateutil@tz2026c` · **22**=`robfig-cron@tz2026a` · **23**=`robfig-cron[seconds]@tz2026a` · **24**=`rrule-go@tz2026a` · **25**=`rrule.js@tzle2026a`

| vector | class | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | dist |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `CRON-ANCH-001` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `CRON-ANCH-002` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-ANCH-003` | POLI | F | F | P | P | P | P | F | F | F | F | P | P | . | P | - | - | - | F | - | - | - | F | P | - | - | **3** |
| `CRON-ANCH-004` | NORM | F | F | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `CRON-DAYF-001` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-DAYF-002` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **4** |
| `CRON-DAYF-003` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-DAYF-004` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-DAYF-005` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-DAYF-006` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **4** |
| `CRON-DAYF-010` | KNOW | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **4** |
| `CRON-DAYF-011` | KNOW | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **4** |
| `CRON-DAYF-012` | KNOW | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **4** |
| `CRON-DAYF-013` | KNOW | P | P | P | P | P | P | N | N | P | P | P | P | . | P | - | - | - | N | - | - | - | N | P | - | - | **3** |
| `CRON-DOW-001` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-DOW-002` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-DOW-003` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-DOW-004` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-DOW-005` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-DOW-006` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-DOW-007` | NORM | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | F | - | - | - | P | P | - | - | **3** |
| `CRON-DOW-008` | NORM | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-DOW-009` | NORM | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-DOW-010` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | P | P | - | - | - | P | - | - | - | P | P | - | - | 0 |
| `CRON-DOW-011` | DIAL | F | F | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | F | - | - | - | P | P | - | - | **4** |
| `CRON-DOW-012` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-DOW-013` | NORM | F | F | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `CRON-DST-001` | POLI | F | F | F | F | F | F | P | P | P | P | P | P | . | P | - | - | - | F | - | - | - | P | F | - | - | **5** |
| `CRON-DST-002` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `CRON-DST-003` | POLI | F | F | P | F | F | F | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **5** |
| `CRON-DST-004` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **4** |
| `CRON-DST-005` | POLI | F | F | F | F | F | F | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **5** |
| `CRON-DST-006` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **4** |
| `CRON-DST-007` | POLI | F | F | P | F | F | F | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | H | F | - | - | **6** |
| `CRON-DST-008` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-DST-009` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-DST-010` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-DST-011` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-DST-012` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-DST-013` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-DST-014` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-DST-015` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-DST-016` | POLI | F | F | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **4** |
| `CRON-DST-017` | POLI | F | F | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `CRON-DST-018` | POLI | F | F | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `CRON-DST-019` | POLI | F | F | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `CRON-DST-020` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-EXT-001` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-EXT-002` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | 0 |
| `CRON-EXT-003` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-EXT-004` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-EXT-005` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | F | - | - | - | P | P | - | - | **3** |
| `CRON-EXT-006` | DIAL | P | P | P | P | F | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-EXT-007` | DIAL | P | P | P | P | F | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-EXT-008` | DIAL | P | P | P | P | F | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-EXT-009` | DIAL | P | P | P | P | F | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-EXT-010` | AMBI | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-EXT-011` | DIAL | P | P | F | P | P | P | P | P | P | P | P | P | P | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-EXT-012` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | P | F | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-EXT-013` | AMBI | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | 0 |
| `CRON-EXT-014` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-FIELDS-001` | NORM | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-FIELDS-002` | DIAL | P | P | P | P | P | P | F | F | F | F | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-FIELDS-003` | DIAL | P | P | P | P | F | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-FIELDS-004` | DIAL | P | P | P | P | P | P | F | F | F | F | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **3** |
| `CRON-FIELDS-005` | INVA | R | R | x | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | **2** |
| `CRON-FIELDS-006` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-FIELDS-007` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | 0 |
| `CRON-FIELDS-008` | NORM | F | F | P | P | P | P | P | P | P | P | F | F | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-FIELDS-009` | NORM | F | F | P | P | P | P | P | P | P | P | F | F | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-FIELDS-010` | NORM | F | F | P | P | P | P | P | P | P | P | F | F | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-FIELDS-011` | NORM | F | F | P | P | P | P | P | P | P | P | F | F | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-FIELDS-012` | NORM | F | F | P | P | P | P | P | P | P | P | F | F | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-FIELDS-013` | AMBI | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | 0 |
| `CRON-INV-001` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-INV-002` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | R | x | - | - | - | R | - | - | - | R | R | - | - | **2** |
| `CRON-INV-003` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-INV-004` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-INV-005` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-INV-006` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-INV-007` | AMBI | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-INV-008` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-INV-009` | INVA | R | R | x | R | R | R | R | R | R | R | R | R | R | R | - | - | - | R | - | - | - | R | R | - | - | **2** |
| `CRON-INV-010` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | x | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-INV-011` | AMBI | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-INV-012` | NORM | P | P | P | F | P | P | P | P | P | P | P | P | F | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-STEP-001` | NORM | F | F | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `CRON-STEP-002` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-STEP-003` | DIAL | P | P | F | F | P | P | F | F | F | F | F | F | . | F | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-STEP-004` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | F | - | - | - | P | P | - | - | **3** |
| `CRON-STEP-005` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | x | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-STEP-006` | NORM | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `CRON-STEP-007` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `CRON-STEP-008` | NORM | F | F | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `CRON-STEP-009` | NORM | F | F | P | F | F | F | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **4** |
| `CRON-STEP-010` | NORM | F | F | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `CRON-STEP-011` | INVA | R | R | R | R | R | R | R | R | R | R | R | R | x | R | - | - | - | R | - | - | - | R | R | - | - | 0 |
| `CRON-STEP-012` | NORM | F | F | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `RRULE-BY-001` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-002` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-003` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-004` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-005` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-006` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-007` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-008` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-009` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-010` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-011` | DIAL | - | - | - | - | - | - | - | - | - | - | - | - | - | - | P | - | - | - | P | P | P | - | - | P | P | **2** |
| `RRULE-BY-012` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-013` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-014` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-015` | INVA | - | - | - | - | - | - | - | - | - | - | - | - | - | - | R | - | - | - | R | R | R | - | - | R | R | **2** |
| `RRULE-BY-016` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | P | - | - | - | P | P | P | - | - | P | P | **2** |
| `RRULE-BY-017` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-018` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-019` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-020` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-021` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-022` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-023` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | . | - | - | - | . | . | . | - | - | . | . | **3** |
| `RRULE-BY-024` | INVA | - | - | - | - | - | - | - | - | - | - | - | - | - | - | R | - | - | - | R | x | x | - | - | x | x | **3** |
| `RRULE-BY-025` | INVA | - | - | - | - | - | - | - | - | - | - | - | - | - | - | x | - | - | - | R | x | x | - | - | x | x | **4** |
| `RRULE-BY-026` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | . | - | - | - | . | . | . | - | - | . | . | **3** |
| `RRULE-BY-027` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | N | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-028` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-029` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-030` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-031` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-BY-032` | INVA | - | - | - | - | - | - | - | - | - | - | - | - | - | - | H | - | - | - | R | x | x | - | - | R | x | **4** |
| `RRULE-CORE-001` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | P | P | - | P | P | P | - | - | P | P | **2** |
| `RRULE-CORE-002` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | P | P | - | P | P | P | - | - | P | P | **2** |
| `RRULE-CORE-003` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | N | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-CORE-004` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-CORE-005` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-CORE-006` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | F | **4** |
| `RRULE-CORE-007` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | F | **4** |
| `RRULE-CORE-008` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | F | **4** |
| `RRULE-CORE-009` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | P | - | - | - | P | P | P | - | - | P | P | **2** |
| `RRULE-CORE-010` | INVA | - | - | - | - | - | - | - | - | - | - | - | - | - | - | x | - | - | - | R | R | R | - | - | x | x | **3** |
| `RRULE-CORE-011` | INVA | - | - | - | - | - | - | - | - | - | - | - | - | - | - | x | - | - | - | R | x | x | - | - | x | x | **4** |
| `RRULE-CORE-012` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | P | P | - | P | P | P | - | - | P | P | **2** |
| `RRULE-CORE-013` | POLI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-CORE-014` | POLI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | P | P | P | - | - | P | P | 0 |
| `RRULE-CORE-015` | INVA | - | - | - | - | - | - | - | - | - | - | - | - | - | - | R | R | R | - | R | R | R | - | - | R | x | **2** |
| `RRULE-CORE-016` | INVA | - | - | - | - | - | - | - | - | - | - | - | - | - | - | R | R | R | - | R | x | x | - | - | x | x | **4** |
| `RRULE-CORE-017` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | P | P | P | - | P | P | P | - | - | N | P | **3** |
| `RRULE-CORE-018` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | P | - | - | - | P | P | P | - | - | P | P | **2** |
| `RRULE-DST-001` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | N | N | N | - | N | N | N | - | - | N | N | **5** |
| `RRULE-DST-002` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | F | F | - | P | P | P | - | - | P | P | **3** |
| `RRULE-DST-003` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | P | P | - | P | P | P | - | - | P | P | **2** |
| `RRULE-DST-004` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | . | . | . | - | . | . | . | - | - | . | . | **3** |
| `RRULE-DST-005` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | . | . | . | - | . | . | . | - | - | . | . | **5** |
| `RRULE-DST-006` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | . | - | - | - | . | . | . | - | - | . | . | **5** |
| `RRULE-DST-007` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | P | F | F | - | P | P | P | - | - | P | P | **2** |
| `RRULE-DST-008` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | P | P | P | - | P | P | P | - | - | P | P | 0 |
| `RRULE-DST-009` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | P | P | - | F | F | F | - | - | F | P | **3** |
| `RRULE-DST-010` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | P | P | - | F | F | F | - | - | F | P | **4** |
| `RRULE-DST-011` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | P | P | - | P | P | P | - | - | P | P | **2** |
| `RRULE-DST-012` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | P | P | - | P | P | P | - | - | P | P | **2** |
| `RRULE-SET-001` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-SET-002` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | F | F | - | - | P | F | **5** |
| `RRULE-SET-003` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | F | F | - | - | P | P | **4** |
| `RRULE-SET-004` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | N | - | - | - | P | P | P | - | - | P | P | **4** |
| `RRULE-SET-005` | POLI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | P | P | **3** |
| `RRULE-SET-006` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | N | - | - | - | P | P | P | - | - | P | P | **4** |
| `RRULE-SET-007` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | F | F | - | - | P | F | **5** |
| `RRULE-SET-008` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | N | - | - | - | P | P | P | - | - | N | N | **5** |
| `RRULE-SET-009` | POLI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | P | - | - | - | P | P | P | - | - | P | P | **2** |
| `RRULE-SET-010` | DIAL | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | P | P | - | - | F | P | **4** |
| `RRULE-SET-011` | DIAL | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | F | P | P | - | - | P | P | **4** |
| `RRULE-SET-012` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | N | - | - | - | P | P | P | - | - | P | P | **4** |
| `RRULE-SET-013` | AMBI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | P | - | - | - | P | P | P | - | - | P | P | **2** |
| `RRULE-SET-014` | NORM | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | - | - | - | P | F | F | - | - | P | F | **5** |
| `TZDB-001` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `TZDB-002` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `TZDB-003` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `TZDB-004` | POLI | - | - | - | - | - | - | - | - | - | - | - | - | - | - | F | P | P | - | P | P | P | - | - | P | P | **3** |
| `TZDB-005` | POLI | F | P | F | F | F | F | P | P | P | P | P | P | . | P | - | - | - | F | - | - | - | P | F | - | - | **6** |
| `TZDB-006` | POLI | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **3** |
| `TZDB-007` | NORM | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
| `TZDB-008` | INVA | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | 0 |
| `TZDB-009` | DIAL | P | P | P | P | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | P | - | - | **2** |
| `TZDB-010` | NORM | P | P | P | F | P | P | P | P | P | P | P | P | . | P | - | - | - | P | - | - | - | P | F | - | - | **2** |
