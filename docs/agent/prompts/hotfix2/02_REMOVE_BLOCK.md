# 02 · The deletion sweep — every module that leaves, in one pass

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). Runs after 01.
**You are the only prompt in this chain permitted to touch `items.lua` or
`metadata.lua`'s `code` list.** That is deliberate — see §1.

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents`. Staleness anchor: link 01's
close-out commit. Todo list before you touch anything: one item per
commit-and-verify unit, and this job has several.

**Read path:** `agent/STATE.md` · `VANILLA_FIX_QA.md` §0 (**before** any report
row — it corrects the report in four places) · `PACK_1_1_0_REVERIFICATION.md`
§1b (the rows) and §1h (the rebreak pass) · `docs/PLAYTEST_CHECKLIST.md` items
98, 115, 117, 118 · `agent/FIX_POLICY.md` · your inbox below.

## ⛔ 1 · BLOCKED until two decisions are ruled

**Do not start without both.** They are in the checklist under "Decisions
waiting on you"; if either is still open, say so and STOP.

- **ck98 — is there a 1.0.7 line?** Decides **delete vs gate** for every row
  below. No 1.0.7 line ⇒ delete the file and its `items.lua` entry. A 1.0.7 line
  ⇒ each module STAYS and gains a 1.1.0 self-check that declines, and this
  becomes a very different, much larger job. ⚠️ ck118 is relevant context, not an
  answer: 1.0.7 players are served a frozen v5 download, which is an argument
  for deleting, but the owner rules it, not you.
- **ck117 — do non-Steam players matter?** Decides `90_SaveSanitizer` (R-36)
  alone. Keep ⇒ its F35 and F48 passes stay and only its dead F03 pass goes
  (R-5). Remove ⇒ the whole module goes with the rest.

## 2 · Why one prompt owns this

`H-10` normally protects against a module missing from `items.lua` shipping
absent. **On this patch it inverts**: 36 modules are leaving, and the failure
mode is a file deleted from `Code/` but left in `items.lua`, or the reverse.
Both portals force a `SaveDef` on upload that rebuilds `metadata.lua`'s `code`
list **solely from `items.lua`** (`Mod.lua:816-840`, `:973`), so an inconsistency
here is not a lint error — it decides what ships.

⇒ Get `Code/`, `items.lua` and the `code` list into ONE consistent state, and
prove it with `python tools/doccheck.py --emit-counts` before you commit.

## 3 · The list — 36 full deletions plus one half-module edit

Every row's evidence is `PACK_1_1_0_REVERIFICATION.md` §1b (and §1h for the
rebreak read). ⛔ **Re-derive the route before deleting**: open the 1.1.0 body
and confirm the defect really is gone. A verdict you inherit is a verdict you
cannot defend to link 99.

**From the REMOVE block (ck115) — R-1…R-19, R-21…R-35, minus R-7:**

`LowStorageWarning` · `LanderCargoRatchet` · `TouristSatisfaction` ·
`AutomationLawCompensation` · `UpgradeModifierLeak` · `SmallLandscapeSites` ·
`DroneUnreachableForever` · `MeteorFrequency` · `MeteorStormWedge` ·
`AsteroidLanderAvailable` · `GridGlobalStorage` · `LastTransmissionStorage` ·
`RainsDeadlock` · `DustSicknessDamage` · `IndependenceTerraforming` ·
`UniversityOvertraining` · `CaveInsNoDisasters` · `CommandCenterNumbers` ·
`DustDevilSpawnGate` · `DustDevilsDescrMap` · `DustStormUndergroundBreaks` ·
`ExtractorStaffedPerformance` · `LanderReturnFuel` · `LandscapeCostRefresh` ·
`LocalizedUIText` · `MilestoneCrash` · `MoraleComfortTooltip` ·
`SpaceYDroneCapBullet` · `StorageRateModifiers` · `TechDescriptionBuilding` ·
`TouristApplicants` · `TrainMinors` · `TrainPlatformWedge`  **(33)**

**Plus the three applies-today harms whose disposition is REMOVE:**

- `FirstAsteroidPrefabs` (F-4) — no cleanup owed. Note for the patch notes:
  prefabs already granted on 1.1.0 saves cannot be taken back, and the
  `SMRFixPack_FirstAsteroidPrefabs` GameVar is absent-tolerant.
- `AstrogeologistExtractors` (F-5) — ⛔ **owes a save cleanup**, §4.
- `DisasterPredictionLeak` (R-20) — the sixth harm, promoted by the QA (§0.1).
  Whole module; nothing to keep. Its `NewDay` sweep clears the game's own
  notification-less `DisasterNormalRains` flag, so a dust storm or cold wave can
  start on top of an incoming rain warning.

**Plus the half-module (R-7), which is an EDIT, not a deletion:**
`Fix_DroneTransportMinors.lua` — delete `repair_unreachables` and
`OnMsg.OnPassabilityChanged` (`:139-160`). ⛔ **Keep half (a)** — it is K-8 on
the KEEP list and still correct. The file stays in `items.lua`.

**Conditional on ck117:** `90_SaveSanitizer` (R-36).

⛔ **Do NOT "repair" the two rename false negatives instead of removing them**
(`DustSicknessDamage` R-15, `IndependenceTerraforming` R-16). The QA explains
why; reopening that is out of fence.

## 4 · The save cleanup F-5 owes (QA §0.2)

Our two `Effect_ModifyLabel` entries live in the **persisted**
`UIColony.label_modifiers`. Deleting the module leaves +10% `production_per_day1`
on AutomaticMetalsExtractors and +10% `water_production` on
MicroGAutoWaterExtractors in every 1.1.0 save that ran under the pack, with
nothing left to clean them.

Key the one-shot cleanup on **`prop` + label**, exactly as the module's own heal
already does (`Fix_AstrogeologistExtractors.lua:207-215`) — read that code before
writing the replacement, and put the cleanup where it survives the module's
deletion (`90_SaveSanitizer` is the home for exactly this class, which is a
second reason ck117's answer matters to you).

⚠️ Vanilla's own key shape on 1.1.0 was NOT checked by the QA reader
(`GetLabelModifierId(parent)`, their "not opened" list) — verify ours cannot
collide with vanilla's before you delete by key.

**Control this owes the owner (~3 min, batch it with 03's):** load an
Astrogeologist save that ran under the pack and confirm the two extractors no
longer carry the +10% — `AutomaticMetalsExtractor` (`production_per_day1`) and
`MicroGAutoWaterExtractor` (`water_production`). ⛔ Route it to
`docs/PLAYTEST_CHECKLIST.md`; a cleanup nobody watched run is a claim, and this
one silently edits a persisted save field.

## 5 · Per-module close-out — all five, every time

1. `Code/Fix_<Name>.lua` deleted.
2. Its `items.lua` entry deleted (`H-10`).
3. The bug entry `agent/bugs/<ID>.md` gains a **dated 1.1.0 observation** —
   ⛔ never a rewritten citation, never a deleted one. The 1.0.7 record stays
   true; you are adding what 1.1.0 changed.
4. The site's fix-list entry (repo `SMR-CommunityMods`, `content/fix-list.md`).
   ⚠️ Committing there does not publish — `publish-site.yml` is
   `workflow_dispatch` only.
5. A patch-note line, drafted for link 06. ⛔ You do not edit `metadata.lua`'s
   `last_changes` — 06 owns it.

## 6 · Consequences to hand forward, not swallow

- `ExtractorStaffedPerformance` (F108) and `LandscapeCostRefresh` (F107) are
  **named on live store surfaces and the site**. Removing them makes those
  claims stale. Route to link 06 with the exact wording that needs to change.
- `TrainMinors` removal leaves **two displays stale** (QA §0.8, R-34) — a
  patch-note item, not a silent drop.
- `LowStorageWarning` (R-1): 1.1.0 **deleted** the Food/maintenance warning
  branches rather than fixing them, so a 1.1.0 player simply gets no low-Food
  warning. That is a feature request if the owner wants it back, not a fix —
  route it to the checklist, do not build it.
- Four rows are marginally WORSE than vanilla today (`SmallLandscapeSites`,
  `TouristApplicants`, `SpaceYDroneCapBullet`, `DustStormUndergroundBreaks`).
  Worth one sentence in your outbox: their removal is a small improvement, not
  neutral.

## 7 · Scope fence

**In:** the deletions above, `items.lua`, the R-7 edit, the F-5 save cleanup,
bug-entry observations, site fix-list entries, drafted patch-note lines.
**Out:** `00_Core.lua`; every FIX-set module (03 and 04 own those); the KEEP set;
`metadata.lua` `last_changes` and any store text; `version` (⛔ `H-02`).
Found something out of fence? **File it, do not fix it.**

## 8 · Stop conditions

- ck98 or ck117 unruled ⇒ STOP, say which.
- A row's defect is NOT actually gone when you re-derive it ⇒ **STOP AND ASK.**
  That is a flipped verdict and it is the owner's call, not a judgement you make
  mid-sweep. The QA flipped none in 46 rows, so a flip is a real finding —
  capture it as drift evidence for 99 either way.
- The F-5 cleanup key could collide with vanilla's ⇒ stop and report.
- `doccheck --emit-counts` disagrees with your expected module count ⇒ stop.
  Do not "fix" the count by editing a doc.

## 9 · What may NOT be claimed

- ⛔ Not "the removed fixes were never needed". They were correct on 1.0.7. What
  is true is that 1.1.0 fixes them itself.
- ⛔ Not "removal is verified safe". You verified it in source. Nothing has run.
- ⛔ Not "no player is affected" — a 1.0.7 player who updates loses these
  (ck118). Say it plainly.
- ⛔ No status moves on evidence you did not witness.

## 10 · Close-out

Green gates (README rule 9) plus `doccheck --emit-counts` re-emitted into
`STATE.md`'s build-state block. Expected boot-log consequence, for 99 to check:
every removed module **gone** from the `[CommunityFixPack]` block — not
`inactive`, absent.

Append your outbox to `03`, `04`, `06` and `99`. Strike your README row,
`git rm` this file, commit together, push.

## Notes from upstream

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08.)*

- ⚠️ From `smr-bugfixpack-cd`, which built `sigcheck.py`/`logscan.py` and wrote
  the re-verification brief: **36 of 80 modules leaving is 44% of the pack, and
  the 08-20 ruling scoped the full release gate's return to "a major overhaul".**
  Hotfix 1 correctly priced itself as maintenance (4 files, +78/-2); do not
  inherit that costing by analogy. This is filed for the owner as part of ck118's
  block — if you conclude it is still maintenance, **say so with reasoning
  rather than by omission**.
- `tools/logscan.py --build <id>` is the safe way to read a boot log; a
  hand-rolled grep undercounted throws 30 vs 157 on 2026-09-08 because the engine
  writes the `[LUA ERROR]` header in two forms. A log copied while `Mars.exe` is
  running is a PARTIAL log and has already cost this project two wrong counts.
- PT-20 uninstall safety was verified on **1.0.7 only**, never on 1.1.0. Removing
  modules that wrote into saves is exactly the class that test covered.

### From link 01 — core, tooling and the manifest

⚠️ **For you specifically:** every module you delete is one I did NOT stamp (items 6, 8) — the 35 KEEP rows carry a manifest, the REMOVE rows do not, so `bodycheck.py` going from 46 `NO-MANIFEST` down toward 10 is a free cross-check that you deleted the right set. Run it before and after.

*(From link 01, `smr-bugfixpack-25`, 2026-09-08. Commits `6d452a3` probe form ·
`401f8a0` bodycheck.py · `6db7457` FIX_POLICY §2a/§2b · `e2490f3` KEEP set
stamped. ⛔ Nothing was run in a game; no status moved.)*

**1 · The `probe` form — exact signature and semantics** (`00_Core.lua`,
`SMRFixPack.Require`). `{ probe = function() … end, reason = "…" }`, a sibling of
`test`:

* The probe takes **no arguments** and runs under `pcall`.
* **ONLY the literal boolean `true` applies.** A throw, `nil`, `false`, or any
  other value (a captured table included) **declines**. "Captured nothing" is
  UNKNOWN and UNKNOWN is not permission.
* A throw is a DECLINE, never propagated. It is logged as
  `<id>: behaviour probe declined (threw: …)` so an authoring error in the probe
  cannot hide inside a silent decline.
* A probe failure returns `c.reason`, exactly like every other form, and does
  **NOT** set `update_suspect` — it is a behaviour verdict, not patch rot, and on
  the other branch a decline is the CORRECT outcome.
* Write the **stub contract beside it**: a comment naming what the stub must
  provide and why the target is safe to call on one. ⛔ Only for targets you can
  show, from the shipped 1.1.0 body, to be **synchronous and side-effect-free on
  a stub**. If you cannot show both, the module gets no probe and keeps its
  existing check — that is a permitted outcome, not a failure.
* Two shared lines were touched and both are identity for every existing form:
  `local ok, name` → `local ok, name, why`, and the return → `c.reason or why or
  (name .. " not found …")`. No existing reason string was reworded.
* `Require` is a plain function, so a `DataPatch` module may call it from inside
  its pass, after `DataLoaded`, for a preset-bound probe.

**2 · The branch guard, and it is not negotiable** (`FIX_POLICY §2a` — link 04,
this is Job D's answer verbatim). ⛔ **Do not build a game-version detector.** It
would be a LABEL check, against the rule that made the F115 gate correct; and it
is unbuildable anyway, because `lua_revision`, `ModMinLuaRevision` and
`ModRequiredLuaRevision` are ALL 350453 on both branches (`EF-077`) — which is
precisely why nothing warns a 1.0.7 player. There is no field to read. ✅ **The
per-module `probe` IS the branch guard**: a probe confirming the 1.1.0 body shape
a module was written for necessarily declines on a 1.0.7 body, per module, with
no version arithmetic anywhere and nothing global to keep in sync.

**3 · The manifest grammar** (`FIX_POLICY §2b` has the authoring rule;
`tools/bodycheck.py`'s docstring has the machine half). Header-block comments:

```lua
-- SRC: <path> <selector> sha256=<64 hex>      -- or:  -- SRC: none <reason>
-- DEFECT: <python regex>                      -- or:  -- DEFECT@<path>: <regex>
```

* `<path>` slash-separated, relative to `ModTools/Src` (`\` accepted).
* `<selector>`, no spaces: `Class:Method` (separator is a hint — both declaration
  forms and `Class.Method = function(` match), a bare `Name` for a global or
  `local function`, or `L<first>-<last>` for a literal span where there is no
  function to name.
* Body = declaration line → first bare `end` at the same indentation. The
  delimiter is `luafn.py:find_bodies`, **imported** by `bodycheck.py`, so there is
  never a second extractor. Line endings normalised, trailing whitespace stripped
  per line; indentation and comments kept; sha256 of the utf-8.
* `-- DEFECT:` searches the body of the `SRC:` above it. `-- DEFECT@<path>:`
  searches that whole file — the **DataPatch shape**: no body to hash, so declare
  `SRC: none` and state the defect against the shipped DATA.
* Several `SRC:` lines per module are fine; each `DEFECT:` binds to the nearest
  above it. Regexes are Python `re`, ONE line, **not** `re.MULTILINE` (`^`/`$`
  will not do what you want — use `\s+` to cross a line break). Shipped Lua
  indents with **tabs**: write `\s+`, never a literal space.
* ⛔ **State the DEFECT, never the PHRASING.** See item 5.
* ⛔ Never hand-type a hash: `python tools/bodycheck.py --pin <path> <selector>`
  emits the line and the range it hashed.

**4 · `tools/bodycheck.py` — CLI and what its falsifier proved.**

```
python tools/bodycheck.py                 # the pack against the live 1.1.0 tree
python tools/bodycheck.py --src <path>    # another ModTools/Src
python tools/bodycheck.py --code <path>   # another Code/ tree
python tools/bodycheck.py --all           # also print OK / NO-MANIFEST rows
python tools/bodycheck.py --module NAME   # one module
python tools/bodycheck.py --pin <path> <selector>
python tools/bodycheck.py --selftest      # ⛔ the falsifier
```

Exit 1 on `BODY-CHANGED`, `DEFECT-GONE`, `TARGET-ABSENT`, `TARGET-MULTI`,
`MALFORMED`; counts only for `NO-MANIFEST`, `NO-DEFECT`, `SRC-NONE`, `OK`.
⚠️ Deviation from the prompt, stated: `TARGET-ABSENT`, `TARGET-MULTI` and
`MALFORMED` also exit non-zero, not just the two named. A stamped module whose
target vanished, resolves ambiguously, or whose manifest does not parse cannot be
re-verified, and a manifest that merely *looks* like coverage is worse than none.

`--selftest` asserts ten legs, permanently, because a tool that returns GREEN on
everything is indistinguishable from a broken one. **Two legs are real game-side
events**: `DEFECT-GONE` fires on one of the actual 32 (`MinDaysFoodSupply
BeforeNotification` is gone from the whole 1.1.0 tree while
`ResourceTracking:GatheredResourcesOnHourlyUpdate` still exists with our arity —
invisible to `Require` and to `sigcheck`), and `TARGET-ABSENT` fires on
`Colonist:UpdateSatisfaction`, which 1.1.0 deleted. `BODY-CHANGED` fires on a
**real body edit** — F116's in-body repair at `add94b3`, pinning the pre-repair
body against the repaired tree — plus a hash negative control and the converse
leg, so it cannot pass by being always red.
⛔ **ONE HONEST LIMIT, in the file itself:** the 1.0.7 tree is GONE from disk
(`EF-075`), so no true 1.0.7-vs-1.1.0 **game** body pair exists to hash. The
mechanism is proven on a pack-side edit and a negative control, not on a
game-side branch pair.

**5 · The finding that will bite you if you skip it.** Writing the tool's OK
control walked straight into the trap. F46's 1.0.7 phrasing was
`station.demand[res]:GetTargetAmount()`; 1.1.0 hoisted it to
`local demand = station.demand and station.demand[res]` / `demand:GetTargetAmount()`
(`Train.lua:794-795`) — a pure **refactor**, defect untouched. A `DEFECT:` pinned
to phrasing therefore reports `DEFECT-GONE` for a bug that is still shipped: a
FALSE "vanilla fixed it", the direction that **retires a live fix** (R-15's
shape). The right expression states the fault — `Min\(carried,\s*station_cap\)`,
the unload computed from the cap alone. Locked in as fixture `Fix_Selftest
RefactorTrap`. ⚠️ **A `DEFECT-GONE` is a REMOVE candidate, never a verdict.**

**6 · What is stamped, and what "verified" means here.** All 35 KEEP rows (§1d),
76 manifest rows, 73 `OK` / 1 `NO-DEFECT` / 2 `SRC-NONE`, exit 0. ⛔ The FIX and
REMOVE sets are deliberately **unstamped** — 46 `NO-MANIFEST`, which is a count,
not a failure, until the pack is whole. Every hash was taken from the live tree,
so "the hash matches" is true by construction and proves nothing; its value is
future. What IS evidence: each target was resolved in the shipped tree and its
DEFECT expression written against the 1.1.0 body and confirmed to match there.
Three targets had moved far enough that the module's own 1.0.7 header no longer
describes them (`GetRareTraitChance` is now 5 lines through
`Techs.GeneSelection:ResolveValue`; `TunnelBase:AddPFTunnel` guards
`self.linked_obj`; `AlienDigger:GameInit` sits at `:87-96`).
⛔ **NOT a claim that the KEEP set is verified** — I pinned bodies the
re-verification read and re-read only what a defect expression needed. No KEEP
verdict was re-derived; K-9 and K-10 stay "on record, not re-read".

**7 · The named exceptions — a defect that is an ABSENCE cannot be stated
directly**, because a regex matches what is present:

| module | why | what was pinned instead |
|---|---|---|
| `Fix_SinkholeIndestructible` | missing `indestructible` / `disasters_strike_immunity` on a generated class table | the whole classdef by span (`L4-25`), so vanilla ADDING the flag reads as `BODY-CHANGED`. The one `NO-DEFECT` row |
| `Fix_BrokenTrackSalvage` (1st target) | `node_idx` missing from the parameters copied onto the repair site | the consequence, against the sort that raises (`a.node_idx < b.node_idx`) |
| `Fix_GeneForging` | `GeneForging` is unknown to `GetRareTraitChance` | the half that IS present. `DEFECT-GONE` will not fire if vanilla adds the tech alongside `GeneSelection` |
| `Fix_FreedHousingNotice` | `RemoveResident` wakes nobody | its tail (`ResetFreeSpace` as the last act), so adding the wake call stops the match |

**8 · Filed, not fixed (out of my fence).**
* **→ link 05:** `bodycheck.py --selftest` is NOT wired into `doccheck.py`; it is
  a manual gate today. Wiring it (alongside `harvest --check`) is the tools-tail
  fence, not mine.
* **→ link 06:** the inherited `metadata.lua` comment claiming "`PackVersion`
  renders version_major.version_minor.version" describes nothing that exists in
  the 1.1.0 tree (zero grep hits). Passed on from link 01's own inbox, still
  unfixed.
* `sigcheck.py` rated `Fix_TrackSalvageWipe` OK both before and after F116's
  defect was found. `bodycheck.py` is the instrument that closes that, and F116
  is now one of its falsifier legs — but only pack-side (see item 4's limit).

**9 · Drift caught in my own work (chain rule 5 — evidence, not shame).**
* The first block-balance checker counted a `for … ipairs({` whose `do` sits on a
  later line as **two** openers and flagged `Fix_RocketInteractGuard`, which is
  byte-identical at HEAD. Caught by checking HEAD before believing it. Fixed to
  pair each loop head with its own `do`, re-falsified against a deliberately
  broken copy; all 81 `Code/*.lua` balance 0. ⚠️ There is no Lua binary on this
  rig — block balance is the whole desk syntax check, so a wrong checker is a
  wrong gate.
* My first `EXPECT` sets in `--selftest` were wrong twice (a stamped fixture
  yields a row per manifest LINE, not one per module). The tool was right both
  times; I corrected the assertions, not the tool.
* Stamping wrote the 35 files LF where the working tree is CRLF. Content in git
  is unaffected (`git diff` = 35 files, 353 insertions, 0 deletions), but the
  repair pass converted **39 files I had not touched**; they had zero content
  diff and were restored with `git checkout --`. ⚠️ If you see EOL-only churn in
  `Code/`, that is where it came from, and it is not in any commit.

⛔ **What may NOT be claimed from this link.** Not "the pack is update-proof" —
class (c), semantics moving under a wrapper, is still seen by **nothing**. Not
"the KEEP set is verified". Not "probes are safe" in general. No status moved: a
tool run is not a test.
