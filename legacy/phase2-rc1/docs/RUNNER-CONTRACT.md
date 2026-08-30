# Runner contract v1

A **runner** is a program that executes corpus vectors against one or more
engines and reports what happened. It is the only thing a third party has to
write in order to join the corpus. Reference runners exist for Python, Bun/
Node, Go, PHP and Ruby under `runners/`; `runners/minimal_runner.py` is a
complete conforming runner in 40 lines of code (non-blank, non-comment lines;
53 physical lines).

## Invocation

```
runner [--vectors PATH] [--out PATH] [--engine NAME] [<engine-specific flags>]
```

* `--vectors PATH` — a `.jsonl` file or a directory of them. **If absent the
  runner MUST read JSON Lines from stdin.**
* `--out PATH` — where to write results. **If absent the runner MUST write to
  stdout.** Nothing else may be written to stdout.
* `--engine NAME` — optional filter; when given, only that engine runs.
* Diagnostics, warnings and progress go to **stderr**, never stdout.

A runner MUST NOT require network access, and MUST NOT mutate the vectors.

## Exit codes

| code | meaning |
|---|---|
| `0` | the run completed and results were emitted |
| `1` | fatal harness error (vectors unreadable, engine could not be imported) |
| `2` | usage error |

**A vector that fails, errors, crashes or hangs is a RESULT, not an exit
code.** A runner that exits non-zero because an engine raised has destroyed
the measurement. This is the single most important rule in the contract.

## Output

One JSON object per line, one line per `(vector, engine)` pair, in any order.

| field | type | required | meaning |
|---|---|---|---|
| `vector_id` | string | yes | the vector's `id` |
| `corpus_version` | string | yes | copied from the vector |
| `runner` | string | yes | identifies this runner program |
| `engine` | string | yes | engine name; append a bracketed suffix for a non-default configuration, e.g. `croniter[day_or=False]` |
| `engine_version` | string | yes | version **and** provenance: a release number, or a VCS host, repo and commit |
| `language` | string | yes | runtime and its version |
| `tzdb` | string | yes | the IANA tzdb release actually in use |
| `tzdb_source` | string | yes | where that data came from (a path, a bundled package, `runtime ICU`) |
| `status` | enum | yes | see below |
| `occurrences` | string[] | yes | canonical occurrence strings; `[]` when none |
| `error` | string\|null | yes | verbatim exception class and message, truncated to 500 bytes |
| `elapsed_ms` | number | no | wall time for the engine call |

### `status`

| value | meaning |
|---|---|
| `ok` | the engine returned at least one occurrence |
| `empty` | the engine returned successfully with no occurrences |
| `error` | the engine raised, rejected the input, or returned an error value |
| `crash` | the process-level failure was contained (segfault, recursion limit) |
| `timeout` | the engine did not return inside the runner's per-vector budget |
| `unsupported` | the engine cannot express this input (record why in `error`) |
| `unsupported_op` | the engine does not implement this `op` at all |

`unsupported` and `unsupported_op` are excluded from scoring. `error` is
**scored**: it is the correct answer for every `INVALID` vector.

### Per-vector time budget

A runner MUST bound each engine call and report `timeout` rather than
aborting the run. The reference runners use 8 s. Two engines in the shipped
matrix hit it, and both hangs are genuine findings.

## Occurrence encoding

Exactly two forms, chosen by whether the vector's input carries a zone.

* **Zoned** (`input.zone` set, or an RRULE whose DTSTART has `TZID=` or a `Z`
  suffix):
  `YYYY-MM-DDTHH:MM:SS±HH:MM|YYYY-MM-DDTHH:MM:SSZ`
  — the local wall time with its offset, a `|`, then the same instant in UTC.
  Both halves are required. An engine that only knows UTC must convert;
  an engine that only knows wall time must resolve the offset. Carrying both
  is what makes DST gaps, folds and tzdb divergence visible in a plain string
  comparison: `2026-11-01T01:30:00-04:00|2026-11-01T05:30:00Z` and
  `2026-11-01T01:30:00-05:00|2026-11-01T06:30:00Z` differ in the second half
  only.
* **Floating** (no zone anywhere): `YYYY-MM-DDTHH:MM:SS`.

Seconds are always present. No fractional seconds; no `T`-less forms; no
locale formatting. Comparison is byte equality of the whole array.

A description-only engine (cronstrue) emits a single element prefixed
`DESCRIPTION:`; scoring treats such a result as accept/reject evidence only.

## Operations

| `op` | input fields | required behaviour |
|---|---|---|
| `cron.next` | `expr`, `start`, `count`, `zone`, `fields`, `inclusive` | the first `count` occurrences strictly after `start` (at or after it when `inclusive`), with `start` interpreted in `zone` |
| `cron.parse` | as above, `count` = 1 | parse only; `error` if the expression is rejected. A runner MAY implement it by calling `cron.next` |
| `rrule.expand` | `ics`, `count`, `zone` | the first `count` members of the recurrence set defined by the `ics` block |
| `rrule.parse` | as above | parse only; a runner MAY implement it via `rrule.expand` |
| `rrule.between` | `ics`, `between: [a, b]`, `zone` | members strictly between the two local timestamps, in the engine's own inclusivity convention (which the vector is measuring) |

`input.ics` is a `\n`-separated block of iCalendar content lines:
`DTSTART` (optionally `;TZID=`), zero or more `RRULE`, `EXRULE`, `RDATE`,
`EXDATE`. No folding, no `BEGIN:VEVENT` wrapper, no CRLF.

## Registering a new engine

1. Write or extend a runner for its language.
2. Record the exact version *and* provenance in `engine_version`. "5.10.0" is
   not enough on its own if the build came from a VCS checkout.
3. Report the tzdb the process actually used. If the runtime does not expose
   it, fingerprint it: `TZDB-001`, `TZDB-002` and `TZDB-003` were chosen so
   that the offsets of `America/Vancouver`, `America/Edmonton` and
   `Africa/Casablanca` on three fixed instants identify the release band
   (`≤2026a` / `2026b` / `≥2026c`) without asking the runtime.
   `runners/run_js.ts` does this because neither Bun nor Node exposes a
   reliable tz version.
4. Run `tools/make_matrix.py`. A new engine never changes an expected value:
   expectations come from sources and from `reference/cron_ref.py`, never
   from an engine.
