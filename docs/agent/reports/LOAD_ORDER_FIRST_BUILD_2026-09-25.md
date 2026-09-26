# Load order: the pack puts itself first (option B) — build report, 2026-09-25

## Must_Read_Header

Report for the owner and the audit seat, executing the one-off
`docs/agent/prompts/LOAD_ORDER_FIRST_high.md` (authored at `9833cca`, fired from `4e4c97b`).
The build is on the short-lived code branch **`load-first`**, one commit, **`8e2325a`**, not merged.
Records are on `main`. Nothing here was uploaded, and no attended sitting ran. Every "the pack
loads first" claim below is desk- and unattended-verified on this one rig; the retail sitting
in §5 is planned for the owner's approval, not run. A save request is not a disk write; the
seven boot logs are the disk evidence. Where a line says MEASURED it names its command or log.

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

## 10 · Handoff to the audit

Branch `load-first` at `8e2325a` (one commit over `4e4c97b`); records in this commit on `main`.
Re-run: `python tools/desk_load_first.py` and `--no-promotion` on the branch; the seven logs;
`python tools/upload_preflight.py .` on the branch's working tree, not a worktree. The brief
stays in place for the audit to `git rm`.
