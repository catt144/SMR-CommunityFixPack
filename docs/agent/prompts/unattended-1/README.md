# Chain — unattended-1 (the first fully unattended batch; 3 prompts, self-consuming)

**Why this chain exists.** Owner order, 2026-08-04: run everything the routing
sweep sent to UNATTENDED as the first true unattended batch, **doubling as the
test bed for unforeseen issues before co-runs scale up**. It executes under the
owner's chain rule of the same date (`WORKFLOW.md` routing triage, mode 1):
volume tier (Opus) executes, top tier (Fable) audits; batches are a full chain
with a terminal top-tier audit. **This folder must be EMPTY when prompt 3
finishes.**

**Authored by the corun-rig terminal session (Fable, 2026-08-04) at peak rig
knowledge.** Model placement lives in the filenames; bodies are model-neutral.

## Manifest

| # | file | model | owner needed? | what it drains |
|---|------|-------|---------------|----------------|
| 1 | ~~`01_OPUS_PREP.md`~~ **DONE 2026-08-04, file consumed** | Opus | No | ✅ SAVE primitive BINNED (Src-verified, deletion route decided agent-side) · leg D re-derived and **split into D1 natural / D2 forced-defect** · **8 parked sources, parse sweep GREEN** (`97_U1Common` + `98_U1C0..C6`) · 7-cycle plan with predictions + 3× watchdogs · run-conditions template + per-leg falsifiers · 3 drift corrections in the open · 1 decision routed to the checklist. Handoff: `02_OPUS_RUN.md` "Notes from upstream" |
| 2 | `02_OPUS_RUN.md` | Opus | **Kickoff word only** (machine must be free; no sitting) | Executes all legs across launch cycles; proves the save primitive FIRST; records with run-conditions headers; archives logs; flips the two `[NEVER RUN]` markers |
| 3 | `03_FABLE_AUDIT.md` | Fable | No (routes decisions) | Adversarial audit vs archived logs; the unforeseen-issues report (the run's second product); integration; folder empty |

## The payload (from the adopted 2026-08-04 routing sweep)

- **Leg A — PT-35 sanitizer do-no-harm, case A.** Both sanitizer calls return
  0, nothing changes, idempotent across a save/reload. ⚠️ Needs the SAVE
  primitive and a fixture confirm (Large Wind Turbine + upgraded Medical
  Center in a dome — unverified on `TEST2H TRAIN`).
- **Leg B — F99 residue BEFORE a reload** (checklist rider, superseded
  TAKEABLE-WHEN). Break a track element, then
  `CheatCompleteAllConstructions()`, watch for `TrackElement.lua:805`, take
  the F99RESIDUE read **before any save/load**.
  ⚠️ **Instrument corrected 2026-08-04 by prompt 1 (chain rule 5).** This
  bullet said `CheatMeteors("single", nil, pos)` "because the meteor path is
  what populates `repair_cgs`, `Meteors.lua:609`". The citation and the
  `repair_cgs` point stand; the instrument does not. `BaseMeteor:HitTracks`
  (`:615-621`) just collects elements and calls the **plain global**
  `BreakTracks(elements)` (`:599-613`) — and it is `BreakTracks` that filters
  to neither-endpoint/no-station (`:601`), calls `BreakTrackElement` (`:603`),
  does `table.insert(track.repair_cgs, cg)` (`:609`) and fires
  `Msg("TrackBroken", track, true)` (`:610`). So `BreakTracks({element})` is
  the meteor's own funnel with the lottery, the disaster thread and the
  collateral removed (WORKFLOW leg-design rule 2) — and it is specifically
  **not** co-run #1's bare `BreakTrackElement`, which does not populate
  `repair_cgs`.
- **Leg C — F99 no-cheat discriminator.** Forced break; **ORGANIC drone
  repair** at speed (the measured path — never completion-cheat it); watch
  for `:805` on the organic completion. ⚖️ The owner's kickoff of this chain
  is the "say the word" their F99 decision line asked for — running the
  discriminator. **The severity decision itself stays theirs.** A single
  no-cheat occurrence moves F99 off `cand`; zero is a rate bound (state the
  condition sampled — WORKFLOW leg-design rule).
- **Leg D — the load-heal round-trip sweep** (campaign Do-first #2), as
  re-derived by prompt 1 from `CHAIN_QA_REPORT.md` §9 item 2. Heal lines are
  load-time log lines; save → reload → reload is the rig's proven core plus
  the save primitive.
- **Leg E — execute the two `[NEVER RUN]` verified-table rows**:
  `CheatDustStorm` (deterministic setting form; confirm storm start/stop in
  the log) and the forced static-charged dust devil (descr copy,
  `electro_chance = 100`). Flip both rows to `[RAN <date>, log <name>]`.
- **Leg F — C42 passage read, ride-along** if the staged copy has a Passage
  with traffic; `SKIP <reason>` line if not.

**Ordering rule (co-run #1 lesson): reads first, mutations last.** Legs that
mutate the world (B, C, E) run after every read on their cycle, or on their
own cycle — cycles cost ~90 s, do not share a cycle to save one.

## Binding chain rules

1. **Staleness check first, every prompt**: `git log --oneline -10` +
   `git pull`.
2. **Inbox/outbox in writing.** Each prompt appends its handoff to the next
   prompt's `## Notes from upstream`, commits, deletes its own file in the
   same commit. Folder emptiness is prompt 3's done-condition.
3. **Route, don't drop**; unsure who owns a discovery → STOP AND ASK.
4. **Self-split at a clean commit boundary** if context runs short.
5. **Drift-evidence capture** — disagreements with the record are corrected
   visibly, never silently.
6. **WORKFLOW elements 1–8 bind** (live todo list; declared read path).
7. **FIX_POLICY §3a**: every run uses a staged COPY (`Copy-Item`, game
   closed); the campaign save is never written; copies die in the recording
   commit. In-run saves (legs A/D) are NEW throwaway files, deleted with the
   copies.
8. **Probe hygiene binds unchanged**, including rule 5 (probe files exist in
   `Code/` only while the run happens; sources live parked beside the briefs
   as `.lua.txt`), C11 (arming edits are script FILES, never inline
   PowerShell one-liners), the `PROBE SWEEP:` line in every result commit,
   and R8 (`git add -f` for every cited log, in the same commit).
9. **doccheck green before every doc commit**; STATE 60-line cap (evict in
   the same commit); commits via `git commit -F <file>`; parse sweep before
   any commit touching Lua; push.
10. **⛔ NO ASSUMED CAPABILITY.** The rig's PROVEN bins are in `WORKFLOW.md`
    "Co-runs" (capability envelope). Anything outside them — **the SAVE
    primitive is the known case**: `SaveGame(display_name, params)`,
    `Savegame.lua:1071`, Src-verified not blacklisted (corun-rig S2 grep),
    NEVER EXECUTED by us — must be proven by a cheap dedicated step BEFORE
    any leg leans on it. If the proof fails, the legs needing it become
    routed gaps, not improvisations.
11. **⛔ The forced-vs-organic rule** (`WORKFLOW.md`): every finding names
    what was forced. Leg C's repair path is organic BY DESIGN — completing
    it by cheat destroys the leg.
12. **⛔ ANTI-SPRAWL (owner, 2026-08-04).** No new standing document, folder,
    or document class. Results land on existing surfaces: entries, the
    checklist, `PLAYTEST_HELP.md` markers, `SESSION_LOG.md`.
13. **⛔ UNATTENDED means unattended.** No step may require a human mid-run.
    A modal dialog, a Steam picker, a hang past the watchdog — anything that
    would need a hand — is a STOP: record what appeared (it is exactly the
    unforeseen-issue evidence this chain exists to collect), quit the game
    if possible, and route. Never wait for a click that is not coming.
14. **⭐ Escalation offer + next-chain handoff (owner rule, 2026-08-04).**
    If any leg turns out to need eyes or hands after all, the discovering
    prompt routes it to the owner in chat AND on the checklist **with an
    offer**: author `02b_OPUS_CORUN.md` — an attended co-run prompt
    inserted immediately before the terminal audit, carrying a
    measure-moments list, prep per rule 5, and the owner-minutes cost.
    Owner says yes → build it and add its manifest row here; owner declines
    or does not answer by the time this prompt must close → the item
    becomes a **TAKEABLE IN a co-run** rider on the checklist and the chain
    continues without it. The terminal audit is the last prompt either
    way. And prompt 3's owner report **ends with the kickoff line for the
    next queued chain** (source: `STATE.md`'s NEXT pointer; if nothing is
    queued, say so).

## Scope fence — the whole chain

**In:** legs A–F; the save-primitive proof; the `[NEVER RUN]` executions;
recording + integration of results; the unforeseen-issues report.
**Out:** building any fix (file, don't fix); F99's fix; anything the sweep
routed to co-run or playtest; changing `tested`/sign-off policy (the tier
decision is still open with the owner); new fixture builds. If a leg turns
out to need eyes or hands after all, that IS a finding — chain rule 14's
escalation offer applies; never improvise attendance.

## Stop conditions (chain-wide)

- The save-primitive proof fails → legs A and D route as gaps; legs B, C, E,
  F still run (they need no in-run save).
- Any `[LUA ERROR]` naming pack code, any modal, any picker → stop the leg,
  record verbatim, continue with independent legs if the game state allows a
  clean relaunch, else route.
- A leg's fixture confirm fails → `SKIP <what was missing>` line + routed
  gap; never a re-choice of save.
- Two consecutive cycles lost to the same unexplained failure → stop the
  chain, write what is known into prompt 3's inbox, route to the owner.
