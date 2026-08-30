// Occurframe conformance-oracle runner: Go engines.
//
// RUNNER CONTRACT: JSONL vectors in (--vectors dir|file, else stdin),
// JSONL results out (--out file, else stdout). Exit 0 = ran; 1 = fatal
// harness error; 2 = usage error. Per-vector failures are RESULTS.
//
// Engines vendored from git (proxy.golang.org unreachable):
//
//	github.com/robfig/cron/v3       @bc59245 (tag v3.0.1, 2021-01-06)
//	github.com/teambition/rrule-go  @e74d163 (2023-04-01)
//
// Both have zero external dependencies. tzdb provenance: Go resolves zones
// through the host /usr/share/zoneinfo unless the `timetzdata` build tag is
// set, so the runner reports the host tzdata release.
package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"runtime/debug"
	"sort"
	"strings"
	"time"

	cronv3 "github.com/robfig/cron/v3"
	rrule "github.com/teambition/rrule-go"
)

type Vector struct {
	ID            string `json:"id"`
	CorpusVersion string `json:"corpus_version"`
	Op            string `json:"op"`
	Input         struct {
		Kind      string   `json:"kind"`
		Expr      string   `json:"expr"`
		Start     string   `json:"start"`
		Count     int      `json:"count"`
		Zone      *string  `json:"zone"`
		Fields    int      `json:"fields"`
		Inclusive bool     `json:"inclusive"`
		ICS       string   `json:"ics"`
		Between   []string `json:"between"`
	} `json:"input"`
}

type Result struct {
	VectorID      string   `json:"vector_id"`
	CorpusVersion string   `json:"corpus_version"`
	Runner        string   `json:"runner"`
	Engine        string   `json:"engine"`
	EngineVersion string   `json:"engine_version"`
	Language      string   `json:"language"`
	Tzdb          string   `json:"tzdb"`
	TzdbSource    string   `json:"tzdb_source"`
	Status        string   `json:"status"`
	Occurrences   []string `json:"occurrences"`
	Error         *string  `json:"error"`
	ElapsedMs     float64  `json:"elapsed_ms"`
}

func offStr(t time.Time) string {
	_, off := t.Zone()
	s := "+"
	if off < 0 {
		s = "-"
		off = -off
	}
	return fmt.Sprintf("%s%02d:%02d", s, off/3600, (off%3600)/60)
}

func fmtZoned(t time.Time) string {
	return t.Format("2006-01-02T15:04:05") + offStr(t) + "|" +
		t.UTC().Format("2006-01-02T15:04:05") + "Z"
}

func fmtNaive(t time.Time) string { return t.Format("2006-01-02T15:04:05") }

func hostTzdb() (string, string) {
	for _, p := range []string{"/usr/share/zoneinfo/tzdata.zi", "/usr/lib/zoneinfo/tzdata.zi"} {
		b, err := os.ReadFile(p)
		if err == nil {
			line := strings.SplitN(string(b), "\n", 2)[0]
			return strings.TrimPrefix(strings.TrimSpace(line), "# version "), filepath.Dir(p)
		}
	}
	return "unknown", "unknown"
}

func startTime(v Vector) (time.Time, error) {
	loc := time.UTC
	if v.Input.Zone != nil {
		l, err := time.LoadLocation(*v.Input.Zone)
		if err != nil {
			return time.Time{}, err
		}
		loc = l
	}
	return time.ParseInLocation("2006-01-02T15:04:05", v.Input.Start, loc)
}

// ------------------------------------------------------------- robfig/cron
func runRobfig(v Vector, withSeconds bool) (out []string, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("panic: %v", r)
		}
	}()
	expr := v.Input.Expr
	if v.Input.Zone != nil {
		expr = "TZ=" + *v.Input.Zone + " " + expr
	}
	var sched cronv3.Schedule
	if withSeconds {
		p := cronv3.NewParser(cronv3.Second | cronv3.Minute | cronv3.Hour |
			cronv3.Dom | cronv3.Month | cronv3.Dow | cronv3.Descriptor)
		sched, err = p.Parse(expr)
	} else {
		sched, err = cronv3.ParseStandard(expr)
	}
	if err != nil {
		return nil, err
	}
	t, err := startTime(v)
	if err != nil {
		return nil, err
	}
	deadline := t.AddDate(60, 0, 0)
	for i := 0; i < v.Input.Count; i++ {
		nt := sched.Next(t)
		if nt.IsZero() || nt.After(deadline) {
			break
		}
		if v.Input.Zone != nil {
			out = append(out, fmtZoned(nt))
		} else {
			out = append(out, fmtNaive(nt))
		}
		t = nt
	}
	return out, nil
}

// ------------------------------------------------------------- rrule-go
func runRRuleGo(v Vector) (out []string, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("panic: %v", r)
		}
	}()
	set, err := rrule.StrToRRuleSet(v.Input.ICS)
	if err != nil {
		return nil, err
	}
	zoned := v.Input.Zone != nil
	if v.Op == "rrule.between" {
		loc := time.UTC
		if zoned {
			loc, _ = time.LoadLocation(*v.Input.Zone)
		}
		a, _ := time.ParseInLocation("2006-01-02T15:04:05", v.Input.Between[0], loc)
		b, _ := time.ParseInLocation("2006-01-02T15:04:05", v.Input.Between[1], loc)
		for _, t := range set.Between(a, b, false) {
			if zoned {
				out = append(out, fmtZoned(t.In(loc)))
			} else {
				out = append(out, fmtNaive(t))
			}
		}
		return out, nil
	}
	next := set.Iterator()
	var loc *time.Location
	if zoned {
		loc, _ = time.LoadLocation(*v.Input.Zone)
	}
	for i := 0; i < v.Input.Count; i++ {
		t, ok := next()
		if !ok {
			break
		}
		if zoned {
			out = append(out, fmtZoned(t.In(loc)))
		} else {
			out = append(out, fmtNaive(t))
		}
	}
	return out, nil
}

type callResult struct {
	occ []string
	err error
}

// callWithTimeout bounds a single engine call. Go cannot kill a goroutine, so
// a hung engine leaks one; that is deliberate — "hangs" is a conformance
// result the corpus must be able to record rather than a reason to abort.
func callWithTimeout(fn func(Vector) ([]string, error), v Vector,
	d time.Duration) ([]string, error) {
	ch := make(chan callResult, 1)
	go func() {
		defer func() {
			if r := recover(); r != nil {
				ch <- callResult{nil, fmt.Errorf("panic: %v", r)}
			}
		}()
		o, e := fn(v)
		ch <- callResult{o, e}
	}()
	select {
	case r := <-ch:
		return r.occ, r.err
	case <-time.After(d):
		return nil, fmt.Errorf("__TIMEOUT__ exceeded %s", d)
	}
}

func main() {
	var vectorsPath, outPath string
	args := os.Args[1:]
	for i := 0; i < len(args); i++ {
		switch args[i] {
		case "--vectors":
			i++
			vectorsPath = args[i]
		case "--out":
			i++
			outPath = args[i]
		default:
			fmt.Fprintln(os.Stderr, "usage: runner [--vectors DIR|FILE] [--out FILE]")
			os.Exit(2)
		}
	}
	var lines []string
	if vectorsPath == "" {
		sc := bufio.NewScanner(os.Stdin)
		sc.Buffer(make([]byte, 1<<22), 1<<22)
		for sc.Scan() {
			if strings.TrimSpace(sc.Text()) != "" {
				lines = append(lines, sc.Text())
			}
		}
	} else {
		var files []string
		st, err := os.Stat(vectorsPath)
		if err != nil {
			fmt.Fprintln(os.Stderr, "fatal:", err)
			os.Exit(1)
		}
		if st.IsDir() {
			ents, _ := os.ReadDir(vectorsPath)
			for _, e := range ents {
				if strings.HasSuffix(e.Name(), ".jsonl") {
					files = append(files, filepath.Join(vectorsPath, e.Name()))
				}
			}
			sort.Strings(files)
		} else {
			files = []string{vectorsPath}
		}
		for _, f := range files {
			b, err := os.ReadFile(f)
			if err != nil {
				fmt.Fprintln(os.Stderr, "fatal:", err)
				os.Exit(1)
			}
			for _, l := range strings.Split(string(b), "\n") {
				if strings.TrimSpace(l) != "" {
					lines = append(lines, l)
				}
			}
		}
	}

	tzdb, tzsrc := hostTzdb()
	goVer := "unknown"
	if bi, ok := debug.ReadBuildInfo(); ok {
		goVer = bi.GoVersion
	}

	w := os.Stdout
	if outPath != "" {
		f, err := os.Create(outPath)
		if err != nil {
			fmt.Fprintln(os.Stderr, "fatal:", err)
			os.Exit(1)
		}
		defer f.Close()
		w = f
	}
	bw := bufio.NewWriter(w)
	defer bw.Flush()

	type eng struct {
		name, version string
		ops           []string
		fn            func(Vector) ([]string, error)
	}
	engines := []eng{
		{"robfig-cron", "v3.0.1 (git robfig/cron @bc59245 2021-01-06)",
			[]string{"cron.next", "cron.parse"},
			func(v Vector) ([]string, error) { return runRobfig(v, false) }},
		{"robfig-cron[seconds]", "v3.0.1 (git robfig/cron @bc59245 2021-01-06)",
			[]string{"cron.next", "cron.parse"},
			func(v Vector) ([]string, error) { return runRobfig(v, true) }},
		{"rrule-go", "v1.8.x (git teambition/rrule-go @e74d163 2023-04-01)",
			[]string{"rrule.expand", "rrule.parse", "rrule.between"}, runRRuleGo},
	}

	for _, l := range lines {
		var v Vector
		if err := json.Unmarshal([]byte(l), &v); err != nil {
			continue
		}
		probe := v.Op
		if v.Op == "cron.parse" {
			probe = "cron.next"
		}
		if v.Op == "rrule.parse" {
			probe = "rrule.expand"
		}
		for _, e := range engines {
			supported := false
			for _, o := range e.ops {
				if o == v.Op || o == probe {
					supported = true
				}
			}
			r := Result{VectorID: v.ID, CorpusVersion: v.CorpusVersion,
				Runner: "runners/go", Engine: e.name, EngineVersion: e.version,
				Language: goVer, Tzdb: tzdb, TzdbSource: tzsrc,
				Occurrences: []string{}}
			if !supported {
				msg := "engine does not implement " + v.Op
				r.Status = "unsupported_op"
				r.Error = &msg
			} else {
				t0 := time.Now()
				occ, err := callWithTimeout(e.fn, v, 8*time.Second)
				r.ElapsedMs = float64(time.Since(t0).Microseconds()) / 1000.0
				if err != nil {
					msg := err.Error()
					if len(msg) > 500 {
						msg = msg[:500]
					}
					r.Status = "error"
					if strings.HasPrefix(msg, "__TIMEOUT__") {
						r.Status = "timeout"
					}
					r.Error = &msg
				} else if len(occ) == 0 {
					r.Status = "empty"
				} else {
					r.Status = "ok"
					r.Occurrences = occ
				}
			}
			b, _ := json.Marshal(r)
			bw.Write(b)
			bw.WriteByte('\n')
		}
	}
}
