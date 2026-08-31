# Runner Protocol v3

Protocol version **`3.0`** uses one JSON object per line over stdin/stdout. Standard output contains protocol messages only; diagnostics belong on standard error. Protocol 2.0 remains at `schemas/runner-protocol-v2.schema.json` solely as a historical contract; current tooling does not accept it.

The flow for each runner process is:

```text
runner -> hello
authority -> case
runner -> started
runner -> result
```

`hello` identifies the protocol, runner, engine version and provenance, runtime/language, capabilities, permanent versioned dialect IDs, semantic profile claims, and structured tzdb provenance.

`case` contains a unique request ID, opaque vector ID and family labels, operation, engine input, semantic context, and `budget_ms`. It is a separately typed projection, not a canonical vector. Semantic context is limited to dialect, civil-time policy, capability, and tzdb requirements needed to execute the question. It never carries expectations, classification, rationale, normative evidence, tags, scoring mode, semantic-axis inventory, or admissible answer sets. The authority retains the canonical vector and joins the observation back to it for scoring. The official certification budget remains 8,000 ms.

`started` must be emitted immediately before entering the native engine operation. Startup/import/protocol time is not engine execution time. The authority starts the engine timeout only after this acknowledgement.

`result` has exactly one engine outcome:

- `occurrences`, including a legitimate `[]`;
- `accepted` for a successful validation-only operation;
- `rejection` for a deliberate parse or validation rejection;
- `unsupported` when the engine cannot express the operation or input;
- `engine_error` for an unexpected engine exception or error.

Warnings are orthogonal diagnostics and may accompany successful results. An `engine_error` never satisfies an expected rejection.

Malformed protocol, startup failure, premature exit, missing acknowledgement, request-ID mismatch, or another adapter/harness fault is `runner_failure`, not an engine result. If no result arrives within `budget_ms` after `started`, the authority terminates the runner, records only the observed `timeout`, and restarts the runner before the next case. It does not claim mathematical non-termination.

Runners report observations; they never receive expectations and never score themselves.
