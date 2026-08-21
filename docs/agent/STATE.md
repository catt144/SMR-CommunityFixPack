# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; full pre-eviction STATE = `git show 2326bd3:docs/agent/STATE.md`.
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Now
- ⭐⭐⭐ **PUBLISHED 2026-08-20 — ④ IS DONE, BOTH PORTALS, by the owner.** Paradox Mods `pdx_id` **156049**
  ships **1.0.0**; Steam `steam_id` **3787202810** ships **1.0.2** — same 78 modules, byte-identical code.
  ⚠️ The split is mechanical, not a mistake: Paradox saves AFTER upload, Steam saves BEFORE packing, so running
  both in one sitting put the bump inside Steam's archive (checklist 71; `PORTAL_PREP` §0.5(c)). ⛔ Do NOT
  re-upload to "fix" the number — a further upload bumps again. This retires 37 Q2, decided by circumstance.
- ⛔ **Owed on the live listings** (owner's hands): `PORTAL_PREP` §0.5(d) required game version **350453** ·
  §0.5(f) delivered-bytes ⚠️ **Paradox only** against md5 `6621384b…`/391,567 B; ⛔ Steam's archive legitimately
  differs (385,131 B — its save stripped comments and bumped the version before packing) · then §1 steps 2–4:
  store links into the site, Pages on, site link back onto both store pages.
- ⭐⭐ **Close-out chain (5 links) CONSUMED 08-20 — VERDICT SHIP, 0 launch blockers; all 5 challenges held.**
  `C50`+`C51` IN 1.0.0 (checklist 58), `C52` `parked`/FROZEN. Ruling receipt checklist 66.
  ⚠️ Link 5 left NO report: its record is commit `2326bd3`'s message + fact `EF-066`.
- ⭐⭐ **`C50`+`C51` are `tested-attended` (08-20, EN+DE, owner at the keyboard): 77 applied, suite 74/0/24/0 of 98.**
  Report `reports/04_ATTENDED_SITTING.md`; logs `archive/link4{en,de,lang}_*`.
  ⛔ SKIPPED BY NAME: `C50`'s challenge landing-spot site, and the in-game Mission Profile on a SpaceY colony.
- **This repo is CLOSED once the owner uploads** — no queued 1.0.1; next effort is the **opt-in pack**
  (owner 08-20, checklist 68); its kickoff reads that repo's own STATE + `reports/PARKED_OPTIN_REFERENCES.md`.
- ⛔ **Shipping artifact: NO PACKED `.fpk` MATCHES THIS TREE.** Expected shape **82 files = 78 `Code/*.lua` +
  `items.lua` + `metadata.lua` + `LICENSE` + `preview.png`** (`tools/pack_predict.py`, emitted).
  ⛔ **The md5/bytes exist only after the owner packs at the sitting — never quote one**; the blank row that
  receives them is `PORTAL_PREP` §0.5(f). Reader `tools/pack_list.py`, upload guard `tools/upload_preflight.py`.
- ⛔ **The console is NOT a route to pack or reload** — `DbgPackMod`/`ReloadLua` are both nil in `_G` at the retail
  console (measured). Only route = Mods Manager → Edit (`Ctrl-E`) → **File → Pack Mod**; ⚠️ it loads a scratch colony.
- ✅ **Rig at the 08-20 sitting: all 3 junctions present, fix pack + TestKit ticked, opt-in pack OFF** (checklist 43).
  The rig runs cheats — the normal config.
- **Owner decisions open** (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"):
  53 (harden now or in 1.0.1; rec 1.0.1) · 51 (both-packs leg timing; rec after launch) · 50 (chain-vs-replace
  wording) · 47 (two modder-page wordings) · 43 (opt-in pack re-tick) · 41 (dialog wording + sweep cap 5→8) ·
  40 (`smr_shuttles` name) · 39 (dialog re-fire) · 37 Q2 (Steam, after Paradox).
- Watches: `EF-066`'s unswept question — the pack wraps ~60 (class, method) targets and no audit has enumerated
  which have shipped SUBCLASS overrides the wrap never reaches (under-coverage only, never new harm; opt-in-era) ·
  ⚠️ German is the ONLY localisation ever SEEN; the other 7 packs stay CSV-measured (`EF-039`) · TestKit wave-12
  clause 1 taxonomy (other repo, `EF-066`) · C47 speed thread (descending ladder, unrun) · C48 CANDIDATE (opt-in
  territory; no seed-family fix code here) · F02/F78/F81 organic · riders C42/F99/F80/F96-R2 post-release ·
  `EF-051` falsifier = any stray save.

## Hazards — each names an action an agent could take unattended; never do it
- **H-01** Tag `fixpack-v1.0.0` was MOVED AGAIN 08-20 onto the close-out audit's commit and now marks what actually
  gets packed. ⛔ Its gate is the ATTENDED SITTING + the one-time release-gate ruling (checklist 57), NOT run B.
  Never move it again without an equivalent gate.
- **H-02** `metadata.lua` is **FROZEN** at 1.0.0 — no version bump, no Mod Editor save
  (every editor save runs `version = version + 1`, `Mod.lua:967`).
- **H-03** No script/console in a launched game may touch a portal API — the FIRST call **creates the listing**
  (`SteamWorkshop.lua:17-22`). Safe: `DbgPackMod`, `tools/upload_preflight.py`. Paradox before Steam.
- **H-04** ✅ **DISCHARGED 2026-08-20 — the owner uploaded; ④ is done and this is the one moment striking it is
  correct.** It stays listed because its successor binds: ⛔ **never call a FUTURE release ready, and never treat
  "published" as covering anything the owner has not done** — the post-upload items above are still open.
- **H-05** Sweep fence, still binding after both chains closed: no session reads
  `prompts/prelaunch-sweep/SWEEP_FINDINGS.md` or the link reports to reach a verdict, and neither STATE nor
  SESSION_LOG ever restates a link verdict — point at the ledger instead.
- **H-06** `EF-056`: loading a COPY of a campaign still runs that campaign's autosave rotation and
  **deletes the owner's autosaves** — pre-copy every autosave first.
- **H-07** Never restore the ~46 parked opt-in references here before the opt-in pack launches; that is ITS
  launch obligation, recorded in that repo. Verbatim parking: `reports/PARKED_OPTIN_REFERENCES.md`.
- **H-08** ⛔ **Pulling a mod's junction COSTS its enable and restoring the folder does NOT buy it back**
  (`EF-055`). Recovery = owner tick + restart, never an agent's. Never pull one to reach a configuration without
  booking that cost. ⚠️ The cost lands when the **id vanishes**; a folder-for-folder swap under the **same id KEEPS**
  the enable. **The opt-in pack is in that state now** (checklist 43).
- **H-09** Never stage a packed folder beside a live junction to reach a packed reading: with both present at
  equal version the **unpacked one WINS**, silently (`Mod.lua:1770`), and the leg measures nothing.
- **H-10** Never add, rename or drop a `Code/*.lua` module without updating `items.lua` — `SaveDef` rebuilds
  `metadata.lua`'s `code` list SOLELY from its items (`Mod.lua:816-840`, `:973`) and both portals force that save
  on a first upload (Steam's BEFORE packing), so a module absent from `items.lua` **ships absent** (checklist 46).

## Rules in force (owner rulings; bodies in checklist/SESSION_LOG)
- Ship line FROZEN (08-12): `fixed` + suite + self-checks + verified save-safety IS the bar.
- A green suite does NOT authorise an upload — config B is the gate (08-17).
- ⛔ **The gate was ONE-TIME, not a per-change tax (08-20, item 57).** Post-release = patch-note-driven
  maintenance: `items.lua` entry (H-10) + one boot `applied` log + doccheck counts. ⛔ Never quote
  `FIX_POLICY` §3a's per-module cost for a single added fix — run B / lens sweep / audit return only for a
  **major overhaul**.
- Both-mods-loaded is the rig's normal config (08-12).
- Status words: `tested-attended`/`tested-unattended`; bare `tested` = legacy, closed to new work,
  never bulk-upgraded (08-15). Screen claims need an attended witness.
- ⛔ SKIPs BY NAME, never a total.
- Display name Relaunched Fix Pack; `id` + `[CommunityFixPack]` log tag KEPT (08-17).
- Never name fredware's mod on a player surface; no player load-order advice (`EF-054`, FIX_POLICY §8).
- STATE.md format: most efficient and safest — one fact per line, byte caps do the read job (08-18, item 42).

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed
```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 77 registered (77 default-active, 0 optional-gated files)
- Code/*.lua files: 78
- TestKit probes: 98
- BUGS index rows: 103 F + 12 D + 53 C
```
Re-emit after any change; game pinned **1.0.7.396349** (`EF-014`).
