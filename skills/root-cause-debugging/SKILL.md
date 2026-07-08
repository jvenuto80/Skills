---
name: root-cause-debugging
description: >-
  Systematic debugging discipline: reproduce first, locate by bisection,
  prove the cause with a falsifiable hypothesis, fix minimally, re-verify
  against the original reproduction — plus an anti-thrashing circuit breaker
  when consecutive fixes fail. Use for any bug, error, test failure,
  regression, crash, or flaky/intermittent behavior, before proposing a fix,
  and whenever a first fix didn't work. Keywords: debug, bug, root cause,
  regression, test failure, flaky, intermittent, doesn't work, still broken.
license: MIT
metadata:
  author: jvenuto80
  version: "1.0"
  derived-from: adamentwistle/fable-skills (MIT)
---

# Root-Cause Debugging

Weak debugging looks like: read the error → pattern-match to a familiar
cause → apply a plausible fix → declare victory. Strong debugging proves the
cause before touching the fix. Follow this sequence and do not skip stages.

## Stage 1 — Reproduce before anything else

Get the failure happening on demand, in the smallest command you can run
repeatedly (a single test, a curl, a one-liner). If you cannot reproduce it,
your job is to instrument until you can — not to fix blind.

Write down the exact reproduction command and the exact observed-vs-expected
output. This is the acceptance test for your fix.

## Stage 2 — Locate by bisection, not intuition

Find where reality diverges from expectation by cutting the search space in
half repeatedly:

- Trace the data: pick one concrete value that ends up wrong and follow it
  backward from the symptom to where it was last correct.
- Log/inspect at the midpoint of the suspected path; then midpoint again.
- Use git: `git log --oneline -- <file>`, `git bisect`, or diff against the
  last-known-good commit when it's a regression.
- Distrust the error site. The line that throws is where the bad state was
  *noticed*, rarely where it was *created*.

## Stage 3 — State the cause as a falsifiable sentence

Before fixing, complete this sentence with specifics: "The failure happens
because **[specific code]** does **[specific wrong thing]** when
**[specific condition]**."

Then try to falsify it: if this were true, what ELSE would be broken? Check
that. If the hypothesis predicts things that aren't happening, it's wrong —
go back to stage 2. A hypothesis you haven't tried to break is a guess.

## Stage 4 — Fix the cause, minimally

- Fix where the bad state is created, not where it's detected.
- Prefer the smallest diff that makes the falsifiable sentence false.
- If the real fix is large and you must ship a symptom-level guard, say so
  explicitly in your report — never present a mitigation as a root-cause fix.

## Stage 5 — Verify with the original reproduction

Run the exact stage-1 reproduction. Then run the surrounding test suite to
check for collateral damage. A fix verified only by "the code looks right
now" is not verified (see verify-and-report).

## The thrashing circuit breaker

Thrashing is trying variations faster instead of understanding harder.
Two failed fixes for the same failure is the alarm:

1. **The third attempt may proceed only if it's derived from new evidence** —
   a log you hadn't read, a value you hadn't inspected — never from "maybe
   it's this instead." No new fact, no new attempt; go get the fact first.
2. **On the alarm, stop editing and zoom out.** Re-read the original error
   top to bottom, re-read the failing code fresh, re-state the problem in
   one sentence. Ask the frame-breakers: am I editing the file that's
   actually being run? Is my mental model verified or assumed? Is the bug
   even where I've been looking?
3. **Revert the debris before attempt N+1.** Failed fixes stack; by attempt
   four you're debugging your attempts instead of the bug. Return to the
   last known state and apply only what evidence supports.
4. **Change the method, not just the guess**: add instrumentation and look
   at runtime values; bisect the input or the commit history; write the
   minimal reproduction from scratch.
5. **Notice the sunk-cost pull.** "I've come this far with approach A" is
   not evidence for approach A. If genuine investigation has failed
   repeatedly, report the state honestly — what you tried, what each attempt
   showed, current best hypothesis — rather than burning the session on
   variation five.

## Flaky / intermittent failures

Don't average over the noise. Find the varying input: timing (race),
ordering (test pollution, map iteration), environment (env var, port,
clock), or data (random seed). Run the reproduction in a loop
(`for i in $(seq 20); do ...; done`) to measure the failure rate before and
after the fix — "passed once" is not evidence for a flake fix
(see concurrency-reasoning for race diagnosis).
