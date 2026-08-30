# Versioning and change control

## Corpus version

`corpus_version` is stamped into every vector and echoed by every runner, so
a result is never orphaned from the corpus that produced it. It is
`MAJOR.MINOR.PATCH`:

* **PATCH** — a vector's `rationale`, `title`, `normative` citations,
  `incumbents` or `tags` changed. No `input` and no `expect` changed. Every
  previously passing result stays valid; no re-run is required.
* **MINOR** — vectors were **added**, or an `expect` gained an admissible
  case that did not exist before (a newly discovered policy an engine
  implements). Existing verdicts cannot flip from pass to fail; they may flip
  from `NOVEL` to `PASS[label]`. Re-run to pick up the new coverage.
* **MAJOR** — an `input` changed, an `expect` narrowed, a classification
  moved, or the runner contract changed. Verdicts may flip in either
  direction. A conformance report against an older MAJOR is not comparable.

A published conformance report MUST name the corpus version, the engine
version and the tzdb release; any two of the three are insufficient.

## Adding a vector

1. Write it in `build/{cron,rrule,tz}_vectors.py`, next to its family.
2. Give it the next free number in its subfamily. Numbers are permanent and
   are never reused, including after retirement.
3. Supply, in order of preference: a quoted normative source; or an
   enumeration of admissible cases with a `when` policy map; or `expect.mode
   = "open"` with a note saying why the space cannot be enumerated.
   **A fabricated single answer is worse than an honest `open`.**
4. If the expected value is mechanical, derive it from
   `reference/cron_ref.py` under an explicitly named policy rather than
   typing it. If it is transcribed from a standard, add a structural
   assertion beside it (weekday, day-of-month, ISO week) so a typo cannot
   survive the build — see `assert_weekday` / `assert_dom` in
   `build/rrule_vectors.py`.
5. Rebuild, re-run every runner, re-freeze incumbents, regenerate the matrix.

## Correcting a vector

* **The expectation was wrong, the input is right** → correct in place, bump
  MAJOR, and record the correction in the vector's `rationale`. The ID does
  not change, so historical reports remain interpretable.
* **The input itself must change** → the vector is *retired*: it keeps its ID
  and gains `"status": "retired"` plus `"superseded_by": "<new id>"`, and a
  new vector is added with a new number. Runners skip retired vectors;
  scorers report them separately. This is the only way a result set from an
  older corpus version can still be read.

## tzdb-dependent vectors

A vector whose answer depends on zone data declares it in `context`:

* `tzdb_min` — the oldest tzdb release for which the stated expectation
  holds. A runner reporting an older release is scored `N/A`, not `FAIL`.
* `tzdb_pin: "per-case"` — the expectation is *keyed by release*: each
  `expect.cases` entry carries `when: {"tz.tzdb_version": "2026a"}` and the
  scorer selects by the runner's reported `tzdb`.

Zone data is the only input to this corpus that changes without anyone
editing it. Roughly four tzdb releases a year change future timestamps, and
2026 alone produced two that changed North American offsets
(`2026b` British Columbia, `2026c` Alberta). A corpus that pinned one
release would be wrong within months; a corpus that ignored the release
would be untestable. Keying by release is the only stable option, and it is
also what forces every conformance report to state its zone data.

## Policy axes

Policy axis names are namespaced (`cron.dom_dow`, `cron.dst_gap`,
`rrule.dtstart_emission`, `tz.tzdb_version`) and are append-only within a
MAJOR. A product declares conformance as a map from axis to value; the
scorer then selects the single admissible case per vector and grades against
it. Adding a *value* to an axis is MINOR; renaming or removing one is MAJOR.

The current axes, with their observed values:

| axis | values |
|---|---|
| `cron.dom_dow` | `or/vixie` · `or-any-nonstar` · `or-set-semantics` · `and` · `and+monday-zero` · `nth` · `reject` · `exclusive` |
| `cron.dow_numbering` | `both` (0 and 7 = Sunday) · `zero` (POSIX) · `quartz` (1=SUN) · `monday_zero` (APScheduler) |
| `cron.sixth_field` | `seconds` (leading) · `seconds_trailing` · `year` · `reject` |
| `cron.bare_start_step` | `start_at` · `ignore_step` · `reject` |
| `cron.step_gt_field` | `accept` · `reject` |
| `cron.range_wrap` | `wrap` · `reject` |
| `cron.dst_gap` | `skip` · `next_valid` · `fire_at_gap_start` · `shift_one_hour` |
| `cron.dst_fold` | `first` · `second` · `both` |
| `cron.start_inclusivity` | `exclusive` · `inclusive` |
| `cron.start_truncation` | `exact` · `truncate` |
| `cron.empty_set` | `empty` · `reject` · `raise` · `unbounded` |
| `cron.L` / `cron.W` / `cron.hash` / `cron.qmark` | `supported` · `unsupported` |
| `rrule.dtstart_emission` | `always` · `if_matching` · `seed_only` · `reject` |
| `rrule.gap` | `omit` · `pre_gap_offset` · `imaginary` · `shift_backward` |
| `rrule.truncation` | `lazy` · `caller_window` · `materialise` |
| `rrule.range_inclusivity` | `[a,b]` · `[a,b)` · `(a,b)` |
| `rrule.exdate_value_type` | `date_matches_day` · `date_is_midnight` · `must_match_dtstart` |
| `rrule.exdate_matching` | `instant` · `wall` |
| `rrule.note2` | `pre_errata` · `post_errata` |
| `rrule.multiple_rrule` | `union` · `first` · `reject` |
| `rrule.rscale_support` | `yes` · `ignore` · `no` |
| `tz.tzdb_version` | `2026a` · `2026b` · `2026c` · … |
| `tz.link_handling` | `resolve` · `reject` |
