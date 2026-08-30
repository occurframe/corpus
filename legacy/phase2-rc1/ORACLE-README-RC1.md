# Occurframe conformance oracle — corpus v1.0.0-rc1

A cross-language conformance corpus for cron expressions and RFC 5545
recurrence rules, with runners in five languages and a differential matrix
over 25 engine builds.

Phase I's central finding was that **no such corpus exists**, so "RFC 5545
compliant" and "DST-safe" are unfalsifiable claims. This is the artefact that
makes them falsifiable.

```
oracle/
├── vectors/            THE CORPUS. 184 vectors, JSON Lines, one per line.
│   ├── manifest.json       counts, family index, source registry
│   ├── incumbents.json     frozen engine measurements, re-injected at build
│   ├── cron-*.jsonl        98 cron vectors in 9 families
│   ├── rrule-*.jsonl       76 RRULE vectors in 4 families
│   └── tzdb-provenance.jsonl   10 tzdb-version vectors
├── docs/
│   ├── FORMAT.md           the vector grammar and its rationale
│   ├── RUNNER-CONTRACT.md  what a third-party runner must do
│   └── VERSIONING.md       how vectors are added, corrected and retired
├── runners/
│   ├── run_python.py       dateutil · croniter · cronsim · APScheduler · pandas
│   ├── run_js.ts           rrule.js · cron-parser · croner · cronstrue (bun/node)
│   ├── go/main.go          robfig/cron · teambition/rrule-go
│   ├── run_php.php         dragonmantank/cron-expression · rlanvin/php-rrule
│   ├── run_ruby.rb         fugit · ice_cube
│   └── minimal_runner.py   a COMPLETE conforming runner in 40 lines of
│                           code (non-blank, non-comment; 53 physical)
├── reference/
│   └── cron_ref.py         independent policy-parameterised cron matcher.
│                           NOT an engine under test: it derives expected
│                           values from a declared policy so the oracle is
│                           not circular.
├── build/                  authoring source; regenerates vectors/
├── tools/
│   ├── make_matrix.py      scores raw results, writes the matrix
│   └── freeze_incumbents.py  folds measurements back into the vectors
├── raw/                    verbatim runner output, one file per runner/tzdb
├── matrix/
│   ├── matrix.md           the differential matrix + scoreboard
│   ├── divergences.md      every vector with >1 distinct answer, in full
│   ├── matrix.json         machine-readable verdicts
│   └── conformance-<engine>.md   a per-engine conformance report
└── engines/                engines vendored from git for this run
```

## Reproduce

Set `ORACLE_ROOT` to this directory and `PROBE_ROOT` to the Phase I probe checkout
that holds the vendored engine tree (`vendor/` plus `env.sh`); the engines and their
commits are listed in `engines/PROVENANCE.md`.

```sh
source "$PROBE_ROOT/env.sh"        # PYTHONPATH for vendored engines; see engines/PROVENANCE.md
cd "$ORACLE_ROOT"                  # this directory (phase-2/oracle)

# 1. build the corpus from its authoring source
(cd build && python3 build_all.py)

# 2. run every engine
python3 runners/run_python.py --vectors vectors --tzdata system   --out raw/python-tz2026a.jsonl
python3 runners/run_python.py --vectors vectors --tzdata vendored --out raw/python-tz2026c.jsonl
bun run runners/run_js.ts --vectors vectors --out raw/js-bun.jsonl
(cd runners/go && GOFLAGS=-mod=mod GOPROXY=off go build -o oracle-go-runner .)
./runners/go/oracle-go-runner --vectors vectors --out raw/go.jsonl
php -d max_execution_time=0 runners/run_php.php --vectors vectors --out raw/php.jsonl
ruby runners/run_ruby.rb --vectors vectors --out raw/ruby.jsonl

# 3. freeze incumbent measurements into the corpus and rebuild
python3 tools/freeze_incumbents.py --raw raw --out vectors/incumbents.json
(cd build && python3 build_all.py)

# 4. score
python3 tools/make_matrix.py --vectors vectors --raw raw --out matrix
```

## The one rule

**No expected value in this corpus is ever copied from an engine.** Expected
values come from (a) a quoted normative source, (b) RFC 5545's own printed
example instance lists, or (c) `reference/cron_ref.py`, an independent
matcher parameterised by an explicitly declared policy. Engine outputs are
recorded beside the expectation in `incumbents`, never as the expectation.
An oracle that learns its answers from the systems it grades is not an
oracle.
