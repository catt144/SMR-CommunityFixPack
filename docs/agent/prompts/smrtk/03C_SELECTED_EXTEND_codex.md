# smrtk 03C — extend the Selected section to the object's own actions

Link 03C of `smrtk`, inserted **2026-09-14 by the owner's ruling on ck175 item 1**: *"item 1
ruled — extend before 08."* **Codex** (Sol — the seat that built P2, so the route is already in
hand). README rules 1–22 are yours. Runs after 03B (`reports/SMRTK_JUDGE.md`, PASS WITH FIXES)
and **before 07**, so the docs describe the surface that actually ships.

Authored against pack HEAD **`1281499`** / TestKit HEAD **`87f3130`**. ⚠️ Several interactive
peers share the pack checkout under one git identity — `git log --author` attributes nothing,
identify by sha + diff, and re-check `git status` immediately before every write. The pack repo
also has a **checklist archival** job in flight that rewrites `docs/PLAYTEST_CHECKLIST.md` with a
sha guard: ⛔ **you write nothing to that file** (see the scope fence).

## 0 · Orient

`git log --oneline -10` + `git pull` in **both** repos, `git status --short`, `ListAgents`.
Then `docs/agent/STATE.md` (mandatory). This brief goes stale the moment a peer commits — check
it against `git log` before trusting any specific below.

⛔ **No stale-probe gate and no launch.** This link builds and desk-checks only; **08 is the
first sitting for this surface**, exactly as it is for every other page. ⛔ Never move a status
you did not witness (rule 17): everything you produce is source-derived until 08 runs it.

## 1 · The job

03B found that the Selected section offers **22 of the 106 member names vanilla's section would
offer**, with **no fallback** — the toolkit deliberately never sets `config.BuildingInfopanelCheats`,
so the other 84 are simply gone. On a selected **Colonist** the section shows *Delete* (raw
`DoneObject`) plus Dump/Pin, while hiding `Colonist:CheatKill` — the blunt universal route is
exposed and the modelled specific one is not.

**Build 03B's recommended shape** (`SMRTK_JUDGE.md` D1, "Recommendation"):

1. **Keep the curated 22 as a labelled top group.** ⛔ Do not fold them into the generic path —
   they carry guards the generic path cannot: the busy-depot refusal
   (`73_SMRTK_Infopanel.lua:64-65`), the before/after depot reads, and the honest Delete caveat
   03B repaired at `87f3130`.
2. **Add a dynamically enumerated "More" group** for the remaining members, walking the
   metatable chain **exactly as `Lua/X/Infopanel.lua:24-36` does**, and dispatching through P2's
   existing untainted path (`obj[method](obj)` at `73_SMRTK_Infopanel.lua:72`) with a generic
   result record.
3. **`AsyncCheat*` is a category, not an afterthought.** It is absent from the toolkit entirely
   today. `SMRTK_UI_HOOKS.md:108` already records that async cheat methods avoid taint, so the
   category was known and dropped silently — include it, and say in your report how you dispatch
   it differently from the sync members if you do.

**Why this crosses no invariant, and the one line that would.** Vanilla's *enumeration* is not
the tainting part — `Lua/X/Infopanel.lua:49` is, because it calls `NetSyncEvent("ObjCheat", …)`.
P2 already replaces that line. Enumerating the chain and dispatching through the existing leaf
path adds no wrapper and no sync call. ⛔ **If you find yourself needing `NetSyncEvent`,
`NetSyncEvents.*`, `LogCheatUsed` or a vanilla wrapper to reach a member, that member does not
go in** — record it as a named skip instead (rule 6).

## 2 · Read path — these files, not their folders

`C:\Dev\SMR-BugFixPack-TestKit\Code\73_SMRTK_Infopanel.lua` (the whole file — it is yours to
extend) · `reports/SMRTK_JUDGE.md` **§D1 only** · `reports/SMRTK_UI_HOOKS.md` §1 (the section
route P2 built on) · `prompts/smrtk/README.md` rules 1–22 and § "What is FIXED" ·
`facts/EF-095.md` (leaf-call premise) and `facts/EF-098.md` (the 13 forbidden leaves) ·
game source `Lua/X/Infopanel.lua:22-51`, `_cobject.lua:1591-1593`, `Lua/Units/Colonist.lua:5144`,
`Lua/Drone.lua:2989`. More via `facts/INDEX.md` — ⛔ grep it, never read it whole.

## 3 · Derived facts (R-C) — every number is a CLAIM; re-derive before building

| fact | measured | at | re-check (scoped so it CAN fail) |
|---|---|---|---|
| 106 members: 94 `Cheat*` + 12 `AsyncCheat*` | 03B, walking object methods | build 24995074 | re-derive both counts against the **live** build; ⛔ report the delta rather than inheriting 106 |
| P2 covers 22 (16 names + `CheatUpgrade1..6`) | `73_SMRTK_Infopanel.lua:6-23` | TestKit `87f3130` | read the `leaves` table and count |
| vanilla enumerates dynamically, no list | `Lua/X/Infopanel.lua:22-40` | 1.1.0.403908 | read the walk; it offers every `Cheat`/`AsyncCheat` member |
| the taint is line :49, not the walk | `NetSyncEvent("ObjCheat", self, …)` | 1.1.0.403908 | `grep -n 'NetSyncEvent("' Lua/X/Infopanel.lua` |
| a Colonist matches exactly 1 of the 22 | `CObject:CheatDelete` is universal | TestKit `87f3130` | match the 22 against `Colonist`'s chain |

## 4 · Scope fence

**IN:** `73_SMRTK_Infopanel.lua` and, only if the enumeration genuinely needs it, shared helpers
in `70_SMRTK_Core.lua`. Your own report at `reports/SMRTK_03C_EXTEND.md`. The smrtk README's
queue row for this link.

**OUT:** ⛔ `docs/PLAYTEST_CHECKLIST.md` — an archival job rewrites that file under a sha guard
and you would abort it or be aborted. Owner items go in your report as `OWNER-ROUTED` lines and
**07 carries them**, exactly as the payloads did. ⛔ The other four pages. ⛔ Anything under the
pack's `Code/`, `items.lua` or `metadata.lua` (rule 11). ⛔ Re-running 02's kill gate — it passed
and is consumed.

**Found something interesting out of scope: FILE IT, do not fix it** (rule 3) — a bug entry, a
fact, or a line in your report's DRIFT section for 99.

## 5 · Gates — green before every commit (rule 15)

`python tools/parsecheck.py` on every `.lua` touched · rule 6's grep and rule 7's grep, **presence
side counted** (a zero from a truncated grep proves nothing) · `python tools/doccheck.py` GREEN in
the pack repo · the P2 smoke script (`reports/SMRTK_P2_SMOKE.py`) still PASS · rule 9: every write
to a real global sits inside a toggle's install with a matching uninstall, or it is a defect.

⚠️ **If your work adds a `SMRTest.Register(` call anywhere in the TestKit tree it moves the pack
repo's probe count**, which REDs `STATE BUILD STATE` for every session in the pack checkout. Cure,
in the same commit: `python tools/doccheck.py --regen`, then commit `docs/agent/STATE.md` by
pathspec. ⛔ `--no-verify` is never the answer. (Measured 09-13: the nine toolkit pages register
zero probes, so this binds you only if you add one.)

⛔ `Code/` edits only with `Mars.exe` closed — `tasklist` first, in a separate command (rule 16).

## 6 · Stop conditions — permission, not failure

Stop and report if: the 106/94/12 counts do not reproduce on the live build · a member cannot be
reached without a wrapper or a sync call **and** it looks important enough that skipping it
changes the answer to ck175 item 1 · the metatable walk cannot be done without patching a vanilla
function while idle (rule 9) · `73_SMRTK_Infopanel.lua` has moved under you · the P2 smoke breaks
and the cause is not obviously yours · doccheck is RED before you start.

## 7 · What may NOT be claimed

- ⛔ **Never claim the section now "replaces the cheat menu."** Claim the coverage you measured,
  as a ratio, with the named skips beside it. That phrasing is what ck175 item 1 was about.
- ⛔ **Never claim a member is untainted because it is in the "More" group.** It is untainted
  because you read its leaf body and it calls none of `EF-098`'s 13 and no wrapper (`EF-095`).
- ⛔ **Never claim anything works in play.** Nothing in this link launches the game; **08 is the
  first contact**. Source-derived is the honest word.
- ⛔ Never state an absence from a truncated grep. A claim that a member is *nowhere* needs the
  presence side counted.

## 8 · Close-out

1. Report at `reports/SMRTK_03C_EXTEND.md`: what you built, the **coverage ratio you measured**,
   the named skips and why each was skipped, DEPARTURES (with reasons — README § "What is FIXED"
   gives you licence to depart), SUGGESTIONS, DRIFT for 99, and `OWNER-ROUTED` lines for 07.
2. Append your outbox to **07's** `## Notes from upstream` and to **99's** (rule 2).
3. Strike this link's row in `prompts/smrtk/README.md`'s queue (strike it, as 01/02/03A/03B were —
   the queue is the chain's record).
4. ⛔ **`git rm` this file** in the same commit. This is a one-off; it does not re-run.
   ⚠️ **`prompts/README.md` carries ONE folder row for `smrtk/`, not a row per link** — verified
   against the PROMPT MAP gate 2026-09-14 (13 perma + 7 one-off rows, none of them a chain
   member). So do **not** touch that map for this file; it is the chain's row and it goes when the
   chain does. Update its "next is…" sentence to name **07** instead of 03C, since that sentence
   is what the next session reads. Re-run `python tools/doccheck.py` after — the gate checks the
   map against disk in both directions.
5. Commit by pathspec in each repo (`git commit -F <file> -- <paths>`), push the pack repo.
   ⛔ TestKit is local-only by design: commit there, never push.

## 9 · Required — a live progress list

Create a todo list covering the whole job before you start, **one item per commit-and-verify
unit** — not one checkbox over "build the thing". Mark each item the moment it completes, keep
exactly one in progress, and expand a stage in the list the moment it turns out to be four
things. **The owner reads this list to decide when to step in**, so a stale item is a wrong
answer to their question.

## Notes from upstream

**From 03B (`reports/SMRTK_JUDGE.md`, PASS WITH FIXES, 2026-09-13):** D1 is the reason this link
exists; its "Recommendation" paragraph is the shape to build. 03B applied one fix in the file you
are extending — the Selected Delete caveat now tells the truth about units (TestKit `87f3130`).
Everything else in P2 held: all 21 Selected actions were opened against the source and every one
calls a clean leaf.

**From the orchestrator (2026-09-14):** the owner ruled *extend before 08* on the cost basis that
this rides P2's already-proven route and therefore costs Codex time rather than owner time,
sparing a second attended sitting. ⚠️ **If that premise breaks — if the extension turns out to
need a route P2 has not already proven — stop and say so** rather than pressing on: the ruling's
condition is recorded in ck175 and it expires with that condition (rule 5a).
