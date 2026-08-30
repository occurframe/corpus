# Contributing Vectors

Add one JSON file under the matching `vectors/<family>/` directory and register its permanent ID. Preserve the distinction between predicate-shaped cron semantics and anchor/generator-shaped RRULE semantics; do not introduce a unified recurrence AST.

A vector must state why it matters, cite normative or ambiguity evidence, name every semantic axis it uses, and choose an expectation mode independently from classification. Do not copy an incumbent result into an expectation. Engine observations belong outside canonical vectors.

Before review:

1. Validate all Draft 2020-12 schemas.
2. Resolve every source, axis, dialect, stable ID, and supersession reference.
3. Verify occurrence order and intentional duplicates by inspection.
4. Run the independent Python reference tests when the reference matcher informed a cron expectation.
5. Run RC1-to-RC2 migration verification for this release line.
6. Build twice and verify byte-identical JSONL and SHA-256 manifests.

Fast pull-request CI proves authority consistency. Full differential certification is a separate workflow and does not run every external engine in ordinary PR CI.

