# C83 fix — arrivals must not be sent into a dead dome (model-agnostic)

⛔ ONE-SHOT: `git rm` this file at close-out. ✅ **TAKEABLE NOW — the owner ruled checklist
143 = FIX on 2026-09-10.** ⛔ **Start only after the C74/C77 build has committed:**
`git status --short` must show no `Code/Fix_SilentHitMomentFX.lua`, `items.lua`,
`metadata.lua` or `bugs/C74.md`/`C77.md` changes. If they are still there, stop and tell the
owner (the tree is shared; that work is another session's). Steps 0–8 run unattended; step 9
needs the owner at the keyboard — ask ONCE, batched, when you reach it. Written 2026-09-10
by the session that filed C83; verify every specific against `git log` and the trees.

## 0 · Read first
`git log --oneline -10` + `git pull` + `git status --short` (+ `ListAgents` where available).
Then: `agent/STATE.md` · `prompts/DISPATCH.md` §0–§2 · **`agent/bugs/C83.md`** (the case;
owner-OBSERVED) · `agent/bugs/F53.md` + `agent/bugs/F117.md` (the module you extend and its
argument probe) · **`Code/Fix_ArrivalDeaths.lua` whole** · `agent/FIX_POLICY.md` §1, §2, §2a,
§2b, §3a, §4a · `EF-022`/`EF-023` (what enters a save) · `reports/REACHABILITY_AUDIT.md`
"Challenge review". Game 1.1.0.403908 (`EF-075`); 1.0.7 archive for the branch check (`EF-083`).

## 1 · Live todo list from your first action — one item per step below, updated the moment each finishes (the owner reads it to decide when to step in).

## 2 · The design (desk-derived in conversation 2026-09-10 — step 0 re-derives it)

**Where:** extend `Fix_ArrivalDeaths`' existing `Colonist:Idle` pre-wrapper (F53 half b,
`Code/Fix_ArrivalDeaths.lua:326-364`). It already runs for every arriving colonist
(`self.arriving`) before vanilla's `Colonist:Arrive` reads the destination into a local
(1.1.0 `Colonist.lua:1592`). Today it re-chooses only when the assigned dome is NOT reachable
(`:341-345`). **Add:** when the assigned dome IS reachable but NOT welcoming — vanilla's own
test, `accept_colonists and ui_working and HasLifeSupport()` (1.1.0 `_GameUtils.lua:382-384`,
1.0.7 `:342-344`, a `local` in both, so it must be copied with an `-- SRC:` line) — re-choose.

**Re-choose:** `GetDomesReachableByColonists(self.city, pos)` — its list holds only walkable,
welcoming domes (`:408-411`) plus station-sweep domes (`:450-480`) — then `ChooseDome(dome_arg,
domes, <nearest welcoming>, dome_elevators)` with `<nearest welcoming>` as the safety fallback,
so an arrival with no free housing lands HOMELESS in the nearest working dome. That is the rule
vanilla already applies to elevator safety domes (`:437`). ⚠️ The station sweep appends AFTER
the distance sort (`:446` vs `:461`), so "nearest" is the minimum of the returned `dome_dist`
(3rd return value), not `domes[1]`. Keep `emigration_elevator` paired from `dome_elevators`
(the module's own rule, `:357-361`). `dome_arg` = the existing F117 `choose_dome_arg(self)`;
`nil` ⇒ stand down, as today.

**If no welcoming dome is reachable:** STAND DOWN — vanilla's choice stands. The alternative
(`emigration_dome = false` ⇒ "Confused Colonists" at the pad, `Colonist.lua:1625-1626`) keeps
them outside and is no safer; do not trade one death for another without the owner.

**Why this seam, not the shared rule:** `GetDomesReachableByColonists`/`ChooseDome` also drive
homeless resettling, the "Abandoned" path and android spawns (F117 lists nine `ChooseDome`
callers); F53 declined a global wrap for the same reason. This stays arrival-only, reuses the
F117 probe and the module's layer-2 save shape, and **declines by construction** if the devs fix
it: a welcoming assigned dome gives the new branch nothing to do.

## 3 · Steps

0. **Challenge §2 and C83 before coding.** Re-derive from both trees, as numbered claims, each
   PASS/FAIL with the line: (a) the fallback has no welcoming test (1.1.0 `:403-407`, 1.0.7
   `:359-362`); (b) the observed split is per-colonist `ChooseDome` + `HasFreeLivingSpaceFor`;
   (c) `HasLifeSupport` = water and (breathable or power and air), `Community.lua:462-463`;
   (d) the wrapper sees EVERY arrival path that sets `arriving` (rockets, and
   `CargoTransporterNew` landers — `:952-953`, `:996`, `:1045`, `:1088`), and runs before
   `Arrive` reads the field; (e) quarantine = `accept_colonists` and does not bar the walk-in
   (observed). A FAIL that changes the design ⇒ fix the design here; if it changes what the
   owner was told, route it to checklist 143 first.
1. **The homeless follow-through (can the fix be undone?).** A colonist placed homeless in a
   full working dome later resettles via `Colonist:FindEmigrationDome` →
   `BuildReachableGraph` / `GetBestReachableCommunities` (`Colonist.lua:3497-3527`) and the
   homeless paths. Trace whether ANY of those can pick a non-welcoming dome (the same fallback
   shape). If yes: do not widen this fix silently — file it as a sibling (C84+, FIX_POLICY
   §4a) and tell the owner in the checklist.
2. **The opt-in pack.** Both mods loaded is the rig's normal config. Read
   `C:\Dev\SMR-OptInPack\Code\Opt_ResidencyControl.lua` (D03 — blocks dome move-ins; proven
   against arrivals on a pad beside a closed dome) for hooks on the same path; the two must
   compose (a re-choose must not hand an arrival a dome D03 would refuse — or show why it can't).
3. **Build** inside `Fix_ArrivalDeaths` (same module ⇒ no `items.lua` change; confirm H-10
   holds): the welcoming check + re-choose, all BEFORE `return orig_idle(...)`, nothing after
   it (layer 2, FIX_POLICY §3a; run `tools/blocking_analysis.py` on any callee you add).
   `-- SRC:` + `-- DEFECT:` lines for the new half (`python tools/bodycheck.py --pin …`); the
   module header's defect list gains a (c). `Require` any method/field the branch reads that
   the module does not already require. §2a: both trees share the welcoming shape — state in the
   header why no new probe is needed, or add one if step 0 finds a branch difference. Decide
   whether the pack's veto id stays `ArrivalDeaths` for both halves (one switch) and say so in
   the header. `python tools/parsecheck.py`; doccheck.
4. **Log line:** one `[CommunityFixPack]` line the first time the new branch re-routes an
   arrival in a session (colonist, old dome, new dome) — step 9's readout reads it.
5. **Desk control** — extend the `tools/desk_f117_recipe.py` pattern (the shipped
   `_GameUtils.lua:382-501` span loaded under its real file name + line offset,
   `tools/deskbench.py` shims). Demands: (a) walkable dead dome assigned + a welcoming dome with
   space ⇒ re-routed there; (b) welcoming dome FULL ⇒ re-routed to it anyway (homeless);
   (c) no welcoming dome ⇒ stands down, assignment untouched; (d) welcoming dome assigned ⇒
   untouched; (e) the F53 not-reachable branch unchanged (regression); (f) `dome_arg` nil ⇒
   stands down; (g) station-sweep-only welcoming dome is picked by `dome_dist`, not list order.
   ⛔ A control must test the premise — include one where the harness would pass for the wrong
   reason and show it does not. Register it in `tools/deskbench.py`.
6. **Save-safety walk (§3a):** nothing new persists; the wrapper frame stays layer 2 with
   nothing after the call; uninstall = vanilla's fallback back, nothing stranded.
7. **Kit probe** if FIX_POLICY requires one for a new branch in a KEEP module (TestKit is
   local-only by design, never pushed).
8. **Records:** C83 `fixed` (NOT `tested-*` yet) with the build notes; F53 gets a one-line
   pointer (the module now carries C83's half); STATE module/row counts via
   `doccheck.py --emit-counts` if they moved.
9. **Attended A/B with the owner (one batched ask; readout = a prefixed `print` + a LOG
   FLUSH — memory "read console output from the log").** ⛔ `H-06` first: copy the colony's
   autosaves. The fixture is the owner's save made just before the landing (C83 §FIXTURE —
   read its `.savegame.sav` header, record the name in C83). The unfixed run is already on
   record (the observed split, 2026-09-10). With the fix: load, let the rocket land ⇒ nobody
   enters the dead dome, the step-4 log line names the re-routes, overflow arrivals sit homeless
   in the working dome; one sol later none of them has moved into the dead dome (step 1's
   question, measured). Plus one ordinary landing next to a working dome with free housing ⇒ no
   re-route line (the fix stays silent when vanilla is right).
10. **Patch note + reporter:** one line to `prompts/RELEASE_OUTBOX.md` (per its header); update
   checklist 143's reporter reply from "logged for a fix" to what shipped. Shipping is the
   owner's.

## 4 · Fence
Never the game dir or the source archives. `Mars.exe` NOT running (`tasklist`) before touching
`Code/`, in a separate step. No `metadata.lua` version edits (H-02), no Mod Editor, no upload,
no tag move (H-01). The opt-in pack is read-only here. A design-flavoured call → the checklist.

## 5 · Close-out
C83 status per the result (`tested-attended` only after step 9); checklist 143 receipt; STATE
only if the kernel changed; SESSION_LOG; commit with `git commit -F <msg> -- <paths>` after
checking `git status` for other sessions' changes; push; `git rm` this prompt.
