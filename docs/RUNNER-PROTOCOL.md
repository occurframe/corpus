# Runner Protocol v2

Protocol version **`2.0`** uses one JSON object per line over stdin/stdout. Standard output contains protocol messages only; diagnostics belong on standard error.

The flow for each runner process is:

```text
runner -> hello
authority -> case
runner -> started
runner -> result
```

`hello` identifies the protocol, runner, engine version and provenance, runtime/language, capabilities, permanent versioned dialect IDs, semantic profile claims, and structured tzdb provenance.

`case` contains a unique request ID, a schema- and semantically-validated vector, and `budget_ms`. The official certification budget is 8,000 ms until a later protocol or corpus version changes it.

`started` must be emitted immediately before entering the native engine operation. Startup/import/protocol time is not engine execution time. The authority starts the engine timeout only after this acknowledgement.

`result` has exactly one engine outcome:

- `occurrences`, including a legitimate `[]`;
- `accepted` for a successful validation-only operation;
- `rejection` for a deliberate parse or validation rejection;
- `unsupported` when the engine cannot express the operation or input;
- `engine_error` for an unexpected engine exception or error.

Warnings are orthogonal diagnostics and may accompany successful results. An `engine_error` never satisfies an expected rejection.

Malformed protocol, startup failure, premature exit, missing acknowledgement, request-ID mismatch, or another adapter/harness fault is `runner_failure`, not an engine result. If no result arrives within `budget_ms` after `started`, the authority terminates the runner, records only the observed `timeout`, and restarts the runner before the next case. It does not claim mathematical non-termination.

Runners report observations; they never score themselves.

