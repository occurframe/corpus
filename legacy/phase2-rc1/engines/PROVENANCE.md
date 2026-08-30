# Vendored engine provenance

Package registries (npm, PyPI, RubyGems, Packagist, crates.io, proxy.golang.org)
were unreachable during this run; every engine was cloned from GitHub and its
commit recorded. Engines already vendored by the Phase I probe are reused from
`/home/claude/calendar-probe/vendor/` and are NOT duplicated here.

| directory | repository | commit | date |
|---|---|---|---|
| `robfig-cron` | github.com/robfig/cron | `bc59245fe10efaed9d51b56900192527ed733435` (tag v3.0.1) | 2021-01-06 |
| `rrule-go` | github.com/teambition/rrule-go | `e74d163475cf1ca1fd019752c5c41ea1f472d4c5` | 2023-04-01 |
| `php-cron-expression` | github.com/dragonmantank/cron-expression | `d425a2403c17d7cf911c55a7170f073979a9f382` | 2025-12-20 |
| `php-rrule` | github.com/rlanvin/php-rrule | `93a083db12dcb6f58e4840392a22e158ce96f1ff` | 2026-07-29 |
| `fugit` | github.com/floraison/fugit | `efda655251c2ae86780f7e472a61653b5b4b528b` | 2026-07-21 |
| `et-orbi` | github.com/floraison/et-orbi | `4725bc964c76bc8752abaff684944b404b49fbec` | 2026-08-28 |
| `raabro` | github.com/floraison/raabro | `af88c0117167538257de731af547ef5e8ce287db` | 2026-08-29 |
| `ice_cube` | github.com/seejohnrun/ice_cube | `32ff145baf152ae4aa130376d66041eba174b085` | 2026-01-20 |
| `tzinfo` | github.com/tzinfo/tzinfo | `ca5752c4b17501b6e08622a9428bca1ceea41e42` | 2025-12-30 |
| `concurrent-ruby` | github.com/ruby-concurrency/concurrent-ruby | (tzinfo runtime dependency) | — |

Reused from the Phase I probe (`/home/claude/calendar-probe/vendor/`):

| engine | commit | date |
|---|---|---|
| croniter | `3dd4d14e971294c03d3fb9be3f5ca03ae1c25310` | 2026-08-14 |
| cronsim | `fd2e617787e94b15beee27fee6ebe6cbe79a72a2` (tag 2.7) | 2025-10-21 |
| APScheduler 3.x | `4308ec95b94069f5dbdddb6c60fb792dfc8c40a4` (tag 3.11.3) | 2026-06-28 |
| rrule.js | `9f2061febeeb363d03352efe33d30c33073a0242` | 2023-11-10 |
| cron-parser | `7b3a0ad748bffd6eaf6af4caac4d83b1fc392378` | 2026-08-28 |
| croner | `713ee7217e3bbb01857559199e312149d2695edb` | 2026-03-01 |
| cronstrue | `b62884a10cc76705c53be65210784108a6d337dd` | 2026-08-21 |
| luxon | `f427515a38f6a671f8de663e6bcc040ed81f114e` | 2026-08-09 |
| PyPI tzdata | `6c7fa78dc6b8fc9bf5301a0a1052d336f7efa192` (2026.3 / IANA 2026c) | 2026-08-04 |

Timezone data actually used, by runtime:

| runtime | tzdb | source |
|---|---|---|
| Python (default) | 2026a | `/usr/share/zoneinfo` (Ubuntu `tzdata 2026a-0ubuntu0.24.04.1`) |
| Python (`--tzdata vendored`) | 2026c | PyPI `tzdata` 2026.3 |
| Go 1.24.7 | 2026a | `/usr/share/zoneinfo` |
| PHP 8.4.21 | 2026a | `timezone_version_get() == "0.system"` |
| Ruby 3.3.6 / tzinfo | 2026a | `TZInfo::DataSources::ZoneinfoDataSource` |
| Node 22.22.2 | 2025c | bundled ICU 78.2 (`process.versions.tz`) |
| Bun 1.3.13 | ≤2026a | ICU; version not exposed, fingerprinted via TZDB-001/002/003 |
