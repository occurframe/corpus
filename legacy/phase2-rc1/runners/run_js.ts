// Occurframe conformance-oracle runner: JavaScript/TypeScript engines.
// Run:  bun run runners/run_js.ts --vectors vectors --out raw/js.jsonl
//
// RUNNER CONTRACT: JSONL vectors in (stdin or --vectors), JSONL results out
// (stdout or --out). Exit 0 = ran; 1 = fatal harness error; 2 = usage error.
// Per-vector failures are RESULTS, never exit codes.
//
// Engines vendored from git (npm registry unreachable in this container):
//   rrule        2.8.0   jkbrzt/rrule           @9f2061f 2023-11-10
//   cron-parser  5.10.0  harrisiirak/cron-parser@7b3a0ad 2026-08-28
//   croner       10.0.1  Hexagon/croner         @713ee72 2026-03-01
//   cronstrue    3.24.0  bradymholt/cRonstrue   @b62884a 2026-08-21
//   luxon        3.7.2   moment/luxon           @f427515 2026-08-09
import { readFileSync, readdirSync, writeFileSync, statSync } from 'fs'
import { join } from 'path'
import { rrulestr } from '../../../calendar-probe/vendor/rrule/src/rrulestr'
import { CronExpressionParser } from '../../../calendar-probe/vendor/cron-parser/src/index'
import { Cron } from '../../../calendar-probe/vendor/croner/src/croner'
import cronstrue from '../../../calendar-probe/vendor/cRonstrue/src/cronstrue'
import { DateTime } from 'luxon'

// tzdb fingerprint: infer the release band from three zones that changed in
// three different releases. Bun does not expose process.versions.tz, and no
// runtime exposes it reliably, so the corpus AUDITS the claim instead of
// trusting it — see TZDB-001/002/003.
function tzdbFingerprint(): string {
  const off = (zone: string, iso: string) => DateTime.fromISO(iso, { zone }).offset
  const van = off('America/Vancouver', '2026-11-02T12:00')
  const edm = off('America/Edmonton', '2026-11-02T12:00')
  const cas = off('Africa/Casablanca', '2026-09-21T12:00')
  if (van === -480) return 'le2026a'
  if (edm === -420 || cas === 60) return '2026b'
  return 'ge2026c'
}
const TZDB = (process as any).versions?.tz ?? tzdbFingerprint()
const RUNTIME = (globalThis as any).Bun
  ? `bun ${(globalThis as any).Bun.version}`
  : `node ${process.version}`

const args = process.argv.slice(2)
function opt(name: string): string | undefined {
  const i = args.indexOf('--' + name)
  return i >= 0 ? args[i + 1] : undefined
}

function loadVectors(p?: string): any[] {
  let text: string
  if (!p) text = readFileSync(0, 'utf8')
  else if (statSync(p).isDirectory())
    text = readdirSync(p).filter(f => f.endsWith('.jsonl')).sort()
      .map(f => readFileSync(join(p, f), 'utf8')).join('')
  else text = readFileSync(p, 'utf8')
  return text.split('\n').filter(l => l.trim()).map(l => JSON.parse(l))
}

// ---------------------------------------------------------------- formatting
function offStr(mins: number): string {
  const s = mins >= 0 ? '+' : '-'
  const a = Math.abs(mins)
  return `${s}${String(Math.floor(a / 60)).padStart(2, '0')}:${String(a % 60).padStart(2, '0')}`
}
function fmtZoned(d: Date, zone: string): string {
  const dt = DateTime.fromJSDate(d).setZone(zone)
  const loc = dt.toFormat("yyyy-LL-dd'T'HH:mm:ss") + offStr(dt.offset)
  return loc + '|' + d.toISOString().replace(/\.\d{3}Z$/, 'Z')
}
function fmtFloatingFromUTCFields(d: Date): string {
  return d.toISOString().replace(/\.\d{3}Z$/, '').replace(/Z$/, '')
}
function fmtLocalNaive(d: Date): string {
  // a Date carrying wall-clock fields in UTC position
  return d.toISOString().slice(0, 19)
}

// ---------------------------------------------------------------- ics parse
function parseIcs(ics: string) {
  const out: any = { dtstart: null, tzid: null, rrule: [], exrule: [], rdate: [], exdate: [] }
  for (const line of ics.split('\n')) {
    const ci = line.indexOf(':')
    const name = line.slice(0, ci), value = line.slice(ci + 1)
    const parts = name.split(';')
    const key = parts[0].toUpperCase()
    const pd: any = {}
    for (const p of parts.slice(1)) { const [k, v] = p.split('='); pd[k.toUpperCase()] = v }
    if (key === 'DTSTART') { out.dtstart = value; out.tzid = pd.TZID }
    else if (key === 'RRULE') out.rrule.push(value)
    else if (key === 'EXRULE') out.exrule.push(value)
    else if (key === 'RDATE') out.rdate.push([pd, value])
    else if (key === 'EXDATE') out.exdate.push([pd, value])
  }
  return out
}

// ---------------------------------------------------------------- engines
type Res = string[]
interface Engine { name: string; version: string; ops: string[]; run(v: any): Res }

const cronParser: Engine = {
  name: 'cron-parser',
  version: '5.10.0 (git harrisiirak/cron-parser @7b3a0ad 2026-08-28)',
  ops: ['cron.next', 'cron.parse'],
  run(v) {
    const i = v.input
    const o: any = { currentDate: i.start }
    if (i.zone) o.tz = i.zone
    const it = CronExpressionParser.parse(i.expr, o)
    const out: string[] = []
    for (let k = 0; k < i.count; k++) {
      const d = it.next()
      out.push(i.zone ? fmtZoned(d.toDate(), i.zone) : fmtLocalNaive(d.toDate()))
    }
    return out
  },
}

const cronParserStrict: Engine = {
  name: 'cron-parser[strict]',
  version: cronParser.version,
  ops: ['cron.next', 'cron.parse'],
  run(v) {
    const i = v.input
    const o: any = { currentDate: i.start, strict: true }
    if (i.zone) o.tz = i.zone
    const it = CronExpressionParser.parse(i.expr, o)
    const out: string[] = []
    for (let k = 0; k < i.count; k++) {
      const d = it.next()
      out.push(i.zone ? fmtZoned(d.toDate(), i.zone) : fmtLocalNaive(d.toDate()))
    }
    return out
  },
}

function cronerRun(v: any, opts: any): Res {
  const i = v.input
  const o: any = { ...opts }
  if (i.zone) o.timezone = i.zone
  const c = new Cron(i.expr, o)
  // croner interprets a Date argument as an absolute instant
  const startMs = i.zone
    ? DateTime.fromISO(i.start, { zone: i.zone }).toJSDate()
    : new Date(i.start + 'Z')
  let prev: Date | null = startMs
  const out: string[] = []
  for (let k = 0; k < i.count; k++) {
    prev = c.nextRun(prev)
    if (!prev) break
    out.push(i.zone ? fmtZoned(prev, i.zone) : fmtLocalNaive(prev))
  }
  return out
}

const croner: Engine = {
  name: 'croner',
  version: '10.0.1 (git Hexagon/croner @713ee72 2026-03-01)',
  ops: ['cron.next', 'cron.parse'],
  run: v => cronerRun(v, {}),
}
const cronerAnd: Engine = {
  name: 'croner[legacyMode=false]',
  version: croner.version,
  ops: ['cron.next', 'cron.parse'],
  run: v => cronerRun(v, { legacyMode: false }),
}

const cronstrueEngine: Engine = {
  name: 'cronstrue',
  version: '3.24.0 (git bradymholt/cRonstrue @b62884a 2026-08-21)',
  ops: ['cron.next', 'cron.parse'],
  run(v) {
    // cronstrue does not compute occurrences; it produces a description.
    // Included because it is a *parser*: its accept/reject decision is a
    // conformance signal for every INVALID vector, and its description is
    // the only observable evidence of how it resolved a dialect ambiguity.
    return ['DESCRIPTION:' + cronstrue.toString(v.input.expr, { throwExceptionOnParseError: true })]
  },
}

const rruleJs: Engine = {
  name: 'rrule.js',
  version: '2.8.0 (git jkbrzt/rrule @9f2061f 2023-11-10)',
  ops: ['rrule.expand', 'rrule.parse', 'rrule.between'],
  run(v) {
    const i = v.input
    const p = parseIcs(i.ics)
    const set: any = rrulestr(i.ics, { forceset: true })
    if (v.op === 'rrule.between') {
      const [a, b] = i.between
      const toD = (s: string) => i.zone
        ? DateTime.fromISO(s, { zone: i.zone }).toJSDate()
        : new Date(s + 'Z')
      const got = set.between(toD(a), toD(b), false)
      return got.map((d: Date) => i.zone ? fmtZoned(d, i.zone) : fmtLocalNaive(d))
    }
    const all: Date[] = []
    set.all((d: Date, len: number) => { all.push(d); return len < i.count })
    return all.slice(0, i.count).map((d: Date) =>
      i.zone ? fmtZoned(d, i.zone) : fmtLocalNaive(d))
  },
}

const ENGINES = [cronParser, cronParserStrict, croner, cronerAnd, cronstrueEngine, rruleJs]

// ---------------------------------------------------------------- driver
const vectors = loadVectors(opt('vectors'))
const only = opt('engine')
const lines: string[] = []
for (const v of vectors) {
  for (const e of ENGINES) {
    if (only && e.name !== only) continue
    const probe = v.op === 'cron.parse' ? 'cron.next'
      : v.op === 'rrule.parse' ? 'rrule.expand' : v.op
    let rec: any
    if (!e.ops.includes(v.op) && !e.ops.includes(probe)) {
      rec = { status: 'unsupported_op', occurrences: [], error: `engine does not implement ${v.op}` }
    } else {
      const t0 = Date.now()
      try {
        const occ = e.run(v)
        rec = { status: occ.length === 0 ? 'empty' : 'ok', occurrences: occ, error: null }
      } catch (ex: any) {
        rec = {
          status: 'error', occurrences: [],
          error: `${ex?.constructor?.name ?? 'Error'}: ${String(ex?.message ?? ex)}`.slice(0, 500),
        }
      }
      rec.elapsed_ms = Date.now() - t0
    }
    Object.assign(rec, {
      vector_id: v.id, corpus_version: v.corpus_version, runner: 'run_js.ts',
      engine: e.name, engine_version: e.version, language: RUNTIME,
      tzdb: TZDB, tzdb_source: 'runtime ICU (fingerprint ' + tzdbFingerprint() + ')',
    })
    lines.push(JSON.stringify(rec))
  }
}
const outPath = opt('out')
if (outPath) writeFileSync(outPath, lines.join('\n') + '\n')
else console.log(lines.join('\n'))
