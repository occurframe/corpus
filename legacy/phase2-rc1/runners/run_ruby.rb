# Occurframe conformance-oracle runner: Ruby engines.
#
# RUNNER CONTRACT: JSONL vectors in (--vectors dir|file, else stdin),
# JSONL results out (--out file, else stdout). Exit 0 = ran; 1 = fatal
# harness error; 2 = usage error. Per-vector failures are RESULTS.
#
# Engines vendored from git (RubyGems unreachable):
#   floraison/fugit    @efda655 2026-07-21  (cron; the engine under rufus-scheduler)
#   seejohnrun/ice_cube@32ff145 2026-01-20  (RRULE)
#   floraison/et-orbi  @4725bc9 · floraison/raabro @af88c01 · tzinfo @ca5752c
#
# tzdb provenance: tzinfo's ZoneinfoDataSource reads the host
# /usr/share/zoneinfo, so the release is taken from tzdata.zi.
require "json"
Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8
Thread.report_on_exception = false

ROOT = File.expand_path("..", __dir__)
$LOAD_PATH.unshift(*%W[
  #{ROOT}/engines/tzinfo/lib
  #{ROOT}/engines/concurrent-ruby/lib/concurrent-ruby
  #{ROOT}/engines/raabro/lib
  #{ROOT}/engines/et-orbi/lib
  #{ROOT}/engines/fugit/lib
  #{ROOT}/engines/ice_cube/lib
])
require "tzinfo"
require "fugit"
require "ice_cube"

def opt(name)
  i = ARGV.index("--#{name}")
  i ? ARGV[i + 1] : nil
end

def tzdb_version
  %w[/usr/share/zoneinfo/tzdata.zi /usr/lib/zoneinfo/tzdata.zi].each do |p|
    next unless File.readable?(p)
    return [File.open(p, &:readline).strip.sub("# version ", ""), File.dirname(p)]
  end
  ["unknown", "unknown"]
end

def off_str(t)
  o = t.utc_offset
  s = o >= 0 ? "+" : "-"
  o = o.abs
  format("%s%02d:%02d", s, o / 3600, (o % 3600) / 60)
end

def fmt_zoned(t)
  t.strftime("%Y-%m-%dT%H:%M:%S") + off_str(t) + "|" +
    t.getutc.strftime("%Y-%m-%dT%H:%M:%SZ")
end

def fmt_naive(t) = t.strftime("%Y-%m-%dT%H:%M:%S")

# ---------------------------------------------------------------- fugit
def fmt_eo_zoned(t)
  o = t.utc_offset
  s = o >= 0 ? "+" : "-"
  o = o.abs
  off = format("%s%02d:%02d", s, o / 3600, (o % 3600) / 60)
  t.strftime("%Y-%m-%dT%H:%M:%S") + off + "|" +
    t.utc.strftime("%Y-%m-%dT%H:%M:%SZ")
end

def run_fugit(v)
  i = v["input"]
  zone = i["zone"]
  expr = zone ? "#{i['expr']} #{zone}" : i["expr"]
  c = Fugit.parse_cron(expr)
  raise ArgumentError, "fugit: parse returned nil for #{expr.inspect}" if c.nil?

  tz = EtOrbi.get_tzone(zone || "UTC")
  raise ArgumentError, "fugit/et-orbi: unknown zone #{zone.inspect}" if tz.nil?

  t = EtOrbi.parse(i["start"].sub("T", " "), zone: tz)
  out = []
  i["count"].times do
    t = c.next_time(t)
    break if t.nil?
    out << (zone ? fmt_eo_zoned(t) : t.strftime("%Y-%m-%dT%H:%M:%S"))
  end
  out
end

# ---------------------------------------------------------------- ice_cube
def run_ice_cube(v)
  i = v["input"]
  zone = i["zone"]
  sched = IceCube::Schedule.from_ical(i["ics"])
  out = []
  sched.first(i["count"]).each do |t|
    out << (zone ? fmt_zoned(t) : fmt_naive(t))
  end
  out
end

# ---------------------------------------------------------------- driver
vectors_path = opt("vectors")
out_path = opt("out")
lines =
  if vectors_path.nil?
    $stdin.read.split("\n")
  elsif File.directory?(vectors_path)
    Dir[File.join(vectors_path, "*.jsonl")].sort
      .flat_map { |f| File.readlines(f, encoding: "UTF-8") }
  elsif File.file?(vectors_path)
    File.readlines(vectors_path, encoding: "UTF-8")
  else
    warn "fatal: no such vectors path"
    exit 1
  end

tzdb, tzsrc = tzdb_version
ENGINES = [
  { name: "fugit", version: "git floraison/fugit @efda655 2026-07-21",
    ops: %w[cron.next cron.parse], fn: method(:run_fugit) },
  { name: "ice_cube", version: "git seejohnrun/ice_cube @32ff145 2026-01-20",
    ops: %w[rrule.expand rrule.parse], fn: method(:run_ice_cube) },
]

fh = out_path ? File.open(out_path, "w") : $stdout
lines.each do |line|
  next if line.strip.empty?
  v = JSON.parse(line)
  probe = case v["op"]
          when "cron.parse" then "cron.next"
          when "rrule.parse" then "rrule.expand"
          else v["op"]
          end
  ENGINES.each do |e|
    rec = { "vector_id" => v["id"], "corpus_version" => v["corpus_version"],
            "runner" => "run_ruby.rb", "engine" => e[:name],
            "engine_version" => e[:version],
            "language" => "ruby #{RUBY_VERSION}",
            "tzdb" => tzdb, "tzdb_source" => tzsrc }
    if !e[:ops].include?(v["op"]) && !e[:ops].include?(probe)
      rec.merge!("status" => "unsupported_op", "occurrences" => [],
                 "error" => "engine does not implement #{v['op']}",
                 "elapsed_ms" => 0)
    else
      t0 = Time.now
      begin
        occ = nil
        # bound each call: a hang is a conformance RESULT, not a crash
        th = Thread.new { occ = e[:fn].call(v) }
        if th.join(8).nil?
          th.kill
          rec.merge!("status" => "timeout", "occurrences" => [],
                     "error" => "exceeded 8s")
        else
          rec.merge!("status" => (occ.nil? || occ.empty? ? "empty" : "ok"),
                     "occurrences" => occ || [], "error" => nil)
        end
      rescue Exception => ex
        rec.merge!("status" => "error", "occurrences" => [],
                   "error" => "#{ex.class}: #{ex.message}"[0, 500])
      end
      rec["elapsed_ms"] = ((Time.now - t0) * 1000).round(2)
    end
    fh.puts(JSON.generate(rec))
  end
end
fh.close if out_path
exit 0
