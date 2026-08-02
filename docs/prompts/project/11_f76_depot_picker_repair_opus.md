# Chain 11 — F76: the depot resource-picker repair (P1, its own dedicated sitting)

> ## ⛔ SEALED: `docs/reports/BLIND_AUDIT.md` — DO NOT OPEN
>
> **This prompt is FORBIDDEN from reading, grepping, summarising, or acting on
> `docs/reports/BLIND_AUDIT.md` or any part of its contents.**
>
> **Why (so this is not rationalised around):** it is a **blind control**. It was
> produced by a fresh session that deliberately read no project docs, and its
> entire evidential value is that it was written without the project's own
> conclusions in view. **Chain prompt 12, job 6b** examines it against the full
> record it was forbidden to see, doing its own pass first and only then opening
> the sealed key — so that neither reading anchors the other. **Any earlier
> prompt that reads it destroys the independence that comparison depends on, and
> the contamination is undetectable afterwards.**
>
> - Do not open it. Do not `grep`/`Read` it. Do not ask a subagent to.
> - **If a broad search incidentally surfaces its contents: stop, discard, do not
>   use it, and say so in your handoff notes.**
> - This is not a scope call you may weigh against a deadline or a judgment call
>   the blanket pre-clearance covers. **Only prompt 12, at job 6b, may open it.**

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.** ⚠ This is the ONE chain prompt that is an ATTENDED sitting:
the standing hard rule bans live UI-internals prototyping in play sessions
precisely because F76's picker interaction once HARD-LOCKED the UI (session
lost) — this dedicated sitting, on a throwaway fixture save, is the sanctioned
place for it.

**Staleness check: `git log --oneline -10` + `git pull`.** Authority: the
BUGS.md **F76 entry** — it carries the owner's verbatim symptom report, the
full live forensics (the picker opens ALIVE at a wrong position on the
4K/80%-scale ultrawide), and the verified `TransferResources` workaround.
**Audit context that raised this item's priority:** an original-game report
shows the same player-visible failure on ordinary setups
(`BUG_LIST_AUDIT.md` §2.2 F76 — "The icon which should appear when I click on
a deposit does not appear!"), so do NOT assume the defect is ultrawide-only;
the fix must not be either.

## Jobs (todo list first)

1. **Game-free design first**: from the entry's forensics, locate the
   positioning path that puts the `ResourceItems` dialog at (886,13) on a
   3751px window; identify the smallest §1-technique repair (anchor/clamp),
   and its self-check. Write the design on the entry BEFORE any live work.
2. **Attended verification sitting** (owner at keyboard, fixture save,
   cheats fine): reproduce once, apply the candidate repair via TestKit
   console harness, verify click-through works at the owner's resolution AND
   at a windowed non-ultrawide resolution (the OG witness says ordinary
   setups hit this too).
3. Build the fix module; probe; the standard A/B leg (stale-probe gate).
4. Records: F76 status, checklist item for the campaign if any residue needs
   eyes, STATUS counts.

## Scope fence

**In:** F76 only. **Out:** any other UI polish; the F13/F14/F19/F20 UI
family (shipped, out of scope); anything the sitting surfaces gets filed.

## Stop conditions

- The UI hard-locks again → quit safely, record the exact step, and STOP —
  a second lock means the repair approach is wrong, not unlucky.
- The positioning path is engine-side (not reachable from Lua) → record the
  finding on the entry, present the workaround-documentation option to the
  owner (MOD_DESCRIPTION `[FAQ]` tag), and close the design question
  honestly rather than shipping a cosmetic half-fix.

## What may not be claimed

"Repaired" needs the attended click-through observed at BOTH resolutions.
An unreproducible session proves nothing — say "did not reproduce", not
"fixed".

## On completion

Outbox → `12_final_qa_backward_check_fable.md`. Delete this file, commit,
push.

## Notes from upstream

(prompt 10 appends state here)
