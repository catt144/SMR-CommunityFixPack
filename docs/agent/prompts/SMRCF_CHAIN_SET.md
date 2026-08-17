# The `smr-community-fixes` follow-up — four chains, and the order they run in

Written 2026-08-16 by the coverage sweep's own session (top tier), at the
owner's instruction: *"I want to write up chains for everything we found we can
fix, if the others are simple they can be combined chains. Complex can be stand
alone. the jump underground should be a solo issue chain."*

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

- **A** → `docs/agent/prompts/smrcf-verify/01_PROBE_opus.md` — *"run the smrcf verify probe"*
- **B** → `docs/agent/prompts/smrcf-text/01_BUILD_opus.md` — *"run the smrcf text chain"*
- **C** → `docs/agent/prompts/smrcf-modbrowser/01_SPEC_fable.md` — *"run the mod browser chain"*
- **D** → `docs/agent/prompts/jumbo-cave/01_FEASIBILITY_opus.md` — *"run the jumbo cave chain"*
- **docs checkup** → `docs/agent/prompts/PUBLIC_DOCS_CHECKUP_fable.md` — *"run the public docs checkup"*
