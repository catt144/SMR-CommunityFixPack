# HOTFIX 2 — HANDOFF: build the fix prompts, audit them, get it patched

Paste into a fresh Claude Code session. Written **2026-09-08** by the session
that ran `PACK_1_1_0_REVERIFICATION.md` and `VANILLA_FIX_QA.md` (out of
context; nothing owed by it). **Start with `git log --oneline -10` +
`git pull` + `ListAgents`** (sibling sessions edit this tree). Read
`docs/agent/STATE.md` (mandatory), `agent/FIX_POLICY.md`, `agent/WORKFLOW.md`
"Authoring a prompt", `agent/reports/CHAIN_METHOD.md`.

> 🎯 **YOUR JOB, IN THREE ACTS.** (1) Turn the audited findings into a
> self-consuming chain of fix prompts that apply EVERYTHING we can take up.
> (2) Author the terminal audit prompt that a fresh context runs over the
> whole result. (3) Work with the owner through the boot log, the attended
> controls, the patch notes and the upload sitting until hotfix 2 is live.
> ⛔ You do not implement the fixes yourself in this session — you author the
> chain, then EXECUTE it link by link (a link may be you, in a fresh context,
> or a sub-session), then audit, then patch. Owner rule: *"The last thing I
> want is to release a half-baked patch and then have to immediately
> repatch it."* That sentence is the bar.

## 0 · Where things stand (read these, do not re-derive them)

- **The evidence, double-checked:** `agent/reports/PACK_1_1_0_REVERIFICATION.md`
  (all 80 modules against 1.1.0: 10 FIX / 35 REMOVE / 35 KEEP; §1a–§1d the
  buckets, §1h the rebreak pass, §4 the tooling design) and
  `agent/reports/VANILLA_FIX_QA.md` **§0** (three fresh readers over all 46
  REMOVE/FIX claims: 0 flips, 0 vanilla rebreaks, and FOUR amendments that
  are now binding — R-20 is a sixth applies-today harm, F-5 and F-1 owe save
  cleanups, R-36 is platform-conditional, R-17 is a plain REMOVE). ⛔ Read QA
  §0 before any row of the main report; it corrects the main report in
  places and the main report says so.
- **Owner items open:** checklist 114 (the six applies-today harms), 115 (the
  REMOVE block), 116 (tooling), 117 (non-Steam players ⇒ sanitizer),
  **98** (a 1.0.7 line or not — decides delete vs gate for the 35), 111
  (F116's orphan policy), 112/113 (store text). ⚠️ **98 and 117 change what
  the prompts write.** Ask for them FIRST, in one message, with a
  recommendation each (mine: 98 = no 1.0.7 line ⇒ deletions; 117 = keep the
  sanitizer's F35+F48 passes unless the owner says Steam-only).
- **The owner has told players a patch is coming and wants the best version,
  not the fastest.** Marathon, not sprint. Extensive play is NOT wanted; a
  handful of minutes-long attended controls is (§3).
- Tools that exist: `tools/sigcheck.py`, `tools/logscan.py`, `tools/luafn.py`
  (function extractor, added 09-08), `tools/doccheck.py --emit-counts`,
  `tools/harvest_wrap_targets.py`. Game source: the 1.1.0 tree at
  `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`; the 1.0.7
  tree is GONE (`EF-075`). Canonical boot log:
  `archive/logs/gated110_Mars.exe-20260908-17.51.09-6a91a190.log` (17
  inactive / 14 named — really 16, `SaintBlessing` heals at `:186`).

## 1 · What the chain must take up — all of it

Every item below has its evidence row named; the prompt you write for it
must RE-DERIVE the route from the 1.1.0 tree before editing (`CHAIN_METHOD`
lesson 3 — every route failure this project has had sat above correct
citations). The QA pinned shapes; a prompt that departs from them must say why.

**A · The six applies-today harms (ck114) — repair or remove, each with its control.**
| module | action | shape pinned by the QA | evidence |
|---|---|---|---|
| `SaintBlessing` (F-1) | FIX | behavioural probe in the `DataPatch` pass: call the real `AddDomeColonistsModifier` on a stub unit/dome, patch only if it captures `Religious`; **fail CLOSED** (nothing captured ⇒ decline); **plus a 1.1.0 save re-base** — vanilla's one-shot fixup already ran with our wrong value on any save loaded under the broken pack (`_fixup.lua:2143-2170`) and will not run again | report F-1; QA §0.3 |
| `StaleReservations` (F-2) | FIX or REMOVE (owner) | if kept: skip colonists with `expedition_residence` truthy; premise is now committed-shuttle limbo only, say so | report F-2; QA §0.4 |
| `ShelterReflex` (F-3) | FIX | delete half (a) (the `IsSuitable` replacement); keep half (b) | report F-3 |
| `FirstAsteroidPrefabs` (F-4) | REMOVE | file + `items.lua` (H-10); no cleanup owed | report F-4 |
| `AstrogeologistExtractors` (F-5) | REMOVE **+ one-shot save cleanup** | remove our two persisted `Effect_ModifyLabel` keys from `UIColony.label_modifiers`, keyed on `prop` + label as the module's own heal does (`:207-215`) | report F-5; QA §0.2 |
| `DisasterPredictionLeak` (R-20) | REMOVE | whole module; the sweep clears the game's legitimate notification-less `DisasterNormalRains` flag | report R-20; QA §0.1 |

**B · The two re-copies (ck115) — 1.1.0 bodies, our change re-applied.**
`RocketDroneChurn` (F-7: carry `not self.refuel_disabled`,
`CargoTransporterNew.lua:1442`); `PayloadTemplateRefill` (F-6: carry the
tutorial branch and the destination-pick semantics, stamp the flag on the
CONFIRMED path `CargoRequestNew.lua:376-379`, not on `Apply` entry). ⚠️ Each
re-copy header must carry the `SRC:`/`DEFECT:` manifest lines from §4 of the
report so the next update is a tool run.

**C · The three gated re-derivations — take them up as re-copies.**
`LandscapeUnitFilter` (F-8: repair the body on `(map, mark, callback, ...)`
reading `map.Landscapes[mark]`, pass `filter_embark`; KEEP the gate; reach is
now Clear-Waste-Rock only); `VacuumWalks` (F-9: re-copy the 1.1.0 body with
the one-line change, read `g_Consts` at call time, make the gate deliberate;
⛔ never a distance pre-wrapper); `TrainCargoDumping` (F-10: re-copy
`Train.lua:779-805` with `station:IsResourceEnabled(res)`, carry the BlackCube
hook `:800-802`; keep the gate for the NEXT change). ⚠️ These three revert
owner ruling ck109's "gate, not repair" for F-8 — ask; the owner said "take
up everything we can", which I read as yes, but it is their call.

**D · The REMOVE block (ck115) — 34 modules after A took two and R-36 left.**
R-1…R-19 and R-21…R-35 of the report, minus R-7 which is HALF a module (delete
`repair_unreachables` + `OnMsg.OnPassabilityChanged` in
`Fix_DroneTransportMinors.lua:139-160`, keep (a)). Delete vs gate per decision
98. Every deletion: `Code/` file + `items.lua` entry (H-10) + the bug entry's
status/observation (`agent/bugs/<id>.md` gets a dated 1.1.0 observation, never
a rewritten citation) + the site's fix-list entry + a patch-note line.
⛔ Do NOT "repair" the rename false negatives instead of removing (R-15
`DustSicknessDamage`, R-16 `IndependenceTerraforming`) — the QA explains why.

**E · `90_SaveSanitizer` (R-36, ck117)** — keep the F35 + F48 passes unless
the owner rules Steam-only; the F03 pass is dead either way (R-5).

**F · The KEEP set needs nothing** — except A-1 (`GeneForging` reads the
legacy `TechDef` map; prefer `Techs.GeneForging:ResolveValue("param1")`).

**G · Tooling (ck116) — lands in the same patch cycle, not after.**
`tools/bodycheck.py` + the `-- SRC:`/`-- DEFECT:` header manifest on every
surviving replacement and wrapper (report §4 item 2); a `probe` form in
`SMRFixPack.Require` (§4 item 1, F-1 is its first user); `sigcheck.py` over
`SetGlobal` sites (A-4); `logscan.py` heal-aware counts + benign latches listed
as retire candidates (A-2/A-3).

**H · Text.** ck112/113 store wording (already proposed, owner leaning yes);
`metadata.lua` `last_changes` for hotfix 2; `UPLOAD_WORKFLOW` §3 paste backups
synced (store-card backups are the real delivery path); the site fix list.

## 2 · The chain shape (house method)

Numbered prompts in `agent/prompts/hotfix2/`, each sized to one session, each
ending by appending its outbox to the NEXT prompt's inbox and to the terminal
audit prompt, committing, and deleting its own file in the same commit. A
suggested split — adjust after you have read the evidence:

1. `01_DECISIONS_AND_MANIFEST.md` — ask 98/117/C, write the `SRC:`/`DEFECT:`
   manifest spec and `bodycheck.py` (so every later link can run it).
2. `02_REMOVE_BLOCK.md` — D + E, one sweep, with `items.lua`, bug entries,
   patch-note lines; boot log expected: every removed module gone from the
   `[CommunityFixPack]` block, counts re-emitted.
3. `03_HARMS.md` — A (six modules), each with its probe/cleanup/re-base.
4. `04_RECOPIES.md` — B + C, each header carrying the manifest lines.
5. `05_TOOLS_AND_CORE.md` — G (probe form in `00_Core`, tool extensions).
6. `06_TEXT.md` — H.
7. `99_TERMINAL_AUDIT.md` — see §4.
Every link: `python tools/doccheck.py` GREEN, `sigcheck.py`, `bodycheck.py`,
a parse sweep of every touched `.lua`, commit `-F <file>`, push. ⛔ `Code/`
edits only with `Mars.exe` closed. ⛔ Never move a status you did not witness.

## 3 · What must be SEEN before upload (owner time, minutes each — batch them)

One 1.1.0 boot on the patched tree (menu-only is enough for counts), then on
the owner's existing `BlankBig_02` colony, in ONE sitting:
- a Saint in a dome with Religious colonists shows "Blessed by a Saint"
  (F-1, with the re-base on a save that loaded under the broken pack);
- an asteroid habitat with a trait filter: no throw (F-3);
- an Astrogeologist save after the cleanup: no +10% on the two extractors (F-5);
- the first train leaves its platform, a landscaping site progresses (owed
  since hotfix 1 — the gates are measured, the play is not);
- an expedition sent and returned past 5 sols keeps its home (F-2) — only if
  the module is kept.
Everything else stays a source verdict; say so in the notes. ⛔ Untick the
Test Kit's force leg first if armed. ⛔ Cheats are normal on the owner's
saves — a confound only where a reading intersects what they change.

## 4 · The terminal audit prompt (you author it; a FRESH context runs it)

It trusts nothing forward. It must: re-run `sigcheck`/`bodycheck`/`logscan`
on the final tree; re-derive every A/B/C change against the 1.1.0 body (the
QA's pinned shapes are its checklist); confirm every removed module is gone
from `items.lua` AND the boot log AND the fix list; confirm the two save
cleanups are keyed as the QA says; confirm nothing on the KEEP list was
touched; read the store text against `STORE_CARD_LIVE.md`; and end with the
one-line verdict SHIP / SHIP WITH CHANGES / DO NOT SHIP, plus the "what would
make this half-baked" list the QA format uses. ⛔ It moves no status; it names
what was not exercised in play.

## 5 · Bindings

`H-02` (no Mod Editor, no `version` edit, no upload — the sitting's),
`H-03`, `H-04`, `H-08`, `H-10` (every dropped module leaves `items.lua`).
Owner decisions go in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on
you", never only in agent docs. `STATE.md` is byte-capped (9209 of 9216 warn
right now — every addition needs an eviction in the same commit). Keep the
live todo list current — the owner reads it to decide when to step in. A WARN
from doccheck goes verbatim into your summary.

## 6 · Not done, so nobody assumes it

Nothing was played on the patched tree (it does not exist yet). The 1.0.7
line question (98) is open. The three C re-copies and F-2's fate are owner
calls. F116's two divergences (ck111) are untouched. No fix prompt has been
written — that is where you start.
