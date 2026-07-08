---
name: edge-case-sweep
description: >-
  Enumerate edge cases against a concrete checklist before declaring code
  complete: empty/null/boundary/huge inputs, unicode and weird text,
  idempotency, concurrency, stale state, timezones, and failing
  dependencies. Use when implementing or reviewing any function, handler,
  parser, validator, or data transformation — after the happy path works
  and before reporting done. Keywords: edge cases, boundary conditions,
  input validation, null, empty, corner cases, robustness.
license: MIT
metadata:
  author: jvenuto80
  version: "1.0"
  derived-from: adamentwistle/fable-skills (MIT)
---

# Edge-Case Sweep

The happy path is the easy 80%. Sweep this list against every new or changed
code path and either handle, explicitly reject, or consciously note each
relevant case.

## Inputs

- empty: `""`, `[]`, `{}`, zero rows, zero-byte file
- absent: null / undefined / missing key / missing flag — distinct from empty
- boundaries: 0, -1, exactly-at-limit, limit+1, first and last element
- huge: 10^6 items, multi-GB file, pathologically long string
- weird text: unicode, emoji, RTL, newlines-in-fields, quotes,
  leading/trailing whitespace, case variants
- duplicates and unsorted order where uniqueness/order is assumed

## State & time

- called twice (idempotency), called concurrently, retried after partial
  success (see concurrency-reasoning)
- stale state: file changed since read, record deleted between fetch and
  update
- timezone, DST, end-of-month/year, clock skew

## Environment

- dependency down / slow / returning errors: what does the caller see?
- permissions denied, disk full, network cut mid-operation

## The decision rule

For each case that applies: decide **handle** vs **reject loudly**. The
unacceptable outcome is silent wrong behavior. If a case is deliberately
unhandled, say so in the completion report — a stated limitation is fine, a
hidden one is a bug report waiting (see verify-and-report).
