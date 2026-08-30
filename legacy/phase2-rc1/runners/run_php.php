<?php
/**
 * Occurframe conformance-oracle runner: PHP engines.
 *
 * RUNNER CONTRACT: JSONL vectors in (--vectors dir|file, else stdin),
 * JSONL results out (--out file, else stdout). Exit 0 = ran; 1 = fatal
 * harness error; 2 = usage error. Per-vector failures are RESULTS.
 *
 * Engines vendored from git (Packagist unreachable):
 *   dragonmantank/cron-expression @d425a24 2025-12-20  (v3.x line)
 *   rlanvin/php-rrule             @93a083d 2026-07-29  (v2.x line)
 * Both are dependency-free at runtime; a minimal PSR-4 autoloader is
 * registered below instead of Composer's.
 *
 * tzdb provenance: PHP reports timezone_version_get(); "0.system" means the
 * host /usr/share/zoneinfo is used, so the release is read from tzdata.zi.
 */
declare(strict_types=1);

$ENGINE_ROOT = dirname(__DIR__) . '/engines';
spl_autoload_register(function ($class) use ($ENGINE_ROOT) {
    $map = [
        'Cron\\'  => $ENGINE_ROOT . '/php-cron-expression/src/Cron/',
        'RRule\\' => $ENGINE_ROOT . '/php-rrule/src/',
    ];
    foreach ($map as $prefix => $dir) {
        if (strncmp($class, $prefix, strlen($prefix)) === 0) {
            $rel = str_replace('\\', '/', substr($class, strlen($prefix)));
            $f = $dir . $rel . '.php';
            if (file_exists($f)) { require $f; return; }
        }
    }
});

function opt(string $name): ?string {
    global $argv;
    $i = array_search('--' . $name, $argv, true);
    return $i === false ? null : ($argv[$i + 1] ?? null);
}

function tzdbVersion(): array {
    $v = timezone_version_get();
    if ($v !== '0.system') return [$v, 'PHP bundled'];
    foreach (['/usr/share/zoneinfo/tzdata.zi', '/usr/lib/zoneinfo/tzdata.zi'] as $p) {
        if (is_readable($p)) {
            $line = trim(fgets(fopen($p, 'r')));
            return [str_replace('# version ', '', $line), dirname($p)];
        }
    }
    return ['unknown', 'unknown'];
}

function offStr(DateTimeInterface $d): string {
    $o = (int)$d->getOffset();
    $s = $o >= 0 ? '+' : '-';
    $o = abs($o);
    return sprintf('%s%02d:%02d', $s, intdiv($o, 3600), intdiv($o % 3600, 60));
}
function fmtZoned(DateTimeInterface $d): string {
    $u = (clone $d)->setTimezone(new DateTimeZone('UTC'));
    return $d->format('Y-m-d\TH:i:s') . offStr($d) . '|' . $u->format('Y-m-d\TH:i:s') . 'Z';
}
function fmtNaive(DateTimeInterface $d): string { return $d->format('Y-m-d\TH:i:s'); }

/** cron: dragonmantank/cron-expression */
function runCronExpression(array $v): array {
    $i = $v['input'];
    $zone = $i['zone'];
    $tz = new DateTimeZone($zone ?? 'UTC');
    $expr = new Cron\CronExpression($i['expr']);
    $cur = new DateTime($i['start'], $tz);
    $out = [];
    for ($k = 0; $k < $i['count']; $k++) {
        $d = $expr->getNextRunDate($cur, 0, false, $zone ?? 'UTC');
        $out[] = $zone ? fmtZoned($d) : fmtNaive($d);
        $cur = $d;
    }
    return $out;
}

/** RRULE: rlanvin/php-rrule */
function runPhpRRule(array $v): array {
    $i = $v['input'];
    $zone = $i['zone'];
    $set = new RRule\RSet($i['ics']);
    $out = [];
    if ($v['op'] === 'rrule.between') {
        $tz = new DateTimeZone($zone ?? 'UTC');
        $a = new DateTime($i['between'][0], $tz);
        $b = new DateTime($i['between'][1], $tz);
        foreach ($set as $d) {
            if ($d <= $a) continue;
            if ($d >= $b) break;
            $out[] = $zone ? fmtZoned($d) : fmtNaive($d);
        }
        return $out;
    }
    $n = 0;
    foreach ($set as $d) {
        $out[] = $zone ? fmtZoned($d) : fmtNaive($d);
        if (++$n >= $i['count']) break;
    }
    return $out;
}

// ------------------------------------------------------------------ driver
$vectorsPath = opt('vectors');
$outPath = opt('out');
$lines = [];
if ($vectorsPath === null) {
    $lines = explode("\n", stream_get_contents(STDIN));
} elseif (is_dir($vectorsPath)) {
    $files = glob($vectorsPath . '/*.jsonl');
    sort($files);
    foreach ($files as $f) $lines = array_merge($lines, explode("\n", file_get_contents($f)));
} elseif (is_file($vectorsPath)) {
    $lines = explode("\n", file_get_contents($vectorsPath));
} else {
    fwrite(STDERR, "fatal: no such vectors path\n");
    exit(1);
}

[$tzdb, $tzsrc] = tzdbVersion();
$engines = [
    ['name' => 'php-cron-expression',
     'version' => 'dragonmantank/cron-expression @d425a24 2025-12-20',
     'ops' => ['cron.next', 'cron.parse'], 'fn' => 'runCronExpression'],
    ['name' => 'php-rrule',
     'version' => 'rlanvin/php-rrule @93a083d 2026-07-29',
     'ops' => ['rrule.expand', 'rrule.parse', 'rrule.between'], 'fn' => 'runPhpRRule'],
];

$fh = $outPath ? fopen($outPath, 'w') : STDOUT;
foreach ($lines as $line) {
    if (trim($line) === '') continue;
    $v = json_decode($line, true);
    $probe = $v['op'] === 'cron.parse' ? 'cron.next'
           : ($v['op'] === 'rrule.parse' ? 'rrule.expand' : $v['op']);
    foreach ($engines as $e) {
        $rec = ['vector_id' => $v['id'], 'corpus_version' => $v['corpus_version'],
                'runner' => 'run_php.php', 'engine' => $e['name'],
                'engine_version' => $e['version'],
                'language' => 'php ' . PHP_VERSION,
                'tzdb' => $tzdb, 'tzdb_source' => $tzsrc];
        if (!in_array($v['op'], $e['ops'], true) && !in_array($probe, $e['ops'], true)) {
            $rec += ['status' => 'unsupported_op', 'occurrences' => [],
                     'error' => 'engine does not implement ' . $v['op'], 'elapsed_ms' => 0];
        } else {
            $t0 = microtime(true);
            try {
                set_time_limit(10);
                $occ = ($e['fn'])($v);
                $rec += ['status' => count($occ) ? 'ok' : 'empty',
                         'occurrences' => $occ, 'error' => null];
            } catch (Throwable $ex) {
                $rec += ['status' => 'error', 'occurrences' => [],
                         'error' => substr(get_class($ex) . ': ' . $ex->getMessage(), 0, 500)];
            }
            $rec['elapsed_ms'] = round((microtime(true) - $t0) * 1000, 2);
        }
        fwrite($fh, json_encode($rec) . "\n");
    }
}
if ($outPath) fclose($fh);
exit(0);
