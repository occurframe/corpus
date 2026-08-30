# Phase II RC1 Historical Evidence

This directory preserves the Research II oracle at `1.0.0-rc1`: vectors, runner implementations, raw observations, matrix/reference material, provenance, and enough build/tooling source to audit the research. Transient compiled binaries are excluded.

RC1 is historical evidence, **not current authority**. Canonical RC2 authority lives in the authored `spec/`, `schemas/`, `registry/`, and `vectors/` trees.

Incumbent observations and matrices must never define future expectations. They are measurements, not doctrine, and must not be copied into canonical vectors.

RC1's overloaded `error` semantics are retained only for reproducibility. An RC1 `error` may mean deliberate rejection or an unexpected exception; it must never be guessed into protocol-v2 `rejection` or `engine_error`. The RC2 migration report lists every ambiguous legacy cell explicitly.

The original RC1 oracle overview is preserved as `ORACLE-README-RC1.md`.

