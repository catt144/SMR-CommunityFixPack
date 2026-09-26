# Load order: the pack puts itself first (option B) — build and audit, 2026-09-25

## Must_Read_Header

Report for the owner, repair seat and audit seat, executing the now-consumed one-off
`docs/agent/prompts/LOAD_ORDER_FIRST_high.md` (retrievable at `4e4c97b`).
The build is on the short-lived code branch **`load-first`**, repaired at **`8ea5449`**, not merged.
Records are on `main`. Nothing here was uploaded, and no attended sitting ran. Every "the pack
loads first" claim below is desk- and unattended-verified on this one rig; the retail sitting
in §5 is planned for the owner's approval, not run. A save request is not a disk write; the
seven boot logs are the disk evidence. Where a line says MEASURED it names its command or log.

**Latest audit verdict: CHANGES on `8ea5449`, records `4e704c1`.** The re-audit in §13
accepts R1–R4 and R6 within their stated limits. R5 still needs a positive sync-completion
witness and a restoration sequence that survives the final option click. The branch remains
unmerged and the sitting held. Sections 0–12 retain the build, first audit and repair history;
§13 supersedes their current clearance claims. The retained FIXED list and owner authority
remain in §11.

## 0 · Read this first — what the owner sees that the brief did not say

1. **The pack is back on the Mod Options page**, with one toggle, *"Load this pack first"*
   (default on). That is the player opt-out the brief fixes. It reverses the 2026-08-12 shape
   ("this pack has nothing for a player to set", `metadata.lua`, `items.lua`); the condition
   that ruling was made under no longer holds and the record stays in both files. DEPARTURE D2.
2. **The notice offers "Restart now" / "Later"** on PC, using the game's own restart routine
   (`ModsRestartApp`, the one behind the Mod Manager's Restart button). "Later" leaves the
   change for the next start. Elsewhere it is a plain OK box. DEPARTURE D3.
3. **The canary cannot log a line**: `metadata.lua` runs in an environment holding only
   `PlaceObj` and `box` (`Mod.lua:1715-1724`). Its check is the package and the writeback; the
   log search is a null control. Prediction per portal in §6. DEPARTURE D4.
4. **Your own mod order was changed and put back** by the unattended launches (§4, L1→L7). It
   reads today exactly as before (`L7`, fresh boot on `main`). Two lines of residue remain in
   `account.dat`: the pack's persistent-slot record (`SMRFixPack.LoadFirst v1 promotions=2 …`)
   and the TestKit's (`loadfirst-set …`). Both are inert data in per-mod slots. **When
   `load-first` merges, your next launch will promote the pack (it is third) and show the
   notice once.**
5. **A defect was found and fixed during the build**: the first LoadAllMods detector misread any
   saved list that happened to sort ascending (two mods do that half the time) and would have
   left real players unpromoted. It is replaced by an exact, net-zero probe (§2 case 3, D1).
6. **Your 23:08 play session ran on the branch and promoted your order.** The repair seat had
   `load-first` checked out on the junction when you started the game (log
   `Mars.exe-20260925-23.08.46`): the pack moved itself from third to first, you saw the
   restart box and chose Later. That was the rails' failure, not the module's: the module did
   what it says. Your order was put back afterwards (§12, L10/L11) and reads as before from a
   fresh boot on `main`. Until the branch merges, your next launch changes nothing.

## 1 · What was built (branch `load-first`, `8e2325a`)

| file | change |
|---|---|
| `Code/01_LoadFirst.lua` (new) | Registered as `LoadFirst`, `optional = true`. At code load: read the saved enable list through `GetModsEnabledByUser()`; if this pack is not at index 1, rebuild it through `TurnModOff(id)` for every entry, `TurnModOn(this pack)`, then `TurnModOn(each other id)` in the old order (`CommonLua/UI/ModManager.lua:35-41`, the Mod Manager's own helpers); verify the read-back; request the account save through a changed `WriteModPersistentData` (`Mod.lua:1487-1503`, the one public route: `AccountStorage` and `SaveAccountStorage` are blacklisted, EF-096); tell the player at the pregame menu. Already first: no write, no request, no notice. |
| `metadata.lua` | `Code/01_LoadFirst.lua` second in the code list; `default_options { LoadFirst = true }`; the C canary (§6). |
| `items.lua` | `ModItemOptionToggle` `LoadFirst` and the `01_LoadFirst` code item. |
| `tools/desk_load_first.py` | The desk harness (§2). |
| `tools/arming/legs/load-first-{read,set}.json`, `tools/arming/payloads/98_LoadFirst{Read,Set}.lua.txt` | The unattended legs (§4). Kit payloads, never in the pack. |
| `tools/README.md` | The generated tool row. |

**Engine facts the module rests on, each re-read on the archived 1.1.1.405907 tree this
session (SOURCE):** the saved list is the loading queue's seed (`Mod.lua:1995-2000`,
`:1873-1993`); enabling appends (`ModManager.lua:35-37`); the manager writes through on each
toggle (`ModUI_Entry:SetEnabledAndSync`, `:1532-1551`) and saves on close when the list
differs (`ModsUIDialogEnd`, `:123-166`); an order-only change never triggers the hot reload
(`Mod.lua:2104-2112` compares sorted sets); the persistent-data writer saves only on a changed
value (`:1499`); `WaitQuestion`/`WaitMessage` return `"ok"`/`"cancel"` (`StdDialogs.lua:619-646`);
`ModsRestartApp` relaunches then quits, and quit flushes a pending account save
(`ModManager.lua:96-121`, `AccountStorage.lua:168-190`); `PreGameMenuOpen` is never posted in
this title, so the notice polls `GetPreGameMainMenu()` as `00_Core.lua`'s update report does;
`LoadAllMods` (`Mod.lua:1997`) has no setter anywhere in the shipped Lua for the account flag.

**Player control.** Options → Mod Options → Relaunched Fix Pack → *Load this pack first*.
Off: the saved order is left alone from then on. On again: the pack promotes at once and
shows the notice. Modders and the console keep `SMRFixPack_Disabled["LoadFirst"] = true`.

**Notice text (verbatim, `Untranslated`):**
> The Relaunched Fix Pack has moved itself to the front of your mod load order, so its repairs
> are applied before other mods change the same parts of the game. Your other mods keep their
> order.
>
> This takes effect the next time the game starts.
>
> To keep your own order instead, turn off "Load this pack first" under Options > Mod Options >
> Relaunched Fix Pack.

Buttons on PC: **Restart now** / **Later**. If the game's restart routine returns an error, a
second box says so and asks the player to restart by hand.

**Log lines, one per outcome** (`[CommunityFixPack] LoadFirst: …`): `moved to the front of the
saved mod order via startup (was N of M): <before> -> <after>; applies at the next game start` ·
`already first of M (<list>); nothing written` · `not applied — <reason>; the saved order is
untouched` · `turned off in Mod Options` (via `inactive`). `SMRFixPack.ListFixes()` shows the
same as the `LoadFirst` row's detail.

## 2 · "Must hold" — each case, its control, its result

Desk: `python tools/desk_load_first.py` on the branch, **50 of 50 demands held**; the control
`--no-promotion` (the pack loaded without `01_LoadFirst.lua`) **fails 33 of 50 demands across
all 17 cases, none vacuous** — every case has at least one demand that fails without the
promotion (the "no write" halves hold either way; each case's status demand is its control).
The harness loads the pack's files **under the shipped sandbox metatable over the shipped
blacklist**, the shipped helpers, the shipped queue and the shipped persistent-data writer
(archived 1.1.1.405907, spans and hashes on its first lines). Transcript:
[`measurements.txt`](../../archive/load_order_first_2026-09-25/measurements.txt). Retail: the
launch logs of §4.

| # | case | desk demands (held) | control without promotion | retail (log) |
|---|---|---|---|---|
| 1 | Promotion, middle and last | `B,PACK,C → PACK,B,C`; `A,B,PACK → PACK,A,B`; next queue matches; running `ModsLoaded` untouched; exactly one save request, delay 1000; one question with Restart now / Later; Later restarts nothing, Restart now calls the routine once; a Lua reload writes nothing more and shows nothing more | list unchanged, no request, no `LoadFirst` row, no question | L1: `was 3 of 5`, running order untouched; L4: `was 6 of 6` |
| 2 | Already first | list unchanged, no request, row `active` "first of 3 …", no notice, slot untouched | row absent | L2, L3, L5, L6: `already first … nothing written` |
| 3 | LoadAllMods, both flags | raw list byte-identical, no request, row `inactive` naming LoadAllMods, a `not applied` log line | row absent | not reachable in retail (no setter in the shipped Lua; `config.LoadAllMods` is a developer switch) |
| 4 | Opt-out | option off: untouched, no request, `inactive` "turned off in Mod Options"; toggled on: promotes at once, one request, notice; toggled off again: `inactive`, order left as promoted, no new request; veto: `disabled`, untouched | row absent | sitting S3 (clicks) |
| 5 | Own persistent slot | our line first with `promotions=1 from=2 of=3`; two foreign lines kept verbatim; a second promotion writes `promotions=2` and keeps them; already first never rewrites a foreign slot | our line absent | L1 then L4 wrote the record (`promotions=2` now in `account.dat`) |
| 6 | Dependencies | own prerequisite A: saved `PACK,B,A`, queue `A,PACK,B` (A hoisted, PACK before B); Z requiring the pack: saved `PACK,Z,B`, queue `PACK,Z,B` | list unchanged | none installed declares one (cross-check inventory) |
| 7 | Passage Network | PN before pack: `VacuumWalks` `inactive` (declared shape declines), `HubLocalAccess` not active; saved `PN,PACK → PACK,PN`; loading in that order both `active`, pack writes nothing | queue stays `PN,PACK`; the next launch's guards decline | **L4: both inactive** (`the shipped emigration code has no work-slot reservation…`, `Dome not found`), pack promoted 6→1; **L5: both `active`**, nothing written |
| audit 2 | list shapes | pack absent: untouched, `inactive` "not in the saved mod list"; `B,PACK,B,GHOST → PACK,B,GHOST` (duplicate collapsed to its first position, stale id kept), one request; five mods pack third → others keep `A,B,C,D` | row absent | L1 (5 mods, third), L4 (6 mods, last) |
| canary | `metadata.lua` | loads under the metadata env and returns a `ModDef`; declared property set = pre-canary set + `default_options`; the literal is in the file and leaks no global; the code list starts `00_Core, 01_LoadFirst` | independent of the module (reported apart) | preflight 26 checked, 0 FAIL on the branch tree; `pack_predict` 48 files |

**Case 3, how the branch is told apart (D1).** `config.LoadAllMods` is read directly. The
account flag cannot be read, and its result can be identical to a normal list (every installed
mod enabled, in ascending id order). So, only when a rebuild is about to happen anyway, the
module appends a probe id with `TurnModOn`, reads the copy, and removes it with `TurnModOff`:
the normal branch shows the probe, the sorted-keys branch cannot. No helper yields between the
two calls; the list is byte-identical afterwards (desk demand 3b, `AccountStorage.LoadMods`
compared raw) and nothing is requested. Read strictly, that is a transient in-memory mutation
with zero net change; the audit judges whether "no write" admits it. The heuristic it replaced
misread `SMR_CommunityFixPack, iooW34Y` (this rig with Passage Network) as LoadAllMods.

## 3 · Verification beyond the harness

- `python tools/parsecheck.py` — 44 files, 0 errors. `python tools/doccheck.py` — GREEN on the
  branch with both legs disarmed. `python tools/upload_preflight.py .` — 26 checked, 0 FAIL on
  the branch's working tree (the worktree copy in the transcript shows one FAIL on `.git`,
  a worktree artefact explained there).
- `python tools/deskbench.py` — the whole desk suite: `desk_load_first.py` HELD;
  `desk_mystery_tech_migration.py` and `desk_probes_f67_f59.py` REFUTED, **identically on
  `main` at `4e4c97b`**, and neither references a mod-order name (grep count 0). Pre-existing,
  routed in §8.
- Kit probe hygiene: the stale-probe sweep read 0 hits before and after (doccheck
  `TEMPORARY SWEEP`); the two payloads carried the marker while armed and are disarmed.

## 4 · The unattended launches (this rig, 2026-09-25 20:02–20:13)

Seven launches, `steam.exe -applaunch 3215050`, each about 30 s to the menu and out; the kit
read payload logged the saved list at its own file scope and at the menu, the running
`ModsLoaded`, and the three statuses; the set payload rewrote the saved order through the same
helpers and requested the save through the kit's own slot. Logs:
[`docs/archive/load_order_first_2026-09-25/`](../../archive/load_order_first_2026-09-25/).
**Zero `[LUA ERROR]` lines in all seven.** Every launch ran with `[PdxSDK] Started up`.

| launch | tree | saved list at kit load (raw) | what happened | log |
|---|---|---|---|---|
| L1 | branch | `Kit, TrainHub, PACK, OptIn, RailShaft` (the owner's order, L0) | `LoadFirst: moved to the front … (was 3 of 5)`; running order untouched (`Loaded mod items for:` = L0); at the menu the saved copy reads `PACK, Kit, …`; notice shown | `L1_promote_…20.02.57` |
| L2 | branch | `PACK, Kit, TrainHub, OptIn, RailShaft` | **the promoted order survived a full restart**: `Loaded mod items for: SMR_CommunityFixPack, …`; `already first of 5 … nothing written`; no notice | `L2_restart_…20.03.47` |
| L3 | branch | same | set payload: order → `Kit, TrainHub, OptIn, RailShaft, iooW34Y, PACK` (PN before the pack, pack last), save requested | `L3_set_PN_first_…20.05.05` |
| L4 | branch | `Kit, TrainHub, OptIn, RailShaft, iooW34Y, PACK` | **the field report reproduced**: `VacuumWalks: inactive (the shipped emigration code has no work-slot reservation…)`, `HubLocalAccess: inactive (Dome not found…)`, the update dialog names both; `LoadFirst: moved to the front … (was 6 of 6)` | `L4_PN_before_pack_…20.05.53` |
| L5 | branch | `PACK, Kit, TrainHub, OptIn, RailShaft, iooW34Y` | **both guards `active`** with PN loaded after the pack; `already first of 6 … nothing written` | `L5_pack_before_PN_…20.06.35` |
| L6 | branch | same | set payload: order → L0 (PN removed, pack third), save requested | `L6_restore_L0_…20.07.40` |
| L7 | **main** (`4e4c97b`, no LoadFirst) | `Kit, TrainHub, PACK, OptIn, RailShaft` = L0 | **read back from a fresh boot**: saved and loaded both L0; `LoadFirst status=nil`; both guards `active` | `L7_readback_main_…20.12.55` |

What these seven settle on this rig (MEASURED): the promotion writes and the write lands
(L1→L2); a launch that finds the pack first writes nothing (L2, L3, L5, L6); the pack-last
shape promotes (L4); the Passage Network pair end to end (L4→L5); the owner's order restored
(L7). What they do not settle: any other rig, the Paradox playset sync as an explicit act, the
hot enable/disable path through the Mod Manager, the Restart now button, and what the player
sees on screen. Those are §5.

**An instrument note.** `account.dat`'s modification time moved on every launch, promotion or
not (the game saves the account at boot for its own reasons), so it is not an instrument for
"the pack wrote nothing". The pack's own log line and the next boot's raw list are.

## 5 · The retail sitting plan — for the owner's approval, not prepared yet

**Precondition:** `load-first` merged to `main`, or the junction pointed at the branch for the
sitting and restored afterwards (WORKFLOW, "Release marking"). The owner's saved order is L0
today (pack third), which is the right starting state. **Instrument:** one preloaded SMRTK slot,
*Order read*, which logs the saved list, the running list and the three statuses (the read
payload's census as a slot function); everything else is Mod Manager and Options clicks. No
typed console line. The attending agent reads the log after each exit.

| leg | owner does (clicks) | prediction (fails if…) | minutes |
|---|---|---|---|
| S1 restart survives + the notice | Start the game. Read the box. Click **Later**. Press *Order read*. Quit. Start again. Press *Order read*. | Boot 1 log: `moved to the front … (was 3 of 5)`; the box shows once with the text in §1; slot: saved `PACK, …`, loaded L0. Boot 2: `Loaded mod items for: SMR_CommunityFixPack, …`; `already first`; **no box**. Fails if boot 2 loads the old order or shows the box again. | 3 |
| S2 hot disable/re-enable + Restart now | Mod Manager: untick the pack, tick it again, close. (The pack is now last in the saved list; the manager reloads.) Read the box that appears; click **Restart now**. After the game comes back, press *Order read*. | On close: `moved to the front … (was 5 of 5)` in the same process (the hot path), the box appears over the menu; Restart now relaunches the game by itself; the new log: `already first of 5`. Fails if no box, if the game does not come back (then the "could not restart" box or nothing), or if the new boot is not pack-first. | 3 |
| S3 opt-out both ways | Options → Mod Options → Relaunched Fix Pack: untick *Load this pack first*, Apply. Mod Manager: untick/tick the pack, close. Press *Order read*. Then tick the option again, Apply. Press *Order read*. | After the first close: **no box**, slot: saved list with the pack **last**, `LoadFirst inactive (turned off in Mod Options)`. After Apply on: the box appears at once, `moved to the front … via Mod Options`, slot: pack first. Fails if the order changes while off, or nothing happens when on. | 3 |
| S4 Paradox sync | With the Paradox account signed in, open the Mod Manager's Paradox browser page (it syncs the playset), close, quit, start, press *Order read*. | Pack still first; `already first`. Fails if the saved list reads in another order after the sync. | 2 |
| S5 (optional) Passage Network with eyes | Enable PN in the manager, untick/tick the pack (PN before the pack), quit, start: read the update dialog naming two switched-off fixes; click Later; quit; start; *Order read*. Disable PN afterwards. | Boot 1: the dialog names VacuumWalks and HubLocalAccess; `was 6 of 6`. Boot 2: both `active`, no dialog. This ran unattended (L4/L5); repeat only for eyes on the dialog. | 4 |

Total **about 11 owner minutes, 15 with S5**. Tier B evidence card afterwards: the four
log excerpts and the slot lines. Nothing in S1–S4 needs a save; no colony is loaded.

## 6 · The C canary

**Design (owner's shape, inert by construction).** `metadata.lua` now holds the def in a local,
carries one hand-written statement beyond the declared properties, and returns the def:

```lua
local def = PlaceObj('ModDef', { … })
local SMRFixPack_LoadOrderCanary = "SMRFP-LOADORDER-CANARY-2026-09-25-b7e1"
return def
```

Nothing reads the local, no method is overridden, no field is written on the def, so it can
neither run nor change loading whether it survives or not. It cannot log: the metadata
environment holds only `PlaceObj` and `box` (`Mod.lua:1715-1724`). A field write on the def was
avoided on purpose: `PropertyObject.__newindex` asserts on undeclared members behind `dbg`,
which is `empty_func` in retail (`lib.lua:58`), so it would work, but "would work" is not inert.

**Inertness proof at the desk (harness, canary demands).** The file loads under the metadata
env's shape and returns a `ModDef`; its declared property set equals the committed pre-canary
file's set plus `default_options`; the literal leaks no global; the code list is intact. The Mod
Editor loads defs through the same `pdofile(metadata.lua, metadata_env, "t")` (`Mod.lua:1745,
1764`) and packs the folder's files from disk filtered by `ignore_files` only
(`GedModEditor.lua:676-739`), so loading and packing do not depend on the file's shape beyond
returning a def. Preflight and `pack_predict` pass on the branch tree.

**Prediction, SOURCE-VERIFIED path.** `ModDef:SaveDef` (`Mod.lua:973-993`) regenerates the file
from declared properties, so any save strips the canary. Upload validation saves a dirty mod
before packing (`GedModEditor.lua:836-842`; editing the change-note box makes it dirty), and
Paradox saves again after its upload (`ParadoxMods.lua:173`); Steam is uploaded second and packs
the file as it then is (`SteamWorkshop.lua:17-22` saves only on a first upload). So:
**the Steam package: stripped; the local writeback: stripped.** The Paradox package: stripped
if the owner edits the box before uploading (the usual sitting), **present** if nothing is
dirty at upload — that case would mean hand-written metadata code reaches Paradox players and
not Steam players, a constraint any C design would have to live with.

**The check, after the owner's upload, three parts, before `POST_UPLOAD_CLOSE.md` §2 restores
the comments (which brings the canary back from git):**

1. Workshop package: `python tools/flpk_extract.py "A:\SteamLibrary\steamapps\workshop\content\3215050\3787202810\ModContent.fpk" <outdir>` then `grep -c SMRFP-LOADORDER-CANARY <outdir>/metadata.lua`; positive control `grep -c "'id', \"SMR_CommunityFixPack\"" <outdir>/metadata.lua` must read 1. Expected 0 / 1.
2. The local writeback: `grep -c SMRFP-LOADORDER-CANARY metadata.lua` in the tree as the upload left it (the comment count is 0 at that moment, `POST_UPLOAD_CLOSE.md` §1). Expected 0.
3. A fresh boot log after the upload: `grep -c SMRFP-LOADORDER-CANARY <newest Mars.exe-*.log>`. Expected 0 **by design** (it cannot print); this part shows only that nothing else echoes the file.

If part 1 reads 1, C reopens as a separate design question (and part 1 on a Paradox-downloaded
package would then be the second half). If it reads 0 with the control at 1, C closes with that
evidence. The release outbox names the canary; `POST_UPLOAD_CLOSE.md` §1 points here.

## 7 · DEPARTURES from the brief, each with its evidence

- **D1 — LoadAllMods detected by a net-zero probe, not by reading.** Evidence: the first
  heuristic misread `SMR_CommunityFixPack, iooW34Y` as LoadAllMods (harness run 1, case 7b
  FAIL); the account flag has no reader open to mods and no setter in the shipped Lua; the
  probe is exact and the raw list is byte-identical afterwards (case 3b).
- **D2 — the Mod Options page returns.** The brief fixes a player opt-out; the game's only
  player-facing per-mod control is Mod Options, driven by `00_Core.lua`'s dormant reconciler
  (desk case 4 exercises it through the real `ApplyModOptions` message). The 2026-08-12 record
  is kept in both files with the reason the condition changed.
- **D3 — "Restart now".** The brief asks that the player be told; the game's own Mod Manager
  offers Restart in the same situation (`ModManager.lua:146-158`), so the notice does too,
  guarded to PC and to the routine existing. Desk demand 1b; S2 tests it live.
- **D4 — the canary cannot log**, so the check's third part is a null control; a per-portal
  prediction is added because the upload flow saves at different points per portal.
- **D5 — cases 1b and 7 ran in retail unattended** (L4/L5), which the brief placed in the
  sitting; the sitting shrinks to the four click legs of §5 plus an optional repeat.
- **D6 — the sitting's slot file is not written.** The brief says the owner approves the plan
  before anyone prepares it, and `80_AgentSlots.lua` is the kit lane's file; §5 names the one
  slot the preparing seat writes.
- **D7 — two more records on `main`** than the brief names: a sentence in `FIX_POLICY.md` §8
  and a correction bullet in EF-054, because both would read as false the day the branch
  merges ("no way to request a position", "not ours to set").
- **Not done, by the rails:** the hot enable path through the Mod Manager and the Paradox sync
  as an explicit act need clicks (S2, S4); no upload; no merge.

## 8 · SUGGESTIONS (seen, not done)

1. **TestKit:** `OptionsMenuFixPack` (`60_Probes_Opt.lua:1044`) will FAIL on the next `RunAll`
   with the pack's `default_options` back; amend it to allow exactly `LoadFirst`. The
   `fix pack present: N/N` gate line and `SMRTK_FINGERPRINT`'s `fix_pack_present` now count an
   optional row that reads `inactive` when a player turns the toggle off; decide how the kit
   reports it. A `LoadFirst` probe (`GetModsEnabledByUser()[1] == pack id`, or the row's status)
   would make the suite read it.
2. **`tools/arm_leg.ps1`:** `Strip-LegLines` drops every line naming a `mustNotBeListed` entry,
   **commented lines included**, so each arm removed the kit's two disarm-convention comments
   (`97_ForceInactive`, `98_EnablePathLeg`). Restored from HEAD after each disarm this session
   (hash-checked). Fix: strip only active entries; add a self-test leg for it.
3. **EF-096:** `TurnModOn`, `TurnModOff`, `GetModsEnabledByUser`, `WaitQuestion`, `WaitMessage`,
   `ModsRestartApp`, `GetPreGameMainMenu`, `Platform` are now measured open in retail (this
   build); worth adding to the open list with the call-shape rule.
4. **Two desk harnesses REFUTED on `main`**, unrelated to this build (§3): route
   `desk_mystery_tech_migration.py` and `desk_probes_f67_f59.py` to their owners.
5. **Release surfaces:** the change note line and whether the fix list gets a row are the
   release seat's calls from the outbox entry; the pack's own notice is the only load-order
   text this build adds, per the brief's scope.
6. **Persistence failure mode:** if an account file never persists (a platform this rig cannot
   see), the pack promotes and shows the notice on every launch. That is the honest behaviour
   ("nothing happens silently") but worth a field watch after release.
7. **`docs/archive/PassageNetwork_1.38_Code_PassageNetwork.lua`** is whole-CRLF in an LF tree
   (doccheck WARN, pre-existing); `--fix-eol` when a lane touches the archive.

## 9 · Do not claim

"The pack loads first" is desk- and unattended-verified on this rig only, until the sitting
runs. A save request is not a disk write; here the next boot's raw list is the disk evidence,
and only for this rig's Steam account. The canary shows only whether code of that shape
survives packaging; it says nothing about whether C's hook would work. `account.dat`'s
modification time is not evidence of anything the pack did.

## 10 · Build handoff to the audit (consumed)

Branch `load-first` at `8e2325a` (one commit over `4e4c97b`); records in this commit on `main`.
Re-run: `python tools/desk_load_first.py` and `--no-promotion` on the branch; the seven logs;
`python tools/upload_preflight.py .` on the branch's working tree, not a worktree. The audit
below consumed the brief and its map row in the audit commit.

## 11 · Fresh-context audit — CHANGES, 2026-09-25

**Disposition:** repair the named changes below on the code branch, then re-audit before
SHIP-TO-SITTING. This audit authorizes neither a merge nor a sitting or upload. The saved-order
route works in the normal cases; the failures are repairable, so the verdict is CHANGES, not NO.

### Evidence and reproducibility

MEASURED: `git pull` completed with “Already up to date”; the clean records checkout was
`f65b609d14a05546649672362a06ec8891c97598`. The audited code was
`8e2325aa219efc253e2c957eb776ca77ca06a2d2`, exported with `git archive` into an isolated
`scratch/` directory. The branch diff was read against `4e4c97b`; the inputs added since
`9833cca` were checked. No installed file, junction, account order, save or game process was
changed by this audit. No new game launch ran.

The [audit instrument](../../archive/load_order_first_audit_2026-09-25/load_first_audit.py)
checks the tested code and harness bytes against the audited commit, runs the builder's
harness and controls, removes only the rebuild loops in a scratch copy, restores both code
and harness with matching hashes, and runs the additional cases. It uses the builder's
extracted **archived 1.1.1.405907** helpers and real pack core/sandbox. UI, scheduling and
disk writes are desk stubs. In particular, the new notice cases run the startup threads
*before* a later Options click. They measure whether another notice gets scheduled, not a
rendered dialog.

RAN 2026-09-25, from the repo root (scripts were in `scratch/` during the run; identical
copies are archived here):

```text
python scratch/load_first_audit_setup.py
python scratch/load_first_audit.py scratch/load_first_audit_8e2325a scratch/load_first_audit_results
python scratch/load_first_audit_receipts.py
```

For replay, use the archived scripts with the same arguments and a fresh scratch export.
The [setup script](../../archive/load_order_first_audit_2026-09-25/load_first_audit_setup.py)
refuses to overwrite an existing export. The [main transcript](../../archive/load_order_first_audit_2026-09-25/audit.txt)
records input hashes, commands, named cases and reconciled totals. `HEAD f65b609` printed
inside exported-tree harnesses is the parent records repository's HEAD, **not** the code
under test; the `IDENTITY` and `INPUT` lines establish the exported `8e2325a` code.

The [source/verification receipt](../../archive/load_order_first_audit_2026-09-25/receipts.txt)
comes from [this script](../../archive/load_order_first_audit_2026-09-25/load_first_audit_receipts.py).
Every cited game-source file below was read from
`B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src`, and the inspected files matched that
archive's `MANIFEST.sha256`. The receipt contains line-numbered source slices and fingerprints.

| Check, command/filter | Fresh result and its limit |
|---|---|
| `python tools/desk_load_first.py` in the export; count named `PASS`/`FAIL` lines and reconcile with its final demands line | **50/50 held**. Normal middle/last promotion, unchanged running queue, already-first no-write, opt-out/veto, prerequisites/dependants and the PN pair reproduced. |
| Same command with `--no-promotion` | **33/50 failed**, reconciled with the printed control total; this omits the entire module, including its registry row. R4 explains why that is insufficient. |
| Same harness, only the rebuild loops removed | First run aborts at the inline case-5b assertion. Keeping that call but removing only its assertion permits a complete run: **24/50 failed, 26/50 held**. `CONTROL_RECONCILE` names every group still passing. Both scratch files were restored and hash-checked. |
| Audit `SHAPE_MEMBERS`: permutations of `A,B,C,PACK`, plus absent, duplicate/stale and duplicate-pack lists | **27/27 held**, reconciled with `relative-order shape census`. Other IDs keep their first-occurrence relative order; stale `GHOST` stays. Already-first/absent lists do not request a save. |
| Audit `AUDIT_DEMAND` rows, reconciled with `AUDIT_TOTAL` | **10 failed expectations**, individually named, plus the held shape census. These are counterexamples grouped into R1–R3/R5 below, not a broad reliability percentage. |
| `python tools/parsecheck.py`; `python tools/upload_preflight.py .` in the restored export | Both exit 0. Parsing and preflight do not establish runtime behavior or actual Editor packing. |

### Changes required

**R1 — High: schedule the notice when promotion occurs, including a later opt-in.**

MEASURED: start with the option off, let startup threads finish, then apply the option on.
The saved list becomes `PACK,B,C`, one save is requested, `pending_notice=true`, but there
are no notice threads and no question. The same happens after an already-first boot,
turning the option off, moving the pack last, then turning it on. A later promotion after
an earlier notice is suppressed by the process-wide `notice_shown` latch.

Cause in `8e2325a:Code/01_LoadFirst.lua`: the only notice thread is created at file scope
(:276); it returns when nothing is pending (:280). `Promote` merely sets a flag (:225),
and `on_activate` (:262) schedules nothing. The builder's 4b test turns the option on
*before* it first runs the recorded threads, masking the actual sequence. This violates
FIXED 3: the player is told when a restart is needed. Repair the notification lifecycle
and add cold-off→later-on, already-first→later-on, and repeated-promotion controls with
realistic thread chronology. Deduplicate reloads of the same pending change without
silencing a new change.

**R2 — Medium: preserve existing persistent-slot bytes, including on write refusal.**

MEASURED with the real archived writer: a valid full slot containing `z` repeated 32768
times becomes only the new promotion record. The log explicitly says “rewriting with our
line only”. Smaller inputs also lose data: `alpha\n\nbeta\n` loses its empty lines and
trailing newline; `SMRFixPack.LoadFirstExtra payload` is mistaken for this module's record
and removed. These are synthetic preservation cases, not a claim that a player has lost
data in the field.

Cause: the parser (:119–134) skips empty lines and accepts every line sharing the prefix;
the fallback (:147–153) deliberately discards the foreign tail. Archived 1.1.1.405907
`CommonLua/Modding/Mod.lua:1487–1503` refuses an oversized value *before* writing it, so
the loss is introduced by the module's retry. Preserve unrelated data exactly, match only
the module's own record, and decline or roll back safely if a changed value cannot fit.
Do not sacrifice existing data to force the save request. Add boundary/refusal controls
alongside the builder's ordinary two-line case.

**R3 — Medium: make the LoadAllMods claim match every covered list shape.**

MEASURED: with either LoadAllMods flag set and installed IDs `PACK,z`, the module reports
`active`, “first of 2 in the saved mod order”; no detection runs. The selector's sorted
installed list is being described as the saved list because `pos == 1` returns at :177
before `load_all_reason` at :185. Separately, with the account flag set and a saved stale
`SMRFixPack.LoadFirst.probe` ID, the “net-zero” probe removes that ID permanently while
requesting no save. That edge is explicitly anticipated by the code's stale-probe comment.

Archived 1.1.1.405907 `Mod.lua:1995–2001` confirms that LoadAllMods ignores the saved list;
`CommonLua/UI/ModManager.lua:35–41` confirms the probe helpers really mutate it. Preserve
pre-existing IDs, and diagnose LoadAllMods without calling an installed-ID view a saved
order. The indistinguishable account-flag case may need a stated, evidence-backed limitation
instead of an exact-detection claim; do not add unconditional writes merely to keep the
claim. D1's synchronous transient probe is acceptable in principle, but the present
“byte-identical afterwards” claim is false for its own stale-ID case.

**R4 — Medium: replace registry-presence controls with behavioral controls and fix the claims.**

MEASURED: with only the promotion loops removed, groups `2`, `3a`, `3b`, `4a`, `4d`, `5c`
still pass in full, as does the intentionally independent canary group. Omitting the whole
module instead makes their status assertions fail merely because `LoadFirst` is absent.
That does not falsify their no-write or preservation promises. “None vacuous” in §2 is
therefore not the result the audit brief asked for.

Keep a registration-preserving no-promotion mutant for positive promotion/dependency/PN
cases. A no-op case naturally survives removal of a mutation: test those cases against a
mutant that wrongly writes or ignores the relevant guard. Keep all cases running after a
failure; the inline assertion currently truncates the run. Add the R1–R3 cases and separate
measured behavior from mere status-row existence. Also retain the cross-check's distinction:
first file execution does not promise every deferred data repair precedes every content edit.

**R5 — Medium: repair the sitting's triggers, sync observation and restoration.**

SOURCE + MEASURED: S2 unticks and reticks the pack before closing the same manager visit.
Archived 1.1.1.405907 `ModManager.lua:123–166` saves this changed order, but
`Mod.lua:2104–2112` sorts the new and running sets and returns when they match. Running
the extracted `ModsReloadItems` body on that exact shape leaves saved `B,C,PACK`, running
`PACK,B,C`, with no promotion or notice. Its predicted hot reload cannot happen. S5 can
also lose its PN-before-pack condition if adding PN causes a real reload that promotes
before the planned cold boot.

S4 also needs an observation of the actual sync, not just an opened page. The inspected
`ModManager.lua:1902–1906` queues `SyncPdxMods` on `PdxLogin`; a browser click alone is not
proof it ran or rewrote an enable list. The revised plan below separates these paths and
includes a final restore/readback. Preserve the owner's full enabled set, relative order
and LoadFirst option, not just PN's final disabled state. The old estimate in §5 no longer
prices a valid test.

**R6 — Medium: supply Editor load/pack evidence, and qualify the canary prediction.**

SOURCE: the local literal and returned `ModDef` in `8e2325a:metadata.lua` are inert: no
native method override, no global or def-field write. The rerun confirms the stand-in
metadata environment accepts it. This satisfies the safety test; it does not execute
the Mod Editor's loading and packing path.

The builder's decoded measurements/logs contain preflight and pack-prediction evidence,
not an Editor pack result or an extracted generated package. The receipt's keyword census
includes those positive controls; the artifact inventory and contents were also read.
Archived 1.1.1.405907 `CommonLua/Classes/GedModEditor.lua:742–751,884–893` shows the actual
pack action, and :713–739 calls `ReloadLua` and `AsyncPack`, neither exercised by the
metadata fixture. Before clearing the canary for the sitting/release, record an actual
isolated Editor load and local pack, the resulting package, and its decoded metadata,
or provide a demonstrably equivalent test and state its limits. No upload is needed.

The §6 stripped-Steam/local prediction is conditional: dirty validation saves
(`GedModEditor.lua:836–842`), successful Paradox upload saves
(`CommonLua/Libs/Paradox/ParadoxMods.lua:165–173`), and creation of a new Steam item saves
(`CommonLua/Platforms/steam/SteamWorkshop.lua:17–25`). A clean existing Steam upload with
no successful preceding Paradox save can retain the canary. Record portal and save path
with every observation. A missing Steam canary after a forced save closes only that tested
path; it does not disprove survival in a clean Paradox package. The null log control and
the warning that canary survival proves nothing about a working C hook remain correct.

### Existing retail evidence and broader checks

MEASURED by re-reading the decoded L1–L7 logs committed in `f65b609`: their revision is
405907 and their loaded lists support the normal promotion/restart and PN-before/after
claims. L1 :96/:186 separates the changed saved order from the running order; L2 :184
loads pack first. L4 :111/:114 declines the guards; L5 :82/:85 applies them. L7 :179/:204
reads back the original enabled order with no LoadFirst row. The audit transcript records
each log's hash and exact hits. Its `LOG_TOTAL` reconciles **7 logs, 7 revision lines,
7 loaded-list lines, 0 `[LUA ERROR]` lines**. These observations do not show an attended
dialog, a click on Restart now, explicit sync, or a byte hash of the Lua used by each retail
launch. The desk input hashes do match the builder's archived `measurements.txt`.

MEASURED: `SMR_TESTKIT=B:/Dev/SMR/SMR-BugFixPack-TestKit python tools/deskbench.py` in the
export returned **39 held / 44 harnesses**, reconciled against every summary member in
[desk_suite.txt](../../archive/load_order_first_audit_2026-09-25/desk_suite.txt) and
`SUITE_TOTAL` in the receipt. Each failed harness was then run individually on `main`
`f65b609`, with the same failure class:

- `desk_c104_political_animal.py`: requirement-set/achievement expectations differ.
- `desk_c107_dry_farming.py`: missing `TechModifierName` in its fixture.
- `desk_c92_achievement.py`: achievement hypothesis expectations differ.
- `desk_mystery_tech_migration.py`: missing `ResolveTechMystery` in its fixture.
- `desk_probes_f67_f59.py`: the old F59 error-message expectation differs.

The named difference from §3's claimed failing set is **Political Animal, Dry Farming and
C92 achievement**. Their harness bytes and relevant existing production files are unchanged
between the branch and records. This is baseline harness debt, not attributed to LoadFirst.
The whole suite uses its existing mixture of source routes, including live-tree reads;
only the targeted LoadFirst audit is pinned throughout to archived 1.1.1.405907.
The main transcripts are [here](../../archive/load_order_first_audit_2026-09-25/main_failed_harnesses.txt)
and [here](../../archive/load_order_first_audit_2026-09-25/main_additional_failed_harnesses.txt).
No colony, account persistence or TestKit UI was exercised anew. Doccheck for the audit
records is recorded by the audit commit's gate, independently of these behavioral failures.

### Departures judged

| Builder departure | Audit judgment |
|---|---|
| D1, transient LoadAllMods probe | Route acceptable in principle; implementation and exactness claim need R3. |
| D2, return of the Mod Options page | Accepted: the player now has a required opt-out, so the earlier “nothing to set” condition no longer holds. |
| D3, Restart now button | Accepted: use of the native routine is justified; click/relaunch remains a sitting prediction. Correct quit-flush citation: archived 1.1.1.405907 `CommonLua/AccountStorage.lua:166–187`. |
| D4, canary without a log line | Accepted as explicitly inert; R6 corrects proof and portal conclusions. |
| D5, unattended retail work reduces the sitting | Accepted within the owner's authorization; logs establish those limited results. |
| D6, slot not prepared before approval | Accepted; no sitting was prepared by this audit. |
| D7, policy/EF records | Appropriate homes for the changed mechanism; audit corrections are carried by this report and the release hold. |

The builder's suggestion to normalize the archived PN file is rejected: the archive is
append-only. None of its existing bytes were changed. The other §8 suggestions remain
observations, not authorization to expand this audit into unrelated implementation work.

### Revised sitting proposal — held for repairs and owner approval

This replaces §5's recipe. **Not prepared or run.** After R1–R6 are closed and re-audit
returns SHIP-TO-SITTING, the preparing seat can present this plan for approval. The sitting
uses preloaded SMRTK buttons and native UI clicks; it requires no owner console typing or
colony save. Before approval, the preparer still owes an exact, source-traced S4 click path
and a completion/error observation for the intended Paradox sync.

The preparation captures the fresh starting enabled set, order, option and junction target,
then provides **Order read**, **Stage PN-before-pack for next boot**, and **Restore starting
settings** slots. A staged test order is distinguished from a measured production promotion.
Restoration inhibits promotion until the restored order is read back on a fresh boot, then
restores the original option without another promotion before exit. Logs are read after exit
and archived with the sitting result. This preserves the original brief's restoration duty.

| Leg | Owner clicks | Prediction that can fail | Estimated minutes, `<<PENDING-RUN>>` |
|---|---|---|---|
| A, cold start | Start from a deliberately captured pack-later order; read notice, choose Later, Order read, quit; restart and Order read. | First boot changes saved order only and shows the notice. Next boot is pack-first, requests no promotion save, and shows no duplicate notice. | 3 |
| B, actual hot enable and restart | Disable pack and close the manager to apply that disabled set; follow the native unload prompt. Reopen the manager, enable pack, close; choose Restart now when the pack's notice appears. | A real enabled-set change reaches reload; promotion and notice occur; native restart returns pack-first. A same-visit off/on is recorded separately as an order-only path, with no hot-reload expectation. | 4 |
| C, later opt-in | On a settled menu, turn LoadFirst off and Apply; move pack last through the manager, close and Order read; turn LoadFirst on and Apply. | While off, order stays last. Later-on promotes and presents a new notice after the startup thread has already ended. This is the R1 falsifier. | 3 |
| D, explicit Paradox sync | Use the source-traced native sync/login action supplied by the preparing seat; wait for recorded completion, Order read; quit/restart, Order read. | Completion is positively observed. Saved/next-loaded order stays first; an error or missing completion is inconclusive, never PASS. | 2 |
| E, restoration | Restore starting settings, quit, start the restoration/readback leg, Order read, exit. | Saved order, enabled set, option and junction equal the captured start; no promotion silently undoes restoration. | 3 |
| Optional PN | Stage PN-before-pack for next boot; quit/start, observe guards and notice, choose Later; quit/start and Order read. Finish with E. | First boot really loads PN before pack and declines the two guards; second loads pack first and applies both. | +4 |

Cost is an unmeasured estimate: **15 owner minutes; 19 with PN**, `<<PENDING-RUN>>`.
The arithmetic is in the receipt, not a timing measurement. S4's exact clicks remain part
of R5, so this proposal is not ready for an approval request today.

### Authority and open work retained from the consumed brief

Owner, 2026-09-25, verbatim:

> “I want B or C, the rest of those are just more bandaides for the problem”

> “Can we go with B first, and if it works and we upload it, can we test the shap of C, put
> something harmless in the metadata that we can easily check for to see if it survives”

> “Make sure we don't put them in a box, allow it to change the plan if it finds a better way
> to do something.”

> “let them know they are free to start the game up for any unattended testing.”

> “I am going to build with fable since this is going to be critical to get right, and audit
> with astra.”

The 2026-09-24 goal remains verbatim in the cross-check report's header. The retained FIXED
requirements for the repair/re-audit are: vanilla repairs before content mods for uninstructed
players; no game-file changes and nothing shipping outside the pack; other mods' relative order,
player opt-out and a restart notice; no guard-hardening substitute; no attended sitting or upload
without owner approval; an inert canary; and a separate audit. The mechanism and other DEFAULT
details remain delegated judgment, with departures and their evidence disclosed to the owner.

Unattended testing remains authorized with the original conditions: first check whether Mars.exe
is running and leave the owner's instance alone; close only instances started by the worker;
use scratch saves only; obey `tools/arming/README.md`; preserve and restore the owner's enabled
set/order and any changed junction, reading restoration back from a fresh boot; archive cited
logs in the citing commit. No route meeting the FIXED requirements means report the stop, not
silently relax them. An unsafe canary is omitted from B with that disposition recorded.

The repair seat's open work is R1–R6, the still-held sitting, and the post-upload canary checks
already carried by §6 and the release outbox, with R6's portal qualifications. The release hold
now points here rather than to the deleted brief. The brief and map row are consumed by this
audit; retirement does not waive any of those obligations.

## 12 · Repairs after the audit — branch `load-first` at `8ea5449`, 2026-09-25

One commit over `8e2325a`, code only; these records are on `main`. The audit's R1–R4 and R6 are
repaired and re-measured; R5 is answered as a corrected plan (still held for approval). The
retail evidence of §4 stands. Transcript, logs, both Editor-made packages and their decoded
metadata: [`docs/archive/load_order_first_repairs_2026-09-25/`](../../archive/load_order_first_repairs_2026-09-25/).

**Read this first, owner.** While the repair seat had the branch checked out on the junction, you
started the game (23:08, `Mars.exe-20260925-23.08.46`, excerpted in the archive): the pack promoted
your order from third to first and you chose **Later** on its box. That is the first time a
person saw the notice; it is not a tested-attended claim, because nobody asked you to look. Your
order was restored at 23:21 (L10) and read back from a fresh boot on `main` at 23:23 (L11):
`Kit, TrainHub, Pack, OptIn, RailShaft`, no `LoadFirst` row. The failure was the seat's: a
checked-out code branch is what your game loads. It is recorded so the next seat does not repeat
it, and the branch is on the junction no longer than a launch needs.

### R1 — the notice is scheduled by the promotion (fixed)

`Promote` sets `pending_notice` and calls `schedule_notice()`, which creates one real-time thread
per pending promotion: it waits for the pregame menu, shows the box once, clears the flag. A later
opt-in through Mod Options (the reconciler's `run_apply` or `on_activate`) therefore gets its own
thread and box; a second promotion in the same process gets a second box; a Lua reload re-arms a
thread only when a promotion is pending and no live thread holds it (`IsValidThread` when
reachable, else the module's own live flag). The process-wide `notice_shown` latch is gone.
Controls, all with the startup threads drained BEFORE the later click (the audit's chronology):
R1a cold option off then later on: promotes, one box; R1b already-first boot, off, moved last, on:
one box; R1c promotion boot, off, moved last, on: two boxes, two save requests; R1d reload while a
box is pending: one box. Killed by `no-notice` and, where a promotion is involved, by `no-rebuild`
and `not-optional`.

### R2 — foreign slot bytes preserved exactly, refusal drops nothing (fixed)

The slot is split on the newline byte keeping empty pieces; only the first line matching the
record pattern `SMRFixPack.LoadFirst v<n> promotions=<n>` is ours; the rest is re-joined unchanged
behind the new line. `alpha`, blank line, `beta`, trailing newline keeps its blank line and its
trailing newline; `SMRFixPack.LoadFirstExtra payload` is foreign and kept. When the record would
not fit, the shipped writer refuses before writing (`Mod.lua:1494-1496`), the module writes nothing
else, the rebuilt order stands in memory and the log says the save could not be requested through
the slot. Controls R2a–R2c (`z` × 32768: slot byte-identical, order promoted, zero save requests,
the log line present), killed by `clobber-slot`. **Stated exception to §2 case 1:** with a full
foreign slot the promotion makes no save request; the game's own account save at boot (observed on
every launch on this rig, §4's instrument note) carries it, and if none comes the next start
promotes and tells again.

### R3 — LoadAllMods edges (fixed, with one stated limit)

`config.LoadAllMods` is read before anything is concluded, so a pack that sorts first is still
diagnosed `inactive` (R3b). The account flag is probed only on the rebuild path, with a
per-process unique id (`SMRFixPack.LoadFirst.probe.<time>.<n>`); an id already visible in the
copy proves the normal branch without a write, and the probe never removes an id it did not add,
so a stale id stays where it was under either flag (R3a, raw list byte-identical). **Stated limit
(R3c):** when the pack is already at index 1 nothing is written and nothing is probed, so with the
account flag set and the pack alphabetically first the status line reads "first in the list the
game loads (N mods); nothing written", which is then the installed list, not the saved one. The
wording is chosen for that case; the module header says so. Killers: `ignore-loadall` (both
routes off) for 3a, `ignore-probe` for 3b, `ignore-config` for R3b, `fixed-probe` for R3a,
`always-rebuild` for R3c.

### R4 — behavioural controls (rebuilt harness)

`python tools/desk_load_first.py`: baseline **64 of 64**, then twelve mutants of the module
source, each an exact single-occurrence replacement asserted to have taken, each case group
naming the mutants that must kill it; no inline assertion, every case runs after a failure.
From the archived transcript:

| mutant | what it breaks | kills (groups) |
|---|---|---|
| `no-rebuild` | the list is never rebuilt | 1a 1b 4b 4c 5a 5b 6a 6b 7a 7b R1a–d R2a–c R3a shape |
| `always-rebuild` | already-first no longer returns | 1a 2 4b 4c 5c 7b R1a R1b R1d R3c shape (engine) |
| `ignore-option` | option off ignored at apply | 4a |
| `not-optional` | invisible to the reconciler | 4b 4c R1a R1b R1c |
| `ignore-config` / `ignore-probe` / `ignore-loadall` | one or both LoadAllMods routes off | R3b / 3b R3a / 3a 3b R3a R3b |
| `ignore-absent` | a pack absent from the list is inserted | shape |
| `clobber-slot` | foreign bytes dropped | 5a 5b R2a R2b R2c |
| `no-notice` | promotion schedules nothing | 1a 1b 4b 4c R1a–d |
| `bypass-veto` | promotes at file end regardless | 4a 4d |
| `fixed-probe` | fixed, pre-cleared probe id | R3a |

Control verdict: every group's expected killers kill; no group is vacuous; `canary` and
`engine` are independent by design and reported apart. The `engine` case runs the shipped
`ModsReloadItems` (`Mod.lua:2099-2179`) on a same-visit off/on: the running list is unchanged,
no promotion, no notice, which is the sitting's S2 fact (R5). The module header now also states
the cross-check's distinction: first file execution does not promise that a deferred data repair
precedes every content mod's edit.

### R5 — the sitting, corrected (held for approval; not prepared)

The audit's revised legs A–E and the optional PN leg are adopted as written in §11, with these
completions:

- **B, hot path.** Disable the pack, close the manager (a real enabled-set change: the manager
  saves and reloads, `ModManager.lua:123-166`; `Mod.lua:2104-2112` does not short-circuit). Reopen,
  enable, close: the reload runs the pack's code, `Promote` runs on the hot path, the box appears;
  choose Restart now. A same-visit off/on is recorded separately as order-only (the `engine` case)
  with no reload expectation.
- **D, explicit Paradox sync, source-traced clicks.** Main menu bottom bar, the Paradox account
  button (`idParadoxAccount`, `Lua/XDef/PGBottomButtons.generated.lua:70`), then **Log out** (the
  button shows while `g_Pdx.account`, `ParadoxMenu.lua:357`; `PDXAccountObject:LogOut` :239 calls
  `PdxSDK:LogOut` :377, which posts `PdxLogout` :389 and clears the download queue,
  `ModManager.lua:1919-1925`), then **Log in** with the owner's credentials (`PDXAccountObject:Login`
  :138 calls `PdxSDK:LogIn` :392, which posts `PdxLogin` :405). `OnMsg.PdxLogin`
  (`ModManager.lua:1902-1917`) pushes `SyncPdxMods` (:1864-1885) on `g_PopsDownloadModsQueue`, a
  `PdxTaskQueue` (`PdxSDK.lua:900-960`); per subscribed mod `SyncUpdatePdxMod` (:1763) calls
  `TurnModOff` or `TurnModOn` only on a version change or an install. **Completion witness:** a
  *Sync read* slot logs the queue length (`#g_PopsDownloadModsQueue`; the `g_Pops` name is outside
  the blacklisted prefixes) and the saved list before the click, after the queue reads 0, and after
  the next boot; the log's `PdxSDKMods` lines (`mods_print`, `ModManager.lua:15-19`) carry any
  "Failed to get subscribed mods for sync." A login error or a queue that never empties is
  inconclusive, never PASS. If the account panel shows no Log out, the owner is not signed in and
  D is NOT RUN, not PASS. Whether the owner uses a Paradox account on this rig is not known from
  the logs, which show `[PdxSDK] Started up` only.
- **E, restoration, with the promotion inhibited.** The kit cannot veto the pack once the pack loads
  first, and cannot write Mod Options, so E is: the owner turns *Load this pack first* OFF (a
  click); the *Restore starting settings* slot rebuilds the captured start order and requests the
  kit's save; quit; boot; *Order read* confirms the start order with `LoadFirst inactive (turned
  off in Mod Options)`; the owner turns the option back ON (a click); quit without another boot.
  Then the junction goes back to `main` (precondition 2) and reads back once more; after a merge
  the next launch promotes by design and E's readback is the last boot before it.
- **Cost:** the audit's estimate, 15 owner minutes, 19 with PN, `<<PENDING-RUN>>`, unmeasured.

### R6 — Editor load and pack evidence (measured on this rig)

A SCRATCH mod, `SMR_LoadFirstCanaryScratch`, was built in the appdata Mods folder from the branch's
`metadata.lua` (id and title changed, store ids removed, the canary lines intact) with an empty
`items.lua`, never enabled, so nothing of it ran. A kit payload vetoed the real pack's LoadFirst
and, at the menu, called the Editor's own steps: `PackModForBugReporter` (the packer,
`GedModEditor.lua:756-765`, which calls `CreatePackageForUpload` :676-739; `DbgPackMod` itself is
blacklisted for mods, `PackModForBugReporter` is not) and, in the second launch,
`ModDef:SaveWholeMod` (`Mod.lua:1153-1170`, which calls `SaveDef` :973-993) first. Logs L8 and L9;
the packages were copied from the game's `ModUpload\Pack\ModContent.fpk` under the local temp
folder after each exit and decoded with `tools/flpk_extract.py`.

| step | scratch `metadata.lua` on disk | decoded package `metadata.lua` |
|---|---|---|
| before anything | 34,496 B, sha `ab3b99ca…`, canary 1, comment lines 329, first line `local def = PlaceObj(`, last `return def` | none yet |
| L8 pack, no save (`IsDirty` nil) | unchanged | 34,496 B, sha `ab3b99ca…`, **canary 1**, comments 329, same first and last lines; id control 1 |
| L9 `SaveWholeMod` (version 21 to 22) then pack | 8,703 B, sha `989f2642…`, **canary 0**, comments 0, first line `return PlaceObj('ModDef', {`, last `})` | 8,703 B, sha `989f2642…`, **canary 0**, comments 0; id control 1 |

MEASURED: the packer takes the on-disk file byte for byte; the Editor's save regenerates it and
strips every hand-written statement and comment. So per portal, following the save points the
audit listed (`GedModEditor.lua:836-842`, `ParadoxMods.lua:165-173`, `SteamWorkshop.lua:17-25`):
a dirty-validation save before packing strips it for both stores; without one, the Paradox
package carries it and the Steam package, uploaded second after Paradox's post-upload save, does
not; a clean Steam-only update would carry it. The post-upload check (§6) must therefore record
the portal and whether a save preceded packing, and a stripped Steam package decides only that
path. **Limits:** the scratch mod had no loaded items, so its regenerated file also lost
`default_options` (the real pack, whose items load, keeps it, `Mod.lua:983`); the canary and
comment results do not depend on items. No upload was made; the Editor UI was not opened; the
same functions the UI calls were called.

### Rig state and the kit

The TestKit's `metadata.lua` was restored to HEAD after every disarm (hash-checked; the
harness's strip of commented `mustNotBeListed` lines is still SUGGESTION 2). The scratch mod
folder is deleted. The kit carries an **uncommitted edit to `Code/80_AgentSlots.lua`** (93
insertions, 8 deletions, modified 23:21:50, last committed by the hub lane at 22:53 as
`cb49f07`) that this seat did not make and did not touch; routed to that lane.

### Handoff to the re-audit

Branch `load-first` at `8ea5449` (`8e2325a` plus one commit). Re-run `python tools/desk_load_first.py`
on the branch (baseline and every mutant in one run; `--mutant NAME` for one, `--list` for the
killers); read L8–L11 and the owner-session excerpt; decode the two archived packages. The
sitting stays held; no merge, no upload.

## 13 · Re-audit — CHANGES, 2026-09-26

**CHANGES on `load-first` at `8ea5449`, against records `main` at `4e704c1`.** The code
repairs answer R1–R4; the decoded packages and native save/pack source answer R6 within the
limits below. R5's hot-enable trigger is corrected, but its sync-completion witness can pass
before work completes, and its final option click undoes restoration. Those are sitting-plan
defects, not demands to undo the repaired production behavior. No sitting approval is sought
while they remain. The retained FIXED requirements in §11 are unchanged.

### Evidence and repair judgments

The repair diff `git diff 8e2325a 8ea5449` changes `Code/01_LoadFirst.lua`,
`tools/desk_load_first.py`, `tools/arming/legs/load-first-pack.json` and its payload
`tools/arming/payloads/98_LoadFirstPack.lua.txt`. Metadata, items and the PN repairs are
unchanged. Tests ran in a disposable `git archive` export of the exact audited commit;
the installed checkout stayed on `main`. The outer [receipt](../../archive/load_order_first_reaudit_2026-09-26/reaudit.txt)
records full commits and verifies input bytes against `git show 8ea5449:<path>`. Harness
headings inherit the enclosing records repository's HEAD; they do not identify the exported
code. The module SHA-256 is `c7fdea6a3c878fb49d9e8f5bdf25b369c7eabb3600d4b106b530ec0a06838e79`.
Audit commands from the repository root were `python scratch/load_first_reaudit.py` and
`python scratch/load_first_reaudit_counterexamples.py`; their archived script copies can be
run from that same working directory. The latter exits successfully only when both named
plan failures and their positive controls reproduce as recorded.

| Repair | Re-audit disposition |
|---|---|
| R1, later notice | Accepted. Promotion schedules a notice; later opt-in after startup threads drain and a later second promotion are exercised. Pending reload does not duplicate the box in the fixture. Actual click/relaunch remains a sitting test. |
| R2, slot preservation | Accepted with the disclosed full-slot exception. Blank lines, trailing newline and foreign lookalike prefixes survive; writer refusal leaves foreign data intact. The refusal path promotes in memory and makes no save request. This is not a durable-order guarantee: a later game save must carry it, or a subsequent boot repeats promotion/notice. The archived writer is `1.1.1.405907/Src/CommonLua/Modding/Mod.lua:1487–1503`, with the size refusal at :1492–1494. |
| R3, LoadAllMods | Accepted with the disclosed already-first account-flag limit. Config is checked before the first-position return; a stale probe is preserved; the normal/alphabetical paths have opposing controls. The status wording no longer claims the saved list was inspected when it was not. |
| R4, controls | Accepted. The actual mutated behaviors fail named demands, and the expected group-to-killer mapping holds. The independent engine and inert-canary checks are reported separately. This is evidence for the declared cases, not exhaustive coverage. |
| R5, sitting | B accepted; D and E remain open as detailed below. |
| R6, canary | Accepted as a scratch metadata load/save/pack experiment through native functions, not a full real-pack Editor/UI or store round trip. See package and log checks below. |

MEASURED: `python tools/desk_load_first.py` in the export returns **64/64 baseline demands
held** and catches **every declared mutant**. `--list` was read; each `--mutant NAME` was also
run independently. All ran the same 64 demands, reconciled by the runner against their named
PASS/FAIL lines and the aggregate summary. Verbose mutant mode exits successfully even when
demands fail; the audit counts those failures rather than treating exit status as the verdict.

| Mutant | Failed demands |
|---|---:|
| no-rebuild | 34 |
| always-rebuild | 16 |
| ignore-option | 3 |
| ignore-config | 1 |
| ignore-probe | 4 |
| ignore-absent | 1 |
| clobber-slot | 5 |
| no-notice | 9 |
| bypass-veto | 4 |
| fixed-probe | 1 |
| ignore-loadall | 8 |
| not-optional | 8 |

The table's 12 members reconcile to `MUTANT_TOTAL members=12, with_failures=12`; baseline
members reconcile to `BASELINE` and `RESULT` in [baseline_and_mutants.txt](../../archive/load_order_first_reaudit_2026-09-26/baseline_and_mutants.txt).
The [runner](../../archive/load_order_first_reaudit_2026-09-26/load_first_reaudit.py),
individual mutant outputs, parsecheck and upload-preflight outputs are archived alongside it.
Parsecheck and the preflight's runnable guards pass; the latter still cannot check login.
The unrelated full-suite debts recorded in §11 were not rerun or reclassified.

### R5-D — queue emptiness is not sync completion

The login route reaches `SyncPdxMods`, but the proposed *Sync read* slot cannot establish
completion. Archived build **1.1.1.405907**, `Src/CommonLua/Libs/Paradox/PdxSDK.lua:894–916`,
removes a task from the queue before calling its callback. `Src/CommonLua/UI/ModManager.lua:1864–1885`
then makes an asynchronous subscription request before scheduling child updates. The queue
can therefore be empty while the root request or the final child is still in progress.
Logout also clears the queue (:1922–1927); emptiness alone does not distinguish completion
from cancellation. Absence of the initial subscription-error message does not close that gap.

MEASURED: the [counterexample](../../archive/load_order_first_reaudit_2026-09-26/counterexamples.txt)
runs the archived queue methods with a yielding callback. At observation, `queued=0`,
`started=true`, `done=nil`, worker `suspended`: the plan's completion demand fails.
Resuming the callback produces `done=true`, worker `dead`, with the queue still zero; the
positive completion control holds. This models an outstanding asynchronous call, not a live
Paradox service test. Source file fingerprints match the archive manifest in the same receipt.

**Required repair:** present a source-backed completion/error witness tied to this login/sync
attempt, covering both the root callback and all scheduled child work. Demonstrate that an
in-flight callback, cancellation and failed work cannot be recorded as PASS. Queue length can
remain diagnostic data. Prepare the sitting only after that witness and its controls are
reviewable; the owner's account state is still unknown and an unavailable route remains NOT RUN.

### R5-E — restoring ON immediately promotes again

The proposed sequence restores the captured pack-later order while the option is OFF,
reads it on a fresh boot, then turns the option ON and quits. That last click invokes the
reconciler immediately: branch `8ea5449` `Code/00_Core.lua:569–602` calls the module's apply/
activation path (`Code/01_LoadFirst.lua:351–376`). No further boot is required to promote
and request a save. This is the behavior R1 deliberately repaired.

MEASURED in the real-core branch fixture: OFF preserves
`Kit,TrainHub,Pack,OptIn,RailShaft` with no promotion save; turning ON changes it immediately
to `Pack,Kit,TrainHub,OptIn,RailShaft`, requests a save and leaves a notice pending. Draining
the notice thread produces the expected box. The OFF and notice controls hold; the demand
that the final ON click preserve the captured order fails. The [runnable check](../../archive/load_order_first_reaudit_2026-09-26/load_first_reaudit_counterexamples.py)
and receipt retain the exact demands. An independent read-only audit found the same source paths.

**Required repair:** place the final saved-order restoration after every promotion-capable
option click, or restore under the nonpromoting records build, and read back the captured
enabled set, order, option and junction on a fresh boot. Specify that ordering concretely and
check it against the original ON/pack-later start. The restored pack-later state cannot remain
unchanged across a later feature-enabled boot with the option ON; that next promotion is
intended. L10–L11 prove the repair seat's actual restoration, not this proposed OFF/readback/ON
recipe. No production-code change is required merely to make that flawed recipe pass.

### R6 and L8–L11 — independent reads and decodes

MEASURED: `python tools/flpk_extract.py --selftest` passes, then the runner calls its `extract`
API on each archived `canary_pack_*_ModContent.fpk`. Each decoded package contains only
`items.lua` and `metadata.lua`; the latter matches its previously archived decoded copy byte
for byte. The [metadata comparison](../../archive/load_order_first_reaudit_2026-09-26/metadata_comparison.txt)
checks the no-save metadata against branch `8ea5449`: only the scratch title/id substitution
and removal of store ids differ. The experiment preserves the actual canary shape.

| Archived package | Decoded metadata bytes | Canary matches | Scratch-id controls | Comment lines |
|---|---:|---:|---:|---:|
| nosave, SHA-256 `49ecf2df…` | 34,496 | 1 | 1 | 329 |
| aftersave, SHA-256 `e666cabb…` | 8,703 | 0 | 1 | 0 |

The runner searches the complete decoded text for the exact canary, anchored scratch-id
property and lines beginning with `--` after whitespace. `PACKAGE` records every matching
line and full package/metadata hashes; `PACKAGE_TOTAL` reconciles both rows. Thus the absent
marker after save has a positive identity control. The package contents limit the claim:
they contain no real pack Code files, and the scratch items were not loaded.

Archived **1.1.1.405907** `Src/CommonLua/Classes/GedModEditor.lua:742–764` gives `DbgPackMod`
and `PackModForBugReporter` the same dirty-save and `CreatePackageForUpload` route.
`Src/CommonLua/Modding/Mod.lua:973–993,1153–1170` shows why `SaveWholeMod` regenerates metadata.
This supports the equivalent native-function experiment and §12's conditional portal
prediction. It does not establish an actual upload result or that an active C override would
be safe. The inert canary remains inert; post-upload checks still record portal and save path.

The complete archived L8–L11 logs were decoded and scanned. Their relevant numbered lines,
hashes, revision controls and totals are in the receipt; original logs remain in the
[repair archive](../../archive/load_order_first_repairs_2026-09-25/).

- L8 :200–287 records the no-save pack, an unloaded scratch definition, success and unchanged
  saved order. L9 :199–287 records `SaveWholeMod` (version 21 to 22), then pack and success.
- On both boots LoadFirst was already first and applied before the kit's veto (:71–72 in L8,
  :72–73 in L9). The disabled line appears only at :204 during the packer's reload. These logs
  do not prove the kit inhibited startup promotion; none was needed for that already-first order.
- L10 :201–206 restores the captured order and requests a save. L11 :81–82 and :197–203 reads
  that same saved and loaded order at load/menu on `main`, reports no LoadFirst row and active
  VacuumWalks/HubLocalAccess. This supports restoration at that recorded boot, not today's rig state.

`LOG_TOTAL` reconciles the four named logs to four revision-405907 lines, four loaded-list
lines and zero `[LUA ERROR]` lines. This is that exact filter, not an absence of all errors.
The owner-session excerpt was also read; it is an excerpt, not a newly checked whole log or
an attended test. No game, account, installed junction or TestKit setting was changed by this
re-audit; no retail launch, merge, upload or sitting preparation was performed.

### Remaining work

Repair R5-D and R5-E in the concrete sitting proposal and re-audit those changes against the
counterexamples. Keep the code at its reviewed revision unless evidence calls for a code
change. SHIP-TO-SITTING still precedes the owner's sitting approval; the upload and post-upload
canary obligations remain as retained in §11 and the release outbox. The consumed brief stays
retired. This verdict narrows the hold to the named remaining defects; it does not reopen
accepted repairs or relax the FIXED list.
