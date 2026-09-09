# The `smr-community-fixes` follow-up — four chains, and the order they run in

> ⚠️ **2026-09-09 — WHAT THIS FILE IS, because it reads like something it is not.**
> The owner asked, verbatim: *"I am still confused by this. It sounds more like
> documentation on how chains are created."* **It is not that.** Two different
> documents, and the confusion is understandable because this one opens with
> chain vocabulary:
>
> | | |
> |---|---|
> | **How to build ANY chain** (the reusable method, the template, parallel-vs-sequential, failure modes) | `agent/reports/CHAIN_METHOD.md` — the playbook, written 2026-08-03 by the chain-12 QA session |
> | **THIS file** | a **work order** for four SPECIFIC chains against four SPECIFIC defects (`C50`/`C51`, `C52`, `C25`), plus the order they must run in and what was deliberately given no chain at all |
>
> So this is a **map of a particular backlog**, not a method. Its only reusable
> content is the *shape* of the decision it records — which candidates earned a
> chain, which were combined, which were refused — and that shape is already
> generalised in `CHAIN_METHOD.md` §5.
>
> ⛔ **THREE OF ITS FOUR ROWS ARE NOW DEAD. As a map it is down to one live row.**
>
> | chain | folder | state 2026-09-09 |
> |---|---|---|
> | **A** | `smrcf-verify/` | ⚖️ **REWRITTEN 2026-09-09** — the 3-file chain is replaced by one brief, `smrcf-verify/C35_DETECTOR.md`. 5 of its 6 deliverables were dead; only the `C35` detector survives |
> | **B** | ~~`smrcf-text/`~~ | ⛔ **CONSUMED 2026-09-09.** `C50`+`C51` were built 08-20 then DELETED in the 1.1.0 REMOVE pass; the dust-devil rider is REFUTED on 1.1.0 and its evidence moved to `facts/EF-084.md` |
> | **C** | `smrcf-modbrowser/` | ⏸ **kept** (owner, 09-09) — `C52` is `parked`, but its three source findings still hold and defect 3 touches our own store preview |
> | **D** | `jumbo-cave/` | ⛔ **CONSUMED 2026-09-09** (`49e32bf`, grave `33b3ad0`) — `C25` was confirmed from a field save and shipped as `F110` |
>
> ⇒ **This file's own disposition rule still binds and has NOT been met:** it says
> below that it is deleted by the LAST chain of the set to close. A and C still
> exist, so it stays — but a reader should treat it as a historical work order
> with one live row, not as current planning.

Written 2026-08-16 by the coverage sweep's own session (top tier), at the
owner's instruction: *"I want to write up chains for everything we found we can
fix, if the others are simple they can be combined chains. Complex can be stand
alone. the jump underground should be a solo issue chain."*

> ⛔⛔ **2026-08-20 — THIS MAP IS THREE-QUARTERS OVERTAKEN. Read this before
> acting on any row below.** The owner reversed the "post-launch" premise
> (checklist 58) and the close-out chain `closeout-1.0.0/` did the work instead:
> **`C50` and `C51` are BUILT and IN 1.0.0** (`Code/Fix_SpaceYDroneCapBullet.lua`,
> `Code/Fix_LocalizedUIText.lua`, 08-20) ⇒ ⛔ **chain B must not be run — it would
> rebuild shipped modules**; **`C52` is `parked`/FROZEN by the same ruling** ⇒ ⛔
> chain C is fenced, not merely gated; **`C49` is retired `wontfix`** (owner,
> 08-20). What survives untouched: chain A (`smrcf-verify/`), chain D
> (`jumbo-cave/`), and the dust-devil marker gate that chain B was carrying as a
> rider. ⛔ The counts quoted throughout this set are era-stale (they read 74–76
> modules; the tree is at 77) — re-emit, never read one from here.

**This file is a map, not a chain.** It is NOT self-consuming — it is deleted by
the LAST chain of the set to close, and its grave named there. Each chain
folder below self-consumes normally.

⛔⛔ **NONE OF THIS IS A RELEASE GATE.** The ship line is FROZEN pre-release and
step ④ (upload) is one owner action away. Every chain here is post-launch work
by the owner's own recommendation-in-hand (checklist item 34). **If ④ has not
happened, ④ comes first.**

---

## The four chains

| # | folder | subject | prompts | owner time | gated on |
|---|---|---|---|---|---|
| **A** | `smrcf-verify/` | answers every open reachability + feasibility question at once, arms two standing detectors | 2 | **zero** | nothing — runs first |
| **B** | `smrcf-text/` | `C50` SpaceY + `C51` localization (+ the dust-devil marker gate if A clears it) | 3 | ~15 min, one sitting | A |
| **C** | `smrcf-modbrowser/` | `C52` — three defects on the Mod Manager detail path | 4 | ~15 min, one sitting | A |
| **D** | `jumbo-cave/` | `C25` — solo by owner instruction | 4 | one playthrough segment | A |

**Chain A runs first and is the reason the other three are affordable.** Three
of them currently rest on unanswered questions — is the dust-devil marker path
reachable, does `AsyncPopsDownloadFile` exist, can map generation be driven from
Lua. A answers all of them in one unattended launch. **Do not author B, C or D's
build steps before A returns**; their briefs say so themselves.

B, C and D are **independent of each other** and may run in any order.

## What is deliberately NOT here

- **`C49`** (soil overlay) — reachability tier R4. `FIX_POLICY` §366-368: *"R4
  does not ship — record it `wontfix — unreachable` with the search that proved
  it."* No chain. A one-line status flip is owed and is on checklist item 34.
- **Restore Clustered Lights** — rejected during the sweep; the assertion is
  engine-side C++ with zero hits in all of Src. Not adjudicable, no chain.
- **`C35`** (lander cargo ramp) — **not a fix chain, an evidence problem**, and
  it is folded in rather than given a folder: its standing detector is armed by
  chain A (log-only, zero cost) and its 10-minute attended trigger rides B's
  sitting. If the detector ever fires, `C35` gets its own chain then — with
  evidence, which it does not have now.

## Model placement — owner's call, and why it is small here

`CHAIN_METHOD` §4.0: at **5 prompts or fewer the owner assigns models
themselves**; 6+ and a top-tier session should do the decomposition. Every chain
here is 2–4 prompts, so each is inside the owner's own range. **The
decomposition across all four was done by a top-tier session (this one)**, which
is the part §4.0 actually reserves.

The standing unattended rule (`CHAIN_METHOD` §4.0, owner 2026-08-04) sets the
floor and is honoured throughout: **even a single unattended item is a minimum
chain of two — the volume tier executes, the top tier audits adversarially
against the archived logs.** Routing lives in FILENAMES only; every prompt body
is model-neutral so the owner can re-route per task.

## Prior art, standing

Every chain here traces to a lead in `fredware`'s **SMR Community Fixes**, and
`FIX_POLICY` §8 credit applies to anything that ships. The sweep's full record,
including the two leads we rejected and the one we killed, is
`agent/reports/SMRCF_COVERAGE_SWEEP.md`. ⛔ The reference clone at
`C:\Dev\_ref\smr-community-fixes` is not ours to maintain: never a submodule,
never committed, never named in a shipped doc.

## ⭐ And one standalone prompt, outside the set — run it BEFORE ④

`agent/prompts/PUBLIC_DOCS_CHECKUP_fable.md` — a pre-upload sweep of every
player-facing surface (site ×5, three store cards, three `metadata.lua`
descriptions) for accuracy, forgotten updates, readability and flow. **Not part
of any chain, not gated on anything, and unlike everything above it is
time-sensitive**: these pages ship the moment ④ happens.

It already carries three confirmed findings as seeds — a live page that
contradicts itself about how many fixes are judgment calls, and a suite count
that is wrong on two surfaces for the second time.

## Kickoff lines

Start any chain by opening a fresh session at the named file and saying so:

- **A** → `docs/agent/prompts/smrcf-verify/C35_DETECTOR.md` — *"build the C35 detector"* (the old `01_PROBE_opus.md` kickoff is retired with the chain it started)
- ~~**B**~~ — CONSUMED 2026-09-09; nothing to run. Refutation: `facts/EF-084.md`.
- **C** → `docs/agent/prompts/smrcf-modbrowser/01_SPEC_fable.md` — *"run the mod browser chain"*
- **D** → `docs/agent/prompts/jumbo-cave/01_FEASIBILITY_opus.md` — *"run the jumbo cave chain"*
- **docs checkup** → `docs/agent/prompts/PUBLIC_DOCS_CHECKUP_fable.md` — *"run the public docs checkup"*
