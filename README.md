# Skills

A curated library of **14 engineering-discipline agent skills** in the
[Agent Skills](https://agentskills.io) open format — compatible with
**GitHub Copilot in VS Code**, Copilot CLI, Copilot coding agent,
**Claude Code**, and any other skills-compatible agent.

Each skill encodes one habit of a careful senior engineer — prove the bug
before fixing it, sweep edge cases before declaring done, look before you
delete — as a focused instruction file the agent loads only when relevant.

Derived from [adamentwistle/fable-skills](https://github.com/adamentwistle/fable-skills)
(MIT) with the changes listed under [What was improved](#what-was-improved).

## Operating manual

[operating-manual.md](operating-manual.md) is the reasoning philosophy behind
these skills — nine principles for working carefully (read what's actually
being asked, verify by re-deriving, find where the risk lives, route around
your own limits) plus a five-question self-test. Where each skill is a
situational checklist, the manual is the mindset they all share; read it once,
then let the skills fire it at the right moment.

### What's inside

- **Nine principles**, each written as *procedure → worked example → the
  failure it prevents*: (1) read what's actually being asked, (2) break the
  problem into independently checkable pieces, (3) find where the risk actually
  lives, (4) verify by re-deriving rather than recognizing, (5) separate known
  from guessed and label it, (6) attack your own conclusion before shipping it,
  (7) communicate answer → reasoning → risk, (8) the mistakes that look like
  competence, (9) what to do when the problem exceeds your reach.
- **A five-question self-test** to run on any answer before sending it.

### How it differs from a skill

The skills in this repo are *situational* — an agent auto-loads one only when a
task matches its description (progressive disclosure). The operating manual is
the opposite: a single *always-on* mindset. That means it isn't installed as a
`SKILL.md`; you either read it yourself or wire it into an agent's standing
instructions so it applies to **every** task, as described next.

### Using it as a human

Read it once end-to-end, then keep the five-question self-test somewhere handy
(a pinned note, an editor snippet) and run it before you hit send on anything
consequential. The worked examples are the fastest way in.

### Wiring it into an agent

**Per project (shared with your team):** reference it from the standing
instructions file your agent already reads, so it applies to every task in the
repo. Copy the manual to your repo root and add a pointer:

```bash
cp operating-manual.md ./operating-manual.md
# then, in .github/copilot-instructions.md (Copilot) or AGENTS.md / CLAUDE.md:
echo "Follow the reasoning discipline in [operating-manual.md](operating-manual.md) on every task." >> .github/copilot-instructions.md
```

VS Code Copilot reads `.github/copilot-instructions.md` automatically; Claude
Code and other agents read `AGENTS.md` / `CLAUDE.md`. Any of them will pull in
the linked manual as context.

**Personal (all your projects):** paste the manual — or just the nine
principle headers and the self-test — into your agent's personal/global
instructions (in VS Code: *Copilot → Personal instructions*). Because it loads
on every conversation, prefer a condensed version if your agent caps how much
standing instruction it keeps in context.

> Note: standing instructions *bias* an agent strongly but aren't a hard
> guarantee every principle fires every time; they shape behavior, they don't
> enforce it.

## Installation

**Per project (recommended — shared with your team via source control):**
copy the skill folders you want into `.github/skills/` at your repo root:

```bash
mkdir -p .github/skills
cp -r skills/root-cause-debugging skills/security-review .github/skills/
```

VS Code also discovers project skills in `.claude/skills/` and
`.agents/skills/`, so the same folders work for Claude Code unchanged.

**Personal (all projects):** copy into `~/.copilot/skills/`,
`~/.claude/skills/`, or `~/.agents/skills/`.

**Via GitHub CLI (public preview):**

```bash
gh skill install jvenuto80/Skills --skill root-cause-debugging
```

Verify discovery in VS Code by typing `/skills` in Copilot Chat; a skill can
also be invoked directly, e.g. `/root-cause-debugging`.

## Catalog

| Skill | Fires when… |
|---|---|
| [codebase-orientation](skills/codebase-orientation/SKILL.md) | starting in an unfamiliar repo or module |
| [root-cause-debugging](skills/root-cause-debugging/SKILL.md) | any bug, regression, or flaky failure — includes an anti-thrashing circuit breaker |
| [edge-case-sweep](skills/edge-case-sweep/SKILL.md) | after the happy path works, before "done" |
| [test-design](skills/test-design/SKILL.md) | writing tests or judging existing ones |
| [security-review](skills/security-review/SKILL.md) | diffs touching input, auth, secrets, SQL, HTML, URLs, subprocesses |
| [untrusted-content-guard](skills/untrusted-content-guard/SKILL.md) | processing fetched/external content (prompt-injection defense) |
| [perf-sanity](skills/perf-sanity/SKILL.md) | loops over unbounded data, queries in loops, hot paths |
| [concurrency-reasoning](skills/concurrency-reasoning/SKILL.md) | async fan-out, streams, jobs, caches, races |
| [data-loss-guard](skills/data-loss-guard/SKILL.md) | any destructive command (rm, reset --hard, DELETE, force-push) |
| [data-migration-safety](skills/data-migration-safety/SKILL.md) | schema changes, backfills, wire-format changes |
| [git-hygiene](skills/git-hygiene/SKILL.md) | committing, branching, staging |
| [escalate-vs-decide](skills/escalate-vs-decide/SKILL.md) | uncertain mid-task: ask or proceed? |
| [verify-and-report](skills/verify-and-report/SKILL.md) | before declaring done or writing the final summary |
| [llm-app-code](skills/llm-app-code/SKILL.md) | agent loops, tool definitions, prompt/model changes |

## What was improved

Relative to the upstream fable-skills library:

1. **Agent Skills spec compliance.** Frontmatter now carries `license` and
   `metadata` alongside the required `name`/`description`; names and
   descriptions respect the spec's 64/1024-character limits; layout follows
   the `.github/skills/<name>/SKILL.md` convention documented for VS Code,
   Visual Studio, and Copilot.
2. **Descriptions rewritten as discovery surfaces.** Copilot activates a
   skill by reading its description, so each one now front-loads concrete
   trigger keywords ("race condition, TOCTOU, flaky…") instead of prose.
3. **Zero dangling cross-references.** Upstream contained ~a dozen
   `see <skill>` references to skills that don't exist in the repo. Every
   cross-reference here resolves, and CI enforces it.
4. **Consolidated 35 → 14.** The always-on `workmanship` skill (which would
   fire on every task, defeating progressive disclosure) became the
   completion-triggered `verify-and-report`; `stop-thrashing` was folded
   into `root-cause-debugging` where it's actually needed;
   Claude-Code-specific skills (subagent fan-out, context checkpointing)
   were dropped for portability; narrower situational skills were cut in
   favor of a set where every skill earns its context window.
5. **Tool-agnostic wording.** References to `AGENTS.md` /
   `.github/copilot-instructions.md` / `CLAUDE.md` rather than any single
   agent's conventions.
6. **CI validation.** `scripts/validate.py` checks frontmatter, name/dir
   agreement, spec limits, and cross-reference integrity on every push and
   PR.

## A note on expectations

Skills like these reliably help on tasks shaped like their checklists
(seeded-bug review, process-heavy debugging). Treat any benchmark claims —
upstream's included — as directional. The honest pitch is narrower and
still worthwhile: explicit discipline, applied at the right moment, catches
the failure modes agents most often skip.

## License

MIT — see [LICENSE](LICENSE). Derived from
[fable-skills](https://github.com/adamentwistle/fable-skills) by
Adam Entwistle (MIT).
