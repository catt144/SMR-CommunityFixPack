# Chain — corun-batch-1 (the first batched co-run sitting; 3 prompts, self-consuming)

**Why this chain exists.** Owner order, 2026-08-04 ("Go ahead and build them
out"): batch the co-run-ready front of the routing queue into ONE attended
sitting, per WORKFLOW "Co-runs" batching rule — the launch and warm-up are the
fixed cost; the owner sits once. Authored by the unattended-1 terminal session
(Fable, 2026-08-04) at peak knowledge of that chain's 8-entry
unforeseen-issues ledger; **the guardrails it produced are BINDING here**
(`WORKFLOW.md` "Co-runs": resolution cross-check, ARM GATE, liveness
witnesses named in the brief, `pcall` always printed, no per-chain fact in a
per-process flag). **This folder must be EMPTY when prompt 3 finishes.**

Model placement lives in the filenames; bodies are model-neutral.

## Manifest

| # | file | model | owner needed? | what it drains |
|---|------|-------|---------------|----------------|
| 1 | `01_OPUS_PREP.md` | Opus | No | fixture confirms on a staged copy (one unattended confirm cycle) · every leg re-derived in rig terms from its ENTRY · probe sources parked here as `.lua.txt` · the sitting brief with its **measure-moments list** (each moment: what the owner does/looks at, verdict words, minutes) · predictions per leg · Src-verification of the two `[NEVER RUN]` recipes the sitting will execute |
| 2 | `02_OPUS_SITTING.md` | Opus | **YES — the sitting.** Attended for the NAMED moments only (est. 15–25 min of attention across the batch; exact minutes come from prompt 1's brief) | the batch: legs 1–5 + ride-alongs, results recorded on entries, evidence cards per the ADOPTED tiers |
| 3 | `03_FABLE_AUDIT.md` | Fable | No (routes decisions) | adversarial audit vs archived logs · integration · unforeseen-issues delta vs unattended-1's ledger · folder empty |

## The payload (front of the co-run queue, routing sweep 2026-08-04)

All legs run on staged COPIES of `TEST2H TRAIN` (FIX_POLICY §3a); the
campaign save is never written. The SAVE primitive is PROVEN (envelope) —
in-run saves on throwaway names are allowed and die in the recording commit.

- **Leg 1 — PT-37: the F48 DECIDER** (owner eyes: route formation + the
  salvage-cursor check). Case A (healthy track) + case B (meteor-damaged
  track), exact console procedure on `agent/bugs/F48.md` (2026-08-03 block).
  Damage staged via `CheatTriggerMarsquake()` near a track or
  `CheatMeteors("single", nil, <pos>)` (HELP table — always pass a position).
  PASS both → F48 unblocks into the sanitizer; dirty FAIL on case B → closes
  `wontfix`. ⚠️ `ProcessTrackElements` reachability from the mod env/console
  is **prep's job to verify** before the sitting leans on it.
- **Leg 2 — PT-47: F26 bombardment volley** (owner eyes: scatter-vs-rank —
  the one thing that is eyes by nature; camera low). Forced via the entry's
  recipe `StartBombard(UIColony:GetCityAtMap(MainMap), 40*guim, 8, 500, 1500)`
  — ⛔ that call is itself `[NEVER RUN]`; unattended-1 leg E proved a
  Src-verified `[NEVER RUN]` recipe can be broken in a way only running shows
  (the `table.copy` devil row). Prep Src-verifies the signature; the sitting
  executes it as a FIRST EXECUTION: `pcall`, result printed, witness read
  before any verdict. The five integrity checks (decals, dome crack,
  notification, interception, volley ENDS) are agent-side reads per the entry.
- **Leg 3 — PT-42: F22/F75 Last Transmission reserves** (owner eyes: the
  faction panel goals at 3–4 named moments). ⚠️ FIXTURE-GATED: prep must
  confirm Last Transmission is an active faction on the staged save; absent →
  `SKIP <reason>` + stays routed, never a re-choice of save. Stock/drain
  staged at speed agent-side; the Oxygen-only clearing of the Oxygen goal is
  the F75 read.
- **Leg 4 — PT-53 E: D07 precedence + uninstall shape** (owner hands ×2:
  the manual Senior assignment, and the Mod-Manager disable click). The
  manual-assign half runs EARLY (module live); ⛔ **the Mod-Manager-disable +
  load-clean half is the LAST ACT of the whole sitting** — after it the pack
  is not loaded and no pack leg is valid. A toggle cannot answer an uninstall
  question ("OFF is three different things").
- **Leg 5 — PT-35 turbine-half fixture, OPTIONAL owner minutes (~3–5):**
  `CheatResearchAll()` (verified) grants FrictionlessComposites; the owner
  PLACES one Large Wind Turbine and applies one building upgrade (placement is
  UI — the one thing the rig cannot do); save as a named FIXTURE save. That
  discharges the unattended-1 routed gap's fixture request; the re-run of leg
  A itself then routes as a cheap 2-prompt unattended chain, NOT this sitting.
- **Ride-alongs (no extra fixture, batched free):**
  - **F21 reads** during leg 1's train activity (platform-wait Comfort +
    "Travel time (rolling average)" — re-earns `tested` for the wrapper).
  - **C42 within-session read** — generate passage traffic at speed, take
    `C42STALE` BEFORE any save/load (discharges the unattended-1 routed gap;
    no eyes). The denominator is UNIT ENTRIES, not passages.
  - **Popup keystone + F85 + §3.6 corner** — one cheap choice popup; F85 is
    a HANDS-ONLY moment (rebind Quick Save to F9, press it under the popup).
- **Deliberately NOT in this batch:** PT-27/PT-28 (need SAVE-A + Dust In The
  Wind), PT-18 (SAVE-E is ~30 min of owner provisioning), PT-10/PT-15/PT-60/
  PT-20, F74+F53(a) (fresh vanilla colony), F34(d)/F38 (situational
  fixtures). They stay routed; over-batching one sitting is how legs get cut
  mid-run.

**Ordering rule (binding): reads first, mutations last, process-mutations
dead last.** F21/C42/PT-42 reads → PT-53 manual-assign → PT-37 (track
mutation + save/reloads) → PT-47 (bombardment, most destructive) → popup
trio → leg 5 fixture build → PT-53 E uninstall half (final act).

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
7. **FIX_POLICY §3a**: staged COPY (`Copy-Item`, game closed); the campaign
   save is never written; copies + throwaway saves die in the recording
   commit (the leg-5 FIXTURE save is the one deliberate survivor — it is a
   provisioned fixture, named in the recording commit, not a throwaway).
8. **Probe hygiene binds unchanged** — sources parked here as `.lua.txt`;
   files in `Code/` only while the run happens; C11 + its piping corollary;
   ARM GATE before every launch; `PROBE SWEEP:` line in every result commit;
   R8 `git add -f` for every cited log.
9. **doccheck green before every doc commit**; STATE 60-line cap; commits via
   `git commit -F <file>`; parse sweep before any commit touching Lua; push.
10. **⛔ NO ASSUMED CAPABILITY.** PROVEN bins are WORKFLOW's envelope. The two
    `[NEVER RUN]` executions this chain makes (`StartBombard`,
    `ProcessTrackElements` from console) follow the first-execution
    discipline: cheap dedicated verify BEFORE the leg leans on it; failure →
    routed gap, not improvisation.
11. **⛔ The forced-vs-organic rule**: every finding names what was forced.
    The bombardment and the quake are FORCED upstream conditions; the
    measured paths (volley behaviour, repair routing) stay the game's own.
12. **⛔ ANTI-SPRAWL.** No new standing document, folder, or document class.
    Results land on entries, the checklist, HELP markers, `SESSION_LOG.md`.
    Evidence cards are transient sign-off artifacts (corun-rig precedent).
13. **Sign-off runs on the ADOPTED tiers** (owner, 2026-08-04; WORKFLOW).
    The brief tags every moment Tier A (eyes), HANDS-ONLY, or Tier B/C
    (card/digest). `tested` still means a pass at the keyboard — a co-run
    pass the owner witnesses CAN earn it (routing-sweep consequence); a
    log-only result cannot.
14. **⭐ Kickoff + next-chain handoff.** Prompt 3's owner report ENDS with the
    next-chain kickoff line (source: `STATE.md` NEXT; nothing queued → say
    so). Mid-sitting, if a leg needs owner time beyond its stated minutes,
    the owner decides live — that is what attended means; record the actual
    minutes against the estimate either way.

## Scope fence — the whole chain

**In:** the payload above; recording + integration; evidence cards; the
sitting's log review (PT-22).
**Out:** building any fix (F48's sanitizer repair ships only AFTER the owner
sees the PT-37 result — deciding ≠ building); PT-35 leg A's re-run (routes to
a 2-prompt unattended chain once the fixture exists); anything listed
"deliberately NOT in this batch"; changing any owner decision.

## Stop conditions (chain-wide)

- A fixture confirm fails in prep → that leg becomes `SKIP <reason>` in the
  brief; the sitting runs the rest. Two or more core legs dead → route to the
  owner before scheduling the sitting.
- Any `[LUA ERROR]` naming pack code mid-sitting → stop the leg, record
  verbatim, continue with independent legs if the game state allows.
- The owner has to leave → finish the current leg's read, save nothing
  unplanned, record what ran; the remainder stays on the checklist as
  TAKEABLE IN the next co-run. An honestly-closed partial sitting beats a
  rushed one.
- PT-53's uninstall half, once started, is not interleaved with anything —
  it is last precisely so a stop there costs nothing else.
