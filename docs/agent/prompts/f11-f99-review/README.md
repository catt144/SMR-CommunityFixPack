# Chain — F11 / F99 second opinion (2 prompts, self-consuming)

**Why this chain exists.** On 2026-08-03 one session ran the F11 rider, filed
F99 from the same sitting's log, and proposed a code change (converting
`Fix_TrainPlatformWedge` from a full method copy to a pre-wrapper). That session
was the reporter, the interpreter and the proposer of its own findings. The
owner asked for a second set of eyes on both before anything is built.

**Owner decision on the record (2026-08-03):** the F11 fix **stays and ships**
regardless of what this chain concludes about reachability — *"If we are sure
the code is faulty imo we fix it and ship it unless we get evidence it does harm
fixing it."* This chain may **not** re-open that. What it may decide is the
**shape** of the fix and whether F99 becomes work.

## Manifest

| # | file | model | owner needed? | what it drains |
|---|------|-------|---------------|----------------|
| ~~1~~ | ~~`01_OPUS_RESET_THE_THEORY.md`~~ | ~~Opus~~ | — | ✅ **DRAINED 2026-08-03.** Derivation committed sealed (`28c253f`) then diffed; verdicts, 8 disagreements and one self-reversal in prompt 2's `## Notes from upstream`; working kept as `DERIVATION.md`. ⛔ **The seal could not be held** — chain rule 1 and `CLAUDE.md`'s mandatory STATE.md read both hand over sealed material before the prompt is opened; attested in full and owed to `CHAIN_METHOD.md`. Filed `C42`, `C43`, two riders |
| 2 | `02_FABLE_QA_AND_BUILD.md` | **Fable** | **NO — unattended** | Audits prompt 1, adjudicates, builds the F11 conversion or declines it, decides F99's disposition, empties this folder |

⭐ **Model placement ASSIGNED BY THE OWNER, 2026-08-03** (`CHAIN_METHOD.md` §4.0
— at 5 prompts or fewer the owner decides): **Opus on the derivation, Fable on
the QA and build.** That puts the scarce tier on the terminal adversarial QA,
which is also the only prompt that writes code — both places where errors
compound. Routing lives in the filenames; the prompt bodies are model-neutral,
so the owner can re-route by renaming.

**Both prompts are UNATTENDED.** Neither needs the game, the keyboard, or the
owner. That is deliberate: everything this chain can settle is settleable from
`ModTools\Src`, the two archived logs, and the raw readings quoted in prompt 1.
Anything that turns out to need a keyboard gets FILED as a rider, never run here.

## Binding chain rules

1. **Staleness check first, every prompt.** `git log --oneline -10` + `git pull`
   before anything else. This folder can be overtaken by a playtest sitting.
2. **Inbox / outbox in writing.** Nothing owed lives in a session's memory. A
   prompt ends by appending its handoff to the NEXT prompt's
   `## Notes from upstream`, committing, and **deleting its own file in the same
   commit**. The folder's emptiness is the done-condition.
3. **Route, don't drop.** Anything discovered that this chain does not own goes
   to `agent/bugs/` as an entry, or to `PLAYTEST_CHECKLIST.md` as a rider with a
   **TAKEABLE WHEN <condition>**. If you are unsure who owns it, **STOP AND ASK**
   rather than dropping it or absorbing it.
4. **Self-split at a clean commit boundary** if a prompt will not finish
   comfortably in context. The continuation is a first-class chain member with
   its own manifest row. Never push a job to the edge of the window.
5. **Drift-evidence capture.** Every disagreement with the 2026-08-03 record —
   including ten-second corrections — is APPENDED to the outbox, never silently
   fixed. A silently-corrected instance is destroyed evidence.
6. **The record is a claim too.** `agent/bugs/` entries, `agent/facts/` files and
   this README are all claims. **Re-derive the ROUTE, not just the citations** —
   this project has twice been wrong in a direction where every cited line was
   individually correct.
7. **WORKFLOW elements 1–7 bind** (`agent/WORKFLOW.md`), including the live todo
   list: one item per commit-and-verify unit, one in progress, updated
   immediately — the owner reads it to decide whether to step in.
8. **`FIX_POLICY.md` §3a and §2 bind any code written.** Parse sweep (python +
   luaparser, `utf-8-sig`) before ANY commit touching Lua. Commits via
   `git commit -F <file>`, no embedded double quotes. Push.
9. **`python tools/doccheck.py` before every doc commit; red blocks.** STATE.md
   is hard-capped at 60 lines — adding means evicting to
   `docs/archive/SESSION_LOG.md` in the same commit.
10. **Owner decisions are ROUTED, never absorbed** — to
    `PLAYTEST_CHECKLIST.md` "Decisions waiting on you", packaged with a
    recommendation.
11. **⛔ The seal (prompt 1 only).** Prompt 1 commits its own derivation BEFORE
    reading the 2026-08-03 write-ups. The seal is what makes the second opinion
    worth having; breaking it costs the chain its entire point. Prompt 1 attests
    to the seal in its outbox.

## Scope fence — the whole chain

**In:** F11's reachability reasoning and the proposed pre-wrapper conversion;
F99's mechanism, attribution and disposition; the correctness of the
2026-08-03 record on both.

**Out:** re-opening whether the F11 fix ships (owner decided). Any other module.
Any live playtesting. The `PLAYTEST_HELP.md:312` `ListFixes` count staleness
(flagged 2026-08-03, deliberately left for a sitting that can read the live
number). D12, PT-62, the drone work.
